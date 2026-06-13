"""
GuardianAI Dashboard API

Provides analytics and monitoring endpoints for institutions
to visualize student mental health data and intervention effectiveness.

All endpoints require API key authentication via X-API-Key header.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc, or_

from backend.database.connection import get_db
from backend.database import crud, models

logger = logging.getLogger(__name__)

router = APIRouter(tags=["dashboard"])

# API Key Authentication
def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Verify API key from request header.
    
    In production, store hashed keys in database with institution mapping.
    For now, using environment variable for simplicity.
    
    Args:
        x_api_key: API key from X-API-Key header
    
    Returns:
        Verified API key
    
    Raises:
        HTTPException: If API key is invalid or missing
    """
    valid_api_key = os.getenv("DASHBOARD_API_KEY", "guardianai_dev_key_2024")
    
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include X-API-Key header."
        )
    
    if x_api_key != valid_api_key:
        logger.warning(f"Invalid API key attempt: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )
    
    return x_api_key


@router.get("/{institution_id}/overview")
async def get_institution_overview(
    institution_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Get high-level institution dashboard overview.
    
    Returns:
        - Total active students
        - Count by risk state (stable, at_risk, crisis)
        - 7-day check-in rate
        - Today's intervention count
        - Active cohort alerts
    
    Example:
        GET /dashboard/123e4567-e89b-12d3-a456-426614174000/overview
        Headers: X-API-Key: your_api_key
    """
    try:
        inst_uuid = UUID(institution_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid institution ID format"
        )
    
    # Verify institution exists
    inst_result = await db.execute(
        select(models.Institution).where(models.Institution.id == inst_uuid)
    )
    institution = inst_result.scalar_one_or_none()
    
    if not institution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institution not found"
        )
    
    # Get all active students
    students_result = await db.execute(
        select(models.Student).where(
            and_(
                models.Student.institution_id == inst_uuid,
                models.Student.is_active == True
            )
        )
    )
    students = list(students_result.scalars().all())
    total_students = len(students)
    
    # Count students by risk state (based on latest burnout state)
    stable_count = 0
    at_risk_count = 0
    crisis_count = 0
    
    for student in students:
        latest_state = await crud.get_latest_burnout_state(db, student.id)
        if latest_state:
            if latest_state.state == "stable":
                stable_count += 1
            elif latest_state.state == "at_risk":
                at_risk_count += 1
            elif latest_state.state == "crisis":
                crisis_count += 1
        else:
            # No assessment yet, assume stable
            stable_count += 1
    
    # Calculate 7-day check-in rate
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    checkin_count_result = await db.execute(
        select(func.count(func.distinct(models.CheckIn.student_id))).where(
            and_(
                models.CheckIn.student_id.in_([s.id for s in students]),
                models.CheckIn.checked_in_at >= seven_days_ago,
                models.CheckIn.skipped == False
            )
        )
    )
    students_who_checked_in = checkin_count_result.scalar() or 0
    check_in_rate_7d = (students_who_checked_in / total_students * 100) if total_students > 0 else 0.0
    
    # Count interventions today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    interventions_today_result = await db.execute(
        select(func.count(models.Intervention.id)).where(
            and_(
                models.Intervention.student_id.in_([s.id for s in students]),
                models.Intervention.triggered_at >= today_start
            )
        )
    )
    interventions_today = interventions_today_result.scalar() or 0
    
    # Count active cohort alerts
    active_alerts_result = await db.execute(
        select(func.count(models.CohortAlert.id)).where(
            and_(
                models.CohortAlert.institution_id == inst_uuid,
                models.CohortAlert.acknowledged == False
            )
        )
    )
    cohort_alerts_active = active_alerts_result.scalar() or 0
    
    return {
        "total_students": total_students,
        "stable_count": stable_count,
        "at_risk_count": at_risk_count,
        "crisis_count": crisis_count,
        "check_in_rate_7d": round(check_in_rate_7d, 1),
        "interventions_today": interventions_today,
        "cohort_alerts_active": cohort_alerts_active
    }


@router.get("/{institution_id}/heatmap")
async def get_institution_heatmap(
    institution_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
) -> List[Dict[str, Any]]:
    """
    Get heatmap data for all students in institution.
    
    Returns array of students with current risk state, last check-in,
    and trend direction for visual heatmap rendering.
    
    Example:
        GET /dashboard/123e4567-e89b-12d3-a456-426614174000/heatmap
        Headers: X-API-Key: your_api_key
    """
    try:
        inst_uuid = UUID(institution_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid institution ID format"
        )
    
    # Get all active students
    students_result = await db.execute(
        select(models.Student).where(
            and_(
                models.Student.institution_id == inst_uuid,
                models.Student.is_active == True
            )
        ).order_by(models.Student.batch.asc(), models.Student.name.asc())
    )
    students = list(students_result.scalars().all())
    
    heatmap_data = []
    
    for student in students:
        # Get latest burnout state
        latest_state = await crud.get_latest_burnout_state(db, student.id)
        
        if latest_state:
            state = latest_state.state
            
            # Map state to meaningful risk score (0-100)
            # HMM probability has numerical underflow, so we use state + modifiers
            if state == "crisis":
                # Crisis: base 85-95 risk
                base_risk = 85
                # Add points for consecutive low days (up to +10)
                consecutive_bonus = min(latest_state.consecutive_low_days * 2, 10)
                risk_score = min(base_risk + consecutive_bonus, 95)
            elif state == "at_risk":
                # At-risk: base 50-70 risk
                base_risk = 50
                # Negative trend increases risk (up to +20)
                trend_penalty = max(int(abs(latest_state.trend_score) * 10), 0) if latest_state.trend_score < 0 else 0
                risk_score = min(base_risk + trend_penalty, 70)
            else:  # stable
                # Stable: 5-35 risk (everyone has some baseline risk)
                base_risk = 15
                # Slight positive trend reduces risk
                trend_bonus = max(int(latest_state.trend_score * 5), 0) if latest_state.trend_score > 0 else 0
                risk_score = max(base_risk - trend_bonus, 5)
            
            # Determine trend from trend_score
            if latest_state.trend_score < -0.5:
                trend = "declining"
            elif latest_state.trend_score > 0.5:
                trend = "improving"
            else:
                trend = "stable"
        else:
            state = "stable"
            risk_score = 10  # Unknown state gets low risk
            trend = "stable"
        
        # Get last check-in
        last_checkin_result = await db.execute(
            select(models.CheckIn).where(
                models.CheckIn.student_id == student.id
            ).order_by(models.CheckIn.checked_in_at.desc()).limit(1)
        )
        last_checkin = last_checkin_result.scalar_one_or_none()
        
        heatmap_data.append({
            "student_id": str(student.id),
            "name": student.name,
            "batch": student.batch,
            "state": state,
            "risk_score": risk_score,
            "last_checkin": last_checkin.checked_in_at.isoformat() if last_checkin else None,
            "trend": trend
        })
    
    # Sort by risk score descending (highest risk first)
    heatmap_data.sort(key=lambda x: x["risk_score"], reverse=True)
    
    return heatmap_data


@router.get("/student/{student_id}/profile")
async def get_student_profile(
    student_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Get comprehensive student profile with full history.
    
    Returns:
        - Basic info (name, batch, phone, etc.)
        - Last 14 days of check-ins (scores, onewords, sentiments)
        - HMM state history (for timeline visualization)
        - All interventions with outcomes
        - Adversarial validation summary
    
    Example:
        GET /dashboard/student/456e4567-e89b-12d3-a456-426614174111/profile
        Headers: X-API-Key: your_api_key
    """
    try:
        stud_uuid = UUID(student_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID format"
        )
    
    # Get student with institution
    student = await crud.get_student_by_id(db, stud_uuid)
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Basic info
    basic_info = {
        "id": str(student.id),
        "name": student.name,
        "phone": student.phone,
        "email": student.email,
        "batch": student.batch,
        "year_of_study": student.year_of_study,
        "baseline_score": student.baseline_score,
        "enrolled_at": student.enrolled_at.isoformat() if student.enrolled_at else None,
        "institution": student.institution.to_dict() if student.institution else None
    }
    
    # Last 14 days of check-ins
    checkins_14d_result = await db.execute(
        select(models.CheckIn).where(
            and_(
                models.CheckIn.student_id == stud_uuid,
                models.CheckIn.checked_in_at >= datetime.utcnow() - timedelta(days=14)
            )
        ).order_by(models.CheckIn.checked_in_at.asc())
    )
    checkins_14d = list(checkins_14d_result.scalars().all())
    
    checkins_data = [
        {
            "checked_in_at": c.checked_in_at.isoformat(),
            "mood_score": c.mood_score,
            "ate_properly": c.ate_properly,
            "one_word": c.one_word,
            "sentiment": c.sentiment,
            "sentiment_score": c.sentiment_score
        }
        for c in checkins_14d
    ]
    
    # HMM state history (last 30 days for timeline)
    state_history_result = await db.execute(
        select(models.BurnoutState).where(
            and_(
                models.BurnoutState.student_id == stud_uuid,
                models.BurnoutState.assessed_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).order_by(models.BurnoutState.assessed_at.asc())
    )
    state_history = list(state_history_result.scalars().all())
    
    state_history_data = [
        {
            "assessed_at": s.assessed_at.isoformat(),
            "state": s.state,
            "hmm_probability": s.hmm_probability,
            "trend_score": s.trend_score,
            "consecutive_low_days": s.consecutive_low_days,
            "variance_flag": s.variance_flag,
            "cohort_flag": s.cohort_flag
        }
        for s in state_history
    ]
    
    # All interventions
    interventions_result = await db.execute(
        select(models.Intervention).where(
            models.Intervention.student_id == stud_uuid
        ).order_by(models.Intervention.triggered_at.desc())
    )
    interventions = list(interventions_result.scalars().all())
    
    interventions_data = [
        {
            "id": str(i.id),
            "triggered_at": i.triggered_at.isoformat(),
            "level": i.level,
            "trigger_reason": i.trigger_reason,
            "action_taken": i.action_taken,
            "message_sent": i.message_sent,
            "recipient": i.recipient,
            "was_acknowledged": i.was_acknowledged,
            "acknowledged_at": i.acknowledged_at.isoformat() if i.acknowledged_at else None,
            "outcome": i.outcome
        }
        for i in interventions
    ]
    
    # Adversarial validation summary
    # Count how many times gaming was detected
    gaming_detected_count = sum(1 for s in state_history if s.variance_flag)
    total_assessments = len(state_history)
    gaming_percentage = (gaming_detected_count / total_assessments * 100) if total_assessments > 0 else 0.0
    
    adversarial_summary = {
        "total_assessments": total_assessments,
        "gaming_detected_count": gaming_detected_count,
        "gaming_percentage": round(gaming_percentage, 1),
        "last_gaming_detected": None
    }
    
    # Find last time gaming was detected
    for s in reversed(state_history):
        if s.variance_flag:
            adversarial_summary["last_gaming_detected"] = s.assessed_at.isoformat()
            break
    
    return {
        "basic_info": basic_info,
        "checkins_14d": checkins_data,
        "state_history": state_history_data,
        "interventions": interventions_data,
        "adversarial_summary": adversarial_summary
    }


@router.get("/{institution_id}/cohorts")
async def get_cohorts_analytics(
    institution_id: str,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
) -> List[Dict[str, Any]]:
    """
    Get cohort-level analytics for all batches in institution.
    
    Returns array of batches with:
        - Batch name
        - Total students
        - Average mood score (7-day)
        - Risk distribution
        - Active alerts
    
    Example:
        GET /dashboard/123e4567-e89b-12d3-a456-426614174000/cohorts
        Headers: X-API-Key: your_api_key
    """
    try:
        inst_uuid = UUID(institution_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid institution ID format"
        )
    
    # Get all active students grouped by batch
    students_result = await db.execute(
        select(models.Student).where(
            and_(
                models.Student.institution_id == inst_uuid,
                models.Student.is_active == True
            )
        ).order_by(models.Student.batch.asc())
    )
    students = list(students_result.scalars().all())
    
    # Group students by batch
    batches: Dict[str, List[models.Student]] = {}
    for student in students:
        if student.batch:
            if student.batch not in batches:
                batches[student.batch] = []
            batches[student.batch].append(student)
    
    cohorts_data = []
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    for batch_name, batch_students in batches.items():
        # Count risk states
        stable = at_risk = crisis = 0
        
        for student in batch_students:
            latest_state = await crud.get_latest_burnout_state(db, student.id)
            if latest_state:
                if latest_state.state == "stable":
                    stable += 1
                elif latest_state.state == "at_risk":
                    at_risk += 1
                elif latest_state.state == "crisis":
                    crisis += 1
            else:
                stable += 1
        
        # Calculate average mood score (last 7 days)
        student_ids = [s.id for s in batch_students]
        
        scores_result = await db.execute(
            select(models.CheckIn.mood_score).where(
                and_(
                    models.CheckIn.student_id.in_(student_ids),
                    models.CheckIn.checked_in_at >= seven_days_ago,
                    models.CheckIn.mood_score.isnot(None),
                    models.CheckIn.skipped == False
                )
            )
        )
        scores = [s for s in scores_result.scalars().all() if s is not None]
        avg_mood_7d = (sum(scores) / len(scores)) if scores else 0.0
        
        # Count active alerts for this batch
        alerts_result = await db.execute(
            select(func.count(models.CohortAlert.id)).where(
                and_(
                    models.CohortAlert.institution_id == inst_uuid,
                    models.CohortAlert.batch == batch_name,
                    models.CohortAlert.acknowledged == False
                )
            )
        )
        active_alerts = alerts_result.scalar() or 0
        
        cohorts_data.append({
            "batch": batch_name,
            "total_students": len(batch_students),
            "avg_mood_7d": round(avg_mood_7d, 2),
            "risk_distribution": {
                "stable": stable,
                "at_risk": at_risk,
                "crisis": crisis
            },
            "active_alerts": active_alerts
        })
    
    return cohorts_data


@router.get("/interventions/recent")
async def get_recent_interventions(
    institution_id: Optional[str] = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_api_key)
) -> List[Dict[str, Any]]:
    """
    Get recent autonomous interventions across institution(s).
    
    Shows full reasoning chain for transparency and debugging.
    
    Query params:
        - institution_id (optional): Filter by institution
        - limit (default 20): Number of interventions to return
    
    Example:
        GET /dashboard/interventions/recent?institution_id=123e4567&limit=10
        Headers: X-API-Key: your_api_key
    """
    if limit > 100:
        limit = 100  # Cap at 100 for performance
    
    query = select(models.Intervention).join(
        models.Student,
        models.Intervention.student_id == models.Student.id
    )
    
    # Filter by institution if provided
    if institution_id:
        try:
            inst_uuid = UUID(institution_id)
            query = query.where(models.Student.institution_id == inst_uuid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid institution ID format"
            )
    
    query = query.order_by(models.Intervention.triggered_at.desc()).limit(limit)
    
    interventions_result = await db.execute(query)
    interventions = list(interventions_result.scalars().all())
    
    # Enrich with student info
    interventions_data = []
    
    for intervention in interventions:
        student = await crud.get_student_by_id(db, intervention.student_id)
        
        interventions_data.append({
            "id": str(intervention.id),
            "triggered_at": intervention.triggered_at.isoformat(),
            "student": {
                "id": str(student.id),
                "name": student.name,
                "batch": student.batch,
                "institution": student.institution.name if student.institution else None
            },
            "level": intervention.level,
            "level_name": {
                1: "Peer Nudge",
                2: "Counsellor Soft Alert",
                3: "Emergency Escalation",
                4: "Institutional Action"
            }.get(intervention.level, "Unknown"),
            "trigger_reason": intervention.trigger_reason,
            "action_taken": intervention.action_taken,
            "message_sent": intervention.message_sent,
            "recipient": intervention.recipient,
            "was_acknowledged": intervention.was_acknowledged,
            "acknowledged_at": intervention.acknowledged_at.isoformat() if intervention.acknowledged_at else None,
            "outcome": intervention.outcome
        })
    
    return interventions_data


@router.get("/health")
async def dashboard_health_check() -> Dict[str, str]:
    """
    Health check endpoint (no auth required).
    
    Example:
        GET /dashboard/health
    """
    return {
        "status": "healthy",
        "service": "guardianai-dashboard",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }
