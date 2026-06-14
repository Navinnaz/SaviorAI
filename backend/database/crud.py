"""
SaviorAI Database CRUD Operations
Async database operations for all models using SQLAlchemy 2.0
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from sqlalchemy.orm import selectinload

from .models import (
    Student, Institution, CheckIn, BurnoutState, 
    Intervention, CohortAlert
)


async def get_student_by_phone(db: AsyncSession, phone: str) -> Optional[Student]:
    """
    Get student by phone number.
    
    Args:
        db: Async database session
        phone: Phone number (with or without whatsapp: prefix)
    
    Returns:
        Student object or None if not found
    """
    # Clean phone number
    phone = phone.replace("whatsapp:", "").strip()
    
    result = await db.execute(
        select(Student)
        .where(Student.phone == phone)
        .options(selectinload(Student.institution))
    )
    return result.scalar_one_or_none()


async def get_recent_scores(
    db: AsyncSession, 
    student_id: UUID, 
    days: int = 14
) -> List[int]:
    """
    Get recent mood scores for a student.
    
    Args:
        db: Async database session
        student_id: Student UUID
        days: Number of days to look back (default 14)
    
    Returns:
        List of mood scores (1-5) in chronological order
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(CheckIn.mood_score)
        .where(
            and_(
                CheckIn.student_id == student_id,
                CheckIn.checked_in_at >= cutoff_date,
                CheckIn.mood_score.isnot(None),
                CheckIn.skipped == False
            )
        )
        .order_by(CheckIn.checked_in_at.asc())
    )
    
    scores = [score for score in result.scalars().all() if score is not None]
    return scores



async def get_recent_onewords(
    db: AsyncSession, 
    student_id: UUID, 
    days: int = 7
) -> List[str]:
    """
    Get recent one-word responses for a student.
    
    Args:
        db: Async database session
        student_id: Student UUID
        days: Number of days to look back (default 7)
    
    Returns:
        List of one-word responses in chronological order
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(CheckIn.one_word)
        .where(
            and_(
                CheckIn.student_id == student_id,
                CheckIn.checked_in_at >= cutoff_date,
                CheckIn.one_word.isnot(None),
                CheckIn.skipped == False
            )
        )
        .order_by(CheckIn.checked_in_at.asc())
    )
    
    onewords = [word for word in result.scalars().all() if word and word.strip()]
    return onewords


async def save_checkin(
    db: AsyncSession, 
    checkin_data: Dict[str, Any]
) -> CheckIn:
    """
    Save a new check-in to the database.
    
    Args:
        db: Async database session
        checkin_data: Dictionary with checkin fields
    
    Returns:
        Created CheckIn object
    """
    checkin = CheckIn(**checkin_data)
    db.add(checkin)
    await db.flush()
    await db.refresh(checkin)
    return checkin



async def save_burnout_state(
    db: AsyncSession,
    student_id: UUID,
    assessment: Any,  # BurnoutAssessment dataclass
    validation: Dict[str, Any]
) -> BurnoutState:
    """
    Save HMM burnout state assessment to database.
    
    Args:
        db: Async database session
        student_id: Student UUID
        assessment: BurnoutAssessment object from HMM
        validation: Adversarial validation result dict
    
    Returns:
        Created BurnoutState object
    """
    burnout_state = BurnoutState(
        student_id=student_id,
        state=assessment.state,
        hmm_probability=assessment.probability,
        trend_score=assessment.trend_score,
        consecutive_low_days=assessment.consecutive_low_days,
        variance_flag=validation.get("is_suspicious", False),
        cohort_flag=False  # Will be updated by cohort detector
    )
    
    db.add(burnout_state)
    await db.flush()
    await db.refresh(burnout_state)
    return burnout_state


async def get_last_intervention(
    db: AsyncSession, 
    student_id: UUID
) -> Optional[Intervention]:
    """
    Get the most recent intervention for a student.
    
    Args:
        db: Async database session
        student_id: Student UUID
    
    Returns:
        Most recent Intervention object or None
    """
    result = await db.execute(
        select(Intervention)
        .where(Intervention.student_id == student_id)
        .order_by(Intervention.triggered_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()



async def save_intervention(
    db: AsyncSession, 
    intervention_data: Dict[str, Any]
) -> Intervention:
    """
    Save an autonomous intervention to the database.
    
    Args:
        db: Async database session
        intervention_data: Dictionary with intervention fields
    
    Returns:
        Created Intervention object
    """
    intervention = Intervention(**intervention_data)
    db.add(intervention)
    await db.flush()
    await db.refresh(intervention)
    return intervention


async def get_all_students_by_institution(
    db: AsyncSession, 
    institution_id: UUID
) -> List[Student]:
    """
    Get all students belonging to an institution.
    
    Args:
        db: Async database session
        institution_id: Institution UUID
    
    Returns:
        List of Student objects
    """
    result = await db.execute(
        select(Student)
        .where(
            and_(
                Student.institution_id == institution_id,
                Student.is_active == True
            )
        )
        .order_by(Student.name.asc())
    )
    return list(result.scalars().all())



async def get_cohort_data_by_batch(
    db: AsyncSession,
    institution_id: UUID,
    batch: str
) -> List[Dict[str, Any]]:
    """
    Get cohort data for anomaly detection.
    Returns recent averages and baselines for all students in a batch.
    
    Args:
        db: Async database session
        institution_id: Institution UUID
        batch: Batch name (e.g., "CSE-2022")
    
    Returns:
        List of dicts with student_id, recent_avg, baseline
    """
    # Get all students in this batch
    students_result = await db.execute(
        select(Student)
        .where(
            and_(
                Student.institution_id == institution_id,
                Student.batch == batch,
                Student.is_active == True
            )
        )
    )
    students = students_result.scalars().all()
    
    cohort_data = []
    cutoff_date = datetime.utcnow() - timedelta(days=7)
    
    for student in students:
        # Get recent scores (last 7 days)
        scores_result = await db.execute(
            select(CheckIn.mood_score)
            .where(
                and_(
                    CheckIn.student_id == student.id,
                    CheckIn.checked_in_at >= cutoff_date,
                    CheckIn.mood_score.isnot(None),
                    CheckIn.skipped == False
                )
            )
        )
        recent_scores = [s for s in scores_result.scalars().all() if s is not None]
        
        if recent_scores:
            recent_avg = sum(recent_scores) / len(recent_scores)
            cohort_data.append({
                "student_id": str(student.id),
                "name": student.name,
                "recent_avg": round(recent_avg, 2),
                "baseline": student.baseline_score
            })
    
    return cohort_data



# Additional helper functions for dashboard and analytics

async def get_student_by_id(
    db: AsyncSession, 
    student_id: UUID
) -> Optional[Student]:
    """Get student by ID with institution loaded."""
    result = await db.execute(
        select(Student)
        .where(Student.id == student_id)
        .options(selectinload(Student.institution))
    )
    return result.scalar_one_or_none()


async def get_latest_burnout_state(
    db: AsyncSession,
    student_id: UUID
) -> Optional[BurnoutState]:
    """Get the most recent burnout state for a student."""
    result = await db.execute(
        select(BurnoutState)
        .where(BurnoutState.student_id == student_id)
        .order_by(BurnoutState.assessed_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_all_checkins_for_student(
    db: AsyncSession,
    student_id: UUID,
    days: int = 30
) -> List[CheckIn]:
    """Get all check-ins for a student within specified days."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(CheckIn)
        .where(
            and_(
                CheckIn.student_id == student_id,
                CheckIn.checked_in_at >= cutoff_date
            )
        )
        .order_by(CheckIn.checked_in_at.desc())
    )
    return list(result.scalars().all())


async def get_interventions_for_student(
    db: AsyncSession,
    student_id: UUID,
    limit: int = 10
) -> List[Intervention]:
    """Get recent interventions for a student."""
    result = await db.execute(
        select(Intervention)
        .where(Intervention.student_id == student_id)
        .order_by(Intervention.triggered_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())



async def save_cohort_alert(
    db: AsyncSession,
    alert_data: Dict[str, Any]
) -> CohortAlert:
    """Save a cohort anomaly alert."""
    alert = CohortAlert(**alert_data)
    db.add(alert)
    await db.flush()
    await db.refresh(alert)
    return alert


async def get_active_cohort_alerts(
    db: AsyncSession,
    institution_id: UUID
) -> List[CohortAlert]:
    """Get unacknowledged cohort alerts for an institution."""
    result = await db.execute(
        select(CohortAlert)
        .where(
            and_(
                CohortAlert.institution_id == institution_id,
                CohortAlert.acknowledged == False
            )
        )
        .order_by(CohortAlert.detected_at.desc())
    )
    return list(result.scalars().all())


async def update_student_baseline(
    db: AsyncSession,
    student_id: UUID,
    new_baseline: float
) -> Student:
    """Update a student's baseline score."""
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one()
    student.baseline_score = new_baseline
    await db.flush()
    await db.refresh(student)
    return student


async def get_institution_statistics(
    db: AsyncSession,
    institution_id: UUID
) -> Dict[str, Any]:
    """
    Get dashboard statistics for an institution.
    Returns counts of students by risk state.
    """
    # Get all active students
    students_result = await db.execute(
        select(Student)
        .where(
            and_(
                Student.institution_id == institution_id,
                Student.is_active == True
            )
        )
    )
    students = students_result.scalars().all()
    
    total_students = len(students)
    
    # Get latest burnout state for each student
    state_counts = {"stable": 0, "at_risk": 0, "crisis": 0}
    
    for student in students:
        latest_state = await get_latest_burnout_state(db, student.id)
        if latest_state:
            state_counts[latest_state.state] = state_counts.get(latest_state.state, 0) + 1
        else:
            state_counts["stable"] += 1
    
    return {
        "total_students": total_students,
        "stable": state_counts["stable"],
        "at_risk": state_counts["at_risk"],
        "crisis": state_counts["crisis"]
    }

