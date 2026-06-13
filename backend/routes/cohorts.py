"""
GuardianAI - Cohorts API Routes
Batch-level analytics and cohort anomaly detection
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from uuid import UUID

from backend.database.connection import get_db
from backend.database.models import CohortAlert, Student, CheckIn

router = APIRouter()


@router.get("/alerts")
async def get_cohort_alerts(
    institution_id: str = None,
    acknowledged: bool = None,
    db: AsyncSession = Depends(get_db)
):
    """Get cohort-level anomaly alerts."""
    query = select(CohortAlert)
    
    if institution_id:
        query = query.where(CohortAlert.institution_id == UUID(institution_id))
    
    if acknowledged is not None:
        query = query.where(CohortAlert.acknowledged == acknowledged)
    
    query = query.order_by(CohortAlert.detected_at.desc())
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    
    return {
        "cohort_alerts": [
            {
                "id": str(a.id),
                "batch": a.batch,
                "detected_at": a.detected_at.isoformat(),
                "affected_students": a.affected_students,
                "affected_percentage": a.affected_percentage,
                "avg_score_drop": a.avg_score_drop,
                "likely_cause": a.likely_cause,
                "recommended_action": a.institutional_action_recommended,
                "acknowledged": a.acknowledged
            }
            for a in alerts
        ]
    }


@router.get("/batches")
async def get_batch_analytics(
    institution_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get analytics for all batches in an institution."""
    query = select(Student)
    
    if institution_id:
        query = query.where(Student.institution_id == UUID(institution_id))
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    # Group by batch
    batches = {}
    for student in students:
        batch = student.batch or "Unknown"
        if batch not in batches:
            batches[batch] = []
        batches[batch].append(student)
    
    return {
        "batches": [
            {
                "batch": batch,
                "student_count": len(students_in_batch)
            }
            for batch, students_in_batch in batches.items()
        ]
    }
