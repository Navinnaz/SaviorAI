"""
GuardianAI - Dashboard API Routes
Dashboard data for counsellors and administrators
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from uuid import UUID

from database import get_db
from database.models import Student, BurnoutState, CheckIn, Intervention

router = APIRouter()


@router.get("/overview")
async def get_dashboard_overview(
    institution_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get overall dashboard statistics.
    Returns risk distribution, recent interventions, and trends.
    """
    # Get latest burnout state for each student
    latest_states_query = select(BurnoutState).where(
        BurnoutState.assessed_at >= datetime.utcnow() - timedelta(days=1)
    )
    
    if institution_id:
        latest_states_query = latest_states_query.join(Student).where(
            Student.institution_id == UUID(institution_id)
        )
    
    result = await db.execute(latest_states_query)
    states = result.scalars().all()
    
    # Count by state
    state_counts = {"stable": 0, "at_risk": 0, "crisis": 0}
    for state in states:
        state_counts[state.state] = state_counts.get(state.state, 0) + 1
    
    return {
        "total_students": len(states),
        "stable": state_counts["stable"],
        "at_risk": state_counts["at_risk"],
        "crisis": state_counts["crisis"],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/risk-heatmap")
async def get_risk_heatmap(
    institution_id: str = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Get risk heatmap data for visualization.
    Returns students with their latest risk state.
    """
    query = """
    SELECT DISTINCT ON (s.id)
        s.id, s.name, s.batch, s.year_of_study,
        bs.state, bs.hmm_probability, bs.trend_score, bs.consecutive_low_days
    FROM students s
    LEFT JOIN burnout_states bs ON s.id = bs.student_id
    ORDER BY s.id, bs.assessed_at DESC
    """
    
    result = await db.execute(query)
    rows = result.fetchall()
    
    return {
        "students": [
            {
                "id": str(row[0]),
                "name": row[1],
                "batch": row[2],
                "year": row[3],
                "state": row[4] or "stable",
                "probability": row[5],
                "trend": row[6]
            }
            for row in rows
        ]
    }
