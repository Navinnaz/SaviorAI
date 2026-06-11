"""
GuardianAI - Daily Check-in Scheduler
APScheduler for automated daily WhatsApp check-ins
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os

from services.whatsapp import send_whatsapp_message
from database import AsyncSessionLocal
from database.models import Student
from sqlalchemy import select

scheduler = AsyncIOScheduler()


async def send_daily_checkins():
    """
    Send daily check-in messages to all active students.
    Scheduled to run at 8 PM IST every day.
    """
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Student).where(Student.is_active == True)
        )
        students = result.scalars().all()
        
        checkin_message = (
            "🌟 GuardianAI Daily Check-in\n\n"
            "How are you doing today?\n"
            "Reply with: [mood 1-5] [ate properly? yes/no] [one word]\n\n"
            "Example: 4 yes focused"
        )
        
        for student in students:
            await send_whatsapp_message(student.phone, checkin_message)
        
        print(f"✅ Sent {len(students)} daily check-ins at {datetime.now()}")


def start_scheduler():
    """
    Start the scheduler for daily check-ins.
    Called on application startup.
    """
    # Schedule daily check-ins at 8 PM IST
    hour = int(os.getenv("CHECK_IN_TIME_HOUR", "20"))
    minute = int(os.getenv("CHECK_IN_TIME_MINUTE", "0"))
    
    scheduler.add_job(
        send_daily_checkins,
        trigger="cron",
        hour=hour,
        minute=minute,
        id="daily_checkin",
        replace_existing=True
    )
    
    scheduler.start()
    print(f"✅ Scheduler started. Daily check-ins at {hour}:{minute:02d}")


def stop_scheduler():
    """Stop the scheduler."""
    scheduler.shutdown()
    print("🔌 Scheduler stopped")
