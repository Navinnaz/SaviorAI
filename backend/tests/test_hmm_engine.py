"""
SaviorAI - HMM Engine Test Suite

Tests for the Hidden Markov Model burnout detection engine.
Validates state detection, trend calculation, and reasoning generation.
"""

import pytest
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from agents.hmm_engine import BurnoutHMM, BurnoutAssessment


class TestBurnoutHMM:
    """Test suite for BurnoutHMM class"""
    
    @pytest.fixture
    def hmm(self):
        """Create HMM instance for testing"""
        return BurnoutHMM()
    
    def test_stable_student(self, hmm):
        """
        Test stable student detection.
        Scores: [4,4,5,3,4,4] - consistently good with normal variation
        Expected: 'stable' state
        """
        scores = [4, 4, 5, 3, 4, 4]
        assessment = hmm.assess(scores, baseline=3.0)
        
        assert assessment.state == 'stable', \
            f"Expected 'stable' but got '{assessment.state}'"
        assert assessment.probability > 0.5, \
            "Stable state should have >50% probability"
        assert assessment.consecutive_low_days == 0, \
            "Stable student should have 0 consecutive low days"
        
        print(f"✓ Stable student test passed")
        print(f"  State: {assessment.state}")
        print(f"  Probability: {assessment.probability:.2%}")
        print(f"  Reasoning: {assessment.reasoning}")
    
    def test_at_risk_student(self, hmm):
        """
        Test at-risk student detection.
        Scores: [4,3,3,2,2,3,2] - declining with multiple low scores
        Expected: 'at_risk' state
        """
        scores = [4, 3, 3, 2, 2, 3, 2]
        assessment = hmm.assess(scores, baseline=3.5)
        
        assert assessment.state == 'at_risk', \
            f"Expected 'at_risk' but got '{assessment.state}'"
        assert assessment.trend_score < 0, \
            "At-risk student should have negative trend"
        
        print(f"✓ At-risk student test passed")
        print(f"  State: {assessment.state}")
        print(f"  Probability: {assessment.probability:.2%}")
        print(f"  Trend: {assessment.trend_score:+.2f}")
        print(f"  Reasoning: {assessment.reasoning}")
    
    def test_crisis_student(self, hmm):
        """
        Test crisis student detection.
        Scores: [4,3,2,2,1,1,2,1] - severe decline with consecutive lows
        Expected: 'crisis' state
        """
        scores = [4, 3, 2, 2, 1, 1, 2, 1]
        assessment = hmm.assess(scores, baseline=3.5)
        
        assert assessment.state == 'crisis', \
            f"Expected 'crisis' but got '{assessment.state}'"
        assert assessment.consecutive_low_days >= 1, \
            "Crisis student should have consecutive low days"
        assert assessment.trend_score < -1.0, \
            "Crisis student should have significant negative trend"
        
        print(f"✓ Crisis student test passed")
        print(f"  State: {assessment.state}")
        print(f"  Probability: {assessment.probability:.2%}")
        print(f"  Trend: {assessment.trend_score:+.2f}")
        print(f"  Consecutive low days: {assessment.consecutive_low_days}")
        print(f"  Reasoning: {assessment.reasoning}")
    
    def test_insufficient_data(self, hmm):
        """
        Test handling of insufficient data.
        Scores: [3,4] - only 2 check-ins
        Expected: 'stable' with explanatory note
        """
        scores = [3, 4]
        assessment = hmm.assess(scores, baseline=3.0)
        
        assert assessment.state == 'stable', \
            "Insufficient data should default to 'stable'"
        assert "Insufficient data" in assessment.reasoning, \
            "Reasoning should mention insufficient data"
        assert assessment.consecutive_low_days == 0
        assert assessment.trend_score == 0.0
        
        print(f"✓ Insufficient data test passed")
        print(f"  Reasoning: {assessment.reasoning}")
    
    def test_trend_calculation(self, hmm):
        """
        Test trend score calculation accuracy.
        Scores: [3,3,3,3,2,2,2] with baseline 3.0
        Recent 5: [3,3,2,2,2] = avg 2.4
        Trend: 2.4 - 3.0 = -0.6
        """
        scores = [3, 3, 3, 3, 2, 2, 2]
        baseline = 3.0
        assessment = hmm.assess(scores, baseline=baseline)
        
        # Recent 5 scores: [3,2,2,2]  wait, last 5 are [3,3,2,2,2]
        recent_5 = scores[-5:]  # [3,2,2,2]
        expected_recent_avg = sum(recent_5) / len(recent_5)  # 2.4
        expected_trend = round(expected_recent_avg - baseline, 2)  # -0.6
        
        assert assessment.trend_score == expected_trend, \
            f"Expected trend {expected_trend}, got {assessment.trend_score}"
        
        print(f"✓ Trend calculation test passed")
        print(f"  Baseline: {baseline}")
        print(f"  Recent 5 scores: {recent_5}")
        print(f"  Recent average: {expected_recent_avg:.2f}")
        print(f"  Calculated trend: {assessment.trend_score}")
    
    def test_consecutive_low_counter(self, hmm):
        """
        Test consecutive low days counting.
        Scores: [5,4,3,2,1,2,1] - last 4 are low (≤2)
        Expected: consecutive_low_days = 2 (1 and 2 at end, stopped by nothing after)
        
        Wait, let's recount: reversed [1, 2, 1, 2, 3, 4, 5]
        - 1 ≤ 2: count = 1
        - 2 ≤ 2: count = 2  
        - 1 ≤ 2: count = 3
        - 2 ≤ 2: count = 4
        - 3 > 2: stop
        Expected: 4 consecutive low days
        """
        scores = [5, 4, 3, 2, 1, 2, 1]
        assessment = hmm.assess(scores, baseline=4.0)
        
        # Count from end: 1, 2, 1, 2 (all ≤ 2) = 4 consecutive
        expected_consec = 4
        
        assert assessment.consecutive_low_days == expected_consec, \
            f"Expected {expected_consec} consecutive low days, got {assessment.consecutive_low_days}"
        
        print(f"✓ Consecutive low counter test passed")
        print(f"  Scores: {scores}")
        print(f"  Consecutive low days: {assessment.consecutive_low_days}")
    
    def test_no_consecutive_lows(self, hmm):
        """Test case with no consecutive low days"""
        scores = [3, 4, 3, 5, 4, 3, 4]
        assessment = hmm.assess(scores, baseline=3.5)
        
        assert assessment.consecutive_low_days == 0, \
            "Should have 0 consecutive low days"
        
        print(f"✓ No consecutive lows test passed")
    
    def test_baseline_sensitivity(self, hmm):
        """
        Test that personal baseline matters.
        Same scores, different baselines should give different trends.
        """
        scores = [3, 3, 3, 3, 3]
        
        # Student with high baseline
        assessment_high = hmm.assess(scores, baseline=4.5)
        
        # Student with low baseline
        assessment_low = hmm.assess(scores, baseline=2.0)
        
        assert assessment_high.trend_score < assessment_low.trend_score, \
            "Higher baseline should result in more negative trend"
        
        print(f"✓ Baseline sensitivity test passed")
        print(f"  Scores: {scores}")
        print(f"  High baseline (4.5) trend: {assessment_high.trend_score}")
        print(f"  Low baseline (2.0) trend: {assessment_low.trend_score}")
    
    def test_batch_assess(self, hmm):
        """Test batch assessment of multiple students"""
        students = [
            {
                'student_id': 'student_1',
                'scores': [4, 4, 5, 3, 4, 4],
                'baseline': 3.0
            },
            {
                'student_id': 'student_2', 
                'scores': [4, 3, 2, 2, 1, 1, 2, 1],
                'baseline': 3.5
            },
            {
                'student_id': 'student_3',
                'scores': [4, 3, 3, 2, 2, 3, 2],
                'baseline': 3.5
            }
        ]
        
        assessments = hmm.batch_assess(students)
        
        assert len(assessments) == 3, "Should return 3 assessments"
        assert assessments[0].state == 'stable', "Student 1 should be stable"
        assert assessments[1].state == 'crisis', "Student 2 should be crisis"
        assert assessments[2].state == 'at_risk', "Student 3 should be at-risk"
        
        print(f"✓ Batch assess test passed")
        for i, assessment in enumerate(assessments, 1):
            print(f"  Student {i}: {assessment.state} ({assessment.probability:.2%})")
    
    def test_score_to_obs_mapping(self, hmm):
        """Test score to observation conversion"""
        assert hmm.score_to_obs(1) == 0, "Score 1 should map to obs 0 (low)"
        assert hmm.score_to_obs(2) == 0, "Score 2 should map to obs 0 (low)"
        assert hmm.score_to_obs(3) == 1, "Score 3 should map to obs 1 (mid)"
        assert hmm.score_to_obs(4) == 2, "Score 4 should map to obs 2 (high)"
        assert hmm.score_to_obs(5) == 2, "Score 5 should map to obs 2 (high)"
        
        print(f"✓ Score to observation mapping test passed")
    
    def test_viterbi_empty_scores(self, hmm):
        """Test Viterbi with empty score list"""
        states, probs = hmm.viterbi([])
        
        assert states == ['stable'], "Empty scores should default to stable"
        assert len(probs) == 1
        
        print(f"✓ Viterbi empty scores test passed")
    
    def test_reasoning_generation(self, hmm):
        """Test that reasoning is generated appropriately"""
        # Test declining student
        declining_scores = [4, 3, 2, 2, 1, 1]
        assessment = hmm.assess(declining_scores, baseline=4.0)
        
        assert len(assessment.reasoning) > 0, "Reasoning should not be empty"
        assert "consecutive" in assessment.reasoning.lower() or \
               "dropped" in assessment.reasoning.lower() or \
               "decline" in assessment.reasoning.lower(), \
               "Reasoning should mention the decline"
        
        print(f"✓ Reasoning generation test passed")
        print(f"  Reasoning: {assessment.reasoning}")


def test_dataclass_structure():
    """Test BurnoutAssessment dataclass structure"""
    assessment = BurnoutAssessment(
        state='at_risk',
        probability=0.65,
        trend_score=-1.2,
        consecutive_low_days=3,
        reasoning="Test reasoning"
    )
    
    assert assessment.state == 'at_risk'
    assert assessment.probability == 0.65
    assert assessment.trend_score == -1.2
    assert assessment.consecutive_low_days == 3
    assert assessment.reasoning == "Test reasoning"
    
    print(f"✓ Dataclass structure test passed")


if __name__ == "__main__":
    """Run tests directly with python"""
    print("=" * 60)
    print("SaviorAI HMM Engine Test Suite")
    print("=" * 60)
    print()
    
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--tb=short"])

