"""
Check Priya Sharma's burnout state history
"""
import asyncio
import sys

sys.path.insert(0, 'backend')

from backend.database.connection import AsyncSessionLocal, init_db
from backend.database.models import Student, BurnoutState, CheckIn
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def check_priya():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Find Priya Sharma
        result = await db.execute(
            select(Student).where(Student.name == 'Priya Sharma')
        )
        priya = result.scalar_one_or_none()
        
        if not priya:
            print("❌ Priya Sharma not found!")
            return
        
        print(f"✅ Found: {priya.name}")
        print(f"   ID: {priya.id}")
        print(f"   Baseline: {priya.baseline_score}")
        
        # Get check-ins
        checkins_result = await db.execute(
            select(CheckIn)
            .where(CheckIn.student_id == priya.id)
            .order_by(CheckIn.checked_in_at.asc())
        )
        checkins = list(checkins_result.scalars().all())
        
        print(f"\n📊 Check-ins: {len(checkins)}")
        if checkins:
            print(f"   First: {checkins[0].checked_in_at.date()}")
            print(f"   Last:  {checkins[-1].checked_in_at.date()}")
        
        # Get burnout states
        states_result = await db.execute(
            select(BurnoutState)
            .where(BurnoutState.student_id == priya.id)
            .order_by(BurnoutState.assessed_at.asc())
        )
        states = list(states_result.scalars().all())
        
        print(f"\n🧠 Burnout State Assessments: {len(states)}")
        
        if states:
            print("\n📈 State Timeline:")
            for i, state in enumerate(states, 1):
                # Calculate display percentage (same logic as frontend)
                if state.state == 'crisis':
                    display_pct = 85 + min(state.consecutive_low_days * 2, 10)
                elif state.state == 'at_risk':
                    display_pct = 50 + max(abs(state.trend_score) * 10, 0)
                else:
                    display_pct = max(15 - (state.trend_score if state.trend_score > 0 else 0) * 5, 5)
                display_pct = min(round(display_pct), 95)
                
                print(f"   {i}. {state.assessed_at.date()} - {state.state.upper():8} | "
                      f"Display: {display_pct:2}% | "
                      f"Trend: {state.trend_score:+.1f} | "
                      f"Consec Low: {state.consecutive_low_days}")
        
        print("\n💡 Each bar in the timeline represents one HMM assessment")
        print("   This is normal - states are assessed periodically (after each check-in)")

if __name__ == "__main__":
    asyncio.run(check_priya())
