"""
GuardianAI Demo Data Runner

Populates database with realistic demo data for presentations.
Idempotent: safe to run multiple times (clears and recreates).

Usage:
    python -m backend.utils.demo_runner
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import delete
from backend.database.connection import AsyncSessionLocal
from backend.database.models import (
    Institution, Student, CheckIn, BurnoutState, 
    Intervention, CohortAlert
)
from backend.utils.data_generator import generate_demo_data


async def clear_existing_data(db):
    """
    Clear all existing demo data.
    Deletes in correct order to respect foreign key constraints.
    """
    print("\n🗑️  Clearing existing demo data...")
    
    # Delete in reverse dependency order
    await db.execute(delete(Intervention))
    print("  ✓ Cleared interventions")
    
    await db.execute(delete(BurnoutState))
    print("  ✓ Cleared burnout states")
    
    await db.execute(delete(CheckIn))
    print("  ✓ Cleared check-ins")
    
    await db.execute(delete(CohortAlert))
    print("  ✓ Cleared cohort alerts")
    
    await db.execute(delete(Student))
    print("  ✓ Cleared students")
    
    await db.execute(delete(Institution).where(Institution.name == "IIT Delhi"))
    print("  ✓ Cleared institutions")
    
    await db.commit()
    print("✅ Database cleared\n")


async def populate_database(num_students: int = 50):
    """
    Populate database with demo data.
    
    Args:
        num_students: Total number of students to generate
    """
    print("\n" + "="*60)
    print("GuardianAI Demo Data Population")
    print("="*60 + "\n")
    
    # Generate demo data
    print("📊 Generating demo data...")
    demo_data = generate_demo_data(num_students)
    print()
    
    # Insert into database
    async with AsyncSessionLocal() as db:
        try:
            # Clear existing data first
            await clear_existing_data(db)
            
            print("💾 Inserting data into database...\n")
            
            # 1. Insert institution
            institution = Institution(**demo_data["institution"])
            db.add(institution)
            await db.flush()
            print(f"✅ Created institution: {institution.name}")
            
            # 2. Insert students
            student_count = 0
            for student_data in demo_data["students"]:
                student = Student(**student_data)
                db.add(student)
                student_count += 1
            await db.flush()
            print(f"✅ Created {student_count} students")
            
            # 3. Insert check-ins (in batches for performance)
            checkin_count = 0
            batch_size = 100
            for i in range(0, len(demo_data["checkins"]), batch_size):
                batch = demo_data["checkins"][i:i+batch_size]
                for checkin_data in batch:
                    checkin = CheckIn(**checkin_data)
                    db.add(checkin)
                checkin_count += len(batch)
            await db.flush()
            print(f"✅ Created {checkin_count} check-ins")
            
            # 4. Insert burnout states
            state_count = 0
            for state_data in demo_data["burnout_states"]:
                state = BurnoutState(**state_data)
                db.add(state)
                state_count += 1
            await db.flush()
            print(f"✅ Created {state_count} burnout states")
            
            # 5. Insert interventions
            intervention_count = 0
            for intervention_data in demo_data["interventions"]:
                intervention = Intervention(**intervention_data)
                db.add(intervention)
                intervention_count += 1
            await db.flush()
            print(f"✅ Created {intervention_count} interventions")
            
            # 6. Insert cohort alerts
            if demo_data.get("cohort_alerts"):
                alert_count = 0
                for alert_data in demo_data["cohort_alerts"]:
                    alert = CohortAlert(**alert_data)
                    db.add(alert)
                    alert_count += 1
                await db.flush()
                print(f"✅ Created {alert_count} cohort alerts")
            
            # Commit all changes
            await db.commit()
            
            print("\n" + "="*60)
            print("✅ Demo Data Population Complete!")
            print("="*60 + "\n")
            
            # Print summary
            print("📊 Data Summary:")
            print(f"  • Institution: {institution.name}")
            print(f"  • Students: {student_count}")
            print(f"  • Check-ins: {checkin_count}")
            print(f"  • Burnout States: {state_count}")
            print(f"  • Interventions: {intervention_count}")
            print()
            
            print("🎭 Demo Personas:")
            print("  • Priya Sharma (CSE-2022) - Crisis student [FLAGSHIP]")
            print("  • 3 gaming students - Adversarial detection demo")
            print("  • 12 MECH-2023 students - Cohort anomaly demo")
            print(f"  • {num_students - 16} normal students - Realistic variance")
            print()
            
            print("🚀 Next Steps:")
            print("  1. Start FastAPI server: python backend/main.py")
            print("  2. Open dashboard: http://localhost:8000/api/dashboard/health")
            print(f"  3. View overview: GET /api/dashboard/{institution.id}/overview")
            print()
            
        except Exception as e:
            await db.rollback()
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            raise


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Populate GuardianAI database with demo data")
    parser.add_argument(
        "--students",
        type=int,
        default=50,
        help="Total number of students to generate (default: 50)"
    )
    parser.add_argument(
        "--skip-clear",
        action="store_true",
        help="Skip clearing existing data (append mode)"
    )
    
    args = parser.parse_args()
    
    if args.skip_clear:
        print("⚠️  Running in append mode (existing data will NOT be cleared)")
    
    await populate_database(num_students=args.students)


if __name__ == "__main__":
    asyncio.run(main())
