"""
SaviorAI - Adversarial Check-in Validator

Detects students gaming the check-in system.

Key insight: Real emotional states have variance.
A student reporting exactly 4/5 every day for 14 days 
is statistically improbable — and itself a signal.

This is the feature no existing mental health app has.

The validator is completely deterministic - same input always produces
the same output, ensuring consistent detection across runs.
"""

import numpy as np
from typing import List, Dict
import logging

# Configure logging
logger = logging.getLogger(__name__)


class AdversarialValidator:
    """
    Detects students gaming the check-in system.
    
    This validator detects four types of suspicious patterns:
    1. Low variance: Scores too consistent (real emotions vary)
    2. Perfect streaks: Same score repeated for many days
    3. Sudden recovery: Jumping from crisis to high after masking
    4. Ceiling effect: Always maximum scores (disengagement)
    
    The validator is deterministic - no randomness, same input = same output.
    """
    
    VARIANCE_THRESHOLD = 0.15        # Below this = suspiciously flat
    PERFECT_STREAK_THRESHOLD = 7    # Days of same score = flag
    SUDDEN_RECOVERY_THRESHOLD = 2.0 # Score jump after crisis pattern
    
    def validate(self, scores: List[int]) -> Dict:
        """
        Validate check-in scores for gaming/masking behavior.
        
        Args:
            scores: List of mood scores (1-5) in chronological order
        
        Returns:
            Dict with:
            - is_suspicious: bool
            - confidence: float (0.0-1.0)
            - flags: List of flag dicts
            - recommendation: str or None
        
        The method is deterministic - no randomness involved.
        """
        if len(scores) < 5:
            logger.debug(f"Insufficient data for validation: {len(scores)} scores")
            return {
                "is_suspicious": False,
                "confidence": 0.0,
                "reason": "insufficient_data",
                "flags": []
            }
        
        variance = float(np.var(scores))
        flags = []
        
        logger.info(f"Validating {len(scores)} scores, variance: {variance:.3f}")
        
        # Flag 1: Suspiciously low variance (too consistent)
        if variance < self.VARIANCE_THRESHOLD:
            flag = {
                "type": "low_variance",
                "detail": f"Score variance of {variance:.3f} is statistically improbable for genuine responses",
                "severity": "medium"
            }
            flags.append(flag)
            logger.warning(f"LOW VARIANCE FLAG: {flag['detail']}")
        
        # Flag 2: Perfect streak (same score many days in a row)
        streak = self._longest_streak(scores)
        if streak >= self.PERFECT_STREAK_THRESHOLD:
            flag = {
                "type": "perfect_streak",
                "detail": f"Same score repeated {streak} consecutive days",
                "severity": "high" if streak >= 10 else "medium"
            }
            flags.append(flag)
            logger.warning(f"PERFECT STREAK FLAG: {flag['detail']}")
        
        # Flag 3: Sudden recovery after a declining trend
        if len(scores) >= 7:
            recent_low = sum(s <= 2 for s in scores[-7:-2])
            if recent_low >= 3 and scores[-1] >= 4:
                jump = scores[-1] - scores[-2]
                if jump >= self.SUDDEN_RECOVERY_THRESHOLD:
                    flag = {
                        "type": "sudden_recovery",
                        "detail": f"Score jumped {jump} points after {recent_low} low-score days — possible masking",
                        "severity": "high"
                    }
                    flags.append(flag)
                    logger.warning(f"SUDDEN RECOVERY FLAG: {flag['detail']}")
        
        # Flag 4: Always maximum score (5/5 every day)
        if all(s == 5 for s in scores[-7:]) and len(scores) >= 7:
            flag = {
                "type": "ceiling_effect",
                "detail": "Consistently maximum scores — may indicate disengagement with the system",
                "severity": "low"
            }
            flags.append(flag)
            logger.warning(f"CEILING EFFECT FLAG: {flag['detail']}")
        
        is_suspicious = len(flags) > 0
        confidence = min(1.0, len(flags) * 0.35)
        
        if is_suspicious:
            logger.info(f"Validation SUSPICIOUS: {len(flags)} flags, confidence {confidence:.2f}")
        else:
            logger.debug("Validation CLEAN: No suspicious patterns detected")
        
        return {
            "is_suspicious": is_suspicious,
            "confidence": round(confidence, 2),
            "flags": flags,
            "recommendation": (
                "Consider gentle direct outreach rather than automated alert — "
                "student may be masking distress"
            ) if is_suspicious else None
        }
    
    def get_masking_probability(self, scores: List[int]) -> float:
        """
        Calculate probability (0.0-1.0) that student is gaming the system.
        
        This is a simplified probability estimate based on validation flags.
        Higher values indicate higher likelihood of deliberate masking.
        
        Args:
            scores: List of mood scores (1-5)
        
        Returns:
            Float between 0.0 and 1.0
            - 0.0-0.3: Low probability, likely genuine
            - 0.3-0.6: Moderate probability, monitor closely
            - 0.6-1.0: High probability, likely masking
        
        The method is deterministic.
        """
        if len(scores) < 5:
            return 0.0
        
        validation = self.validate(scores)
        
        # Base probability from confidence
        probability = validation["confidence"]
        
        # Adjust based on severity of flags
        for flag in validation.get("flags", []):
            if flag["severity"] == "high":
                probability += 0.15
            elif flag["severity"] == "medium":
                probability += 0.10
        
        # Cap at 1.0
        probability = min(1.0, probability)
        
        logger.debug(f"Masking probability: {probability:.2f} ({len(validation.get('flags', []))} flags)")
        
        return round(probability, 2)
    
    def _longest_streak(self, scores: List[int]) -> int:
        """Find the longest streak of identical consecutive scores."""
        if not scores:
            return 0
        max_streak = current_streak = 1
        for i in range(1, len(scores)):
            if scores[i] == scores[i-1]:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1
        return max_streak

