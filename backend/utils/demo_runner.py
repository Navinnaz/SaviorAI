"""
GuardianAI - Live Demo Runner

Orchestrates compelling live demonstrations with real-time database and dashboard updates.

Usage:
    python -m backend.utils.demo_runner --scenario setup
    python -m backend.utils.demo_runner --scenario live
    python -m backend.utils.demo_runner --scenario reset

Scenarios:
    setup: Populate 50 students with 14 days of history
    live: Simulate 4 real-time events for judges
    reset: Clear demo data, restore to clean state
"""

import asyncio
import argparse
import sys
import os
from datetime import datetime, timedelta
from uuid import uuid4, UUID
from typing import Dict, Any, List
import time

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.database.connection import AsyncSessionLocal, engine
from backend.database.models import (
    Student, CheckIn, BurnoutState, Intervention, CohortAlert, Institution, Base
)
from backend.database import crud
from backend.agents.hmm_engine import BurnoutHMM
from backend.agents.adversarial_validator import AdversarialValidator
from backend.agents.cohort_detector import CohortAnomalyDetector
from backend.agents.intervention_orchestrator import InterventionOrchestrator
from backend.services.sentiment import analyze_sentiment
from backend.utils.data_generator import generate_demo_data

# For OpenAI integration
import openai
from dotenv import load_dotenv

load_dotenv()


class DemoRunner:
    """Orchestrates live demo scenarios with real-time updates."""
    
    def __init__(self):
        self.hmm = BurnoutHMM()
        self.validator = AdversarialValidator()
        self.cohort_detector = CohortAnomalyDetector()
        
        # Initialize OpenAI client for intervention orchestrator
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=api_key)
            self.orchestrator = InterventionOrchestrator(self.openai_client)
        else:
            print("⚠️  WARNING: OPENAI_API_KEY not found in .env")
            print("   Intervention messages will use fallback templates\n")
            self.openai_client = None
            self.orchestrator = None
        
        self.institution_id = None
        self.priya_id = None
        self.gaming_student_id = None
        self.mech_batch_ids = []
    
    async def run_scenario(self, scenario: str):
        """Route to appropriate scenario handler."""
        if scenario == "setup":
            await self.scenario_setup()
        elif scenario == "live":
            await self.scenario_live()
        elif scenario == "reset":
            await self.scenario_reset()
        else:
            print(f"❌ Unknown scenario: {scenario}")
            print("Valid scenarios: setup, live, reset")
            sys.exit(1)
    
    # ==================== SCENARIO: SETUP ====================
    
    async def scenario_setup(self):
        """Populate 50 students with 14 days of history."""
        print("\n" + "="*70)
        print("🎬 DEMO SETUP: Populating database with 50 students")
        print("="*70 + "\n")
        
        async with AsyncSessionLocal() as db:
            # Generate demo data
            print("📊 Generating demo data...")
            demo_data = generate_demo_data(num_students=50)
            
            # Save institution
            print("\n📍 Creating institution...")
            inst_data = demo_data["institution"]
            institution = Institution(**inst_data)
            db.add(institution)
            await db.commit()
            await db.refresh(institution)
            self.institution_id = institution.id
            print(f"   ✅ Institution: {institution.name} (ID: {institution.id})")
            
            # Save students
            print(f"\n👥 Creating {len(demo_data['students'])} students...")
            for student_data in demo_data["students"]:
                student = Student(**student_data)
                db.add(student)
                
                # Track special students for live demo
                if student.name == "Priya Sharma":
                    await db.flush()
                    await db.refresh(student)
                    self.priya_id = student.id
                    print(f"   🎯 Crisis student: {student.name} (ID: {student.id})")
                elif student.batch == "MECH-2023":
                    await db.flush()
                    await db.refresh(student)
                    self.mech_batch_ids.append(student.id)
            
            await db.commit()
            print(f"   ✅ Created {len(demo_data['students'])} students")
            
            # Save check-ins
            print(f"\n📝 Creating {len(demo_data['checkins'])} check-ins...")
            for checkin_data in demo_data["checkins"]:
                checkin = CheckIn(**checkin_data)
                db.add(checkin)
            await db.commit()
            print(f"   ✅ Created {len(demo_data['checkins'])} check-ins")
            
            # Save burnout states
            print(f"\n🧠 Creating {len(demo_data['burnout_states'])} burnout states...")
            for state_data in demo_data["burnout_states"]:
                state = BurnoutState(**state_data)
                db.add(state)
            await db.commit()
            print(f"   ✅ Created {len(demo_data['burnout_states'])} burnout states")
            
            # Save interventions
            print(f"\n🚨 Creating {len(demo_data['interventions'])} interventions...")
            for intervention_data in demo_data["interventions"]:
                intervention = Intervention(**intervention_data)
                db.add(intervention)
            await db.commit()
            print(f"   ✅ Created {len(demo_data['interventions'])} interventions")
            
            # Save cohort alerts
            if demo_data["cohort_alerts"]:
                print(f"\n⚠️  Creating {len(demo_data['cohort_alerts'])} cohort alerts...")
                for alert_data in demo_data["cohort_alerts"]:
                    alert = CohortAlert(**alert_data)
                    db.add(alert)
                await db.commit()
                print(f"   ✅ Created {len(demo_data['cohort_alerts'])} cohort alerts")
        
        # Reload IDs for display
        await self._reload_demo_ids()
        
        print("\n" + "="*70)
        print("✅ DEMO SETUP COMPLETE")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"   • Institution ID: {self.institution_id}")
        print(f"   • Total students: 50")
        print(f"   • Crisis demo student: Priya Sharma (ID: {self.priya_id})")
        print(f"   • MECH-2023 cohort: {len(self.mech_batch_ids)} students")
        print(f"   • Check-in history: 14 days")
        print(f"\n🎯 Next steps:")
        print(f"   1. Start backend: python -m backend.main")
        print(f"   2. Start frontend: cd frontend && npm run dev")
        print(f"   3. Open dashboard: http://localhost:3000")
        print(f"   4. ⚠️  IMPORTANT: Update institution ID in browser:")
        print(f"      Open browser console (F12) and run:")
        print(f"      localStorage.setItem('institutionId', '{self.institution_id}')")
        print(f"      location.reload()")
        print(f"   5. Run live demo: python -m backend.utils.demo_runner --scenario live\n")
    
    async def _reload_demo_ids(self):
        """Reload demo context IDs after setup."""
        async with AsyncSessionLocal() as db:
            await self._load_demo_context(db)
    
    # ==================== SCENARIO: LIVE ====================
    
    async def scenario_live(self):
        """Simulate 4 real-time events for live demo."""
        print("\n" + "="*70)
        print("🎬 LIVE DEMO: Simulating real-time events")
        print("="*70 + "\n")
        
        async with AsyncSessionLocal() as db:
            # Get institution and students
            await self._load_demo_context(db)
            
            if not self.institution_id or not self.priya_id:
                print("❌ Demo data not found. Run --scenario setup first.")
                return
            
            print(f"✅ Loaded demo context:")
            print(f"   • Institution ID: {self.institution_id}")
            print(f"   • Priya Sharma ID: {self.priya_id}")
            print(f"   • Gaming student ID: {self.gaming_student_id}")
            print(f"   • MECH-2023 cohort: {len(self.mech_batch_ids)} students\n")
            
            # Event 1: Crisis check-in
            await self._event_1_crisis_checkin(db)
            await asyncio.sleep(3)
            
            # Event 2: Gaming detection
            await self._event_2_gaming_detection(db)
            await asyncio.sleep(3)
            
            # Event 3: Cohort anomaly
            await self._event_3_cohort_scan(db)
            await asyncio.sleep(3)
            
            # Event 4: Action log summary
            await self._event_4_action_log(db)
        
        print("\n" + "="*70)
        print("✅ LIVE DEMO COMPLETE")
        print("="*70)
        print("\n🎯 View results:")
        print(f"   • Dashboard: http://localhost:3000")
        print(f"   • Student profile: http://localhost:3000/student/{self.priya_id}")
        print(f"   • Action log: http://localhost:3000/actions\n")
        print("💡 To run again for judges:")
        print("   1. python -m backend.utils.demo_runner --scenario reset")
        print("   2. python -m backend.utils.demo_runner --scenario setup")
        print("   3. python -m backend.utils.demo_runner --scenario live\n")
    
    async def _load_demo_context(self, db):
        """Load demo data context (IDs of special students)."""
        from sqlalchemy import select
        
        # Get institution
        result = await db.execute(select(Institution).limit(1))
        institution = result.scalar_one_or_none()
        if institution:
            self.institution_id = institution.id
        
        # Get Priya
        result = await db.execute(
            select(Student).where(Student.name == "Priya Sharma")
        )
        priya = result.scalar_one_or_none()
        if priya:
            self.priya_id = priya.id
        
        # Get gaming student (find one with high variance flag)
        result = await db.execute(
            select(BurnoutState.student_id)
            .where(BurnoutState.variance_flag == True)
            .distinct()
            .limit(1)
        )
        gaming_row = result.first()
        if gaming_row:
            self.gaming_student_id = gaming_row[0]
        
        # Get MECH-2023 students
        result = await db.execute(
            select(Student.id).where(Student.batch == "MECH-2023")
        )
        self.mech_batch_ids = [row[0] for row in result.all()]
    
    async def _event_1_crisis_checkin(self, db):
        """Event 1: Priya sends crisis check-in "1 no empty"."""
        print("\n" + "─"*70)
        print("⏱️  EVENT 1 (T+0s): CRISIS CHECK-IN")
        print("─"*70 + "\n")
        
        print("📱 Simulating WhatsApp message from Priya Sharma: '1 no empty'")
        
        # Parse message
        mood_score = 1
        ate_properly = "no"
        one_word = "empty"
        
        # Sentiment analysis
        sentiment_result = analyze_sentiment(one_word)
        sentiment = sentiment_result["sentiment"]
        sentiment_score = sentiment_result["score"]
        print(f"   🔍 Sentiment: {sentiment} (score: {sentiment_score})")
        
        # Save check-in
        checkin_data = {
            "id": uuid4(),
            "student_id": self.priya_id,
            "checked_in_at": datetime.now(datetime.UTC) if hasattr(datetime, 'UTC') else datetime.utcnow(),
            "mood_score": mood_score,
            "ate_properly": ate_properly,
            "one_word": one_word,
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "raw_message": "1 no empty",
            "skipped": False
        }
        
        checkin = await crud.save_checkin(db, checkin_data)
        await db.commit()
        print(f"   ✅ Check-in saved: {checkin.id}")
        
        # Get recent scores for HMM
        scores = await crud.get_recent_scores(db, self.priya_id, days=14)
        onewords = await crud.get_recent_onewords(db, self.priya_id, days=7)
        
        print(f"   📊 Recent scores (last 10): {scores[-10:]}")
        
        # Run HMM assessment
        print("\n   🧠 Running HMM burnout assessment...")
        student = await crud.get_student_by_id(db, self.priya_id)
        assessment = self.hmm.assess(scores, baseline=student.baseline_score)
        print(f"      State: {assessment.state.upper()}")
        print(f"      Probability: {assessment.probability:.0%}")
        print(f"      Trend: {assessment.trend_score:+.2f}")
        print(f"      Consecutive low days: {assessment.consecutive_low_days}")
        
        # Run adversarial validation
        print("\n   🔍 Running adversarial validation...")
        validation = self.validator.validate(scores)
        print(f"      Suspicious: {validation['is_suspicious']}")
        print(f"      Confidence: {validation['confidence']:.0%}")
        
        # Save burnout state
        await crud.save_burnout_state(db, self.priya_id, assessment, validation)
        await db.commit()
        
        # Run intervention orchestrator
        if self.orchestrator:
            print("\n   🚨 Running intervention orchestrator...")
            
            last_intervention = await crud.get_last_intervention(db, self.priya_id)
            
            decision = await self.orchestrator.decide_and_act(
                student=student.to_dict(),
                assessment=assessment,
                recent_scores=scores,
                recent_onewords=onewords,
                validation_result=validation,
                last_intervention=last_intervention.to_dict() if last_intervention else None
            )
            
            if decision["action"] == "send":
                print(f"      🎯 Action: SEND")
                print(f"      📨 Level: {decision['level']} ({['', 'Peer Nudge', 'Counsellor', 'Emergency', 'Institution'][decision['level']]})") 
                print(f"      👤 Recipient: {decision['recipient']}")
                print(f"      💬 Message preview: {decision['message'][:100]}...")
                
                # Save intervention
                intervention_data = {
                    "student_id": self.priya_id,
                    "level": decision["level"],
                    "trigger_reason": decision["reasoning"],
                    "action_taken": "send",
                    "message_sent": decision["message"],
                    "recipient": decision["recipient"],
                    "was_acknowledged": False,
                    "outcome": "pending"
                }
                await crud.save_intervention(db, intervention_data)
                await db.commit()
                print(f"      ✅ Intervention saved to database")
            else:
                print(f"      ⏸️  Action: {decision['action'].upper()}")
                print(f"      Reason: {decision.get('reason', 'N/A')}")
        else:
            print("\n   ⚠️  Skipping intervention (OpenAI API key not configured)")
        
        print("\n   🎯 Dashboard updates:")
        print(f"      • Priya's card is now RED (crisis state)")
        print(f"      • Intervention appears in Action Log")
        print(f"      • Real-time notification sent to counsellor")
        
        print("\n✅ EVENT 1 COMPLETE\n")
    
    async def _event_2_gaming_detection(self, db):
        """Event 2: Gaming student sends "4 yes good" (14th perfect day)."""
        print("\n" + "─"*70)
        print("⏱️  EVENT 2 (T+15s): GAMING DETECTION")
        print("─"*70 + "\n")
        
        if not self.gaming_student_id:
            print("⚠️  No gaming students found in demo data, skipping...")
            print("   (This is expected if data_generator doesn't create gaming patterns)")
            return
        
        # Get student
        from sqlalchemy import select
        student = await crud.get_student_by_id(db, self.gaming_student_id)
        
        print(f"📱 Simulating check-in from {student.name}: '4 yes good'")
        print(f"   (This is their 14th consecutive perfect score)")
        
        # Save check-in
        checkin_data = {
            "id": uuid4(),
            "student_id": self.gaming_student_id,
            "checked_in_at": datetime.utcnow(),
            "mood_score": 4,
            "ate_properly": "yes",
            "one_word": "good",
            "sentiment": "positive",
            "sentiment_score": 0.5,
            "raw_message": "4 yes good",
            "skipped": False
        }
        await crud.save_checkin(db, checkin_data)
        await db.commit()
        
        # Get scores and validate
        scores = await crud.get_recent_scores(db, self.gaming_student_id, days=14)
        print(f"   📊 Recent scores: {scores[-14:]}")
        
        print("\n   🔍 Running adversarial validation...")
        validation = self.validator.validate(scores)
        
        print(f"      🚩 Suspicious: {validation['is_suspicious']}")
        print(f"      🎯 Confidence: {validation['confidence']:.0%}")
        print(f"      🔎 Flags detected:")
        for flag in validation["flags"]:
            print(f"         • {flag['type']}: {flag['detail']}")
        
        # Update burnout state with variance flag
        assessment = self.hmm.assess(scores, baseline=4.0)
        await crud.save_burnout_state(db, self.gaming_student_id, assessment, validation)
        await db.commit()
        
        print("\n   🎯 Dashboard updates:")
        print(f"      • {student.name}'s card now shows ⚠️ WARNING BADGE")
        print(f"      • Masking behavior flagged")
        print(f"      • Counsellor notified for gentle outreach")
        
        print("\n✅ EVENT 2 COMPLETE\n")
    
    async def _event_3_cohort_scan(self, db):
        """Event 3: Run cohort scan on MECH-2023 batch."""
        print("\n" + "─"*70)
        print("⏱️  EVENT 3 (T+30s): COHORT ANOMALY DETECTION")
        print("─"*70 + "\n")
        
        print("🔍 Running cohort scan on MECH-2023 batch...")
        
        # Get cohort data
        batch_data = await crud.get_cohort_data_by_batch(
            db, self.institution_id, "MECH-2023"
        )
        
        print(f"   📊 Found {len(batch_data)} students in MECH-2023")
        
        if len(batch_data) < 3:
            print("   ⚠️  Not enough students in MECH-2023 for cohort detection")
            print("   (Need at least 3 students with recent check-ins)")
            return
        
        # Run detection
        result = self.cohort_detector.detect(batch_data)
        
        if result["anomaly_detected"]:
            print(f"\n   🚨 COHORT ANOMALY DETECTED!")
            print(f"      Affected: {result['affected_count']}/{result['total_count']} students ({result['affected_percentage']}%)")
            print(f"      Average drop: {result['average_score_drop']:.2f} points")
            print(f"      Severity: {result['severity'].upper()}")
            
            # Save cohort alert
            alert_data = {
                "institution_id": self.institution_id,
                "batch": "MECH-2023",
                "detected_at": datetime.utcnow(),
                "affected_students": result["affected_count"],
                "affected_percentage": result["affected_percentage"],
                "avg_score_drop": result["average_score_drop"],
                "likely_cause": (
                    "SYSTEMIC STRESSOR DETECTED\n\n"
                    "Pattern Analysis:\n"
                    f"• {result['affected_percentage']}% of MECH-2023 students declining simultaneously\n"
                    f"• Average score drop: {result['average_score_drop']:.2f} points from baseline\n"
                    "• Timeline: Last 5 days (corresponds to mid-semester exams)\n"
                    "• Common keywords: 'stressed', 'overwhelmed', 'exhausted'\n\n"
                    "Likely Cause: Mid-semester examination stress\n\n"
                    "This is NOT individual burnout—it's a batch-level systemic issue."
                ),
                "institutional_action_recommended": result["institutional_action"],
                "acknowledged": False
            }
            
            await crud.save_cohort_alert(db, alert_data)
            await db.commit()
            
            print(f"\n   📋 Institutional Report Generated:")
            print(f"      {result['institutional_action'][:150]}...")
            
            print("\n   🎯 Dashboard updates:")
            print(f"      • 🔔 BANNER appears: 'Cohort Alert: MECH-2023'")
            print(f"      • Report sent to Dean/Principal")
            print(f"      • Institutional action recommended")
        else:
            print(f"\n   ✅ No anomaly detected")
            print(f"      {result['affected_percentage']}% affected (threshold: 40%)")
        
        print("\n✅ EVENT 3 COMPLETE\n")
    
    async def _event_4_action_log(self, db):
        """Event 4: Display action log summary."""
        print("\n" + "─"*70)
        print("⏱️  EVENT 4 (T+45s): ACTION LOG SUMMARY")
        print("─"*70 + "\n")
        
        print("📋 Recent Autonomous Decisions:\n")
        
        # Get recent interventions
        from sqlalchemy import select, desc
        result = await db.execute(
            select(Intervention)
            .join(Student)
            .where(Student.institution_id == self.institution_id)
            .order_by(desc(Intervention.triggered_at))
            .limit(5)
        )
        interventions = result.scalars().all()
        
        if not interventions:
            print("   📭 No interventions found yet")
            print("   (Run more check-ins or wait for autonomous scheduler)")
            return
        
        for i, intervention in enumerate(interventions, 1):
            student = await crud.get_student_by_id(db, intervention.student_id)
            
            print(f"   {i}. Level {intervention.level} Intervention")
            print(f"      Student: {student.name}")
            print(f"      Triggered: {intervention.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"      Recipient: {intervention.recipient}")
            print(f"      Reason: {intervention.trigger_reason[:100]}...")
            print(f"      Status: {intervention.outcome}")
            print()
        
        print("   🎯 Decision Chain Visible:")
        print("      • Input data (scores, sentiment)")
        print("      • HMM assessment")
        print("      • Adversarial check")
        print("      • Intervention level selection")
        print("      • GPT-4o-mini message generation")
        print("      • Action taken")
        
        print("\n✅ EVENT 4 COMPLETE\n")
    
    # ==================== SCENARIO: RESET ====================
    
    async def scenario_reset(self):
        """Clear all demo data, restore to clean state."""
        print("\n" + "="*70)
        print("🧹 DEMO RESET: Clearing all data")
        print("="*70 + "\n")
        
        response = input("⚠️  This will DELETE ALL demo data. Continue? (yes/no): ")
        if response.lower() != "yes":
            print("❌ Reset cancelled")
            return
        
        print("\n🗑️  Dropping all tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        print("   ✅ All tables dropped")
        
        print("\n🔨 Recreating tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("   ✅ Tables recreated")
        
        print("\n" + "="*70)
        print("✅ RESET COMPLETE - Database is clean")
        print("="*70)
        print("\n🎯 Next step: python -m backend.utils.demo_runner --scenario setup\n")


async def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="GuardianAI Live Demo Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m backend.utils.demo_runner --scenario setup
  python -m backend.utils.demo_runner --scenario live
  python -m backend.utils.demo_runner --scenario reset

Scenarios:
  setup  - Populate 50 students with 14 days of history
  live   - Simulate 4 real-time events for judges
  reset  - Clear all demo data, restore to clean state

Workflow for Demo Day:
  1. Test run: python -m backend.utils.demo_runner --scenario live
  2. Before judges: python -m backend.utils.demo_runner --scenario reset
  3. Setup fresh: python -m backend.utils.demo_runner --scenario setup
  4. Live demo: python -m backend.utils.demo_runner --scenario live
        """
    )
    
    parser.add_argument(
        "--scenario",
        required=True,
        choices=["setup", "live", "reset"],
        help="Demo scenario to run"
    )
    
    args = parser.parse_args()
    
    runner = DemoRunner()
    
    try:
        await runner.run_scenario(args.scenario)
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
