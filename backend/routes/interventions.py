"""
GuardianAI - Interventions API Routes
View autonomous intervention history
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from uuid import UUID

from database import get_db
from database.models import Intervention, Student

router = APIRouter()


@router.get("/")
async def get_interventions(
    student_id: str = None,
    level: int = None,
    days: int = 7,
    db: AsyncSession = Depends(get_db)
):
    """Get intervention history, optionally filtered."""
    query = select(Intervention).where(
        Intervention.triggered_at >= datetime.utcnow() - timedelta(days=days)
    )
    
    if student_id:
        query = query.where(Intervention.student_id == UUID(student_id))
    
    if level:
        query = query.where(Intervention.level == level)
    
    query = query.order_by(Intervention.triggered_at.desc())
    
    result = await db.execute(query)
    interventions = result.scalars().all()
    
    return {
        "interventions": [
            {
                "id": str(i.id),
                "student_id": str(i.student_id),
                "level": i.level,
                "trigger_reason": i.trigger_reason,
                "message_sent": i.message_sent,
                "recipient": i.recipient,
                "triggered_at": i.triggered_at.isoformat(),
                "outcome": i.outcome
            }
            for i in interventions
        ]
    }


@router.get("/{intervention_id}")
async def get_intervention(intervention_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single intervention by ID."""
    result = await db.execute(
        select(Intervention).where(Intervention.id == UUID(intervention_id))
    )
    intervention = result.scalar_one_or_none()
    
    if not intervention:
        return {"error": "Intervention not found"}, 404
    
    return {
        "id": str(intervention.id),
        "student_id": str(intervention.student_id),
        "level": intervention.level,
        "trigger_reason": intervention.trigger_reason,
        "action_taken": intervention.action_taken,
        "message_sent": intervention.message_sent,
        "recipient": intervention.recipient,
        "triggered_at": intervention.triggered_at.isoformat(),
        "outcome": intervention.outcome
    }
