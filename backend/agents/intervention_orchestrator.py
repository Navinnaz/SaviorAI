"""
GuardianAI - Autonomous Intervention Orchestrator

The decision-making core of GuardianAI.

This is what makes it AGENTIC:
- It perceives (reads assessment data)
- It reasons (GPT-4o contextualises, adversarial check applied)
- It decides (selects intervention level autonomously)
- It acts (sends messages, files reports)
- It observes (monitors if student responds)
- It adapts (escalates or de-escalates based on response)

No human makes the level decision. The agent does.

Research Basis:
- Crisis intervention escalation protocols (Columbia Protocol, NIMHANS guidelines)
- Autonomous agent decision-making (Russell & Norvig, 2020)
- Mental health triage systems (TAPS, C-SSRS)
- Natural language generation for empathetic communication
"""

from typing import Optional, Dict, List
from datetime import datetime
from dateutil import parser
import logging
import asyncio

logger = logging.getLogger(__name__)


class InterventionOrchestrator:
    """
    The autonomous intervention orchestrator.
    
    This orchestrator implements a complete autonomous agent cycle:
    1. Perceive: Reads student assessment, history, and validation data
    2. Reason: Applies rules and GPT-4o contextual understanding
    3. Decide: Selects intervention level (0-4) with no human input
    4. Act: Generates and sends personalized messages
    5. Observe: Monitors response and outcome
    6. Adapt: Escalates or de-escalates based on student response
    
    Key Features:
    - 48-hour cooldown to prevent intervention spam
    - Retry logic with exponential backoff for GPT-4o failures
    - Fallback template messages when OpenAI unavailable
    - Cost estimation for GPT-4o usage
    - Comprehensive decision logging for audit trails
    - Adversarial detection override (gaming detection)
    """
    
    # Fallback templates when GPT-4o is unavailable
    FALLBACK_TEMPLATES = {
        1: (
            "Hey {name}, hope you're doing okay! We've noticed things might be tough lately. "
            "Want to grab a coffee or just chat? We're here for you. 💙"
        ),
        2: (
            "Counsellor Alert: {name} (Year {year}, {batch}) has shown concerning patterns:\n"
            "- State: {state}\n"
            "- Trend: {trend:+.1f} from baseline\n"
            "- Consecutive low days: {consec}\n"
            "Recommend proactive outreach within 24-48 hours."
        ),
        3: (
            "URGENT: {name} (Year {year}, {batch}) requires immediate attention.\n"
            "Pattern: {reasoning}\n"
            "Action needed: Contact student and emergency contact immediately.\n"
            "Assessment confidence: {probability:.0%}"
        ),
        4: (
            "Institutional Report: Batch {batch} shows systemic stress patterns.\n"
            "Affected students: {count}\n"
            "Recommendation: Batch-level intervention review required.\n"
            "Contact: Counselling team for coordinated response."
        )
    }
    
    # Pricing for GPT-4o (as of 2024, subject to change)
    GPT4O_INPUT_COST_PER_1K = 0.0025   # $0.0025 per 1K input tokens
    GPT4O_OUTPUT_COST_PER_1K = 0.010   # $0.010 per 1K output tokens
    AVG_PROMPT_TOKENS = 250            # Average tokens per intervention prompt
    AVG_COMPLETION_TOKENS = 150        # Average tokens per completion
    
    def __init__(self, openai_client):
        self.client = openai_client
        logger.info("InterventionOrchestrator initialized with OpenAI client")
    
    def estimate_cost(self, num_interventions: int = 1) -> Dict[str, float]:
        """
        Estimate the cost of GPT-4o message generation.
        
        Args:
            num_interventions: Number of interventions to estimate cost for
        
        Returns:
            Dict with cost breakdown:
            - input_cost: Cost of input tokens
            - output_cost: Cost of output tokens
            - total_cost: Total estimated cost
            - per_intervention: Cost per intervention
        
        Example:
            >>> orchestrator.estimate_cost(100)
            {
                'input_cost': 0.0625,
                'output_cost': 0.15,
                'total_cost': 0.2125,
                'per_intervention': 0.002125
            }
        """
        input_cost = (self.AVG_PROMPT_TOKENS / 1000) * self.GPT4O_INPUT_COST_PER_1K * num_interventions
        output_cost = (self.AVG_COMPLETION_TOKENS / 1000) * self.GPT4O_OUTPUT_COST_PER_1K * num_interventions
        total_cost = input_cost + output_cost
        
        logger.debug(
            f"Cost estimate for {num_interventions} interventions: "
            f"${total_cost:.4f} (${total_cost/num_interventions:.6f} per intervention)"
        )
        
        return {
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total_cost": round(total_cost, 4),
            "per_intervention": round(total_cost / num_interventions, 6)
        }
    
    
    async def decide_and_act(
        self,
        student: dict,
        assessment,
        recent_scores: list,
        recent_onewords: list,
        validation_result: dict,
        last_intervention: Optional[dict] = None
    ) -> dict:
        """
        Autonomous intervention decision with complete logging.
        
        This is the core decision-making method that:
        1. Checks cooldown period (48 hours)
        2. Handles adversarial gaming detection
        3. Selects appropriate intervention level
        4. Generates personalized message (with retry + fallback)
        5. Determines recipient
        6. Logs complete decision trail for audit
        
        Args:
            student: Dict with keys: id, name, year_of_study, batch
            assessment: BurnoutAssessment object from HMM engine
            recent_scores: List of recent mood scores (1-5)
            recent_onewords: List of recent one-word responses
            validation_result: Dict from AdversarialValidator
            last_intervention: Optional dict of most recent intervention
        
        Returns:
            Dict with action details:
            - action: "send", "hold", or "send_masking_alert"
            - level: 0-4 (if action="send")
            - message: Generated message text
            - recipient: "student", "counsellor", "emergency", or "institution"
            - reasoning: Human-readable decision explanation
            - decision_log: Complete audit trail
        """
        logger.info(
            f"Intervention decision for student {student.get('id', 'unknown')}: "
            f"state={assessment.state}, prob={assessment.probability:.2f}"
        )
        
        decision_log = {
            "timestamp": datetime.utcnow().isoformat(),
            "student_id": student.get("id"),
            "assessment_state": assessment.state,
            "assessment_probability": assessment.probability,
            "trend_score": assessment.trend_score,
            "consecutive_low_days": assessment.consecutive_low_days,
            "validation_suspicious": validation_result.get("is_suspicious", False),
            "validation_confidence": validation_result.get("confidence", 0.0)
        }
        
        # Rule 1: Never re-trigger same level within 48 hours
        if last_intervention:
            hours_since = self._hours_since(last_intervention["triggered_at"])
            same_or_lower = last_intervention["level"] >= self._assessment_to_level(assessment)
            
            decision_log["last_intervention_hours_ago"] = hours_since
            decision_log["last_intervention_level"] = last_intervention["level"]
            
            if hours_since < 48 and same_or_lower:
                logger.info(
                    f"Holding intervention: last intervention was {hours_since:.1f}h ago "
                    f"(level {last_intervention['level']})"
                )
                decision_log["decision"] = "hold"
                decision_log["reason"] = "cooldown_active"
                return {
                    "action": "hold",
                    "reason": "Recent intervention pending response",
                    "decision_log": decision_log
                }
        
        # Rule 2: Adversarial flag overrides normal level
        if validation_result.get("is_suspicious") and validation_result.get("confidence", 0) > 0.5:
            logger.warning(
                f"Adversarial gaming detected: confidence={validation_result['confidence']:.0%}, "
                f"flags={[f['type'] for f in validation_result.get('flags', [])]}"
            )
            decision_log["decision"] = "adversarial_override"
            result = await self._handle_masking(student, validation_result)
            result["decision_log"] = decision_log
            return result
        
        # Rule 3: Select intervention level from assessment
        level = self._select_level(assessment, last_intervention)
        decision_log["selected_level"] = level
        decision_log["level_reasoning"] = self._get_level_reasoning(assessment, last_intervention, level)
        
        logger.info(f"Selected intervention level {level} for {student.get('name', 'unknown')}")
        
        if level == 0:
            decision_log["decision"] = "no_action_needed"
            return {
                "action": "hold",
                "reason": "Student state is stable",
                "decision_log": decision_log
            }
        
        # Rule 4: Generate human message via GPT-4o (with retry + fallback)
        message = await self._generate_message_with_retry(
            student, assessment, recent_onewords, level
        )
        decision_log["message_generated"] = "gpt4o" if "Hey" in message or "Alert" in message else "fallback"
        
        # Rule 5: Select recipient
        recipient = self._select_recipient(level)
        decision_log["recipient"] = recipient
        decision_log["decision"] = "send"
        
        logger.info(
            f"Intervention ready: level={level}, recipient={recipient}, "
            f"message_length={len(message)} chars"
        )
        
        return {
            "level": level,
            "message": message,
            "recipient": recipient,
            "reasoning": assessment.reasoning,
            "action": "send",
            "decision_log": decision_log
        }
    
    def _get_level_reasoning(self, assessment, last_intervention: Optional[dict], level: int) -> str:
        """Generate human-readable reasoning for level selection."""
        if level == 0:
            return "Student state is stable, no intervention needed"
        elif level == 1:
            return f"First at-risk detection, peer nudge appropriate"
        elif level == 2:
            if last_intervention:
                return f"Escalating from level {last_intervention['level']} - previous intervention not resolved"
            return "At-risk state OR low-confidence crisis, counsellor outreach needed"
        elif level == 3:
            return f"High-confidence crisis (prob={assessment.probability:.0%}, consec_low={assessment.consecutive_low_days})"
        elif level == 4:
            return "Cohort-level anomaly or prolonged crisis requiring institutional action"
        return "Unknown level reasoning"
    
    async def _generate_message_with_retry(
        self,
        student: dict,
        assessment,
        recent_onewords: list,
        level: int,
        max_retries: int = 3
    ) -> str:
        """
        Generate message via GPT-4o with exponential backoff retry.
        Falls back to template if all retries fail.
        
        Retry logic:
        - Attempt 1: immediate
        - Attempt 2: wait 1 second
        - Attempt 3: wait 2 seconds
        - Attempt 4: wait 4 seconds
        - If all fail: use fallback template
        
        Args:
            student: Student dict
            assessment: BurnoutAssessment
            recent_onewords: Recent one-word responses
            level: Intervention level (1-4)
            max_retries: Maximum retry attempts (default: 3)
        
        Returns:
            Generated message string (from GPT-4o or fallback)
        """
        for attempt in range(max_retries + 1):
            try:
                if attempt > 0:
                    wait_time = 2 ** (attempt - 1)  # Exponential backoff: 1s, 2s, 4s
                    logger.info(f"Retrying GPT-4o call (attempt {attempt+1}/{max_retries+1}) after {wait_time}s")
                    await asyncio.sleep(wait_time)
                
                message = await self._generate_message(student, assessment, recent_onewords, level)
                logger.info(f"GPT-4o message generated successfully on attempt {attempt+1}")
                return message
                
            except Exception as e:
                logger.warning(f"GPT-4o generation failed (attempt {attempt+1}/{max_retries+1}): {e}")
                
                if attempt == max_retries:
                    # All retries exhausted, use fallback
                    logger.error("All GPT-4o retries failed, using fallback template")
                    return self._generate_fallback_message(student, assessment, level)
        
        # Should never reach here, but safety fallback
        return self._generate_fallback_message(student, assessment, level)
    
    def _generate_fallback_message(self, student: dict, assessment, level: int) -> str:
        """
        Generate fallback message from template when GPT-4o unavailable.
        
        Args:
            student: Student dict
            assessment: BurnoutAssessment
            level: Intervention level (1-4)
        
        Returns:
            Formatted template message
        """
        template = self.FALLBACK_TEMPLATES.get(level, self.FALLBACK_TEMPLATES[1])
        
        try:
            message = template.format(
                name=student.get("name", "Student"),
                year=student.get("year_of_study", "N/A"),
                batch=student.get("batch", "N/A"),
                state=assessment.state.upper(),
                trend=assessment.trend_score,
                consec=assessment.consecutive_low_days,
                reasoning=assessment.reasoning,
                probability=assessment.probability,
                count="N/A"  # For level 4, would need cohort data
            )
            logger.info(f"Fallback template message generated for level {level}")
            return message
        except Exception as e:
            logger.error(f"Fallback template formatting failed: {e}")
            # Ultra-safe fallback
            return f"Alert: {student.get('name', 'Student')} requires attention. Please review their recent check-ins."
    
    def _assessment_to_level(self, assessment) -> int:
        """Convert assessment state to intervention level for comparison."""
        if assessment.state == 'crisis':
            return 3
        elif assessment.state == 'at_risk':
            return 1
        return 0
    
    def _select_level(
        self, 
        assessment,
        last_intervention: Optional[dict]
    ) -> int:
        """
        Autonomous level selection with complete decision logic.
        
        Level 0: No action (stable state)
        Level 1: Peer nudge — At-Risk, first occurrence
        Level 2: Counsellor soft alert — At-Risk recurring OR low probability crisis
        Level 3: Emergency — Crisis state with high probability (>75%) OR 5+ consecutive low days
        Level 4: Institutional report — Cohort anomaly OR prolonged crisis (not implemented here, requires cohort context)
        
        Escalation Logic:
        - At-Risk → Peer nudge (level 1)
        - At-Risk + previous level 1 intervention → Escalate to counsellor (level 2)
        - Crisis + high confidence (>75% OR 5+ low days) → Emergency (level 3)
        - Crisis + lower confidence → Counsellor first (level 2)
        
        Args:
            assessment: BurnoutAssessment from HMM engine
            last_intervention: Previous intervention dict (if any)
        
        Returns:
            Intervention level (0-4)
        """
        state = assessment.state
        prob = assessment.probability
        consec = assessment.consecutive_low_days
        
        logger.debug(
            f"Level selection: state={state}, prob={prob:.2f}, consec_low={consec}, "
            f"last_level={last_intervention['level'] if last_intervention else None}"
        )
        
        if state == 'stable':
            logger.debug("State is stable, no action needed (level 0)")
            return 0  # No action needed
        
        if state == 'at_risk':
            if last_intervention and last_intervention["level"] >= 1:
                logger.info("Escalating at-risk to counsellor (level 2) - previous peer nudge didn't resolve")
                return 2  # Escalate to counsellor if peer nudge didn't resolve
            logger.info("First at-risk detection, peer nudge appropriate (level 1)")
            return 1   # First at-risk: peer nudge
        
        if state == 'crisis':
            if prob > 0.75 or consec >= 5:
                logger.warning(f"High confidence crisis detected (prob={prob:.0%}, consec={consec}) - emergency (level 3)")
                return 3  # High confidence crisis: emergency
            logger.info(f"Crisis detected but lower confidence (prob={prob:.0%}) - counsellor first (level 2)")
            return 2   # Lower confidence: counsellor first
        
        logger.debug("Default fallback to level 1")
        return 1
    
    async def _generate_message(
        self,
        student: dict,
        assessment,
        recent_onewords: list,
        level: int
    ) -> str:
        """
        GPT-4o generates personalized, contextual message content.
        
        The message is:
        - Warm and human, never clinical or surveillance-focused
        - Specific to the student's pattern and context
        - Appropriate for the recipient (peer, counsellor, emergency, institution)
        - Actionable with clear next steps
        
        Args:
            student: Student information dict
            assessment: BurnoutAssessment from HMM
            recent_onewords: Recent one-word check-in responses
            level: Intervention level (1-4)
        
        Returns:
            Generated message text (raises exception if API fails)
        """
        level_instructions = {
            1: "Write a warm, casual WhatsApp message to a student from their peer support network. NOT clinical. Sound like a caring friend checking in.",
            2: "Write a professional but warm alert to a college counsellor. Include specific data points. Actionable. Under 150 words.",
            3: "Write an urgent but calm emergency notification to a counsellor AND emergency contact. Include the student's name and the specific concerning pattern. Clear call to action.",
            4: "Write an institutional report summary for the Dean/Principal. Professional. Data-driven. Recommendations included."
        }
        
        prompt = f"""
You are GuardianAI, an autonomous student wellbeing agent.

Student: {student.get('name', 'Unknown')}, Year {student.get('year_of_study', 'N/A')}, {student.get('batch', 'N/A')}
Assessment: {assessment.state.upper()} (probability: {assessment.probability:.0%})
Trend: {assessment.trend_score:+.1f} from personal baseline
Consecutive low days: {assessment.consecutive_low_days}
Recent one-word responses: {', '.join(recent_onewords[-5:]) if recent_onewords else 'none'}
Agent reasoning: {assessment.reasoning}

Task: {level_instructions.get(level, level_instructions[1])}

Requirements:
- NEVER mention surveillance or monitoring
- NEVER use clinical language like "depression" or "mental illness"  
- DO mention you noticed they seem to be going through something
- DO offer specific, immediate support options
- Keep it human, warm, and genuinely caring

Generate ONLY the message text. No preamble.
"""
        
        logger.debug(f"Calling GPT-4o-mini for level {level} message generation")
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",  # Affordable: $0.15/1M input, $0.60/1M output (10x cheaper than gpt-4o)
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        message = response.choices[0].message.content.strip()
        logger.debug(f"GPT-4o-mini generated message: {len(message)} chars")
        return message
    
    async def _handle_masking(self, student: dict, validation: dict) -> dict:
        """
        Special handling when gaming/masking behavior is detected.
        
        When adversarial validation flags a student for potential gaming
        (flat scores, perfect streaks, sudden recovery), we bypass normal
        peer nudges and go straight to counsellor with detailed context.
        
        This is critical because gaming behavior is itself a signal of distress—
        students hiding their true state may be at higher risk than HMM indicates.
        
        Args:
            student: Student information dict
            validation: AdversarialValidator result with flags
        
        Returns:
            Action dict with level 2, counsellor-targeted message, and reasoning
        """
        logger.warning(
            f"Handling masking behavior for {student.get('name', 'unknown')}: "
            f"confidence={validation.get('confidence', 0):.0%}"
        )
        
        flags_detail = '\n'.join([
            f"- {f['type'].replace('_', ' ').title()}: {f['detail']}"
            for f in validation.get('flags', [])
        ])
        
        message = f"""Alert: Potential masking behavior detected for {student.get('name', 'Unknown Student')}

Validation confidence: {validation.get('confidence', 0):.0%}
Flags detected: {', '.join([f['type'] for f in validation.get('flags', [])])}

This student may be providing inconsistent responses to avoid detection. 
Recommend direct, gentle outreach rather than automated messaging.

Details:
{flags_detail}

Student Info:
- Name: {student.get('name', 'N/A')}
- Year: {student.get('year_of_study', 'N/A')}
- Batch: {student.get('batch', 'N/A')}

Recommended Action:
Schedule a low-pressure, informal check-in within 24-48 hours.
Masking behavior itself can indicate distress.
"""
        
        logger.info(f"Masking alert message generated for counsellor")
        
        return {
            "level": 2,  # Direct to counsellor, not peer
            "message": message,
            "recipient": "counsellor",
            "reasoning": f"Adversarial validation flags: {[f['type'] for f in validation.get('flags', [])]}",
            "action": "send_masking_alert"
        }
    
    def _select_recipient(self, level: int) -> str:
        """
        Map intervention level to recipient.
        
        Level 0: None (no action)
        Level 1: student (peer nudge via WhatsApp)
        Level 2: counsellor (professional alert)
        Level 3: emergency (counsellor + emergency contact)
        Level 4: institution (Dean/Principal/Admin)
        
        Args:
            level: Intervention level (0-4)
        
        Returns:
            Recipient identifier string
        """
        mapping = {
            0: None,
            1: "student",
            2: "counsellor",
            3: "emergency",
            4: "institution"
        }
        recipient = mapping.get(level, "counsellor")
        logger.debug(f"Level {level} → recipient: {recipient}")
        return recipient
    
    def _hours_since(self, timestamp) -> float:
        """
        Calculate hours elapsed since a timestamp.
        
        Args:
            timestamp: datetime object or ISO format string
        
        Returns:
            Hours elapsed as float
        """
        if isinstance(timestamp, str):
            timestamp = parser.parse(timestamp)
        
        # Make sure we're comparing timezone-aware datetimes
        now = datetime.now(datetime.UTC) if hasattr(datetime, 'UTC') else datetime.utcnow()
        
        # If timestamp is timezone-aware and now is not, make now aware
        if timestamp.tzinfo is not None and (not hasattr(datetime, 'UTC')):
            # Use UTC timezone for comparison
            from datetime import timezone
            now = datetime.now(timezone.utc)
        
        hours = (now - timestamp).total_seconds() / 3600
        return hours
