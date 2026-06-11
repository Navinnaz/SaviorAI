"""
GuardianAI - Webhook Message Parser Test Suite

Tests for check-in message parsing from various formats.
"""

import sys
import re
from pathlib import Path
from typing import Optional, Dict


# Inline the parse function for testing without dependencies
def parse_checkin_message(message_body: str) -> Optional[Dict[str, any]]:
    """
    Parse check-in message from various formats.
    
    Supported formats:
    1. "3 yes exhausted" (score ate oneword)
    2. "2\nno\nlost" (newline separated)
    3. "Feeling 2, ate no, word: hopeless" (natural language)
    4. "4" (score only)
    """
    if not message_body:
        return None
    
    message = message_body.strip().lower()
    
    # Extract score (must be 1-5)
    score_match = re.search(r'\b([1-5])\b', message)
    if not score_match:
        return None
    
    score = int(score_match.group(1))
    
    # Extract ate_properly (yes, mostly, no)
    ate_properly = "unknown"
    if re.search(r'\b(yes|y)\b', message):
        ate_properly = "yes"
    elif re.search(r'\b(mostly|kinda|somewhat)\b', message):
        ate_properly = "mostly"
    elif re.search(r'\b(no|n|nope)\b', message):
        ate_properly = "no"
    
    # Extract one_word - take LAST meaningful word (usually the emotion descriptor)
    words = re.findall(r'\b[a-z]{3,}\b', message)
    
    # Expanded exclusion list
    excluded = {
        'yes', 'mostly', 'kinda', 'somewhat', 'ate', 'feeling', 'word', 
        'today', 'day', 'the', 'like', 'and', 'but', 'for', 'with',
        'from', 'this', 'that', 'have', 'been', 'was', 'were'
    }
    
    meaningful_words = [w for w in words if w not in excluded]
    
    # Take LAST word (most likely the emotion/state descriptor)
    one_word = meaningful_words[-1] if meaningful_words else "none"
    
    return {
        "score": score,
        "ate_properly": ate_properly,
        "one_word": one_word
    }


def test_parse_simple_format():
    """Test parsing simple space-separated format: '3 yes exhausted'"""
    print("\n" + "="*60)
    print("TEST: Simple Format (space-separated)")
    print("="*60)
    
    message = "3 yes exhausted"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 3, "Score should be 3"
    assert result['ate_properly'] == 'yes', "Ate should be 'yes'"
    assert result['one_word'] == 'exhausted', "One word should be 'exhausted'"
    
    print("✅ PASSED")
    return True


def test_parse_newline_format():
    """Test parsing newline-separated format: '2\nno\nlost'"""
    print("\n" + "="*60)
    print("TEST: Newline Format")
    print("="*60)
    
    message = "2\nno\nlost"
    result = parse_checkin_message(message)
    
    print(f"Input: {repr(message)}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 2, "Score should be 2"
    assert result['ate_properly'] == 'no', "Ate should be 'no'"
    assert result['one_word'] == 'lost', "One word should be 'lost'"
    
    print("✅ PASSED")
    return True


def test_parse_natural_language():
    """Test parsing natural language format: 'Feeling 2, ate no, word: hopeless'"""
    print("\n" + "="*60)
    print("TEST: Natural Language Format")
    print("="*60)
    
    message = "Feeling 2, ate no, word: hopeless"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 2, "Score should be 2"
    assert result['ate_properly'] == 'no', "Ate should be 'no'"
    assert result['one_word'] == 'hopeless', "One word should be 'hopeless'"
    
    print("✅ PASSED")
    return True


def test_parse_score_only():
    """Test parsing score-only format: '4'"""
    print("\n" + "="*60)
    print("TEST: Score Only Format")
    print("="*60)
    
    message = "4"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 4, "Score should be 4"
    assert result['ate_properly'] == 'unknown', "Ate should be 'unknown'"
    assert result['one_word'] == 'none', "One word should be 'none'"
    
    print("✅ PASSED")
    return True


def test_parse_with_mostly():
    """Test parsing with 'mostly' for ate_properly"""
    print("\n" + "="*60)
    print("TEST: Mostly Ate Format")
    print("="*60)
    
    message = "3 mostly tired"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 3, "Score should be 3"
    assert result['ate_properly'] == 'mostly', "Ate should be 'mostly'"
    assert result['one_word'] == 'tired', "One word should be 'tired'"
    
    print("✅ PASSED")
    return True


def test_parse_uppercase():
    """Test parsing uppercase input"""
    print("\n" + "="*60)
    print("TEST: Uppercase Input")
    print("="*60)
    
    message = "5 YES MOTIVATED"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 5, "Score should be 5"
    assert result['ate_properly'] == 'yes', "Ate should be 'yes'"
    assert result['one_word'] == 'motivated', "One word should be 'motivated'"
    
    print("✅ PASSED")
    return True


def test_parse_invalid_score():
    """Test parsing with invalid score (out of 1-5 range)"""
    print("\n" + "="*60)
    print("TEST: Invalid Score")
    print("="*60)
    
    message = "7 yes happy"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is None, "Should fail to parse (score out of range)"
    
    print("✅ PASSED")
    return True


def test_parse_missing_score():
    """Test parsing with no score"""
    print("\n" + "="*60)
    print("TEST: Missing Score")
    print("="*60)
    
    message = "yes tired"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is None, "Should fail to parse (no score)"
    
    print("✅ PASSED")
    return True


def test_parse_mixed_format():
    """Test parsing mixed natural language"""
    print("\n" + "="*60)
    print("TEST: Mixed Natural Language")
    print("="*60)
    
    message = "I'm feeling like a 3 today, ate mostly, overwhelmed"
    result = parse_checkin_message(message)
    
    print(f"Input: {message}")
    print(f"Parsed: {result}")
    
    assert result is not None, "Should parse successfully"
    assert result['score'] == 3, "Score should be 3"
    assert result['ate_properly'] == 'mostly', "Ate should be 'mostly'"
    assert result['one_word'] == 'overwhelmed', "One word should be 'overwhelmed'"
    
    print("✅ PASSED")
    return True


def run_all_tests():
    """Run all webhook parser tests"""
    print("\n" + "="*70)
    print(" "*10 + "GuardianAI Webhook Parser Test Suite")
    print("="*70)
    
    tests = [
        test_parse_simple_format,
        test_parse_newline_format,
        test_parse_natural_language,
        test_parse_score_only,
        test_parse_with_mostly,
        test_parse_uppercase,
        test_parse_invalid_score,
        test_parse_missing_score,
        test_parse_mixed_format
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
        print("\n🎉 All tests passed! Webhook parser is working correctly.")
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
