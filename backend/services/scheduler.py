"""
GuardianAI - Autonomous Scheduler
APScheduler for automated daily operations:
1. Daily check-in blast (7:30 PM IST)
2. Morning risk scan (8:00 AM IST)
3. Weekly baseline update (Sunday midnight)
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import os
import statistics

from dotenv import load_dotenv
load_dotenv()

from services.whatsapp import get_whatsapp_service
from database.connection import AsyncSessionLocal
from database.models import Student, CheckIn, BurnoutState, Intervention
from database import crud
from agents.hmm_engine import BurnoutHMM
from agents.adversarial_validator import AdversarialValidator
from agents.cohort_detector import CohortDetector
from agents.intervention_orchestrator import InterventionOrchestrator
from sqlalchemy import select, and_, func
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

# Initialize agents
hmm_engine = BurnoutHMM()
adversarial_validator = AdversarialValidator()
cohort_detector = CohortDetector()


async def daily_checkin_blast():
    """
    JOB 1: Daily Check-in Blast
    Runs at 7:30 PM IST every day.
    Sends WhatsApp check-in prompt to all active students.
    """
    logger.info("🚀 Starting daily check-in blast...")
    whatsapp = get_whatsapp_service()
    
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Student).where(
                and_(
                    Student.is_active == True,
                    Student.consent_given == True
                )
            )
        )
        students = result.scalars().all()
        
        sent_count = 0
        for student in students:
            try:
                # Send check-in prompt
                message = (
                    f"Hey {student.name.split()[0]}! 👋 Quick check-in:\n\n"
                    f"1️⃣ How was today? (1-5)\n"
                    f"2️⃣ Did you eat properly? (yes/mostly/no)\n"
                    f"3️⃣ One word for how you're feeling?"
                )
                whatsapp.send_message(f"whatsapp:{student.phone}", message)
                sent_count += 1
            except Exception as e:
                logger.error(f"Failed to send to {student.name}: {e}")
        
        logger.info(f"✅ Daily check-in blast complete: {sent_count}/{len(students)} sent")


async def morning_risk_scan():
    """
    JOB 2: Morning Risk Scan
    Runs at 8:00 AM IST every day.
    - Runs HMM assessment on all students with new data
    - Triggers interventions for new At-Risk or Crisis detections
    - Runs cohort anomaly scan
    - Generates daily summary for counsellors
    """
    logger.info("🔍 Starting morning risk scan...")
    
    async with AsyncSessionLocal() as db:
        # Get all active students
        students_result = await db.execute(
            select(Student).where(Student.is_active == True)
        )
        students = list(students_result.scalars().all())
        
        new_at_risk = []
        new_crisis = []
        total_assessed = 0
        
        # Assess each student
        for student in students:
            try:
                # Get recent scores (last 30 days)
                recent_scores = await crud.get_recent_scores(db, student.id, days=30)
                recent_onewords = await crud.get_recent_onewords(db, student.id, days=7)
                
                if len(recent_scores) < 3:
                    continue  # Not enough data
                
                # Run HMM assessment
                assessment = hmm_engine.assess(
                    scores=recent_scores,
                    baseline=student.baseline_score or 3.0
                )
                
                # Run adversarial validation
                validation = adversarial_validator.validate(recent_scores)
                
                # Save burnout state
                await crud.save_burnout_state(db, student.id, assessment, validation)
                total_assessed += 1
                
                # Check if state changed to at-risk or crisis
                if assessment.state in ['at_risk', 'crisis']:
                    # Get last intervention
                    last_intervention = await crud.get_last_intervention(db, student.id)
                    
                    # Check cooldown (24 hours)
                    if last_intervention:
                        hours_since = (datetime.utcnow() - last_intervention.triggered_at).total_seconds() / 3600
                        if hours_since < 24:
                            continue  # Still in cooldown
                    
                    # Trigger intervention (simplified for scan)
                    if assessment.state == 'crisis':
                        new_crisis.append(student.name)
                    else:
                        new_at_risk.append(student.name)
                
            except Exception as e:
                logger.error(f"Error assessing {student.name}: {e}")
        
        # Run cohort anomaly scan
        cohort_alerts = await scan_cohort_anomalies(db, students)
        
        # Generate summary
        summary = (
            f"📊 GuardianAI Morning Risk Scan\n"
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Students Assessed: {total_assessed}/{len(students)}\n"
            f"New At-Risk: {len(new_at_risk)}\n"
            f"New Crisis: {len(new_crisis)}\n"
            f"Cohort Alerts: {len(cohort_alerts)}\n\n"
        )
        
        if new_crisis:
            summary += f"🚨 CRISIS: {', '.join(new_crisis)}\n"
        if new_at_risk:
            summary += f"⚠️  AT RISK: {', '.join(new_at_risk)}\n"
        if cohort_alerts:
            summary += f"👥 COHORT ALERTS: {', '.join([a['batch'] for a in cohort_alerts])}\n"
        
        logger.info(f"✅ Morning risk scan complete:\n{summary}")
        
        # TODO: Send summary to counsellors via WhatsApp/email
        await db.commit()


async def scan_cohort_anomalies(db, students):
    """Helper to scan for cohort anomalies across all batches."""
    # Group students by batch
    batches = {}
    for student in students:
        if student.batch:
            if student.batch not in batches:
                batches[student.batch] = []
            batches[student.batch].append(student)
    
    alerts = []
    for batch_name, batch_students in batches.items():
        if len(batch_students) < 8:
            continue  # Need at least 8 students for cohort detection
        
        # Get cohort data
        cohort_data = await crud.get_cohort_data_by_batch(
            db, 
            batch_students[0].institution_id,
            batch_name
        )
        
        # Run cohort detector
        if cohort_data:
            result = cohort_detector.detect_cohort_anomaly(cohort_data, batch_name)
            if result['is_anomaly']:
                alerts.append(result)
                # Save cohort alert to database
                # TODO: Implement save_cohort_alert in crud
    
    return alerts


async def weekly_baseline_update():
    """
    JOB 3: Weekly Baseline Update
    Runs every Sunday at midnight.
    Recalculates personal baseline for each student using median of last 30 days.
    """
    logger.info("📈 Starting weekly baseline update...")
    
    async with AsyncSessionLocal() as db:
        students_result = await db.execute(
            select(Student).where(Student.is_active == True)
        )
        students = list(students_result.scalars().all())
        
        updated_count = 0
        for student in students:
            try:
                # Get last 30 days of scores
                scores = await crud.get_recent_scores(db, student.id, days=30)
                
                if len(scores) < 10:
                    continue  # Need at least 10 data points
                
                # Calculate new baseline (median is robust to outliers)
                new_baseline = statistics.median(scores)
                
                # Update only if significantly different (>0.3 difference)
                if abs(new_baseline - student.baseline_score) > 0.3:
                    await crud.update_student_baseline(db, student.id, new_baseline)
                    updated_count += 1
                    logger.info(f"Updated {student.name}: {student.baseline_score:.1f} → {new_baseline:.1f}")
                
            except Exception as e:
                logger.error(f"Error updating baseline for {student.name}: {e}")
        
        await db.commit()
        logger.info(f"✅ Weekly baseline update complete: {updated_count}/{len(students)} updated")


def start_scheduler():
    """
    Start the scheduler with all 3 autonomous jobs.
    Called on application startup.
    """
    # JOB 1: Daily check-in blast at 7:30 PM IST
    scheduler.add_job(
        daily_checkin_blast,
        trigger="cron",
        hour=19,  # 7:30 PM IST
        minute=30,
        timezone="Asia/Kolkata",
        id="daily_checkin_blast",
        replace_existing=True
    )
    
    # JOB 2: Morning risk scan at 8:00 AM IST
    scheduler.add_job(
        morning_risk_scan,
        trigger="cron",
        hour=8,  # 8:00 AM IST
        minute=0,
        timezone="Asia/Kolkata",
        id="morning_risk_scan",
        replace_existing=True
    )
    
    # JOB 3: Weekly baseline update (Sunday at midnight IST)
    scheduler.add_job(
        weekly_baseline_update,
        trigger="cron",
        day_of_week="sun",
        hour=0,
        minute=0,
        timezone="Asia/Kolkata",
        id="weekly_baseline_update",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("✅ GuardianAI Scheduler started with 3 jobs:")
    logger.info("  📱 Daily check-in blast: 7:30 PM IST")
    logger.info("  🔍 Morning risk scan: 8:00 AM IST")
    logger.info("  📈 Weekly baseline update: Sunday midnight IST")


def stop_scheduler():
    """Stop the scheduler gracefully."""
    scheduler.shutdown(wait=True)
    logger.info("🔌 GuardianAI Scheduler stopped")
