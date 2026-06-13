"""
Quick script to check if your check-ins were saved
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from database.connection import AsyncSessionLocal, init_db
from sqlalchemy import select, and_
from database.models import Student, CheckIn

async def check_checkins():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Find you
        result = await db.execute(
            select(Student).where(Student.phone == '+919944906759')
        )
        student = result.scalar_one_or_none()
        
        if not student:
            print("❌ Student not found!")
            return
        
        print(f"✅ Found: {student.name}")
        print(f"   ID: {student.id}")
        print(f"   Phone: {student.phone}")
        print(f"   Baseline: {student.baseline_score}")
        
        # Get check-ins
        checkins_result = await db.execute(
            select(CheckIn)
            .where(CheckIn.student_id == student.id)
            .order_by(CheckIn.checked_in_at.desc())
        )
        checkins = checkins_result.scalars().all()
        
        print(f"\n📊 Check-ins: {len(checkins)}")
        for i, checkin in enumerate(checkins, 1):
            print(f"   {i}. {checkin.checked_in_at} - Score: {checkin.mood_score}, Ate: {checkin.ate_properly}, Word: {checkin.one_word}")

if __name__ == "__main__":
    asyncio.run(check_checkins())
