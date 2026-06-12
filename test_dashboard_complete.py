"""
Complete Dashboard API test with sample data creation.
"""
import asyncio
import requests
from datetime import datetime, timedelta
from uuid import uuid4

from backend.database.connection import AsyncSessionLocal
from backend.database.models import Institution, Student, CheckIn, BurnoutState, Intervention

BASE_URL = "http://localhost:8000/api/dashboard"
API_KEY = "guardianai_dev_key_2024"
HEADERS = {"X-API-Key": API_KEY}


async def create_test_data():
    """Create sample institution, students, and data for testing."""
    print("\n" + "="*60)
    print("Creating Test Data")
    print("="*60 + "\n")
    
    async with AsyncSessionLocal() as db:
        # Create institution
        institution = Institution(
            id=uuid4(),
            name="Test University",
            type="college",
            city="Mumbai",
            state="Maharashtra",
            counsellor_phone="+919876543210",
            counsellor_email="counsellor@test.edu"
        )
        db.add(institution)
        await db.flush()
        print(f"✅ Created institution: {institution.name} (ID: {institution.id})")
        
        # Create 3 students
        students = []
        for i in range(3):
            student = Student(
                id=uuid4(),
                name=f"Test Student {i+1}",
                phone=f"+9199999{i+10000}",
                email=f"student{i+1}@test.edu",
                institution_id=institution.id,
                batch="CSE-2024",
                year_of_study=2,
                is_active=True,
                baseline_score=3.0
            )
            db.add(student)
            students.append(student)
        
        await db.flush()
        print(f"✅ Created {len(students)} students")
        
        # Create check-ins for each student (last 7 days)
        for student in students:
            for day in range(7):
                checkin = CheckIn(
                    id=uuid4(),
                    student_id=student.id,
                    checked_in_at=datetime.utcnow() - timedelta(days=day),
                    mood_score=3 - day // 3,  # Declining scores
                    ate_properly="yes" if day < 3 else "mostly",
                    one_word=["happy", "tired", "stressed", "overwhelmed", "exhausted", "hopeless", "lost"][day],
                    sentiment="negative" if day > 3 else "neutral",
                    sentiment_score=-0.3 * day,
                    skipped=False
                )
                db.add(checkin)
        
        await db.flush()
        print(f"✅ Created check-ins for last 7 days")
        
        # Create burnout states
        for i, student in enumerate(students):
            state = BurnoutState(
                id=uuid4(),
                student_id=student.id,
                assessed_at=datetime.utcnow(),
                state=["stable", "at_risk", "crisis"][i],
                hmm_probability=[0.2, 0.6, 0.9][i],
                trend_score=[0.5, -0.5, -1.0][i],
                consecutive_low_days=[0, 2, 5][i],
                variance_flag=False,
                cohort_flag=False
            )
            db.add(state)
        
        await db.flush()
        print(f"✅ Created burnout states (stable, at_risk, crisis)")
        
        # Create intervention
        intervention = Intervention(
            id=uuid4(),
            student_id=students[2].id,  # Crisis student
            triggered_at=datetime.utcnow(),
            level=2,
            trigger_reason="Student in crisis state, HMM probability: 0.9",
            action_taken="send",
            message_sent="Dear Counsellor, Test Student 3 needs immediate attention.",
            recipient="counsellor",
            was_acknowledged=False,
            outcome="pending"
        )
        db.add(intervention)
        
        await db.flush()
        await db.commit()
        print(f"✅ Created intervention")
        
        print(f"\n{'='*60}")
        print(f"Test Data Summary:")
        print(f"  Institution ID: {institution.id}")
        print(f"  Student IDs: {[str(s.id) for s in students]}")
        print(f"{'='*60}\n")
        
        return institution.id, students[0].id


def test_health():
    """Test health endpoint (no auth)."""
    print("\n🧪 Testing: GET /health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print(f"   ✅ Health check passed")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_overview(institution_id):
    """Test institution overview."""
    print(f"\n🧪 Testing: GET /{institution_id}/overview")
    response = requests.get(
        f"{BASE_URL}/{institution_id}/overview",
        headers=HEADERS
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Total students: {data['total_students']}")
        print(f"   ✅ Stable: {data['stable_count']}, At-risk: {data['at_risk_count']}, Crisis: {data['crisis_count']}")
        print(f"   ✅ Check-in rate (7d): {data['check_in_rate_7d']}%")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_heatmap(institution_id):
    """Test heatmap endpoint."""
    print(f"\n🧪 Testing: GET /{institution_id}/heatmap")
    response = requests.get(
        f"{BASE_URL}/{institution_id}/heatmap",
        headers=HEADERS
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Students in heatmap: {len(data)}")
        if data:
            print(f"   ✅ Sample: {data[0]['name']} - {data[0]['state']} (risk: {data[0]['risk_score']})")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_student_profile(student_id):
    """Test student profile endpoint."""
    print(f"\n🧪 Testing: GET /student/{student_id}/profile")
    response = requests.get(
        f"{BASE_URL}/student/{student_id}/profile",
        headers=HEADERS
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Student: {data['basic_info']['name']}")
        print(f"   ✅ Check-ins (14d): {len(data['checkins_14d'])}")
        print(f"   ✅ State history: {len(data['state_history'])}")
        print(f"   ✅ Interventions: {len(data['interventions'])}")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_cohorts(institution_id):
    """Test cohorts endpoint."""
    print(f"\n🧪 Testing: GET /{institution_id}/cohorts")
    response = requests.get(
        f"{BASE_URL}/{institution_id}/cohorts",
        headers=HEADERS
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Batches found: {len(data)}")
        if data:
            print(f"   ✅ Sample: {data[0]['batch']} - {data[0]['total_students']} students")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_interventions():
    """Test recent interventions endpoint."""
    print(f"\n🧪 Testing: GET /interventions/recent")
    response = requests.get(
        f"{BASE_URL}/interventions/recent?limit=5",
        headers=HEADERS
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Interventions found: {len(data)}")
        if data:
            print(f"   ✅ Latest: Level {data[0]['level']} - {data[0]['recipient']}")
    else:
        print(f"   ❌ Failed: {response.text}")


def test_auth_failure(institution_id):
    """Test authentication failure."""
    print(f"\n🧪 Testing: Auth failure (no API key)")
    response = requests.get(f"{BASE_URL}/{institution_id}/overview")
    print(f"   Status: {response.status_code}")
    if response.status_code in [401, 422]:
        print(f"   ✅ Auth correctly rejected")
    else:
        print(f"   ❌ Expected 401/422, got {response.status_code}")


async def cleanup_test_data():
    """Clean up test data after tests."""
    print("\n" + "="*60)
    print("Cleaning Up Test Data")
    print("="*60 + "\n")
    
    async with AsyncSessionLocal() as db:
        # Delete test institution (cascade will delete students, check-ins, etc.)
        from sqlalchemy import delete
        result = await db.execute(
            delete(Institution).where(Institution.name == "Test University")
        )
        await db.commit()
        print(f"✅ Cleaned up test data")


async def main():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("GuardianAI Dashboard API - Complete Test Suite")
    print("="*60)
    
    # Create test data
    institution_id, student_id = await create_test_data()
    
    # Run tests
    print("\n" + "="*60)
    print("Running API Tests")
    print("="*60)
    
    test_health()
    test_overview(institution_id)
    test_heatmap(institution_id)
    test_student_profile(student_id)
    test_cohorts(institution_id)
    test_interventions()
    test_auth_failure(institution_id)
    
    # Cleanup
    await cleanup_test_data()
    
    print("\n" + "="*60)
    print("✅ All Tests Complete!")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
