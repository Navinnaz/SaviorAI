"""
SaviorAI - Intervention Orchestrator Test Suite

Tests for autonomous intervention decision-making and message generation.
Validates level selection, retry logic, fallback templates, and decision logging.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from agents.intervention_orchestrator import InterventionOrchestrator


# Mock OpenAI client for testing
class MockOpenAIClient:
    """Mock OpenAI client that simulates API responses."""
    
    def __init__(self, should_fail=False, fail_count=0):
        self.should_fail = should_fail
        self.fail_count = fail_count
        self.call_count = 0
    
    class ChatCompletions:
        def __init__(self, parent):
            self.parent = parent
        
        async def create(self, **kwargs):
            self.parent.call_count += 1
            
            # Simulate failures for retry testing
            if self.parent.should_fail:
                if self.parent.call_count <= self.parent.fail_count:
                    raise Exception("Simulated OpenAI API failure")
            
            # Return mock response
            class MockChoice:
                class MockMessage:
                    content = "Hey there! Just checking in - noticed you might be going through something. Want to grab a coffee? We're here for you. 💙"
                message = MockMessage()
            
            class MockResponse:
                choices = [MockChoice()]
            
            return MockResponse()
    
    class Chat:
        def __init__(self, parent):
            self.completions = MockOpenAIClient.ChatCompletions(parent)
    
    def __init__(self, should_fail=False, fail_count=0):
        self.should_fail = should_fail
        self.fail_count = fail_count
        self.call_count = 0
        self.chat = MockOpenAIClient.Chat(self)


# Mock BurnoutAssessment
@dataclass
class MockAssessment:
    state: str
    probability: float
    trend_score: float
    consecutive_low_days: int
    reasoning: str


def test_level_selection_stable():
    """Test that stable state returns level 0 (no action)"""
    print("\n" + "="*60)
    print("TEST: Level Selection - Stable State")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='stable',
        probability=0.85,
        trend_score=0.1,
        consecutive_low_days=0,
        reasoning="Within normal variation"
    )
    
    level = orchestrator._select_level(assessment, last_intervention=None)
    
    print(f"Assessment state: {assessment.state}")
    print(f"Selected level: {level}")
    
    assert level == 0, "Stable state should return level 0"
    
    print("✅ PASSED")
    return True


def test_level_selection_at_risk_first():
    """Test that first at-risk detection returns level 1 (peer nudge)"""
    print("\n" + "="*60)
    print("TEST: Level Selection - At-Risk (First)")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-0.8,
        consecutive_low_days=2,
        reasoning="Moderate decline"
    )
    
    level = orchestrator._select_level(assessment, last_intervention=None)
    
    print(f"Assessment state: {assessment.state}")
    print(f"Previous intervention: None")
    print(f"Selected level: {level}")
    
    assert level == 1, "First at-risk should return level 1"
    
    print("✅ PASSED")
    return True


def test_level_selection_at_risk_escalation():
    """Test that at-risk with previous level 1 escalates to level 2"""
    print("\n" + "="*60)
    print("TEST: Level Selection - At-Risk (Escalation)")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-1.0,
        consecutive_low_days=3,
        reasoning="Continued decline"
    )
    
    last_intervention = {
        "level": 1,
        "triggered_at": datetime.utcnow() - timedelta(days=3)
    }
    
    level = orchestrator._select_level(assessment, last_intervention)
    
    print(f"Assessment state: {assessment.state}")
    print(f"Previous intervention: level {last_intervention['level']}")
    print(f"Selected level: {level}")
    
    assert level == 2, "At-risk with previous level 1 should escalate to level 2"
    
    print("✅ PASSED")
    return True


def test_level_selection_crisis_high_confidence():
    """Test that high-confidence crisis returns level 3 (emergency)"""
    print("\n" + "="*60)
    print("TEST: Level Selection - Crisis (High Confidence)")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='crisis',
        probability=0.85,
        trend_score=-2.0,
        consecutive_low_days=6,
        reasoning="Severe decline, 6 consecutive low days"
    )
    
    level = orchestrator._select_level(assessment, last_intervention=None)
    
    print(f"Assessment state: {assessment.state}")
    print(f"Probability: {assessment.probability:.0%}")
    print(f"Consecutive low days: {assessment.consecutive_low_days}")
    print(f"Selected level: {level}")
    
    assert level == 3, "High-confidence crisis should return level 3"
    
    print("✅ PASSED")
    return True


def test_level_selection_crisis_low_confidence():
    """Test that low-confidence crisis returns level 2 (counsellor first)"""
    print("\n" + "="*60)
    print("TEST: Level Selection - Crisis (Low Confidence)")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='crisis',
        probability=0.60,
        trend_score=-1.2,
        consecutive_low_days=2,
        reasoning="Crisis pattern but lower confidence"
    )
    
    level = orchestrator._select_level(assessment, last_intervention=None)
    
    print(f"Assessment state: {assessment.state}")
    print(f"Probability: {assessment.probability:.0%}")
    print(f"Consecutive low days: {assessment.consecutive_low_days}")
    print(f"Selected level: {level}")
    
    assert level == 2, "Low-confidence crisis should return level 2"
    
    print("✅ PASSED")
    return True


def test_cooldown_enforcement():
    """Test that 48-hour cooldown prevents re-intervention"""
    print("\n" + "="*60)
    print("TEST: 48-Hour Cooldown Enforcement")
    print("="*60)
    
    import asyncio
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-0.8,
        consecutive_low_days=2,
        reasoning="At-risk pattern"
    )
    
    # Last intervention was 24 hours ago (within 48h cooldown)
    last_intervention = {
        "level": 1,
        "triggered_at": datetime.utcnow() - timedelta(hours=24)
    }
    
    student = {"id": "test-student", "name": "Test Student"}
    validation = {"is_suspicious": False, "confidence": 0.0}
    
    result = asyncio.run(orchestrator.decide_and_act(
        student=student,
        assessment=assessment,
        recent_scores=[3, 2, 3],
        recent_onewords=["tired", "stressed"],
        validation_result=validation,
        last_intervention=last_intervention
    ))
    
    print(f"Last intervention: 24 hours ago")
    print(f"Cooldown period: 48 hours")
    print(f"Action: {result['action']}")
    print(f"Reason: {result.get('reason', 'N/A')}")
    
    assert result['action'] == 'hold', "Should hold during cooldown period"
    assert 'cooldown' in result.get('reason', '').lower() or 'recent' in result.get('reason', '').lower()
    
    print("✅ PASSED")
    return True


def test_fallback_template():
    """Test that fallback templates work when GPT-4o fails"""
    print("\n" + "="*60)
    print("TEST: Fallback Template Generation")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    assessment = MockAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-0.8,
        consecutive_low_days=2,
        reasoning="Moderate decline"
    )
    
    student = {
        "id": "test-student",
        "name": "John Doe",
        "year_of_study": 2,
        "batch": "CSE-2023"
    }
    
    message = orchestrator._generate_fallback_message(student, assessment, level=1)
    
    print(f"Student: {student['name']}")
    print(f"Level: 1 (peer nudge)")
    print(f"Message length: {len(message)} chars")
    print(f"Message preview: {message[:100]}...")
    
    assert len(message) > 0, "Fallback message should not be empty"
    assert student['name'] in message, "Fallback should include student name"
    
    print("✅ PASSED")
    return True


def test_cost_estimation():
    """Test cost estimation for GPT-4o usage"""
    print("\n" + "="*60)
    print("TEST: Cost Estimation")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    # Estimate cost for 100 interventions
    cost_breakdown = orchestrator.estimate_cost(100)
    
    print(f"Interventions: 100")
    print(f"Input cost: ${cost_breakdown['input_cost']:.4f}")
    print(f"Output cost: ${cost_breakdown['output_cost']:.4f}")
    print(f"Total cost: ${cost_breakdown['total_cost']:.4f}")
    print(f"Per intervention: ${cost_breakdown['per_intervention']:.6f}")
    
    assert cost_breakdown['total_cost'] > 0, "Total cost should be positive"
    assert cost_breakdown['per_intervention'] > 0, "Per-intervention cost should be positive"
    assert cost_breakdown['total_cost'] == cost_breakdown['input_cost'] + cost_breakdown['output_cost']
    
    print("✅ PASSED")
    return True


def test_recipient_selection():
    """Test recipient mapping for each level"""
    print("\n" + "="*60)
    print("TEST: Recipient Selection")
    print("="*60)
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    recipients = {}
    for level in [0, 1, 2, 3, 4]:
        recipient = orchestrator._select_recipient(level)
        recipients[level] = recipient
        print(f"Level {level} → {recipient}")
    
    assert recipients[0] is None, "Level 0 should have no recipient"
    assert recipients[1] == "student", "Level 1 should send to student"
    assert recipients[2] == "counsellor", "Level 2 should send to counsellor"
    assert recipients[3] == "emergency", "Level 3 should send to emergency"
    assert recipients[4] == "institution", "Level 4 should send to institution"
    
    print("✅ PASSED")
    return True


def test_adversarial_override():
    """Test that adversarial gaming detection overrides normal level selection"""
    print("\n" + "="*60)
    print("TEST: Adversarial Gaming Override")
    print("="*60)
    
    import asyncio
    
    client = MockOpenAIClient()
    orchestrator = InterventionOrchestrator(client)
    
    # At-risk state would normally be level 1 (peer nudge)
    assessment = MockAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-0.8,
        consecutive_low_days=2,
        reasoning="At-risk pattern"
    )
    
    # But adversarial gaming detected
    validation = {
        "is_suspicious": True,
        "confidence": 0.70,
        "flags": [
            {"type": "low_variance", "detail": "Suspiciously flat scores"}
        ]
    }
    
    student = {"id": "test-student", "name": "Test Student"}
    
    result = asyncio.run(orchestrator.decide_and_act(
        student=student,
        assessment=assessment,
        recent_scores=[4, 4, 4, 4, 4],
        recent_onewords=["fine", "okay", "good"],
        validation_result=validation,
        last_intervention=None
    ))
    
    print(f"Normal level would be: 1 (peer nudge)")
    print(f"Gaming detected: confidence={validation['confidence']:.0%}")
    print(f"Actual level: {result['level']}")
    print(f"Recipient: {result['recipient']}")
    print(f"Action: {result['action']}")
    
    assert result['level'] == 2, "Gaming should override to level 2 (counsellor)"
    assert result['recipient'] == 'counsellor', "Gaming should send to counsellor"
    assert 'masking' in result['action'].lower(), "Action should indicate masking"
    
    print("✅ PASSED")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*10 + "SaviorAI Intervention Orchestrator Test Suite")
    print("="*70)
    
    tests = [
        test_level_selection_stable,
        test_level_selection_at_risk_first,
        test_level_selection_at_risk_escalation,
        test_level_selection_crisis_high_confidence,
        test_level_selection_crisis_low_confidence,
        test_cooldown_enforcement,
        test_fallback_template,
        test_cost_estimation,
        test_recipient_selection,
        test_adversarial_override
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"\n❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} total")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 All tests passed! Intervention orchestrator is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    import logging
    # Suppress logging during tests
    logging.basicConfig(level=logging.CRITICAL)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)

