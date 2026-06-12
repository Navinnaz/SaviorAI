# GuardianAI Demo Data System

Complete demo data generation system for presentations and testing.

---

## Quick Start

**Generate demo data (50 students):**
```bash
python -m backend.utils.demo_runner
```

**Custom student count:**
```bash
python -m backend.utils.demo_runner --students 100
```

**View in dashboard:**
```bash
# Get institution ID from output, then:
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/{INSTITUTION_ID}/overview
```

---

## Demo Personas

### 🚨 **Persona A: Priya Sharma** (Crisis - Flagship Demo)
**Profile:**
- Name: Priya Sharma
- Batch: CSE-2022
- Phone: +919876500001
- Baseline: 3.8

**14-Day Pattern:**
```
Scores:   [4, 4, 3, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 2]
OneWords: ["okay","good","tired","okay","stressed","stressed",
           "exhausted","drained","lost","empty","lost",
           "hopeless","empty","lost"]
```

**Current State:**
- Status: **CRISIS**
- HMM Probability: 0.92
- Trend Score: -1.8 (severe decline)
- Consecutive Low Days: 6

**Intervention Triggered:**
- Level 3 (Emergency)
- Recipient: Counsellor
- Action: Immediate outreach required

**Demo Value:**
- Shows clear declining trajectory
- Triggers highest intervention level
- Demonstrates "catches burnout before tragedy" tagline
- Real emotional language progression

---

### 🎮 **Persona B: Gaming Students** (3 students)
**Profile:**
- Names: Randomly generated
- Batches: CSE-2022, ECE-2023, CSE-2023
- Pattern: **Perfectly flat scores**

**14-Day Pattern:**
```
Scores:   [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
OneWords: ["fine", "good", "fine", "good"] (alternating)
```

**Current State:**
- Status: Stable (but flagged)
- Variance Flag: **TRUE** ⚠️
- Statistical impossibility: σ² = 0.00

**Intervention Triggered:**
- Level 1 (Peer Nudge)
- Recipient: Student
- Action: Gentle reminder about honest reporting

**Demo Value:**
- Adversarial validation in action
- Shows system can't be gamed
- Detects "social desirability bias"
- Encourages authentic reporting

---

### 📚 **Persona C: MECH-2023 Cohort** (12 students)
**Profile:**
- Batch: MECH-2023 (all 12 students)
- Baseline: 3.5-4.2 (varies per student)
- Synchronized decline

**Pattern:**
```
Days 1-9:  Normal scores around baseline
Days 10-14: Sudden 1.5-2.5 point drop (examination stress)
```

**Current State:**
- Status: At Risk (cohort flag enabled)
- 100% of batch affected
- Average score drop: 1.8 points
- Timing: Last 5 days

**Intervention Triggered:**
- Cohort Alert (institutional level)
- Likely Cause: Mid-semester examinations
- Recommended Action: Department-level intervention

**Demo Value:**
- Shows cohort detection capability
- Distinguishes individual vs systemic issues
- Triggers institutional recommendations
- Real-world scenario (exam stress)

---

### 👥 **Persona D: Normal Students** (34 students)
**Profile:**
- Batches: CSE-2022, CSE-2023, ECE-2023, CSE-2024
- Baselines: 2.8-4.0 (realistic distribution)
- Mix of trajectories

**Trajectories:**
1. **Improving:** Gradual upward trend (+0.1 per day)
2. **Stable:** Normal variance around baseline (σ² ≈ 0.5)
3. **Dip & Recover:** Temporary dip (days 5-9), then recovery

**Current States:**
- Mostly Stable (70%)
- Some At-Risk (30%)
- No crisis students

**Demo Value:**
- Provides realistic baseline
- Shows system doesn't over-trigger
- Normal variance doesn't flag
- Demonstrates precision

---

## Data Statistics

**Total Generated:**
- 1 Institution (IIT Delhi)
- 50 Students (across 4 batches)
- 700 Check-ins (14 days × 50 students)
- 50 Burnout States (1 per student)
- 4 Interventions (1 crisis + 3 gaming)
- 1 Cohort Alert (MECH-2023)

**Batch Distribution:**
- CSE-2022: ~15 students
- CSE-2023: ~15 students
- ECE-2023: ~8 students
- MECH-2023: 12 students (cohort anomaly)

**Risk Distribution:**
- Stable: ~36 students (72%)
- At-Risk: ~13 students (26%)
- Crisis: 1 student (2%)

---

## Testing Dashboard API

### 1. Get Institution Overview
```bash
INST_ID="747f60be-c964-448f-879c-04291df5941d"  # From demo_runner output

curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/${INST_ID}/overview"
```

**Expected Response:**
```json
{
  "total_students": 50,
  "stable_count": 36,
  "at_risk_count": 13,
  "crisis_count": 1,
  "check_in_rate_7d": 100.0,
  "interventions_today": 4,
  "cohort_alerts_active": 1
}
```

### 2. Get Student Heatmap
```bash
curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/${INST_ID}/heatmap" | jq
```

### 3. Get Priya Sharma Profile
```bash
# Find Priya's ID from heatmap or logs
PRIYA_ID="c2fef1ff-1b62-40b8-9ab6-a1c9b0438d89"

curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/student/${PRIYA_ID}/profile" | jq
```

### 4. Get Cohort Analytics
```bash
curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/${INST_ID}/cohorts" | jq
```

### 5. Get Recent Interventions
```bash
curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/interventions/recent?limit=10" | jq
```

---

## Demo Presentation Flow

### Slide 1: Overview Dashboard
**Show:** Institution overview with KPIs
- 50 students monitored
- 1 crisis student (2%)
- 100% check-in rate
- 4 autonomous interventions

**Key Message:** "Real-time monitoring of entire institution"

### Slide 2: Heatmap Visualization
**Show:** Color-coded student grid
- Red: Priya Sharma (crisis)
- Yellow: MECH-2023 students (at-risk cohort)
- Green: Most students (stable)

**Key Message:** "Instant visual identification of at-risk students"

### Slide 3: Priya Sharma Deep Dive
**Show:** Complete student profile
- 14-day declining trajectory chart
- Concerning language: "hopeless", "empty", "lost"
- Emergency intervention triggered

**Key Message:** "The agent that catches burnout before it becomes a tragedy"

### Slide 4: Adversarial Detection
**Show:** Gaming student profiles
- Perfectly flat scores (impossible)
- System flagged automatically
- Gentle intervention sent

**Key Message:** "Can't be gamed - encourages authentic reporting"

### Slide 5: Cohort Anomaly
**Show:** MECH-2023 batch alert
- 100% of batch declined simultaneously
- Examination stress detected
- Institutional action recommended

**Key Message:** "Distinguishes individual vs systemic issues"

### Slide 6: Intervention Audit Trail
**Show:** Recent interventions with reasoning
- Full transparency
- AI reasoning visible
- Multiple intervention levels

**Key Message:** "Autonomous but explainable - human oversight enabled"

---

## Regenerating Demo Data

**Safe to run multiple times:**
```bash
python -m backend.utils.demo_runner
```

The script is **idempotent** - it:
1. Clears existing demo data (only IIT Delhi)
2. Regenerates fresh data
3. Preserves any other institutions

**Warning:** This will delete:
- All students from IIT Delhi
- All their check-ins
- All burnout states
- All interventions
- All cohort alerts

---

## Customization

### Change Student Count
```bash
python -m backend.utils.demo_runner --students 100
```

### Modify Personas
Edit `backend/utils/data_generator.py`:
- Adjust Priya's score pattern
- Add more gaming students
- Change cohort anomaly batch
- Modify normal student distribution

### Add More Institutions
```python
# In data_generator.py
def _generate_institution(self):
    return {
        "name": "Your Institution",
        "type": "university",
        # ...
    }
```

---

## Troubleshooting

### Demo data not showing in dashboard
```bash
# Check if data was created
python -c "from backend.database.connection import AsyncSessionLocal; from backend.database.models import Student; import asyncio; async def check(): async with AsyncSessionLocal() as db: from sqlalchemy import select, func; count = await db.execute(select(func.count(Student.id))); print(f'Students: {count.scalar()}'); asyncio.run(check())"
```

### Reset everything
```bash
# Delete all data and regenerate
python -m backend.utils.demo_runner
```

### Performance issues
```bash
# Reduce student count
python -m backend.utils.demo_runner --students 25
```

---

## Production Notes

**DO NOT run in production!**

This script:
- Deletes data without confirmation
- Generates synthetic data
- Uses hardcoded phone numbers
- Is for demo purposes only

For production:
- Use real data import scripts
- Implement proper backup/restore
- Add confirmation prompts
- Log all changes

---

## File Structure

```
backend/utils/
├── data_generator.py    # Data generation logic
│   ├── DemoDataGenerator class
│   ├── Persona A (crisis)
│   ├── Persona B (gaming)
│   ├── Persona C (cohort)
│   └── Persona D (normal)
│
└── demo_runner.py       # Database population script
    ├── clear_existing_data()
    ├── populate_database()
    └── main()
```

---

Built for **FAR AWAY 2026** - Agentic & Autonomous Systems 🎭
