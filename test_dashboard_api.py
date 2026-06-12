"""
Quick test script for Dashboard API endpoints.
Run after server restart to verify all endpoints work.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/dashboard"
API_KEY = "guardianai_dev_key_2024"
HEADERS = {"X-API-Key": API_KEY}

# You'll need to replace these with actual UUIDs from your database
INSTITUTION_ID = "your-institution-uuid"
STUDENT_ID = "your-student-uuid"


def test_health():
    """Test health check (no auth required)"""
    print("Testing: GET /dashboard/health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_overview():
    """Test institution overview"""
    print(f"Testing: GET /dashboard/{INSTITUTION_ID}/overview")
    response = requests.get(
        f"{BASE_URL}/{INSTITUTION_ID}/overview",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")


def test_heatmap():
    """Test student heatmap"""
    print(f"Testing: GET /dashboard/{INSTITUTION_ID}/heatmap")
    response = requests.get(
        f"{BASE_URL}/{INSTITUTION_ID}/heatmap",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total students: {len(data)}")
        if data:
            print(f"Sample student: {json.dumps(data[0], indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")


def test_student_profile():
    """Test student profile"""
    print(f"Testing: GET /dashboard/student/{STUDENT_ID}/profile")
    response = requests.get(
        f"{BASE_URL}/student/{STUDENT_ID}/profile",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Student: {data['basic_info']['name']}")
        print(f"Check-ins (14d): {len(data['checkins_14d'])}")
        print(f"Interventions: {len(data['interventions'])}\n")
    else:
        print(f"Error: {response.text}\n")


def test_cohorts():
    """Test cohort analytics"""
    print(f"Testing: GET /dashboard/{INSTITUTION_ID}/cohorts")
    response = requests.get(
        f"{BASE_URL}/{INSTITUTION_ID}/cohorts",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total batches: {len(data)}")
        if data:
            print(f"Sample batch: {json.dumps(data[0], indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")


def test_recent_interventions():
    """Test recent interventions"""
    print("Testing: GET /dashboard/interventions/recent?limit=5")
    response = requests.get(
        f"{BASE_URL}/interventions/recent?limit=5",
        headers=HEADERS
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total interventions: {len(data)}")
        if data:
            print(f"Latest intervention: {json.dumps(data[0], indent=2)}\n")
    else:
        print(f"Error: {response.text}\n")


def test_auth_failure():
    """Test authentication failure"""
    print("Testing: Auth failure (no API key)")
    response = requests.get(f"{BASE_URL}/{INSTITUTION_ID}/overview")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


if __name__ == "__main__":
    print("="*60)
    print("GuardianAI Dashboard API Test Suite")
    print("="*60 + "\n")
    
    print("⚠️  Update INSTITUTION_ID and STUDENT_ID with real UUIDs first!\n")
    
    # Test health check (no auth)
    test_health()
    
    # Test auth failure
    test_auth_failure()
    
    # Uncomment these after adding real UUIDs:
    # test_overview()
    # test_heatmap()
    # test_student_profile()
    # test_cohorts()
    # test_recent_interventions()
    
    print("="*60)
    print("Tests complete!")
    print("="*60)
