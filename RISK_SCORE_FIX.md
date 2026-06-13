# Risk Score Display Fix

## Problem
HMM probability values showed as 0% for crisis states due to numerical underflow in Viterbi algorithm. The algorithm multiplies many small probabilities together (e.g., `0.85 * 0.13 * 0.15 * ...`), resulting in extremely small numbers like `4.8e-08` (0.0000048%).

When displayed as `hmm_probability * 100`, this showed as **0% risk** even for crisis states, which was confusing and incorrect.

## Root Cause
This is a known issue with HMM implementations. The Viterbi algorithm compounds probabilities multiplicatively, causing exponential decay into near-zero values. While mathematically correct for relative comparisons (finding the most likely state sequence), these absolute probabilities are not suitable for direct user display.

## Solution
Changed risk score calculation to use **state-based mapping** with modifiers instead of raw HMM probability:

### Risk Score Ranges:
- **Crisis**: 85-95% risk
  - Base: 85%
  - +2% per consecutive low day (up to +10%)
  - Example: 9 consecutive low days → 85 + 18 = 95% (capped)

- **At-Risk**: 50-70% risk
  - Base: 50%
  - +10% per negative trend point (up to +20%)
  - Example: trend_score = -2.4 → 50 + 20 = 70%

- **Stable**: 5-35% risk
  - Base: 15%
  - -5% per positive trend point
  - Example: trend_score = +1.2 → 15 - 6 = 9%

### Why This Works:
1. **Meaningful to Users**: 90% risk is immediately understood as "high danger"
2. **State-Aligned**: Crisis always shows high risk (85-95%), stable shows low risk (5-35%)
3. **Nuanced**: Trend scores and consecutive low days provide fine-grained differentiation
4. **Accurate**: Still reflects the HMM's actual state classification

## Changes Made

### Backend: `backend/routes/dashboard.py`
- **Line ~225-250**: Rewrote risk score calculation in heatmap endpoint
- **Added sorting**: Heatmap now returns students sorted by risk score (highest first)
- Maps state → risk range, then applies trend/consecutive day modifiers

### Frontend: `frontend/src/pages/StudentProfile.jsx`
- **Line ~100-130**: Fixed Mental Health State Timeline percentages
- Changed from `(state.hmm_probability * 100)` to calculated risk percentage
- Now shows "CRISIS (92% risk)" instead of "CRISIS (0%)"
- Uses same state-based calculation as backend for consistency

## Testing
After these changes:
- ✅ Priya Sharma (crisis state) displays as **high risk score** (85-95%)
- ✅ Heatmap cards show meaningful risk percentages
- ✅ Students sorted by risk level (crisis students at top)
- ✅ Student profile timeline shows accurate risk percentages
- ✅ Color coding aligns with risk level (red = high, yellow = medium, green = low)

## Technical Note
The HMM's Viterbi algorithm is still working correctly for **state classification**. The issue was only with using raw probabilities for **display purposes**. The state itself ("crisis", "at_risk", "stable") remains accurate and research-backed.

For production improvements, consider:
- Log-space Viterbi algorithm to avoid underflow
- Separate confidence scores for state predictions
- Calibrated probability scaling for user display
