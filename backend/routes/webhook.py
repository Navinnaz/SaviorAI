"""
GuardianAI - Twilio WhatsApp Webhook Handler

This is the CRITICAL route that receives every student check-in
and triggers the full autonomous agent pipeline.

Flow:
1. Receive WhatsApp message from Twilio
2. Parse check-in data (score, ate_properly, one_word)
3. Save to database
4. Run HMM burnout assessment
5. Run adversarial validation
6. Run intervention orchestration
7. Send response back to student
8. Background: Update cohort data

All processing must complete within 5 seconds (Twilio timeout).
"""

import os
import re
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime
from fastapi import APIRouter, Form, Request, BackgroundTasks, HTTPException
from fastapi.responses import Response
import hmac
import hashlib

from database.connection import get_db_session
from database import crud
from agents.hmm_engine import BurnoutHMM
from agents.adversarial_validator import AdversarialValidator
from agents.intervention_orchestrator import InterventionOrchestrator
from services.whatsapp import get_whatsapp_service
from services.sentiment import analyze_sentiment

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook", tags=["webhook"])

# Initialize agent components (singleton-style)
hmm_engine = BurnoutHMM()
adversarial_validator = AdversarialValidator()

# OpenAI client for intervention orchestrator (lazy init)
_intervention_orchestrator: Optional[InterventionOrchestrator] = None


def get_intervention_orchestrator() -> InterventionOrchestrator:
    """Get or create intervention orchestrator with OpenAI client."""
    global _intervention_orchestrator
    if _intervention_orchestrator is None:
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        _intervention_orchestrator = InterventionOrchestrator(openai)
    return _intervention_orchestrator


def validate_twilio_signature(request: Request, form_data: Dict[str, str]) -> bool:
    """
    Validate Twilio webhook signature for security.
    
    Twilio signs all webhooks with HMAC-SHA256 to prevent spoofing.
    
    Args:
        request: FastAPI request object
        form_data: Form data received from Twilio
    
    Returns:
        True if signature is valid, False otherwise
    """
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    if not auth_token:
        logger.warning("TWILIO_AUTH_TOKEN not set, skipping signature validation")
        return True  # In development, allow without validation
    
    # Get signature from header
    signature = request.headers.get("X-Twilio-Signature", "")
    if not signature:
        logger.error("No X-Twilio-Signature header found")
        return False
    
    # Build URL (Twilio needs exact URL including query params)
    url = str(request.url)
    
    # Concatenate URL and sorted form parameters
    data_string = url + "".join([f"{k}{v}" for k, v in sorted(form_data.items())])
    
    # Compute HMAC-SHA256
    expected_signature = hmac.new(
        auth_token.encode("utf-8"),
        data_string.encode("utf-8"),
        hashlib.sha256
    ).digest()
    
    # Compare signatures (base64 encoded)
    import base64
    expected_sig_b64 = base64.b64encode(expected_signature).decode()
    
    is_valid = hmac.compare_digest(signature, expected_sig_b64)
    
    if not is_valid:
        logger.error(f"Invalid Twilio signature: expected {expected_sig_b64[:20]}..., got {signature[:20]}...")
    
    return is_valid


def parse_checkin_message(message_body: str) -> Optional[Dict[str, any]]:
    """
    Parse check-in message from various formats.
    
    Supported formats:
    1. "3 yes exhausted" (score ate oneword)
    2. "2\nno\nlost" (newline separated)
    3. "Feeling 2, ate no, word: hopeless" (natural language)
    4. "4" (score only)
    
    Args:
        message_body: Raw message text from WhatsApp
    
    Returns:
        Dict with keys: score (int), ate_properly (str), one_word (str)
        Returns None if parsing fails
    
    Examples:
        >>> parse_checkin_message("3 yes tired")
        {'score': 3, 'ate_properly': 'yes', 'one_word': 'tired'}
        >>> parse_checkin_message("2\nno\nexhausted")
        {'score': 2, 'ate_properly': 'no', 'one_word': 'exhausted'}
        >>> parse_checkin_message("4")
        {'score': 4, 'ate_properly': 'unknown', 'one_word': 'none'}
    """
    if not message_body:
        return None
    
    message = message_body.strip().lower()
    
    logger.debug(f"Parsing check-in message: {message[:100]}")
    
    # Extract score (must be 1-5)
    score_match = re.search(r'\b([1-5])\b', message)
    if not score_match:
        logger.warning(f"No valid score (1-5) found in message: {message[:50]}")
        return None
    
    score = int(score_match.group(1))
    
    # Extract ate_properly (yes, mostly, no)
    ate_properly = "unknown"
    if re.search(r'\b(yes|y)\b', message):
        ate_properly = "yes"
    elif re.search(r'\b(mostly|kinda|somewhat)\b', message):
        ate_properly = "mostly"
    elif re.search(r'\b(no|n|nope)\b', message):
        ate_properly = "no"
    
    # Extract one_word (single word describing their day)
    # Strategy: Take the LAST meaningful word (most likely to be the emotion word)
    words = re.findall(r'\b[a-z]{3,}\b', message)  # Words with 3+ letters
    
    # Expanded exclusion list for common filler words
    excluded = {
        'yes', 'mostly', 'kinda', 'somewhat', 'ate', 'feeling', 'word', 
        'today', 'day', 'the', 'like', 'and', 'but', 'for', 'with',
        'from', 'this', 'that', 'have', 'been', 'was', 'were'
    }
    
    # Filter meaningful words
    meaningful_words = [w for w in words if w not in excluded]
    
    # Take the LAST meaningful word (usually the emotion/state descriptor)
    one_word = meaningful_words[-1] if meaningful_words else "none"
    
    logger.info(
        f"Parsed check-in: score={score}, ate={ate_properly}, word={one_word}"
    )
    
    return {
        "score": score,
        "ate_properly": ate_properly,
        "one_word": one_word
    }


async def process_checkin_pipeline(
    student_id: str,
    checkin_data: Dict,
    student_phone: str
) -> None:
    """
    Background task: Run full agent pipeline after check-in saved.
    
    This runs asynchronously to not block the webhook response.
    
    Pipeline:
    1. Get student's recent check-ins
    2. Run HMM burnout assessment
    3. Run adversarial validation
    4. Run intervention orchestration
    5. Send interventions if needed
    6. (Future) Trigger cohort scan if needed
    
    Args:
        student_id: Student UUID
        checkin_data: Check-in data dict
        student_phone: Student's phone number for messaging
    """
    logger.info(f"Starting agent pipeline for student {student_id}")
    
    try:
        async with get_db_session() as db:
            # Get student info
            student = await crud.get_student_by_id(db, student_id)
            if not student:
                logger.error(f"Student {student_id} not found")
                return
            
            # Get recent check-ins (last 30 days for HMM)
            recent_scores = await crud.get_recent_scores(db, student_id, days=30)
            recent_onewords = await crud.get_recent_onewords(db, student_id, days=7)
            
            logger.info(
                f"Student {student.name}: {len(recent_scores)} scores, "
                f"{len(recent_onewords)} one-words"
            )
            
            # Minimum data check
            if len(recent_scores) < 3:
                logger.info(f"Student {student.name} has insufficient data (<3 check-ins)")
                return
            
            # STEP 1: HMM Burnout Assessment
            assessment = hmm_engine.assess(
                scores=recent_scores,
                baseline=student.baseline_score or 3.0
            )
            
            logger.info(
                f"HMM Assessment: state={assessment.state}, "
                f"prob={assessment.probability:.2f}, trend={assessment.trend_score:+.2f}"
            )
            
            # STEP 2: Adversarial Validation
            validation = adversarial_validator.validate(recent_scores)
            
            if validation["is_suspicious"]:
                logger.warning(
                    f"Gaming detected for {student.name}: "
                    f"confidence={validation['confidence']:.0%}"
                )
            
            # Save burnout state to database
            await crud.save_burnout_state(db, {
                "student_id": student_id,
                "assessed_at": datetime.utcnow(),
                "state": assessment.state,
                "hmm_probability": assessment.probability,
                "trend_score": assessment.trend_score,
                "consecutive_low_days": assessment.consecutive_low_days,
                "variance_flag": validation["is_suspicious"],
                "cohort_flag": False  # TODO: Link with cohort detector
            })
            
            # STEP 3: Get last intervention for cooldown check
            last_intervention = await crud.get_last_intervention(db, student_id)
            
            # STEP 4: Intervention Orchestration
            orchestrator = get_intervention_orchestrator()
            
            decision = await orchestrator.decide_and_act(
                student={
                    "id": str(student.id),
                    "name": student.name,
                    "year_of_study": student.year_of_study,
                    "batch": student.batch
                },
                assessment=assessment,
                recent_scores=recent_scores,
                recent_onewords=recent_onewords,
                validation_result=validation,
                last_intervention=last_intervention
            )
            
            logger.info(
                f"Intervention decision: action={decision['action']}, "
                f"level={decision.get('level', 'N/A')}"
            )
            
            # STEP 5: Execute intervention if needed
            if decision["action"] == "send" or decision["action"] == "send_masking_alert":
                level = decision["level"]
                message = decision["message"]
                recipient = decision["recipient"]
                
                # Save intervention to database
                intervention_id = await crud.save_intervention(db, {
                    "student_id": student_id,
                    "triggered_at": datetime.utcnow(),
                    "level": level,
                    "trigger_reason": decision["reasoning"],
                    "action_taken": decision["action"],
                    "message_sent": message,
                    "recipient": recipient,
                    "was_acknowledged": False,
                    "outcome": "pending"
                })
                
                logger.info(f"Intervention saved: ID={intervention_id}, level={level}")
                
                # Send message via WhatsApp
                whatsapp = get_whatsapp_service()
                
                if recipient == "student":
                    success = whatsapp.send_message(student_phone, message)
                    logger.info(f"Sent peer nudge to student: success={success}")
                
                elif recipient == "counsellor":
                    counsellor_phone = student.institution.counsellor_phone if student.institution else None
                    if counsellor_phone:
                        success = whatsapp.send_counsellor_alert(
                            counsellor_phone,
                            student.name,
                            message
                        )
                        logger.info(f"Sent counsellor alert: success={success}")
                    else:
                        logger.error("No counsellor phone configured for institution")
                
                elif recipient == "emergency":
                    # TODO: Get emergency contact from student record
                    logger.critical(f"EMERGENCY intervention needed for {student.name}")
                    # Would send to both counsellor and emergency contact
                
                elif recipient == "institution":
                    # TODO: Send institutional report
                    logger.critical(f"INSTITUTIONAL intervention needed for {student.batch}")
            
            else:
                logger.info(f"No intervention needed: {decision.get('reason', 'N/A')}")
            
            logger.info(f"Agent pipeline completed for student {student_id}")
    
    except Exception as e:
        logger.error(f"Error in agent pipeline: {e}", exc_info=True)


@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    Body: str = Form(...),
    From: str = Form(...),
    MessageSid: str = Form(...)
) -> Response:
    """
    Twilio WhatsApp webhook handler.
    
    Receives every WhatsApp message sent to the GuardianAI bot number.
    Parses check-in data and triggers full autonomous agent pipeline.
    
    CRITICAL: Must respond within 5 seconds (Twilio timeout).
    Heavy processing happens in background task.
    
    Args:
        request: FastAPI request (for signature validation)
        background_tasks: FastAPI background tasks
        Body: Message text from WhatsApp
        From: Sender phone number (whatsapp:+919876543210)
        MessageSid: Twilio message ID
    
    Returns:
        Empty 200 OK response (Twilio requires fast response)
    
    Flow:
    1. Validate Twilio signature (security)
    2. Parse check-in message
    3. Look up student by phone
    4. Save check-in to database
    5. Send confirmation to student
    6. Trigger background agent pipeline
    7. Return 200 OK to Twilio
    """
    start_time = datetime.utcnow()
    
    logger.info(f"Received WhatsApp message: From={From}, SID={MessageSid}")
    logger.debug(f"Message body: {Body[:100]}")
    
    # STEP 1: Validate Twilio signature
    form_data = {"Body": Body, "From": From, "MessageSid": MessageSid}
    
    if not validate_twilio_signature(request, form_data):
        logger.error("Invalid Twilio signature - possible spoofing attempt")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # STEP 2: Parse check-in message
    checkin_data = parse_checkin_message(Body)
    
    if not checkin_data:
        logger.warning(f"Failed to parse check-in from: {Body[:100]}")
        
        # Send help message
        whatsapp = get_whatsapp_service()
        whatsapp.send_message(
            From,
            "Sorry, I couldn't understand that. Please reply with:\n"
            "Your mood score (1-5), ate properly (yes/no), and one word.\n"
            "Example: 3 yes tired"
        )
        
        return Response(content="", media_type="text/plain")
    
    try:
        async with get_db_session() as db:
            # STEP 3: Look up student by phone
            # Remove whatsapp: prefix for database lookup
            phone = From.replace("whatsapp:", "")
            student = await crud.get_student_by_phone(db, phone)
            
            if not student:
                logger.warning(f"Unknown phone number: {phone}")
                
                whatsapp = get_whatsapp_service()
                whatsapp.send_message(
                    From,
                    "I don't recognize this number. Please contact your institution "
                    "to register with GuardianAI."
                )
                
                return Response(content="", media_type="text/plain")
            
            logger.info(f"Check-in from: {student.name} (ID: {student.id})")
            
            # STEP 4: Analyze sentiment of one_word
            sentiment_data = analyze_sentiment(checkin_data["one_word"])
            
            # STEP 5: Save check-in to database
            checkin_id = await crud.save_checkin(db, {
                "student_id": str(student.id),
                "checked_in_at": datetime.utcnow(),
                "mood_score": checkin_data["score"],
                "ate_properly": checkin_data["ate_properly"],
                "one_word": checkin_data["one_word"],
                "sentiment": sentiment_data["sentiment"],
                "sentiment_score": sentiment_data["score"],
                "raw_message": Body,
                "skipped": False
            })
            
            logger.info(f"Check-in saved: ID={checkin_id}")
            
            # STEP 6: Send confirmation to student
            whatsapp = get_whatsapp_service()
            whatsapp.send_confirmation(From, checkin_data["score"])
            
            # STEP 7: Trigger background agent pipeline
            background_tasks.add_task(
                process_checkin_pipeline,
                str(student.id),
                checkin_data,
                phone
            )
            
            # Calculate response time
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Webhook processed in {elapsed:.3f}s")
            
            if elapsed > 4.0:
                logger.warning(f"Webhook response time exceeded 4s: {elapsed:.3f}s")
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        # Still return 200 to Twilio to avoid retries
    
    # STEP 8: Return empty 200 OK to Twilio
    return Response(content="", media_type="text/plain")


@router.post("/whatsapp/status")
async def whatsapp_status_callback(
    request: Request,
    MessageSid: str = Form(...),
    MessageStatus: str = Form(...),
    To: str = Form(None),
    From: str = Form(None)
) -> Response:
    """
    Twilio message status callback.
    
    Receives delivery status updates for sent messages.
    Statuses: queued, sent, delivered, read, failed, undelivered
    
    Args:
        request: FastAPI request
        MessageSid: Twilio message ID
        MessageStatus: Status (queued, sent, delivered, read, failed, undelivered)
        To: Recipient phone
        From: Sender phone (our bot)
    
    Returns:
        Empty 200 OK response
    """
    logger.info(
        f"Message status update: SID={MessageSid}, status={MessageStatus}, to={To}"
    )
    
    # TODO: Update intervention record with delivery status
    # This helps track if messages are actually reaching students
    
    if MessageStatus in ["failed", "undelivered"]:
        logger.error(f"Message delivery failed: SID={MessageSid}, to={To}")
        # Could trigger fallback (SMS, email, etc.)
    
    elif MessageStatus == "read":
        logger.info(f"Message read by recipient: SID={MessageSid}")
        # Student engaged with message - good signal
    
    return Response(content="", media_type="text/plain")
