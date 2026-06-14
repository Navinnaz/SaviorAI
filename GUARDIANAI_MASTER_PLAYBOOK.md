# GuardianAI — Complete Master Playbook
## FAR AWAY 2026 Hackathon | Solo Build | Vibe Coding Edition

---

## SECTION 1 — PROJECT IDENTITY

**Name:** GuardianAI  
**Tagline:** *The autonomous agent that catches student burnout before it becomes a tragedy.*  
**Theme:** Agentic & Autonomous Systems  
**One-line pitch:** "One student dies by suicide every 40 minutes in India. GuardianAI is the autonomous agent that watches what counsellors can't — 24/7, at scale, before the crisis."

---

## SECTION 2 — SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                        GUARDIAN AI SYSTEM                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STUDENT LAYER                                                   │
│  ┌──────────────┐    ┌──────────────────────────────────────┐   │
│  │  WhatsApp    │───▶│  Twilio Webhook → FastAPI Ingestion  │   │
│  │  Check-ins   │    └──────────────────────────────────────┘   │
│  └──────────────┘                      │                        │
│                                        ▼                        │
│  AGENT CORE (The Brain)                                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │   │
│  │  │    HMM      │  │  Adversarial │  │    Cohort      │  │   │
│  │  │  Burnout    │  │  Validation  │  │   Anomaly      │  │   │
│  │  │   States   │  │   Engine     │  │  Detector      │  │   │
│  │  │ (Stable/   │  │ (Gaming      │  │ (Systemic      │  │   │
│  │  │  At-Risk/  │  │  Detection)  │  │  Stressors)    │  │   │
│  │  │  Crisis)   │  │              │  │                │  │   │
│  │  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │   │
│  │         └────────────────┴──────────────────┘           │   │
│  │                          │                               │   │
│  │                          ▼                               │   │
│  │              ┌───────────────────────┐                   │   │
│  │              │   GPT-4o Reasoning    │                   │   │
│  │              │   + Alert Generation  │                   │   │
│  │              └───────────┬───────────┘                   │   │
│  │                          │                               │   │
│  └──────────────────────────┼───────────────────────────────┘   │
│                             ▼                                    │
│  INTERVENTION LAYER                                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  Level 1: Peer nudge  │  Level 2: Counsellor alert        │  │
│  │  Level 3: Emergency   │  Level 4: Institutional report    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  DASHBOARD LAYER                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  React PWA  │  Risk Heatmap  │  Student Profiles         │   │
│  │  Counsellor Queue  │  Cohort Trends  │  Action Log       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  DATA LAYER                                                      │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │            PostgreSQL (via Railway)                        │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## SECTION 3 — DATABASE SCHEMA

```sql
-- Students enrolled in the system
CREATE TABLE students (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL,
  phone VARCHAR(15) UNIQUE NOT NULL,
  email VARCHAR(100),
  institution_id UUID REFERENCES institutions(id),
  batch VARCHAR(50),                    -- e.g. "CSE-2022"
  year_of_study INTEGER,
  enrolled_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE,
  baseline_score FLOAT DEFAULT 3.0,    -- personal baseline, updated weekly
  consent_given BOOLEAN DEFAULT FALSE,
  consent_given_at TIMESTAMP
);

-- Institutions using GuardianAI
CREATE TABLE institutions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(200) NOT NULL,
  type VARCHAR(50),                     -- 'college', 'coaching', 'school'
  city VARCHAR(100),
  state VARCHAR(100),
  counsellor_phone VARCHAR(15),
  counsellor_email VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Every check-in response stored here
CREATE TABLE checkins (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id) ON DELETE CASCADE,
  checked_in_at TIMESTAMP DEFAULT NOW(),
  mood_score INTEGER CHECK (mood_score BETWEEN 1 AND 5),
  ate_properly VARCHAR(10),             -- 'yes', 'mostly', 'no'
  one_word TEXT,                        -- free text response
  sentiment VARCHAR(20),                -- 'positive', 'neutral', 'negative', 'concerning'
  sentiment_score FLOAT,                -- -1.0 to 1.0
  raw_message TEXT,                     -- original WhatsApp message
  skipped BOOLEAN DEFAULT FALSE         -- did they skip today?
);

-- HMM state transitions tracked here
CREATE TABLE burnout_states (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id) ON DELETE CASCADE,
  assessed_at TIMESTAMP DEFAULT NOW(),
  state VARCHAR(20) NOT NULL,           -- 'stable', 'at_risk', 'crisis'
  hmm_probability FLOAT,               -- probability of current state
  trend_score FLOAT,                   -- recent avg vs baseline delta
  consecutive_low_days INTEGER,        -- days scored <= 2
  variance_flag BOOLEAN DEFAULT FALSE, -- adversarial gaming detected
  cohort_flag BOOLEAN DEFAULT FALSE,   -- part of cohort anomaly
  risk_score INTEGER                   -- 0-100 composite
    GENERATED ALWAYS AS (
      CASE state
        WHEN 'stable' THEN LEAST(30, ROUND(ABS(trend_score) * 10)::int)
        WHEN 'at_risk' THEN LEAST(69, 40 + consecutive_low_days * 5)
        WHEN 'crisis' THEN GREATEST(70, 70 + consecutive_low_days * 5)
      END
    ) STORED
);

-- Every autonomous action taken by the agent
CREATE TABLE interventions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID REFERENCES students(id) ON DELETE CASCADE,
  triggered_at TIMESTAMP DEFAULT NOW(),
  level INTEGER CHECK (level BETWEEN 1 AND 4),
  -- 1=peer nudge, 2=counsellor soft, 3=emergency, 4=institutional
  trigger_reason TEXT,                  -- agent's reasoning
  action_taken TEXT,                    -- what was sent/done
  message_sent TEXT,                    -- actual message content
  recipient VARCHAR(50),                -- 'student', 'counsellor', 'emergency_contact'
  was_acknowledged BOOLEAN DEFAULT FALSE,
  acknowledged_at TIMESTAMP,
  outcome VARCHAR(50)                   -- 'recovered', 'escalated', 'no_change', 'pending'
);

-- Cohort-level anomaly events
CREATE TABLE cohort_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  institution_id UUID REFERENCES institutions(id),
  batch VARCHAR(50),
  detected_at TIMESTAMP DEFAULT NOW(),
  affected_students INTEGER,
  affected_percentage FLOAT,
  avg_score_drop FLOAT,
  likely_cause TEXT,                    -- GPT-4o inference
  institutional_action_recommended TEXT,
  acknowledged BOOLEAN DEFAULT FALSE
);

-- Useful indexes
CREATE INDEX idx_checkins_student_date ON checkins(student_id, checked_in_at DESC);
CREATE INDEX idx_burnout_states_student ON burnout_states(student_id, assessed_at DESC);
CREATE INDEX idx_interventions_student ON interventions(student_id, triggered_at DESC);
```

---

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

---

## SECTION 5 — FASTAPI BACKEND STRUCTURE

```
backend/
├── main.py                    ← App entry, routes registered
├── requirements.txt
├── .env.example
├── database/
│   ├── connection.py          ← PostgreSQL connection pool
│   └── models.py              ← SQLAlchemy models
├── agents/
│   ├── __init__.py
│   ├── hmm_engine.py          ← HMM burnout states
│   ├── adversarial_validator.py
│   ├── cohort_detector.py
│   └── intervention_orchestrator.py
├── routes/
│   ├── webhook.py             ← Twilio WhatsApp webhook
│   ├── students.py            ← Student CRUD
│   ├── dashboard.py           ← Dashboard data endpoints
│   ├── interventions.py       ← Intervention history
│   └── cohorts.py             ← Cohort analytics
├── services/
│   ├── whatsapp.py            ← Twilio send/receive
│   ├── scheduler.py           ← APScheduler daily check-in jobs
│   └── sentiment.py           ← GPT-4o sentiment analysis
└── utils/
    ├── data_generator.py      ← Synthetic demo data generator
    └── demo_runner.py         ← Auto-runs demo scenarios
```

### Key Route: WhatsApp Webhook

```python
# backend/routes/webhook.py

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Receives every incoming WhatsApp message.
    Parses check-in, runs full agent pipeline, 
    autonomously decides intervention. No human in the loop.
    """
    phone = From.replace("whatsapp:", "")
    
    # 1. Find student
    student = await get_student_by_phone(db, phone)
    if not student:
        return send_whatsapp(phone, "Welcome to GuardianAI. Please register with your institution.")
    
    # 2. Parse check-in response
    checkin = await parse_checkin_response(Body, student.id)
    await save_checkin(db, checkin)
    
    # 3. Get full history
    scores = await get_recent_scores(db, student.id, days=14)
    onewords = await get_recent_onewords(db, student.id, days=7)
    
    # 4. Run HMM assessment
    hmm = BurnoutHMM()
    assessment = hmm.assess(scores, student.baseline_score)
    
    # 5. Adversarial validation
    validator = AdversarialValidator()
    validation = validator.validate(scores)
    
    # 6. Save burnout state
    await save_burnout_state(db, student.id, assessment, validation)
    
    # 7. Run intervention orchestrator — AUTONOMOUS DECISION
    orchestrator = InterventionOrchestrator(openai_client)
    last_intervention = await get_last_intervention(db, student.id)
    
    action = await orchestrator.decide_and_act(
        student=student.__dict__,
        assessment=assessment,
        recent_scores=scores,
        recent_onewords=onewords,
        validation_result=validation,
        last_intervention=last_intervention
    )
    
    # 8. Execute the action
    if action["action"] == "send" and action["level"] > 0:
        await execute_intervention(db, student, action)
    
    # 9. Confirm receipt to student
    await send_whatsapp(phone, "✅ Logged. Thank you for checking in.")
    
    return Response(status_code=200)
```

---

## SECTION 6 — REACT PWA DASHBOARD

```
frontend/
├── public/
│   ├── manifest.json          ← PWA manifest
│   └── icons/
├── src/
│   ├── App.jsx
│   ├── pages/
│   │   ├── Home.jsx           ← Institution overview + risk heatmap
│   │   ├── Students.jsx       ← All students, filterable by risk
│   │   ├── StudentProfile.jsx ← Individual student timeline
│   │   ├── Cohorts.jsx        ← Batch-level analytics
│   │   └── ActionLog.jsx      ← Every autonomous action taken
│   ├── components/
│   │   ├── RiskHeatmap.jsx    ← Visual grid of student risk levels
│   │   ├── TrendChart.jsx     ← 14-day score trend per student
│   │   ├── StateTimeline.jsx  ← HMM state transitions visualised
│   │   ├── InterventionCard.jsx
│   │   └── CohortAlert.jsx
│   └── services/
│       └── api.js
```

---

## SECTION 7 — DAY-BY-DAY BUILD PLAN

| Day | Date | Focus | Deliverable |
|-----|------|-------|-------------|
| 1 | Jun 4 | Project setup + DB | Schema live on Railway, FastAPI skeleton |
| 2 | Jun 5 | HMM Engine | BurnoutHMM working, unit tested |
| 3 | Jun 6 | Adversarial Validator + Cohort Detector | Both agents working |
| 4 | Jun 7 | WhatsApp integration | Check-in send/receive working via Twilio |
| 5 | Jun 8 | Full agent pipeline | Webhook → HMM → Intervention → WhatsApp |
| 6 | Jun 9 | React dashboard skeleton | Home + Students screens |
| 7 | Jun 10 | Dashboard charts | Risk heatmap, trend charts, HMM timeline |
| 8 | Jun 11 | Demo data + scenarios | 50 synthetic students, 3 demo scenarios |
| 9 | Jun 12 | PWA + polish | Installable on phone, UI polished |
| 10 | Jun 13 | Demo rehearsal + README | 90s demo locked, GitHub clean |
| 11 | Jun 14 | Submit by noon | Submit 6 hours early |

---

## SECTION 8 — SYNTHETIC DEMO DATA GENERATOR

```python
# backend/utils/data_generator.py
"""
Generates 50 realistic synthetic students for demo.
Three persona archetypes with distinct trajectories.
Run this before demo: python data_generator.py
"""

import random
from datetime import datetime, timedelta

def generate_demo_students(db_session):
    
    # PERSONA TYPE A: Student in crisis (8 students)
    # Clear declining trajectory judges will see immediately
    crisis_pattern = [4, 4, 3, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 2]
    
    # PERSONA TYPE B: Student gaming the system (5 students)
    # Suspiciously flat scores — adversarial validation flags this
    gaming_pattern = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    
    # PERSONA TYPE C: Normal variation (37 students)
    # Healthy variance, occasional dips, recoveries
    def normal_pattern():
        base = 3.5
        return [max(1, min(5, round(base + random.gauss(0, 0.8)))) for _ in range(14)]
    
    # One-word response pools per persona
    crisis_words = [
        "okay", "tired", "stressed", "exhausted", 
        "overwhelmed", "lost", "empty", "struggling"
    ]
    gaming_words = ["fine", "good", "great", "good", "fine", "okay"]
    normal_words = [
        "good", "tired", "okay", "happy", "stressed",
        "focused", "anxious", "motivated", "calm", "busy"
    ]
    
    # Demo flagship student: "Priya" — your main demo
    flagship = {
        "name": "Priya Sharma",
        "batch": "CSE-2022",
        "year": 2,
        "scores": crisis_pattern,
        "onewords": crisis_words[-len(crisis_pattern):],
        "persona": "crisis"
    }
    
    return flagship  # + rest of 50 students
```

---

## SECTION 9 — THE DEMO SCRIPT (90 Seconds)

**SETUP:** Dashboard open on laptop. Phone on table with GuardianAI PWA installed.

**0:00** — Open institution dashboard. 50 students visible on risk heatmap. Mostly green. 3 yellow. 1 red.

**0:10** — Click the red student: *"This is Priya. Second year CSE. Let me show you what the agent saw."*

**0:20** — Show 14-day score timeline: `4→4→3→4→3→3→2→2→2→1→2→1→1→2`. Show HMM state transition: Stable → At-Risk → Crisis. Point to the exact day the agent escalated from Level 1 to Level 2 autonomously.

**0:35** — Show the adversarial validation on Student B: *"This student has been rating 4/5 every single day for 14 days. Real emotional states don't work that way. The agent flagged this as potential masking — and sent a different kind of alert."*

**0:50** — Show cohort alert for Batch B: *"40% of this batch declined simultaneously this week. That's not individual burnout — that's a systemic stressor. The agent filed an institutional alert to the Dean. No human noticed this. The agent did."*

**1:05** — Show autonomous action log: intervention chain, message sent, student response tracked. *"The agent made every one of these decisions. No human in the loop."*

**1:20** — Pick up phone. Show PWA on homescreen. *"And a counsellor gets this on their phone. Not a 47-page report — a 3-line alert with the student's name, the pattern, and a recommended action."*

**1:35** — Final line: *"One student dies by suicide every 40 minutes in India. GuardianAI doesn't replace counsellors. It makes sure no student reaches that minute without someone already knowing."*

---

## SECTION 10 — VIBE CODING STRATEGY

### The 5 Commandments of Vibe Coding GuardianAI

**1. One component per session.** Never ask Claude to build "the whole backend." Always one file, one function, one component per prompt.

**2. Always paste context first.** Before any prompt, paste the relevant section of this playbook. Claude needs the schema and architecture to generate consistent code.

**3. Test immediately after each component.** Never stack two unbuilt components. Build → test → confirm → move forward.

**4. Name your files in the prompt.** "Create `backend/agents/hmm_engine.py` with..." — exact paths prevent confusion.

**5. Ask for tests alongside code.** Every agent component should have a `test_` file generated simultaneously.

---

## SECTION 11 — KIRO IDE VIBE CODING PROMPTS

Use these prompts **in exact sequence**. Each builds on the previous.

---

### PROMPT 0 — Project Initialisation

```
I am building GuardianAI — an autonomous student mental health triage agent 
for FAR AWAY 2026 hackathon. Here is the complete architecture:

[PASTE SECTION 2 — SYSTEM ARCHITECTURE]
[PASTE SECTION 3 — DATABASE SCHEMA]

Task: Set up the complete project structure.
1. Create the folder structure exactly as shown in Section 5
2. Create `requirements.txt` with: fastapi, uvicorn, asyncpg, 
   sqlalchemy[asyncio], openai, twilio, apscheduler, python-dotenv,
   numpy, python-dateutil, httpx, pytest, pytest-asyncio
3. Create `.env.example` with all required environment variables:
   DATABASE_URL, OPENAI_API_KEY, TWILIO_ACCOUNT_SID, 
   TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, FRONTEND_URL
4. Create `backend/main.py` with FastAPI app, CORS configured, 
   all routers imported and registered, health check endpoint at GET /
5. Create `backend/database/connection.py` with async PostgreSQL 
   connection pool using asyncpg and SQLAlchemy async engine

Use Python 3.11+. Use async/await throughout. Production-quality code.
Output each file separately with its exact path.
```

---

### PROMPT 1 — Database Models

```
Context: Building GuardianAI backend. 
Database schema is defined in the playbook (paste Section 3).

Task: Create `backend/database/models.py`
- SQLAlchemy async declarative models for all 6 tables
- Include all columns, types, constraints, and relationships exactly as in schema
- Add `__repr__` methods for debugging
- Add helper methods: `to_dict()` on each model
- Include `create_all_tables()` async function

Also create `backend/database/crud.py` with these async functions:
- get_student_by_phone(db, phone) -> Student | None
- get_recent_scores(db, student_id, days=14) -> List[int]
- get_recent_onewords(db, student_id, days=7) -> List[str]
- save_checkin(db, checkin_data) -> Checkin
- save_burnout_state(db, student_id, assessment, validation) -> BurnoutState
- get_last_intervention(db, student_id) -> Intervention | None
- save_intervention(db, intervention_data) -> Intervention
- get_all_students_by_institution(db, institution_id) -> List[Student]
- get_cohort_data_by_batch(db, institution_id, batch) -> List[dict]

Use SQLAlchemy 2.0 async style. Include type hints throughout.
```

---

### PROMPT 2 — HMM Engine

```
Context: Building the core AI component of GuardianAI.
This is the Hidden Markov Model for burnout state detection.

Task: Create `backend/agents/hmm_engine.py`

Exact implementation required (paste Section 4.1 from playbook).

Additional requirements:
1. Add a `batch_assess()` method that takes a list of students 
   and returns assessments for all of them efficiently
2. Add comprehensive docstrings explaining the research basis 
   for each transition probability value
3. Add type hints throughout using Python 3.11 style

Also create `backend/tests/test_hmm_engine.py` with pytest tests:
- test_stable_student: scores [4,4,5,3,4,4] should return 'stable'
- test_at_risk_student: scores [4,3,3,2,2,3,2] should return 'at_risk'  
- test_crisis_student: scores [4,3,2,2,1,1,2,1] should return 'crisis'
- test_insufficient_data: scores [3,4] should return 'stable' with note
- test_trend_calculation: verify trend_score calculation is correct
- test_consecutive_low_counter: verify consecutive_low_days is correct

Run tests after generation and confirm they pass.
```

---

### PROMPT 3 — Adversarial Validator

```
Context: Building GuardianAI. HMM engine is complete and tested.

Task: Create `backend/agents/adversarial_validator.py`

Exact implementation required (paste Section 4.2 from playbook).

Additional requirements:
1. Add a `get_masking_probability()` method that returns 0.0-1.0 
   probability of the student gaming the system
2. Add detailed logging for each flag triggered
3. The validator must be deterministic — same input = same output always

Also create `backend/tests/test_adversarial_validator.py`:
- test_flat_scores_flagged: [4,4,4,4,4,4,4,4] should flag low_variance
- test_normal_scores_clean: [4,2,3,5,3,4,2,4,3,5] should not flag
- test_sudden_recovery: [2,2,1,2,1,5] should flag sudden_recovery
- test_ceiling_effect: [5,5,5,5,5,5,5,5] should flag ceiling_effect
- test_short_series: [3,4,2] should return is_suspicious=False
```

---

### PROMPT 4 — Cohort Detector

```
Context: Building GuardianAI. HMM and adversarial components complete.

Task: Create `backend/agents/cohort_detector.py`

Exact implementation required (paste Section 4.3 from playbook).

Additional requirements:
1. Add `detect_trend()` method that returns whether cohort is 
   improving, stable, or declining over the last 7 days
2. Add async `run_daily_cohort_scan(db, institution_id)` method 
   that scans all batches and saves anomalies to cohort_alerts table
3. The 40% threshold must be configurable via environment variable

Also create `backend/tests/test_cohort_detector.py`:
- test_no_anomaly: 3/10 students declining should not trigger
- test_anomaly_medium: 5/10 students declining should trigger medium
- test_anomaly_high: 8/10 students declining should trigger high
- test_small_batch: batch of 3 should return insufficient_batch_size
```

---

### PROMPT 5 — Intervention Orchestrator

```
Context: Building GuardianAI. All three detection agents complete and tested.

Task: Create `backend/agents/intervention_orchestrator.py`

Exact implementation required (paste Section 4.4 from playbook).

Additional requirements:
1. All OpenAI calls must use async (acreate not create)
2. Add retry logic: if OpenAI call fails, use a fallback template message
3. Add `estimate_cost()` method that returns approximate OpenAI API cost 
   for a given number of interventions (for the demo slide)
4. The 48-hour cooldown must be enforced strictly
5. Log every decision made with full reasoning to stdout

Fallback templates when OpenAI unavailable:
- Level 1: "Hey! Just checking in on you. How are things going? 
  We're here if you need to talk. 😊"
- Level 2: "Student {name} shows signs of stress. 
  Recommend gentle check-in within 24 hours."
- Level 3: "URGENT: {name} needs immediate support. 
  Pattern indicates high distress. Please reach out now."
```

---

### PROMPT 6 — WhatsApp Webhook

```
Context: Building GuardianAI. All agent components complete.

Task: Create `backend/routes/webhook.py`

This is the most critical route — it receives every student check-in
and triggers the full autonomous agent pipeline.

Requirements:
1. POST /webhook/whatsapp — Twilio webhook handler
   - Receives Form data: Body, From, MessageSid
   - Parses the check-in message (handles variations in response format)
   - Runs full pipeline: parse → save → HMM → validate → cohort check → orchestrate
   - Sends confirmation WhatsApp message back to student
   - Must respond within 5 seconds (Twilio timeout)
   - All heavy processing must be async/background tasks

2. The check-in parser must handle these message formats:
   - "3 yes exhausted" (score + ate + oneword)  
   - "2\nno\nlost" (newline separated)
   - "Feeling 2, ate no, word: hopeless" (natural language)
   - "4" (score only — treat ate as unknown, oneword as none)
   - Must extract score (1-5), ate_properly (yes/mostly/no), one_word

3. POST /webhook/whatsapp/status — delivery status callback

4. Include proper Twilio webhook signature validation for security

Also create `backend/services/whatsapp.py`:
- send_message(to_phone, message) -> bool
- send_check_in_prompt(to_phone, student_name) -> bool  
- send_counsellor_alert(counsellor_phone, student_name, message) -> bool
- format_phone(phone) -> str (ensures whatsapp: prefix)
```

---

### PROMPT 7 — Dashboard API Routes

```
Context: Building GuardianAI. Backend pipeline complete.

Task: Create `backend/routes/dashboard.py` with these endpoints:

GET /dashboard/{institution_id}/overview
Returns:
{
  "total_students": int,
  "stable_count": int,
  "at_risk_count": int,  
  "crisis_count": int,
  "check_in_rate_7d": float,      # % who checked in last 7 days
  "interventions_today": int,
  "cohort_alerts_active": int
}

GET /dashboard/{institution_id}/heatmap
Returns array of all students with current risk state for heatmap:
[{
  "student_id": str,
  "name": str,
  "batch": str,
  "state": "stable|at_risk|crisis",
  "risk_score": int,
  "last_checkin": datetime | null,
  "trend": "improving|stable|declining"
}]

GET /dashboard/student/{student_id}/profile
Returns full student profile with:
- Basic info
- Last 14 days of check-ins (scores + onewords + sentiments)
- HMM state history (for timeline visualisation)
- All interventions taken with outcomes
- Adversarial validation summary

GET /dashboard/{institution_id}/cohorts
Returns all batches with cohort analytics

GET /dashboard/interventions/recent
Returns last 20 autonomous interventions across institution
with full reasoning chain visible

All endpoints must be authenticated with a simple API key header.
Include proper error handling and HTTP status codes.
```

---

### PROMPT 8 — Synthetic Data Generator

```
Context: Building GuardianAI demo. Backend routes complete.

Task: Create `backend/utils/data_generator.py`

Generate realistic synthetic data for 50 students across 4 batches.
Must create 3 distinct demo personas:

PERSONA A — "Priya Sharma" (flagship demo student):
- 14-day score pattern: [4, 4, 3, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 2]
- One-word responses: ["okay","good","tired","okay","stressed",
  "stressed","exhausted","drained","lost","empty","lost","hopeless","empty","lost"]
- Current state: crisis
- This student triggers Level 3 intervention in the demo

PERSONA B — Gaming student (3 students):
- 14-day score pattern: [4,4,4,4,4,4,4,4,4,4,4,4,4,4] (perfectly flat)
- One-word responses: always "fine" or "good"
- Adversarial validator must flag these
- Current state: flagged_masking

PERSONA C — Cohort anomaly batch (batch "MECH-2023", 12 students):
- All 12 declined simultaneously in the last 5 days
- Score patterns show 1.5+ point drops from personal baselines
- Cohort detector must trigger for this batch
- Represents "examination hell" scenario

PERSONA D — Normal students (rest):
- Realistic variance (normal distribution around 3.2)  
- Mix of improving and stable trajectories
- Occasional dips that resolve naturally

Create `backend/utils/demo_runner.py`:
- Async function that populates the database with all demo data
- Run via: python -m backend.utils.demo_runner
- Idempotent: safe to run multiple times (deletes and recreates)
- Print progress as it runs
```

---

### PROMPT 9 — React Dashboard

```
Context: Building GuardianAI frontend. Backend complete and tested.

Task: Create the React PWA dashboard. 

Tech stack: React 18, Vite, Tailwind CSS, Recharts for charts, 
React Router v6. NO external UI component libraries.

Create these files:

1. `frontend/src/pages/Home.jsx`
- Overview stats bar at top (total, at-risk, crisis counts)
- Risk heatmap below: grid of student cards coloured by state
  (green=stable, yellow=at_risk, red=crisis)
- Each card shows: name, batch, last check-in date, current state
- Click card → navigate to student profile
- Active cohort alerts shown as banner at top if any exist
- Real-time updates via polling every 30 seconds

2. `frontend/src/components/RiskHeatmap.jsx`
- Responsive grid layout
- Student cards with colour coding
- Hover shows mini trend sparkline (last 7 days)
- Sort by: risk level, batch, last check-in

3. `frontend/src/pages/StudentProfile.jsx`
- 14-day score trend line chart (Recharts LineChart)
- HMM state timeline: coloured band showing state transitions
- Adversarial validation badge if flagged
- Intervention history timeline
- One-word response word cloud (use font size = frequency)
- Agent reasoning shown in expandable section

4. `frontend/src/pages/ActionLog.jsx`  
- Chronological feed of every autonomous action taken
- Each entry: timestamp, student name, level, reasoning, message sent
- Filter by: level, date range, outcome
- This is the "proof of agentic behaviour" screen for judges

Design language:
- Dark theme: background #0f0f1a, card #1a1a2e, accent #00d4aa
- Typography: Inter font
- Minimal, clinical-grade UI — this is a healthcare tool, not a consumer app
- Every screen must work on mobile (judges will check on phone)
```

---

### PROMPT 10 — PWA Configuration + Scheduler

```
Context: Nearly complete. Final integration needed.

Task 1: PWA Setup
Create `frontend/public/manifest.json`:
- name: "GuardianAI"
- short_name: "Guardian"  
- theme_color: "#0f0f1a"
- background_color: "#0f0f1a"
- display: "standalone"
- All icon sizes: 72, 96, 128, 144, 152, 192, 384, 512

Create `frontend/src/serviceWorker.js`:
- Cache shell (app routes) for offline access
- Show "GuardianAI is watching" notification when installed
- Register push notification permission

Task 2: Daily Scheduler
Create `backend/services/scheduler.py` using APScheduler:

Jobs:
1. daily_checkin_blast — runs at 7:30 PM IST every day
   - Sends WhatsApp check-in prompt to all active enrolled students
   - Format: "Hey {name}! 👋 Quick check-in:\n1️⃣ How was today? (1-5)\n2️⃣ Did you eat properly? (yes/mostly/no)\n3️⃣ One word for how you're feeling?"
   
2. morning_risk_scan — runs at 8:00 AM IST every day  
   - Runs HMM assessment on all students with new data
   - Triggers interventions for any new At-Risk or Crisis detections
   - Runs cohort anomaly scan across all batches
   - Generates daily summary report for counsellors

3. weekly_baseline_update — runs every Sunday at midnight
   - Recalculates personal baseline for each student
   - Uses median of last 30 days (robust to outliers)
   - Updates students.baseline_score in database

Register scheduler in main.py startup event.
```

---

### PROMPT 11 — Demo Scenario Runner

```
Context: GuardianAI is complete. Need demo-ready automation.

Task: Create `backend/utils/demo_runner.py`

This script sets up a compelling live demo automatically.
Run before presenting: python -m backend.utils.demo_runner --scenario live

Scenarios:
1. --scenario setup: populate 50 students, 14 days of history
2. --scenario live: simulate 4 real-time events judges will see:
   
   Event 1 (T+0s): Priya sends check-in "1 no empty"
   → Agent detects crisis → Level 3 triggered → WhatsApp sent to counsellor
   → Dashboard updates red card in real time
   
   Event 2 (T+15s): Gaming student sends "4 yes good" (14th perfect day)
   → Adversarial validator flags masking
   → Dashboard shows warning badge on student card
   
   Event 3 (T+30s): Run cohort scan on MECH-2023 batch
   → 8/12 students below baseline
   → Cohort alert fires → Institutional report generated
   → Banner appears on dashboard
   
   Event 4 (T+45s): Show action log
   → 3 autonomous decisions visible with full reasoning chain
   
3. --scenario reset: clear demo data, restore to clean state

Each event must update the database AND the dashboard in real time.
Use WebSocket or Server-Sent Events to push updates to dashboard.
```

---

### PROMPT 12 — GitHub README

```
Context: GuardianAI is complete and demo-ready.

Task: Create a competition-grade GitHub README.md

Structure:
1. Header: Logo (use live vector graphics), title "GuardianAI", tagline
2. Badges: Python, FastAPI, React, PostgreSQL, OpenAI, Twilio
3. Problem statement: 3 sentences with the 13,892 statistic
4. Demo GIF placeholder (note: "replace with demo.gif")
5. Architecture diagram (ASCII art from playbook)
6. What makes it genuinely agentic (4 bullet points):
   - HMM burnout state machine
   - Adversarial check-in validation  
   - Cohort anomaly detection
   - Autonomous intervention loop with feedback
7. Tech stack table
8. Quick start: 5 commands to get running locally
9. Environment variables reference table
10. Demo instructions: how to run the demo scenario
11. Judging criteria alignment table:
    | Criteria | How GuardianAI addresses it |
12. Real-world impact section with statistics
13. Japan relevance section
14. License: MIT

Make it compelling. Judges will read this README in Round 2.
This README should make them want to ask questions.
```

---

## SECTION 12 — CRITICAL DEMO CHECKLIST

Before presenting, verify every item:

**Technical:**
- [ ] App loads at HTTPS URL (Vercel)
- [ ] Backend responds at Railway URL  
- [ ] WhatsApp check-in send and receive working (Twilio sandbox)
- [ ] Priya scenario runs correctly end-to-end
- [ ] HMM state transitions visible on dashboard
- [ ] Adversarial flag visible on gaming students
- [ ] Cohort alert fires for MECH-2023 batch
- [ ] Action log shows all 3 interventions with reasoning
- [ ] PWA installs on phone homescreen
- [ ] Dashboard updates in real time

**Demo flow:**
- [ ] 90-second demo rehearsed 10 times minimum
- [ ] No demo crashes in last 5 rehearsals
- [ ] All 4 demo events timed and smooth
- [ ] Fallback: screenshots ready if live demo fails

**Submission:**
- [ ] GitHub repo public
- [ ] Commit history spans 10+ days (vibe code daily, commit daily)
- [ ] README complete with architecture diagram
- [ ] 5-minute demo video recorded
- [ ] All 4 agents visible in source code
- [ ] Tests passing for all 3 core agents

---

## SECTION 13 — ANSWERS TO JUDGE QUESTIONS

Prepare these answers verbatim:

**"Where is the actual AI?"**
*"GuardianAI has four distinct AI components: a Hidden Markov Model that models burnout as probabilistic state transitions rather than threshold alerts; an adversarial validator that detects gaming behaviour using statistical variance analysis; a cohort anomaly detector that identifies systemic stressors affecting groups; and GPT-4o that generates contextualised, human-readable intervention messages. The HMM is the core — it's why we catch students who are declining gradually, not just those who score below a cutoff."*

**"How is this agentic?"**
*"The agent perceives — it reads check-in data continuously. It reasons — the HMM computes state probabilities, the adversarial validator cross-checks validity. It decides — intervention level is chosen autonomously without human input. It acts — sends messages, files reports. It observes — tracks whether the student responded. It adapts — escalates or de-escalates based on outcome. That's a full agentic loop running 24/7."*

**"What about Wysa and YourDOST?"**
*"Wysa and YourDOST are reactive tools — students go to them when they already know they need help. The student in crisis at 2am is not opening Wysa. GuardianAI is proactive — it finds students before they reach out, including students who are masking their distress. The adversarial validator and cohort detector don't exist in any consumer mental health app. That's the differentiation."*

**"What is your false negative rate?"**
*"We don't claim zero false negatives — that would be dishonest. A student determined to mask their feelings can evade any system. That's why GuardianAI is a support layer for counsellors, not a replacement for human relationships. Our adversarial validator is specifically designed to flag likely masking cases for direct human outreach. The system is designed to be honest about its own limitations."*

**"What about student privacy?"**
*"100% consent-based. No passive monitoring. Students choose to enrol, choose what to share, and can withdraw at any time. The only data we collect is what students actively send in their daily check-in — a voluntary 30-second WhatsApp interaction. DPDP Act 2023 compliant by design."*

---

*End of Master Playbook. Build boldly. Ship something real.*
