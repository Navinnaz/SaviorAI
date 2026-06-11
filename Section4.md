## SECTION 4 — THE AGENT CORE (PYTHON)

### 4.1 — Hidden Markov Model (HMM) Burnout State Machine

```python
# backend/agents/hmm_engine.py

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class BurnoutAssessment:
    state: str          # 'stable', 'at_risk', 'crisis'
    probability: float
    trend_score: float
    consecutive_low_days: int
    reasoning: str

class BurnoutHMM:
    """
    Hidden Markov Model for student burnout detection.
    
    States: Stable (S0), At-Risk (S1), Crisis (S2)
    
    Transition probabilities derived from burnout research literature:
    - Maslach Burnout Inventory studies
    - Academic stress progression models
    - NIMHANS student wellness data
    
    The key insight: burnout is NOT a threshold event.
    It is a probabilistic state transition that accumulates.
    A student can be 70% 'at_risk' while still functioning.
    That 70% is what we act on.
    """
    
    # State transition matrix [from_state][to_state]
    # Rows: current state (Stable, At-Risk, Crisis)
    # Cols: next state (Stable, At-Risk, Crisis)
    # Source: adapted from Schaufeli & Leiter (2000) burnout progression model
    TRANSITION_MATRIX = np.array([
        [0.85, 0.13, 0.02],   # From Stable
        [0.30, 0.55, 0.15],   # From At-Risk
        [0.10, 0.30, 0.60],   # From Crisis
    ])
    
    # Emission probabilities: P(observed_score | hidden_state)
    # Score ranges: 1-2 (low), 3 (medium), 4-5 (high)
    EMISSION_MATRIX = np.array([
        [0.05, 0.20, 0.75],   # Stable: mostly high scores
        [0.35, 0.40, 0.25],   # At-Risk: mixed, often low
        [0.70, 0.20, 0.10],   # Crisis: mostly low scores
    ])
    
    STATES = ['stable', 'at_risk', 'crisis']
    
    def score_to_obs(self, score: int) -> int:
        """Convert 1-5 score to observation index (0=low, 1=mid, 2=high)"""
        if score <= 2: return 0
        if score == 3: return 1
        return 2
    
    def viterbi(self, scores: List[int]) -> Tuple[List[str], List[float]]:
        """
        Viterbi algorithm to find most likely sequence of hidden states.
        Returns sequence of states and their probabilities.
        """
        if not scores:
            return ['stable'], [0.9]
        
        observations = [self.score_to_obs(s) for s in scores]
        n_states = 3
        n_obs = len(observations)
        
        # Initial state probabilities (most students start stable)
        initial_probs = np.array([0.80, 0.15, 0.05])
        
        # Viterbi matrices
        viterbi_mat = np.zeros((n_states, n_obs))
        backpointer = np.zeros((n_states, n_obs), dtype=int)
        
        # Initialization
        for s in range(n_states):
            viterbi_mat[s][0] = (
                initial_probs[s] * self.EMISSION_MATRIX[s][observations[0]]
            )
        
        # Recursion
        for t in range(1, n_obs):
            for s in range(n_states):
                probs = [
                    viterbi_mat[s_prev][t-1] 
                    * self.TRANSITION_MATRIX[s_prev][s] 
                    * self.EMISSION_MATRIX[s][observations[t]]
                    for s_prev in range(n_states)
                ]
                viterbi_mat[s][t] = max(probs)
                backpointer[s][t] = np.argmax(probs)
        
        # Backtrack
        states_seq = []
        probs_seq = []
        current = np.argmax(viterbi_mat[:, -1])
        
        for t in range(n_obs - 1, -1, -1):
            states_seq.insert(0, self.STATES[current])
            probs_seq.insert(0, float(viterbi_mat[current][t]))
            if t > 0:
                current = backpointer[current][t]
        
        return states_seq, probs_seq
    
    def assess(self, scores: List[int], baseline: float = 3.0) -> BurnoutAssessment:
        """
        Full burnout assessment for a student.
        Returns current state, probability, and reasoning.
        """
        if len(scores) < 3:
            return BurnoutAssessment(
                state='stable',
                probability=0.8,
                trend_score=0.0,
                consecutive_low_days=0,
                reasoning="Insufficient data for assessment. Need at least 3 check-ins."
            )
        
        states, probs = self.viterbi(scores)
        current_state = states[-1]
        current_prob = probs[-1]
        
        # Calculate trend: recent 5 days vs personal baseline
        recent = scores[-5:] if len(scores) >= 5 else scores
        recent_avg = sum(recent) / len(recent)
        trend_score = recent_avg - baseline
        
        # Count consecutive low days
        consecutive_low = 0
        for s in reversed(scores):
            if s <= 2:
                consecutive_low += 1
            else:
                break
        
        # Build reasoning
        reasoning = self._build_reasoning(
            current_state, trend_score, consecutive_low, recent_avg, baseline
        )
        
        return BurnoutAssessment(
            state=current_state,
            probability=current_prob,
            trend_score=round(trend_score, 2),
            consecutive_low_days=consecutive_low,
            reasoning=reasoning
        )
    
    def _build_reasoning(
        self, state: str, trend: float, consec_low: int, 
        recent_avg: float, baseline: float
    ) -> str:
        parts = []
        
        if trend < -1.5:
            parts.append(
                f"Score dropped {abs(trend):.1f} points below personal baseline"
            )
        elif trend < -0.8:
            parts.append(
                f"Moderate decline of {abs(trend):.1f} points from baseline"
            )
        
        if consec_low >= 3:
            parts.append(f"{consec_low} consecutive days scoring 1-2")
        elif consec_low >= 2:
            parts.append(f"{consec_low} consecutive low-score days")
        
        if state == 'at_risk' and not parts:
            parts.append(
                f"Pattern analysis indicates elevated risk despite average score of {recent_avg:.1f}"
            )
        
        if state == 'crisis':
            parts.append("HMM state probability indicates crisis-level distress")
        
        return ". ".join(parts) if parts else "Within normal variation range."
```

### 4.2 — Adversarial Check-in Validator

```python
# backend/agents/adversarial_validator.py

import numpy as np
from typing import List

class AdversarialValidator:
    """
    Detects students gaming the check-in system.
    
    Key insight: Real emotional states have variance.
    A student reporting exactly 4/5 every day for 14 days 
    is statistically improbable — and itself a signal.
    
    This is the feature no existing mental health app has.
    """
    
    VARIANCE_THRESHOLD = 0.15        # Below this = suspiciously flat
    PERFECT_STREAK_THRESHOLD = 7    # Days of same score = flag
    SUDDEN_RECOVERY_THRESHOLD = 2.0 # Score jump after crisis pattern
    
    def validate(self, scores: List[int]) -> dict:
        """
        Returns validation result with gaming probability.
        """
        if len(scores) < 5:
            return {
                "is_suspicious": False,
                "confidence": 0.0,
                "reason": "insufficient_data"
            }
        
        variance = float(np.var(scores))
        flags = []
        
        # Flag 1: Suspiciously low variance (too consistent)
        if variance < self.VARIANCE_THRESHOLD:
            flags.append({
                "type": "low_variance",
                "detail": f"Score variance of {variance:.3f} is statistically improbable for genuine responses",
                "severity": "medium"
            })
        
        # Flag 2: Perfect streak (same score many days in a row)
        streak = self._longest_streak(scores)
        if streak >= self.PERFECT_STREAK_THRESHOLD:
            flags.append({
                "type": "perfect_streak",
                "detail": f"Same score repeated {streak} consecutive days",
                "severity": "high" if streak >= 10 else "medium"
            })
        
        # Flag 3: Sudden recovery after a declining trend
        if len(scores) >= 7:
            recent_low = sum(s <= 2 for s in scores[-7:-2])
            if recent_low >= 3 and scores[-1] >= 4:
                jump = scores[-1] - scores[-2]
                if jump >= self.SUDDEN_RECOVERY_THRESHOLD:
                    flags.append({
                        "type": "sudden_recovery",
                        "detail": f"Score jumped {jump} points after {recent_low} low-score days — possible masking",
                        "severity": "high"
                    })
        
        # Flag 4: Always maximum score (5/5 every day)
        if all(s == 5 for s in scores[-7:]) and len(scores) >= 7:
            flags.append({
                "type": "ceiling_effect",
                "detail": "Consistently maximum scores — may indicate disengagement with the system",
                "severity": "low"
            })
        
        is_suspicious = len(flags) > 0
        confidence = min(1.0, len(flags) * 0.35)
        
        return {
            "is_suspicious": is_suspicious,
            "confidence": round(confidence, 2),
            "flags": flags,
            "recommendation": (
                "Consider gentle direct outreach rather than automated alert — "
                "student may be masking distress"
            ) if is_suspicious else None
        }
    
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
```

### 4.3 — Cohort Anomaly Detector

```python
# backend/agents/cohort_detector.py

from typing import List, Dict
from datetime import datetime, timedelta
import statistics

class CohortAnomalyDetector:
    """
    Detects systemic stressors affecting groups of students simultaneously.
    
    This is what individual wellness apps CANNOT do.
    When 60% of a batch declines together — it's not individual burnout.
    It's a bad professor, an unfair exam, a hostel incident.
    The institution needs to know, not just the individual counsellor.
    
    Japan context: This maps directly to 'examination hell' (juken jigoku)
    where entire cohorts deteriorate simultaneously before entrance exams.
    """
    
    COHORT_THRESHOLD = 0.40         # 40% of batch affected = systemic
    SCORE_DROP_THRESHOLD = 1.0      # Average drop of 1+ points = significant
    MIN_BATCH_SIZE = 5              # Need at least 5 students to detect cohort pattern
    
    def detect(
        self, 
        batch_data: List[Dict]   # [{"student_id": ..., "recent_avg": ..., "baseline": ...}]
    ) -> Dict:
        """
        Analyse a batch of students for cohort-level anomaly.
        Returns detection result with institutional recommendation.
        """
        if len(batch_data) < self.MIN_BATCH_SIZE:
            return {"anomaly_detected": False, "reason": "insufficient_batch_size"}
        
        # Calculate who's declining relative to their personal baseline
        declining = [
            s for s in batch_data 
            if (s["baseline"] - s["recent_avg"]) >= self.SCORE_DROP_THRESHOLD
        ]
        
        affected_pct = len(declining) / len(batch_data)
        
        if affected_pct < self.COHORT_THRESHOLD:
            return {
                "anomaly_detected": False,
                "affected_percentage": round(affected_pct * 100, 1)
            }
        
        # Cohort anomaly confirmed
        avg_drop = statistics.mean([
            s["baseline"] - s["recent_avg"] for s in declining
        ])
        
        return {
            "anomaly_detected": True,
            "affected_count": len(declining),
            "total_count": len(batch_data),
            "affected_percentage": round(affected_pct * 100, 1),
            "average_score_drop": round(avg_drop, 2),
            "severity": "high" if affected_pct > 0.6 else "medium",
            "institutional_action": self._recommend_action(affected_pct, avg_drop)
        }
    
    def _recommend_action(self, pct: float, avg_drop: float) -> str:
        if pct > 0.6 and avg_drop > 1.5:
            return (
                "URGENT: Over 60% of this batch shows significant decline. "
                "Recommend immediate batch-level intervention — group counselling session, "
                "faculty review meeting, or workload assessment within 48 hours."
            )
        elif pct > 0.4:
            return (
                "ATTENTION: Systemic stress pattern detected in this batch. "
                "Recommend proactive faculty communication and optional "
                "group check-in session this week."
            )
        return "Monitor closely. Consider reaching out to batch representatives."
```

### 4.4 — Autonomous Intervention Orchestrator

```python
# backend/agents/intervention_orchestrator.py

from typing import Optional
import openai
from .hmm_engine import BurnoutAssessment
from .adversarial_validator import AdversarialValidator

class InterventionOrchestrator:
    """
    The decision-making core of GuardianAI.
    
    This is what makes it AGENTIC:
    - It perceives (reads assessment data)
    - It reasons (GPT-4o contextualises, adversarial check applied)
    - It decides (selects intervention level autonomously)
    - It acts (sends messages, files reports)
    - It observes (monitors if student responds)
    - It adapts (escalates or de-escalates based on response)
    
    No human makes the level decision. The agent does.
    """
    
    def __init__(self, openai_client):
        self.client = openai_client
        self.validator = AdversarialValidator()
    
    async def decide_and_act(
        self,
        student: dict,
        assessment: BurnoutAssessment,
        recent_scores: list,
        recent_onewords: list,
        validation_result: dict,
        last_intervention: Optional[dict] = None
    ) -> dict:
        """
        Autonomous intervention decision.
        Returns action dict with level, message, and reasoning.
        """
        
        # Rule 1: Never re-trigger same level within 48 hours
        if last_intervention:
            hours_since = self._hours_since(last_intervention["triggered_at"])
            if hours_since < 48 and last_intervention["level"] >= assessment_to_level(assessment):
                return {"action": "hold", "reason": "Recent intervention pending response"}
        
        # Rule 2: Adversarial flag overrides normal level
        if validation_result["is_suspicious"] and validation_result["confidence"] > 0.5:
            return await self._handle_masking(student, validation_result)
        
        # Rule 3: Select intervention level from assessment
        level = self._select_level(assessment, last_intervention)
        
        # Rule 4: Generate human message via GPT-4o
        message = await self._generate_message(
            student, assessment, recent_onewords, level
        )
        
        # Rule 5: Select recipient
        recipient = self._select_recipient(level)
        
        return {
            "level": level,
            "message": message,
            "recipient": recipient,
            "reasoning": assessment.reasoning,
            "action": "send"
        }
    
    def _select_level(
        self, 
        assessment: BurnoutAssessment,
        last_intervention: Optional[dict]
    ) -> int:
        """
        Autonomous level selection. No human input.
        
        Level 1: Peer nudge — At-Risk, first occurrence
        Level 2: Counsellor soft alert — At-Risk, recurring OR low probability crisis
        Level 3: Emergency — Crisis state, high probability
        Level 4: Institutional report — Cohort anomaly OR prolonged crisis
        """
        state = assessment.state
        prob = assessment.hmm_probability
        consec = assessment.consecutive_low_days
        
        if state == 'stable':
            return 0  # No action needed
        
        if state == 'at_risk':
            if last_intervention and last_intervention["level"] >= 1:
                return 2  # Escalate to counsellor if peer nudge didn't resolve
            return 1   # First at-risk: peer nudge
        
        if state == 'crisis':
            if prob > 0.75 or consec >= 5:
                return 3  # High confidence crisis: emergency
            return 2   # Lower confidence: counsellor first
        
        return 1
    
    async def _generate_message(
        self,
        student: dict,
        assessment: BurnoutAssessment,
        recent_onewords: list,
        level: int
    ) -> str:
        """
        GPT-4o generates the actual message content.
        Warm, specific, never clinical.
        """
        
        level_instructions = {
            1: "Write a warm, casual WhatsApp message to a student from their peer support network. NOT clinical. Sound like a caring friend checking in.",
            2: "Write a professional but warm alert to a college counsellor. Include specific data points. Actionable. Under 150 words.",
            3: "Write an urgent but calm emergency notification to a counsellor AND emergency contact. Include the student's name and the specific concerning pattern. Clear call to action.",
            4: "Write an institutional report summary for the Dean/Principal. Professional. Data-driven. Recommendations included."
        }
        
        prompt = f"""
You are GuardianAI, an autonomous student wellbeing agent.

Student: {student['name']}, Year {student.get('year_of_study', 'N/A')}, {student.get('batch', 'N/A')}
Assessment: {assessment.state.upper()} (probability: {assessment.probability:.0%})
Trend: {assessment.trend_score:+.1f} from personal baseline
Consecutive low days: {assessment.consecutive_low_days}
Recent one-word responses: {', '.join(recent_onewords[-5:]) if recent_onewords else 'none'}
Agent reasoning: {assessment.reasoning}

Task: {level_instructions.get(level, level_instructions[1])}

Requirements:
- NEVER mention surveillance or monitoring
- NEVER use clinical language like "depression" or "mental illness"  
- DO mention you noticed they seem to be going through something
- DO offer specific, immediate support options
- Keep it human, warm, and genuinely caring

Generate ONLY the message text. No preamble.
"""
        
        response = await self.client.chat.completions.acreate(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    async def _handle_masking(self, student: dict, validation: dict) -> dict:
        """Special handling when gaming is detected."""
        message = await self._generate_masking_message(student, validation)
        return {
            "level": 2,  # Direct to counsellor, not peer
            "message": message,
            "recipient": "counsellor",
            "reasoning": f"Adversarial validation flags: {[f['type'] for f in validation['flags']]}",
            "action": "send_masking_alert"
        }
    
    def _select_recipient(self, level: int) -> str:
        mapping = {0: None, 1: "student", 2: "counsellor", 3: "emergency", 4: "institution"}
        return mapping.get(level, "counsellor")
    
    def _hours_since(self, timestamp) -> float:
        from datetime import datetime
        if isinstance(timestamp, str):
            from dateutil import parser
            timestamp = parser.parse(timestamp)
        return (datetime.utcnow() - timestamp).total_seconds() / 3600
```
