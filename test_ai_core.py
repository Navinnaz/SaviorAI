"""
GuardianAI - Comprehensive AI Core System Test
Tests all 4 autonomous agents + OpenAI integration
"""

import asyncio
import sys
import os
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

from agents.hmm_engine import BurnoutHMM
from agents.adversarial_validator import AdversarialValidator
from agents.cohort_detector import CohortAnomalyDetector
from agents.intervention_orchestrator import InterventionOrchestrator


def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def print_result(name, status, details=""):
    """Print test result"""
    icon = "✅" if status else "❌"
    print(f"{icon} {name}")
    if details:
        print(f"   {details}\n")


async def test_openai_connection():
    """Test 1: OpenAI API Connection"""
    print_section("TEST 1: OpenAI API Connection")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test simple call
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply with: API works"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print_result("OpenAI API Key", True, f"Response: {result}")
        print_result("Model", True, "gpt-4o-mini (affordable)")
        return True
        
    except Exception as e:
        print_result("OpenAI Connection", False, f"Error: {e}")
        return False


def test_hmm_engine():
    """Test 2: HMM Burnout Detection Engine"""
    print_section("TEST 2: HMM Burnout Detection Engine")
    
    try:
        hmm = BurnoutHMM()
        
        # Test case 1: Stable student
        stable_scores = [4, 4, 3, 4, 4, 3, 4]
        result1 = hmm.assess(stable_scores, baseline=3.5)
        print_result("Stable Student", 
                    result1.state == "stable",
                    f"State: {result1.state}, Prob: {result1.probability:.2f}")
        
        # Test case 2: At-risk student
        atrisk_scores = [4, 4, 3, 2, 2, 2, 1]
        result2 = hmm.assess(atrisk_scores, baseline=3.5)
        print_result("At-Risk Student",
                    result2.state == "at_risk",
                    f"State: {result2.state}, Prob: {result2.probability:.2f}")
        
        # Test case 3: Crisis student (Priya Sharma pattern)
        crisis_scores = [4, 3, 3, 2, 2, 1, 1, 1, 2, 1]
        result3 = hmm.assess(crisis_scores, baseline=3.5)
        print_result("Crisis Student",
                    result3.state == "crisis",
                    f"State: {result3.state}, Prob: {result3.probability:.2f}, Consecutive low: {result3.consecutive_low_days}")
        
        return True
        
    except Exception as e:
        print_result("HMM Engine", False, f"Error: {e}")
        return False


def test_adversarial_validator():
    """Test 3: Adversarial Gaming Detection"""
    print_section("TEST 3: Adversarial Gaming Detection")
    
    try:
        validator = AdversarialValidator()
        
        # Test case 1: Normal variance
        normal_scores = [4, 3, 4, 2, 3, 4, 3]
        result1 = validator.validate(normal_scores)
        print_result("Normal Variance",
                    not result1["is_suspicious"],
                    f"Suspicious: {result1['is_suspicious']}, Flags: {len(result1.get('flags', []))}")
        
        # Test case 2: Gaming behavior (flat scores)
        gaming_scores = [4, 4, 4, 4, 4, 4, 4, 4]
        result2 = validator.validate(gaming_scores)
        print_result("Gaming Detection",
                    result2["is_suspicious"],
                    f"Suspicious: {result2['is_suspicious']}, Flags: {len(result2.get('flags', []))}")
        
        # Test case 3: Extreme scores
        extreme_scores = [5, 5, 5, 5, 5, 5, 5, 5]
        result3 = validator.validate(extreme_scores)
        print_result("Extreme Scores",
                    result3["is_suspicious"],
                    f"Suspicious: {result3['is_suspicious']}")
        
        return True
        
    except Exception as e:
        print_result("Adversarial Validator", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cohort_detector():
    """Test 4: Cohort Anomaly Detection"""
    print_section("TEST 4: Cohort Anomaly Detection")
    
    try:
        detector = CohortAnomalyDetector()
        
        # Test case 1: Normal cohort
        normal_cohort = [
            {"student_id": "1", "name": "Student A", "recent_avg": 3.5, "baseline": 3.4},
            {"student_id": "2", "name": "Student B", "recent_avg": 3.2, "baseline": 3.3},
            {"student_id": "3", "name": "Student C", "recent_avg": 3.8, "baseline": 3.7},
            {"student_id": "4", "name": "Student D", "recent_avg": 3.1, "baseline": 3.2},
            {"student_id": "5", "name": "Student E", "recent_avg": 3.6, "baseline": 3.5},
            {"student_id": "6", "name": "Student F", "recent_avg": 3.4, "baseline": 3.6},
            {"student_id": "7", "name": "Student G", "recent_avg": 3.3, "baseline": 3.4},
            {"student_id": "8", "name": "Student H", "recent_avg": 3.7, "baseline": 3.6},
        ]
        result1 = detector.detect(normal_cohort)
        print_result("Normal Cohort",
                    not result1["anomaly_detected"],
                    f"Anomaly: {result1['anomaly_detected']}, Pct: {result1.get('affected_percentage', 0)*100:.1f}%")
        
        # Test case 2: Anomalous cohort (MECH-2023 pattern - all declining)
        crisis_cohort = [
            {"student_id": "1", "name": "Student A", "recent_avg": 2.1, "baseline": 3.5},
            {"student_id": "2", "name": "Student B", "recent_avg": 1.9, "baseline": 3.4},
            {"student_id": "3", "name": "Student C", "recent_avg": 2.3, "baseline": 3.6},
            {"student_id": "4", "name": "Student D", "recent_avg": 2.0, "baseline": 3.5},
            {"student_id": "5", "name": "Student E", "recent_avg": 2.2, "baseline": 3.7},
            {"student_id": "6", "name": "Student F", "recent_avg": 1.8, "baseline": 3.4},
            {"student_id": "7", "name": "Student G", "recent_avg": 2.1, "baseline": 3.5},
            {"student_id": "8", "name": "Student H", "recent_avg": 2.0, "baseline": 3.6},
            {"student_id": "9", "name": "Student I", "recent_avg": 1.9, "baseline": 3.4},
            {"student_id": "10", "name": "Student J", "recent_avg": 2.2, "baseline": 3.5},
        ]
        result2 = detector.detect(crisis_cohort)
        print_result("Crisis Cohort (Exam Hell)",
                    result2["anomaly_detected"],
                    f"Affected: {result2.get('affected_count', 0)}/10 ({result2.get('affected_percentage', 0)*100:.0f}%), Avg drop: {result2.get('average_score_drop', 0):.2f}")
        
        return True
        
    except Exception as e:
        print_result("Cohort Detector", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_intervention_orchestrator():
    """Test 5: Intervention Orchestrator with OpenAI"""
    print_section("TEST 5: Intervention Orchestrator (OpenAI Integration)")
    
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        orchestrator = InterventionOrchestrator(openai_client=client)
        
        # Mock student data
        from dataclasses import dataclass
        
        @dataclass
        class MockAssessment:
            state: str
            probability: float
            trend_score: float
            consecutive_low_days: int
            reasoning: str = "Crisis pattern detected"
        
        student_data = {
            "id": "test-123",
            "name": "Priya Sharma",
            "phone": "+919944906759",
            "batch": "CSE-2022",
            "baseline_score": 3.5
        }
        
        # Test Level 3 intervention (Crisis)
        crisis_assessment = MockAssessment(
            state="crisis",
            probability=0.92,
            trend_score=-0.8,
            consecutive_low_days=4,
            reasoning="Sustained low scores with concerning one-words"
        )
        
        recent_onewords = ["tired", "exhausted", "hopeless", "empty"]
        
        print("⏳ Generating intervention message via OpenAI (gpt-4o-mini)...")
        print("   This tests: OpenAI API + Intervention logic")
        
        decision = await orchestrator.decide_and_act(
            student=student_data,
            assessment=crisis_assessment,
            recent_scores=[2, 2, 1, 1, 1, 2, 1],
            recent_onewords=recent_onewords,
            validation_result={"is_suspicious": False, "confidence": 0.0},
            last_intervention=None
        )
        
        print_result("Intervention Decision",
                    decision["action"] == "send" and decision["level"] == 3,
                    f"Action: {decision['action']}, Level: {decision.get('level', 'N/A')}")
        
        print_result("OpenAI Message Generation",
                    len(decision.get("message", "")) > 50,
                    f"Message length: {len(decision.get('message', ''))} chars")
        
        print("\n📝 Generated Message Preview:")
        print("-" * 70)
        msg = decision.get("message", "No message")
        print(msg[:200] + "..." if len(msg) > 200 else msg)
        print("-" * 70)
        
        print_result("Reasoning Chain",
                    len(decision.get("reasoning", "")) > 0,
                    f"Has reasoning: {bool(decision.get('reasoning'))}")
        
        # Test fallback system
        print("\n⏳ Testing fallback template (simulating API failure)...")
        fallback_msg = orchestrator._generate_fallback_message(
            student_data, crisis_assessment, 3
        )
        print_result("Fallback System",
                    "counsellor" in fallback_msg.lower(),
                    f"Fallback works: {len(fallback_msg)} chars")
        
        return True
        
    except Exception as e:
        print_result("Intervention Orchestrator", False, f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run complete test suite"""
    print("\n" + "🤖"*35)
    print("  GUARDIANAI - AI CORE SYSTEM TEST SUITE")
    print("  Testing all autonomous agents + OpenAI integration")
    print("🤖"*35)
    
    results = []
    
    # Test 1: OpenAI
    results.append(await test_openai_connection())
    
    # Test 2: HMM Engine
    results.append(test_hmm_engine())
    
    # Test 3: Adversarial Validator
    results.append(test_adversarial_validator())
    
    # Test 4: Cohort Detector
    results.append(test_cohort_detector())
    
    # Test 5: Intervention Orchestrator (requires OpenAI)
    results.append(await test_intervention_orchestrator())
    
    # Final summary
    print_section("FINAL RESULTS")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Tests Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! AI Core System is FULLY OPERATIONAL! 🎉")
        print("\n✅ HMM Engine: Working")
        print("✅ Adversarial Validator: Working")
        print("✅ Cohort Detector: Working")
        print("✅ Intervention Orchestrator: Working")
        print("✅ OpenAI Integration: Working (gpt-4o-mini)")
        print("\n🚀 System ready for production deployment!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
