"""
GuardianAI - Adversarial Validator Test Suite

Tests for gaming/masking detection in student check-ins.
Validates that the system can detect suspicious patterns.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from agents.adversarial_validator import AdversarialValidator


def test_flat_scores_flagged():
    """
    Test that perfectly flat scores are flagged.
    Pattern: [4,4,4,4,4,4,4,4] - no variance
    Expected: Flag for low_variance
    """
    print("\n" + "="*60)
    print("TEST: Flat Scores Flagged")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [4, 4, 4, 4, 4, 4, 4, 4]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Flags: {[f['type'] for f in result.get('flags', [])]}")
    
    assert result['is_suspicious'] == True, "Flat scores should be flagged"
    assert any(f['type'] == 'low_variance' for f in result['flags']), \
        "Should have low_variance flag"
    
    print("✅ PASSED")
    return True


def test_normal_scores_clean():
    """
    Test that normal variance scores pass validation.
    Pattern: [4,2,3,5,3,4,2,4,3,5] - healthy variance
    Expected: No flags
    """
    print("\n" + "="*60)
    print("TEST: Normal Scores Clean")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [4, 2, 3, 5, 3, 4, 2, 4, 3, 5]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Flags: {[f['type'] for f in result.get('flags', [])]}")
    
    assert result['is_suspicious'] == False, "Normal scores should not be flagged"
    assert len(result.get('flags', [])) == 0, "Should have no flags"
    
    print("✅ PASSED")
    return True


def test_sudden_recovery():
    """
    Test sudden recovery detection.
    Pattern: [2,2,1,2,1,5] - jump from 1 to 5
    Expected: Flag for sudden_recovery
    """
    print("\n" + "="*60)
    print("TEST: Sudden Recovery Detection")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [2, 2, 1, 2, 1, 5]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Flags: {[f['type'] for f in result.get('flags', [])]}")
    
    # Note: This requires 7+ scores for sudden recovery check
    # With 6 scores, it won't trigger. Let's use extended pattern
    scores_extended = [3, 2, 2, 1, 2, 1, 5]
    result_extended = validator.validate(scores_extended)
    
    print(f"\nExtended scores: {scores_extended}")
    print(f"Is suspicious: {result_extended['is_suspicious']}")
    print(f"Flags: {[f['type'] for f in result_extended.get('flags', [])]}")
    
    assert result_extended['is_suspicious'] == True, \
        "Sudden recovery should be flagged"
    
    print("✅ PASSED")
    return True


def test_ceiling_effect():
    """
    Test ceiling effect detection.
    Pattern: [5,5,5,5,5,5,5,5] - all maximum scores
    Expected: Flag for ceiling_effect
    """
    print("\n" + "="*60)
    print("TEST: Ceiling Effect Detection")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [5, 5, 5, 5, 5, 5, 5, 5]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Flags: {[f['type'] for f in result.get('flags', [])]}")
    
    assert result['is_suspicious'] == True, "Ceiling effect should be flagged"
    assert any(f['type'] == 'ceiling_effect' for f in result['flags']), \
        "Should have ceiling_effect flag"
    
    print("✅ PASSED")
    return True


def test_short_series():
    """
    Test insufficient data handling.
    Pattern: [3,4,2] - only 3 scores
    Expected: Not suspicious (insufficient data)
    """
    print("\n" + "="*60)
    print("TEST: Short Series Handling")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [3, 4, 2]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result.get('reason', 'N/A')}")
    
    assert result['is_suspicious'] == False, \
        "Short series should not be flagged"
    assert result.get('reason') == 'insufficient_data', \
        "Should have insufficient_data reason"
    
    print("✅ PASSED")
    return True


def test_perfect_streak():
    """
    Test perfect streak detection.
    Pattern: [3,3,3,3,3,3,3,3,3,3] - 10 day streak
    Expected: Flag for perfect_streak
    """
    print("\n" + "="*60)
    print("TEST: Perfect Streak Detection")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Flags: {[f['type'] for f in result.get('flags', [])]}")
    
    assert result['is_suspicious'] == True, "Perfect streak should be flagged"
    assert any(f['type'] == 'perfect_streak' for f in result['flags']), \
        "Should have perfect_streak flag"
    
    print("✅ PASSED")
    return True


def test_get_masking_probability():
    """Test masking probability calculation"""
    print("\n" + "="*60)
    print("TEST: Get Masking Probability")
    print("="*60)
    
    validator = AdversarialValidator()
    
    # Clean scores - low probability
    clean_scores = [4, 2, 3, 5, 3, 4, 2, 4, 3, 5]
    prob_clean = validator.get_masking_probability(clean_scores)
    
    # Flat scores - medium probability
    flat_scores = [4, 4, 4, 4, 4, 4, 4, 4]
    prob_flat = validator.get_masking_probability(flat_scores)
    
    # Multiple flags - high probability
    ceiling_scores = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
    prob_ceiling = validator.get_masking_probability(ceiling_scores)
    
    print(f"Clean scores probability: {prob_clean:.2f}")
    print(f"Flat scores probability: {prob_flat:.2f}")
    print(f"Ceiling scores probability: {prob_ceiling:.2f}")
    
    assert prob_clean == 0.0, "Clean scores should have 0.0 probability"
    assert prob_flat > 0.0, "Flat scores should have >0.0 probability"
    assert prob_ceiling > prob_flat, "Ceiling should have higher probability than flat"
    assert 0.0 <= prob_flat <= 1.0, "Probability should be between 0 and 1"
    assert 0.0 <= prob_ceiling <= 1.0, "Probability should be between 0 and 1"
    
    print("✅ PASSED")
    return True


def test_deterministic_behavior():
    """Test that validator is deterministic"""
    print("\n" + "="*60)
    print("TEST: Deterministic Behavior")
    print("="*60)
    
    validator = AdversarialValidator()
    scores = [4, 4, 4, 4, 4, 4, 4, 4]
    
    # Run validation multiple times
    result1 = validator.validate(scores)
    result2 = validator.validate(scores)
    result3 = validator.validate(scores)
    
    print(f"Run 1 confidence: {result1['confidence']}")
    print(f"Run 2 confidence: {result2['confidence']}")
    print(f"Run 3 confidence: {result3['confidence']}")
    
    assert result1['confidence'] == result2['confidence'] == result3['confidence'], \
        "Results should be identical across runs"
    assert result1['is_suspicious'] == result2['is_suspicious'] == result3['is_suspicious'], \
        "Suspicious flag should be consistent"
    assert len(result1['flags']) == len(result2['flags']) == len(result3['flags']), \
        "Number of flags should be consistent"
    
    print("✅ PASSED - Validator is deterministic")
    return True


def test_multiple_flags():
    """Test case with multiple simultaneous flags"""
    print("\n" + "="*60)
    print("TEST: Multiple Flags Detection")
    print("="*60)
    
    validator = AdversarialValidator()
    # Scores that should trigger both low variance AND perfect streak
    scores = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    result = validator.validate(scores)
    
    print(f"Scores: {scores}")
    print(f"Is suspicious: {result['is_suspicious']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Number of flags: {len(result.get('flags', []))}")
    print(f"Flag types: {[f['type'] for f in result.get('flags', [])]}")
    
    assert result['is_suspicious'] == True
    assert len(result['flags']) >= 2, "Should have multiple flags"
    assert result['confidence'] > 0.35, "Multiple flags should increase confidence"
    
    print("✅ PASSED")
    return True


def test_variance_calculation():
    """Test variance calculation edge cases"""
    print("\n" + "="*60)
    print("TEST: Variance Calculation")
    print("="*60)
    
    validator = AdversarialValidator()
    
    # Test various variance levels
    high_variance = [1, 5, 1, 5, 1, 5, 1, 5]  # High variance
    low_variance = [3, 3, 3, 3, 3, 3, 3, 3]   # Zero variance
    
    result_high = validator.validate(high_variance)
    result_low = validator.validate(low_variance)
    
    print(f"High variance scores: {high_variance}")
    print(f"  Is suspicious: {result_high['is_suspicious']}")
    print(f"\nLow variance scores: {low_variance}")
    print(f"  Is suspicious: {result_low['is_suspicious']}")
    
    # High variance should not be flagged for low_variance
    assert not any(f['type'] == 'low_variance' for f in result_high.get('flags', [])), \
        "High variance should not trigger low_variance flag"
    
    # Low variance should be flagged
    assert any(f['type'] == 'low_variance' for f in result_low.get('flags', [])), \
        "Low variance should trigger low_variance flag"
    
    print("✅ PASSED")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*10 + "GuardianAI Adversarial Validator Test Suite")
    print("="*70)
    
    tests = [
        test_flat_scores_flagged,
        test_normal_scores_clean,
        test_sudden_recovery,
        test_ceiling_effect,
        test_short_series,
        test_perfect_streak,
        test_get_masking_probability,
        test_deterministic_behavior,
        test_multiple_flags,
        test_variance_calculation
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
            failed += 1
    
    print("\n" + "="*70)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} total")
    print("="*70)
    
    if failed == 0:
        print("\n🎉 All tests passed! Adversarial validator is working correctly.")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    import logging
    # Suppress logging output during tests
    logging.basicConfig(level=logging.CRITICAL)
    
    success = run_all_tests()
    sys.exit(0 if success else 1)
