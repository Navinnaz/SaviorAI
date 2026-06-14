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
