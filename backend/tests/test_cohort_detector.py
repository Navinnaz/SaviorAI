"""
SaviorAI - Cohort Anomaly Detector Test Suite

Tests for systemic stressor detection across student cohorts.
Validates batch-level anomaly identification.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from agents.cohort_detector import CohortAnomalyDetector


def test_no_anomaly():
    """
    Test that small percentage declining does not trigger anomaly.
    3/10 students declining (30%) < 40% threshold
    Expected: No anomaly detected
    """
    print("\n" + "="*60)
    print("TEST: No Anomaly (Below Threshold)")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # 10 students: 3 declining, 7 stable
    batch_data = [
        # Declining students (baseline - recent_avg >= 1.0)
        {"student_id": "1", "baseline": 4.0, "recent_avg": 2.5},  # Drop: 1.5
        {"student_id": "2", "baseline": 3.5, "recent_avg": 2.0},  # Drop: 1.5
        {"student_id": "3", "baseline": 4.5, "recent_avg": 3.0},  # Drop: 1.5
        # Stable students (drop < 1.0)
        {"student_id": "4", "baseline": 3.5, "recent_avg": 3.5},  # Drop: 0.0
        {"student_id": "5", "baseline": 4.0, "recent_avg": 3.5},  # Drop: 0.5
        {"student_id": "6", "baseline": 3.0, "recent_avg": 3.0},  # Drop: 0.0
        {"student_id": "7", "baseline": 4.5, "recent_avg": 4.0},  # Drop: 0.5
        {"student_id": "8", "baseline": 3.5, "recent_avg": 3.0},  # Drop: 0.5
        {"student_id": "9", "baseline": 4.0, "recent_avg": 4.0},  # Drop: 0.0
        {"student_id": "10", "baseline": 3.5, "recent_avg": 3.5},  # Drop: 0.0
    ]
    
    result = detector.detect(batch_data)
    
    print(f"Batch size: {len(batch_data)}")
    print(f"Declining: 3 students (30%)")
    print(f"Threshold: {detector.COHORT_THRESHOLD:.0%}")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    print(f"Affected percentage: {result.get('affected_percentage', 'N/A')}%")
    
    assert result['anomaly_detected'] == False, \
        "30% should not trigger anomaly (threshold 40%)"
    assert result.get('affected_percentage') == 30.0
    
    print("✅ PASSED")
    return True


def test_anomaly_medium():
    """
    Test medium severity anomaly detection.
    5/10 students declining (50%) >= 40% and < 60%
    Expected: Medium severity anomaly
    """
    print("\n" + "="*60)
    print("TEST: Medium Severity Anomaly")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # 10 students: 5 declining, 5 stable
    batch_data = [
        # Declining students
        {"student_id": "1", "baseline": 4.0, "recent_avg": 2.5},
        {"student_id": "2", "baseline": 3.5, "recent_avg": 2.0},
        {"student_id": "3", "baseline": 4.5, "recent_avg": 3.0},
        {"student_id": "4", "baseline": 4.0, "recent_avg": 2.5},
        {"student_id": "5", "baseline": 3.5, "recent_avg": 2.0},
        # Stable students
        {"student_id": "6", "baseline": 3.0, "recent_avg": 3.0},
        {"student_id": "7", "baseline": 4.5, "recent_avg": 4.0},
        {"student_id": "8", "baseline": 3.5, "recent_avg": 3.0},
        {"student_id": "9", "baseline": 4.0, "recent_avg": 4.0},
        {"student_id": "10", "baseline": 3.5, "recent_avg": 3.5},
    ]
    
    result = detector.detect(batch_data)
    
    print(f"Batch size: {len(batch_data)}")
    print(f"Declining: 5 students (50%)")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    print(f"Severity: {result.get('severity', 'N/A')}")
    print(f"Affected percentage: {result.get('affected_percentage', 'N/A')}%")
    print(f"Average drop: {result.get('average_score_drop', 'N/A')}")
    
    assert result['anomaly_detected'] == True, \
        "50% should trigger anomaly"
    assert result['severity'] == 'medium', \
        "50% should be medium severity (< 60%)"
    assert result['affected_count'] == 5
    assert result['affected_percentage'] == 50.0
    
    print("✅ PASSED")
    return True


def test_anomaly_high():
    """
    Test high severity anomaly detection.
    8/10 students declining (80%) >= 60%
    Expected: High severity anomaly with URGENT recommendation
    """
    print("\n" + "="*60)
    print("TEST: High Severity Anomaly")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # 10 students: 8 declining, 2 stable
    # Need avg_drop > 1.5 for URGENT recommendation
    batch_data = [
        # Declining students with larger drops (2.0+ each)
        {"student_id": "1", "baseline": 4.5, "recent_avg": 2.0},  # Drop: 2.5
        {"student_id": "2", "baseline": 4.0, "recent_avg": 2.0},  # Drop: 2.0
        {"student_id": "3", "baseline": 5.0, "recent_avg": 3.0},  # Drop: 2.0
        {"student_id": "4", "baseline": 4.5, "recent_avg": 2.5},  # Drop: 2.0
        {"student_id": "5", "baseline": 4.0, "recent_avg": 2.0},  # Drop: 2.0
        {"student_id": "6", "baseline": 4.5, "recent_avg": 2.5},  # Drop: 2.0
        {"student_id": "7", "baseline": 4.0, "recent_avg": 2.0},  # Drop: 2.0
        {"student_id": "8", "baseline": 5.0, "recent_avg": 3.0},  # Drop: 2.0
        # Stable students
        {"student_id": "9", "baseline": 4.0, "recent_avg": 4.0},  # Drop: 0.0
        {"student_id": "10", "baseline": 3.5, "recent_avg": 3.5},  # Drop: 0.0
    ]
    
    result = detector.detect(batch_data)
    
    print(f"Batch size: {len(batch_data)}")
    print(f"Declining: 8 students (80%)")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    print(f"Severity: {result.get('severity', 'N/A')}")
    print(f"Affected percentage: {result.get('affected_percentage', 'N/A')}%")
    print(f"Recommendation: {result.get('institutional_action', 'N/A')[:50]}...")
    
    assert result['anomaly_detected'] == True, \
        "80% should trigger anomaly"
    assert result['severity'] == 'high', \
        "80% should be high severity (>= 60%)"
    assert result['affected_count'] == 8
    assert result['affected_percentage'] == 80.0
    assert "URGENT" in result['institutional_action'], \
        "High severity should have URGENT recommendation"
    
    print("✅ PASSED")
    return True


def test_small_batch():
    """
    Test that small batches are rejected.
    Batch of 3 students < MIN_BATCH_SIZE (5)
    Expected: insufficient_batch_size
    """
    print("\n" + "="*60)
    print("TEST: Small Batch Handling")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # Only 3 students (below minimum of 5)
    batch_data = [
        {"student_id": "1", "baseline": 4.0, "recent_avg": 2.0},
        {"student_id": "2", "baseline": 3.5, "recent_avg": 1.5},
        {"student_id": "3", "baseline": 4.5, "recent_avg": 2.5},
    ]
    
    result = detector.detect(batch_data)
    
    print(f"Batch size: {len(batch_data)}")
    print(f"Minimum required: {detector.MIN_BATCH_SIZE}")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    print(f"Reason: {result.get('reason', 'N/A')}")
    
    assert result['anomaly_detected'] == False, \
        "Small batches should not trigger"
    assert result.get('reason') == 'insufficient_batch_size', \
        "Should have insufficient_batch_size reason"
    
    print("✅ PASSED")
    return True


def test_detect_trend():
    """Test trend detection over time"""
    print("\n" + "="*60)
    print("TEST: Trend Detection")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # Previous week data (average ~3.5)
    batch_previous = [
        {"student_id": "1", "recent_avg": 3.5},
        {"student_id": "2", "recent_avg": 3.5},
        {"student_id": "3", "recent_avg": 3.5},
        {"student_id": "4", "recent_avg": 3.5},
        {"student_id": "5", "recent_avg": 3.5},
    ]
    
    # Improving cohort (average ~4.0)
    batch_improving = [
        {"student_id": "1", "recent_avg": 4.0},
        {"student_id": "2", "recent_avg": 4.0},
        {"student_id": "3", "recent_avg": 4.0},
        {"student_id": "4", "recent_avg": 4.0},
        {"student_id": "5", "recent_avg": 4.0},
    ]
    
    # Declining cohort (average ~2.5)
    batch_declining = [
        {"student_id": "1", "recent_avg": 2.5},
        {"student_id": "2", "recent_avg": 2.5},
        {"student_id": "3", "recent_avg": 2.5},
        {"student_id": "4", "recent_avg": 2.5},
        {"student_id": "5", "recent_avg": 2.5},
    ]
    
    # Stable cohort (average ~3.6, within 0.3 threshold)
    batch_stable = [
        {"student_id": "1", "recent_avg": 3.6},
        {"student_id": "2", "recent_avg": 3.6},
        {"student_id": "3", "recent_avg": 3.6},
        {"student_id": "4", "recent_avg": 3.6},
        {"student_id": "5", "recent_avg": 3.6},
    ]
    
    trend_improving = detector.detect_trend(batch_improving, batch_previous)
    trend_declining = detector.detect_trend(batch_declining, batch_previous)
    trend_stable = detector.detect_trend(batch_stable, batch_previous)
    
    print(f"Previous avg: 3.5")
    print(f"Improving avg: 4.0 → trend: {trend_improving}")
    print(f"Declining avg: 2.5 → trend: {trend_declining}")
    print(f"Stable avg: 3.6 → trend: {trend_stable}")
    
    assert trend_improving == "improving", "4.0 > 3.5 by >0.3 should be improving"
    assert trend_declining == "declining", "2.5 < 3.5 by >0.3 should be declining"
    assert trend_stable == "stable", "3.6 vs 3.5 change <0.3 should be stable"
    
    print("✅ PASSED")
    return True


def test_threshold_configuration():
    """Test that threshold is configurable via environment"""
    print("\n" + "="*60)
    print("TEST: Threshold Configuration")
    print("="*60)
    
    import os
    
    # Set custom threshold
    os.environ["COHORT_THRESHOLD"] = "0.50"
    os.environ["SCORE_DROP_THRESHOLD"] = "1.5"
    os.environ["MIN_BATCH_SIZE"] = "10"
    
    detector = CohortAnomalyDetector()
    
    print(f"COHORT_THRESHOLD: {detector.COHORT_THRESHOLD}")
    print(f"SCORE_DROP_THRESHOLD: {detector.SCORE_DROP_THRESHOLD}")
    print(f"MIN_BATCH_SIZE: {detector.MIN_BATCH_SIZE}")
    
    assert detector.COHORT_THRESHOLD == 0.50, "Should use env value"
    assert detector.SCORE_DROP_THRESHOLD == 1.5, "Should use env value"
    assert detector.MIN_BATCH_SIZE == 10, "Should use env value"
    
    # Clean up
    del os.environ["COHORT_THRESHOLD"]
    del os.environ["SCORE_DROP_THRESHOLD"]
    del os.environ["MIN_BATCH_SIZE"]
    
    print("✅ PASSED")
    return True


def test_exact_threshold():
    """Test boundary condition at exact threshold"""
    print("\n" + "="*60)
    print("TEST: Exact Threshold Boundary")
    print("="*60)
    
    detector = CohortAnomalyDetector()
    
    # Exactly 40% declining (4/10)
    batch_data = [
        {"student_id": "1", "baseline": 4.0, "recent_avg": 2.5},
        {"student_id": "2", "baseline": 3.5, "recent_avg": 2.0},
        {"student_id": "3", "baseline": 4.5, "recent_avg": 3.0},
        {"student_id": "4", "baseline": 4.0, "recent_avg": 2.5},
        {"student_id": "5", "baseline": 3.0, "recent_avg": 3.0},
        {"student_id": "6", "baseline": 4.5, "recent_avg": 4.0},
        {"student_id": "7", "baseline": 3.5, "recent_avg": 3.0},
        {"student_id": "8", "baseline": 4.0, "recent_avg": 4.0},
        {"student_id": "9", "baseline": 3.5, "recent_avg": 3.5},
        {"student_id": "10", "baseline": 3.5, "recent_avg": 3.5}
    ]
    
    result = detector.detect(batch_data)
    
    print(f"Declining: 4/10 students (40.0%)")
    print(f"Threshold: {detector.COHORT_THRESHOLD:.0%}")
    print(f"Anomaly detected: {result['anomaly_detected']}")
    
    # At exactly 40%, should NOT trigger (needs to be >= threshold, and we check < threshold first)
    # Actually, looking at the code: affected_pct < COHORT_THRESHOLD returns False
    # So affected_pct >= COHORT_THRESHOLD should trigger
    assert result['anomaly_detected'] == True, "Exactly 40% should trigger"
    
    print("✅ PASSED")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*10 + "SaviorAI Cohort Anomaly Detector Test Suite")
    print("="*70)
    
    tests = [
        test_no_anomaly,
        test_anomaly_medium,
        test_anomaly_high,
        test_small_batch,
        test_detect_trend,
        test_threshold_configuration,
        test_exact_threshold
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
        print("\n🎉 All tests passed! Cohort detector is working correctly.")
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

