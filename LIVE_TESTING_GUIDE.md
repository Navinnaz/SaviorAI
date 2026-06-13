# GuardianAI - Complete Live Testing Guide

## 🚀 Real-Time Workflow Testing Checklist

---

## PHASE 1: System Startup (5 minutes)

### Step 1: Start Backend
```bash
# Terminal 1
cd c:\Users\g_and\SaviorAI
.\venv\Scripts\activate
python backend\main.py
```

**✅ Check**:
- [ ] `✅ Database initialized: railway`
- [ ] `✅ GuardianAI database connection pool initialized`
- [ ] `✅ GuardianAI Scheduler started with 3 jobs`
- [ ] `INFO: Application startup complete`
- [ ] Server running on `http://127.0.0.1:8000`

### Step 2: Start Frontend
```bash
# Terminal 2 (new terminal)
cd c:\Users\g_and\SaviorAI\frontend
npm run dev
```

**✅ Check**:
- [ ] `VITE ready`
- [ ] `Local: http://localhost:5173`
- [ ] No errors in console

### Step 3: Populate Demo Data (if needed)
```bash
# Terminal 3 (if database is empty)
cd c:\Users\g_and\SaviorAI
.\venv\Scripts\activate
python -m backend.utils.demo_runner
```

**✅ Check**:
- [ ] `Created 50 students`
- [ ] `Created 700 check-ins`
- [ ] `Created 4 interventions`
- [ ] `✅ Demo data populated successfully`

---

## PHASE 2: Dashboard Testing (10 minutes)

### Test 2.1: Homepage Dashboard
**URL**: http://localhost:5173

**✅ Check**:
- [ ] Page loads without errors
- [ ] Overview stats visible:
  - Total Students: 50
  - Stable: ~34
  - At-Risk: ~12
  - Crisis: ~4
- [ ] Risk heatmap shows student cards
- [ ] Student cards color-coded:
  - 🟢 Green = Stable
  - 🟡 Yellow = At-Risk
  - 🔴 Red = Crisis
- [ ] Polling indicator (updates every 30s)
- [ ] No console errors (F12)

**Action**: Wait 30 seconds
**✅ Check**: Stats update automatically

### Test 2.2: Student Profile View
**Action**: Click "Priya Sharma" (crisis student - red card)

**✅ Check**:
- [ ] Profile page loads
- [ ] Student info displayed:
  - Name: Priya Sharma
  - Batch: CSE-2022
  - State: Crisis (red badge)
- [ ] 14-day score chart visible (Recharts line chart)
- [ ] Score trend shows decline (4 → 1)
- [ ] HMM state timeline shows color bands
- [ ] One-word responses visible (hopeless, empty, lost, etc.)
- [ ] Intervention history shown (if any)
- [ ] "Back" button works

### Test 2.3: Action Log
**Action**: Click "Action Log" in navigation

**✅ Check**:
- [ ] Intervention entries visible
- [ ] Each entry shows:
  - Timestamp
  - Student name
  - Level (1, 2, or 3)
  - Reasoning
  - Message preview
- [ ] Filter by level works
- [ ] Chronological order (newest first)
- [ ] Shows autonomous actions

### Test 2.4: PWA Features
**Action**: Desktop - Click install icon in address bar

**✅ Check**:
- [ ] Install prompt appears
- [ ] App installs as standalone
- [ ] Opens in new window (no browser chrome)
- [ ] Notification: "GuardianAI is watching"
- [ ] Works offline (enable airplane mode, refresh)

**Action**: Mobile - Add to home screen

**✅ Check**:
- [ ] Icon appears on home screen
- [ ] Opens fullscreen
- [ ] Dark theme applied
- [ ] Touch-optimized

---

## PHASE 3: API Testing (10 minutes)

### Test 3.1: Health Check
**Method**: Browser or curl

```bash
# Browser: http://localhost:8000
# Or curl:
curl http://localhost:8000/health
```

**✅ Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "agent_core": "ready",
  "hmm_engine": "loaded",
  "adversarial_validator": "loaded",
  "cohort_detector": "loaded",
  "intervention_orchestrator": "ready"
}
```

### Test 3.2: Dashboard API - Overview
```bash
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/747f60be-c964-448f-879c-04291df5941d/overview
```

**✅ Check**:
- [ ] Returns JSON with stats
- [ ] `total_students`: 50
- [ ] `stable_count`, `at_risk_count`, `crisis_count` present
- [ ] `check_in_rate_7d`: percentage
- [ ] Status 200

### Test 3.3: Dashboard API - Heatmap
```bash
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/747f60be-c964-448f-879c-04291df5941d/heatmap
```

**✅ Check**:
- [ ] Returns array of 50 students
- [ ] Each has: `student_id`, `name`, `batch`, `state`, `risk_score`
- [ ] States: "stable", "at_risk", or "crisis"
- [ ] Status 200

### Test 3.4: Dashboard API - Student Profile
```bash
# Get a student ID from heatmap response, then:
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/student/{STUDENT_ID}/profile
```

**✅ Check**:
- [ ] Student details returned
- [ ] `recent_checkins` array (14 days)
- [ ] `state_history` array
- [ ] `interventions` array
- [ ] Status 200

### Test 3.5: Dashboard API - Authentication
```bash
# Test without API key:
curl http://localhost:8000/api/dashboard/747f60be-c964-448f-879c-04291df5941d/overview
```

**✅ Check**:
- [ ] Status 401 Unauthorized
- [ ] Error message about missing API key

---

## PHASE 4: WhatsApp Webhook Testing (15 minutes)

### Prerequisites:
- [ ] Twilio account configured
- [ ] WhatsApp sandbox active
- [ ] ngrok running: `ngrok http 8000`
- [ ] Webhook URL set in Twilio: `https://YOUR-NGROK.ngrok-free.app/api/webhook/whatsapp`

### Test 4.1: Send Check-in (Valid Format)
**Action**: Send WhatsApp message to Twilio number

**Message 1**: Simple format
```
3 yes tired
```

**✅ Check Backend Logs**:
- [ ] `Received WhatsApp webhook`
- [ ] `Parsed: score=3, eating=yes, oneword=tired`
- [ ] `Student found: {name}`
- [ ] `Check-in saved`
- [ ] `HMM assessment complete: state={state}`
- [ ] `Adversarial validation: suspicious={true/false}`
- [ ] Response time < 500ms

**✅ Check WhatsApp**:
- [ ] Confirmation message received:
  - "Got it! Score: 3/5, Eating: yes, Feeling: tired"

### Test 4.2: Send Check-in (Natural Language)
**Message 2**: Natural format
```
Hi! Today was okay, I'd say 4 out of 5. 
I ate properly - yes. 
One word? Productive.
```

**✅ Check Backend Logs**:
- [ ] GPT-4o parsing triggered
- [ ] Extracted: score=4, eating=yes, oneword=productive
- [ ] Check-in saved
- [ ] Confirmation sent

### Test 4.3: Send Check-in (Crisis Trigger)
**Message 3**: Crisis scenario
```
1 no hopeless
```

**✅ Check Backend Logs**:
- [ ] Check-in saved
- [ ] HMM assessment: `state=crisis`
- [ ] Sentiment: `concerning`
- [ ] Intervention triggered (if not in cooldown)
- [ ] Level 3 (emergency) selected
- [ ] OpenAI message generation
- [ ] WhatsApp alert sent to counsellor

**✅ Check Dashboard**:
- [ ] Refresh dashboard
- [ ] Student's card now red (crisis)
- [ ] New intervention in Action Log

### Test 4.4: Gaming Detection
**Action**: Send same score 8 times in a row

**Messages**:
```
4 yes fine
4 yes fine
4 yes fine
4 yes fine
4 yes fine
4 yes fine
4 yes fine
4 yes fine
```

**✅ Check Backend Logs**:
- [ ] All check-ins saved
- [ ] Adversarial validator flags:
  - `LOW VARIANCE FLAG`
  - `PERFECT STREAK FLAG`
- [ ] `is_suspicious: true`
- [ ] Masking alert generated

**✅ Check Dashboard**:
- [ ] Student flagged as "flagged_masking"
- [ ] Badge visible on profile

---

## PHASE 5: Scheduler Testing (20 minutes)

### Test 5.1: Immediate Scheduler Test
**Action**: Modify `scheduler.py` temporarily for testing

**Edit** (Line 477 in `start_scheduler()`):
```python
# Change from cron to interval for testing:
scheduler.add_job(
    daily_checkin_blast,
    trigger="interval",
    minutes=2,  # Run every 2 minutes
    id="daily_checkin_blast",
    replace_existing=True
)
```

**Action**: Restart backend

**✅ Check Logs** (wait 2 minutes):
- [ ] `🚀 Starting daily check-in blast...`
- [ ] `✅ Daily check-in blast complete: X/50 sent`
- [ ] WhatsApp messages sent (check Twilio logs)

### Test 5.2: Morning Risk Scan
**Edit** (modify to run every 3 minutes):
```python
scheduler.add_job(
    morning_risk_scan,
    trigger="interval",
    minutes=3,
    id="morning_risk_scan",
    replace_existing=True
)
```

**Action**: Restart backend, wait 3 minutes

**✅ Check Logs**:
- [ ] `🔍 Starting morning risk scan...`
- [ ] `Students Assessed: X/50`
- [ ] `New At-Risk: X`
- [ ] `New Crisis: X`
- [ ] `Cohort Alerts: X`
- [ ] Summary printed
- [ ] `✅ Morning risk scan complete`

### Test 5.3: Baseline Update
**Edit** (modify to run every 5 minutes):
```python
scheduler.add_job(
    weekly_baseline_update,
    trigger="interval",
    minutes=5,
    id="weekly_baseline_update",
    replace_existing=True
)
```

**Action**: Restart backend, wait 5 minutes

**✅ Check Logs**:
- [ ] `📈 Starting weekly baseline update...`
- [ ] `Updated {name}: {old} → {new}`
- [ ] `✅ Weekly baseline update complete: X/50 updated`

**IMPORTANT**: Revert scheduler back to original cron times before demo!

---

## PHASE 6: Cohort Detection Testing (10 minutes)

### Test 6.1: Create Cohort Anomaly
**Action**: Manually trigger cohort scan

```bash
# Create test script:
python
>>> from backend.agents.cohort_detector import CohortAnomalyDetector
>>> detector = CohortAnomalyDetector()
>>> 
>>> # Simulate exam hell scenario
>>> batch_data = [
...     {"student_id": f"s{i}", "name": f"Student {i}", 
...      "recent_avg": 2.0, "baseline": 3.5}
...     for i in range(12)
... ]
>>> 
>>> result = detector.detect(batch_data)
>>> print(result)
```

**✅ Check**:
- [ ] `anomaly_detected: true`
- [ ] `affected_count: 12`
- [ ] `severity: high`
- [ ] Institutional action recommended

### Test 6.2: Check Dashboard
**Action**: Refresh dashboard after cohort alert

**✅ Check**:
- [ ] Cohort alert banner visible at top
- [ ] Shows batch name (e.g., "MECH-2023")
- [ ] Shows severity and affected count
- [ ] Alert is dismissible

---

## PHASE 7: Full End-to-End Flow (15 minutes)

### Scenario: New Crisis Student

**Step 1**: Send declining check-ins
```
Day 1: 4 yes good
Day 2: 3 yes tired
Day 3: 3 mostly stressed
Day 4: 2 no exhausted
Day 5: 2 no drained
Day 6: 1 no empty
Day 7: 1 no hopeless
```

**Step 2**: Watch Pipeline Execute
**✅ Check Backend Logs**:
- [ ] Each check-in processed
- [ ] HMM state evolves: stable → at_risk → crisis
- [ ] Adversarial validation runs each time
- [ ] Sentiment gets more concerning
- [ ] Intervention triggered on Day 6 or 7

**Step 3**: Verify Dashboard
**✅ Check Frontend**:
- [ ] Student card turns yellow (at-risk) around Day 4
- [ ] Student card turns red (crisis) by Day 7
- [ ] Score chart shows clear downward trend
- [ ] State timeline shows color progression
- [ ] One-word cloud shows concerning words larger

**Step 4**: Verify Intervention
**✅ Check Action Log**:
- [ ] New entry appears
- [ ] Level 3 (Emergency)
- [ ] Student name: {your test student}
- [ ] Reasoning explains decision
- [ ] Message preview visible
- [ ] Timestamp recent

**Step 5**: Verify WhatsApp
**✅ Check Messages**:
- [ ] Student received confirmation
- [ ] Counsellor received alert (if configured)
- [ ] Emergency contact notified (Level 3)

---

## PHASE 8: Error Handling & Edge Cases (10 minutes)

### Test 8.1: Invalid Check-in Format
**Message**: `hello how are you`

**✅ Check**:
- [ ] Backend handles gracefully
- [ ] Error message sent to student
- [ ] No crash

### Test 8.2: OpenAI Failure Simulation
**Action**: Set invalid API key temporarily in `.env`

**Send**: `1 no hopeless`

**✅ Check**:
- [ ] Intervention triggered
- [ ] OpenAI call fails
- [ ] Fallback template used
- [ ] Message still sent
- [ ] No system crash

### Test 8.3: Database Connection Loss
**Action**: Stop Railway database temporarily

**✅ Check**:
- [ ] Backend handles gracefully
- [ ] Error logged
- [ ] System doesn't crash
- [ ] Reconnects when DB back

### Test 8.4: Rate Limiting
**Action**: Send 20 check-ins rapidly

**✅ Check**:
- [ ] All processed (or queued)
- [ ] No crashes
- [ ] Appropriate cooldowns enforced

---

## PHASE 9: Performance Testing (5 minutes)

### Test 9.1: Dashboard Load Time
**Action**: Open dashboard, check Network tab (F12)

**✅ Targets**:
- [ ] Initial load < 2 seconds
- [ ] API calls < 500ms each
- [ ] Heatmap renders < 1 second
- [ ] Student profile < 800ms

### Test 9.2: Concurrent Users
**Action**: Open dashboard in 3 different browsers

**✅ Check**:
- [ ] All load correctly
- [ ] All show same data
- [ ] Polling doesn't conflict
- [ ] No performance degradation

### Test 9.3: Memory Leaks
**Action**: Leave dashboard open for 10 minutes

**✅ Check**:
- [ ] Memory usage stable (check Task Manager)
- [ ] No console errors accumulating
- [ ] Polling continues smoothly

---

## PHASE 10: Mobile Testing (5 minutes)

### Test 10.1: Mobile Browser
**Action**: Open http://localhost:5173 on phone (same network)

**✅ Check**:
- [ ] Responsive layout
- [ ] Cards stack vertically
- [ ] Navigation works
- [ ] Charts visible and scrollable
- [ ] Touch targets adequate size

### Test 10.2: PWA on Mobile
**Action**: Add to home screen

**✅ Check**:
- [ ] Installs successfully
- [ ] Fullscreen mode
- [ ] Splash screen shows
- [ ] Notification permission requested
- [ ] Works offline

---

## CHECKLIST SUMMARY

### Critical Tests (Must Pass):
- [x] Backend starts without errors
- [x] Frontend loads dashboard
- [x] Demo data populates
- [x] Dashboard shows 50 students
- [x] Student profile loads
- [x] API endpoints respond
- [x] WhatsApp webhook processes check-in
- [x] Crisis triggers intervention
- [x] OpenAI generates message
- [x] Fallback works if OpenAI fails
- [x] Gaming detection flags suspicious patterns
- [x] Scheduler jobs start
- [x] PWA installs

### Important Tests (Should Pass):
- [ ] 30-second polling works
- [ ] Action log shows interventions
- [ ] Cohort detection works
- [ ] All 3 scheduler jobs run
- [ ] Mobile responsive
- [ ] Performance adequate
- [ ] Error handling graceful

### Nice to Have (Optional):
- [ ] Offline mode works
- [ ] Push notifications work
- [ ] Twilio WhatsApp live
- [ ] Cohort alerts visible
- [ ] Multiple concurrent users

---

## TROUBLESHOOTING

### Backend won't start
- Check `.env` file exists
- Verify DATABASE_URL is correct
- Test: `python -c "from backend.database.connection import init_db; import asyncio; asyncio.run(init_db())"`

### Frontend blank screen
- Check browser console (F12)
- Verify backend is running
- Check API proxy in vite.config.js
- Try hard refresh (Ctrl+Shift+R)

### Dashboard shows 0 students
- Run demo data: `python -m backend.utils.demo_runner`
- Check database connection
- Verify institution ID matches

### WhatsApp not working
- Check Twilio credentials in `.env`
- Verify ngrok running
- Check Twilio webhook URL
- Review Twilio debugger logs

### Scheduler not running
- Check backend logs for "Scheduler started"
- Verify pytz installed: `pip install pytz`
- Check for errors in scheduler.py

---

## DEMO SCRIPT (For Judges)

**Duration**: 5 minutes

1. **Show Dashboard** (1 min)
   - 50 students, color-coded heatmap
   - Stats overview
   - Explain 30-second polling

2. **Click Crisis Student** (1 min)
   - Priya Sharma (red card)
   - Show declining score chart
   - Point out concerning one-words
   - Show HMM state progression

3. **Show Action Log** (1 min)
   - Autonomous interventions
   - Full reasoning visible
   - "No human in loop"

4. **Show Scheduler** (1 min)
   - Backend terminal
   - 3 jobs listed
   - Explain autonomous cycle

5. **Show PWA** (30 sec)
   - Install demo
   - Works offline
   - "Always monitoring"

6. **Wrap Up** (30 sec)
   - "Catches burnout before tragedy"
   - "Fully autonomous 24/7"
   - "Cost: <$2/month for 1000 students"

---

**Ready for Testing!** 🚀

Follow phases 1-10 in order for comprehensive validation.
