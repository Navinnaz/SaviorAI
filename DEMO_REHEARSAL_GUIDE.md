# 🎭 SaviorAI Demo Rehearsal Guide

## ✅ FIXES APPLIED

### React Hook Error Fixed
**Problem**: Frontend showed blank screen with "Cannot read properties of null (reading 'useState')"

**Solution**: Added explicit `React` imports to all component files:
- ✅ `frontend/src/App.jsx`
- ✅ `frontend/src/components/RiskHeatmap.jsx`
- ✅ `frontend/src/pages/Home.jsx`
- ✅ `frontend/src/pages/Login.jsx`
- ✅ `frontend/src/pages/StudentProfile.jsx`
- ✅ `frontend/src/pages/ActionLog.jsx`

This resolves the duplicate React copy issue with Vite bundling.

---

## 🚀 HOW TO REHEARSE THE DEMO (4 EVENTS)

### Step 1: Ensure Backend is Running
```bash
# In terminal 1
cd backend
python main.py
```

**Expected**: Backend starts on `http://localhost:8000`

### Step 2: Ensure Frontend is Running
```bash
# In terminal 2
cd frontend
npm run dev
```

**Expected**: Frontend starts on `http://localhost:3000` or `http://localhost:3001`

### Step 3: Reset & Setup Demo Data
```bash
# In terminal 3
cd backend/utils
python demo_runner.py --reset
python demo_runner.py --setup
```

**Expected**:
- ✅ Database cleared (preserving institution)
- ✅ 50 demo students created
- ✅ Priya Kumar shows as **GREEN/STABLE** on dashboard
- ✅ 14 days of stable check-in history for Priya

### Step 4: Login to Dashboard
1. Open browser to `http://localhost:3000` (or 3001)
2. Click **"🎭 Demo Login (IIT Delhi)"** button
3. Dashboard loads showing 50 students

**Verify**:
- Priya Kumar card is **GREEN** (stable state)
- Other students distributed across green/yellow/red
- Dashboard stats show overview

### Step 5: Run the 4 Events Live Demo
```bash
# In terminal 3
cd backend/utils
python demo_runner.py --live
```

**What Happens** (watch both terminal and dashboard):

#### 🎯 Event 1 (T+0s): Crisis Detection - Priya Kumar
```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                         🚨 EVENT 1: CRISIS DETECTION (PRIYA)                        ║
╚═════════════════════════════════════════════════════════════════════════════════════╝

📱 SIMULATING: Priya sends "1 no terrible" via WhatsApp
   └─→ Actual webhook pipeline: POST /api/webhook
   └─→ HMM engine analyzes: mood_score=1, one_word="terrible"
   └─→ Adversarial validator: genuine distress, NOT gaming
   └─→ State assessment: CRISIS (80%+ risk)
   
🎯 INTERVENTION TRIGGERED:
   ├─ Level 3: Emergency
   ├─ Recipient: 911saviourofstudents@gmail.com
   ├─ Email sent: ✅
   └─ Reasoning: "Consecutive low mood scores (1/5), negative sentiment..."

✅ EVENT 1 COMPLETE - Check dashboard: Priya's card should now be RED
```

**Verify on Dashboard**:
- Refresh page
- Priya Kumar card turns **RED** (crisis state)
- Risk score elevated to 80%+
- Click on Priya's card → see crisis intervention in history

#### ⚠️ Event 2 (T+15s): Gaming Detection
```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                   ⚠️ EVENT 2: GAMING DETECTION (ADVERSARIAL)                        ║
╚═════════════════════════════════════════════════════════════════════════════════════╝

📱 SIMULATING: Gaming student sends "4 yes good" (14th perfect day in a row)
   └─→ Adversarial validator flags: MASKING pattern detected
   └─→ Variance check: 0.0 (suspiciously consistent)
   └─→ Gaming score: 0.85 (high confidence)
   
🎯 ADVERSARIAL ALERT LOGGED:
   └─ Dashboard shows warning badge on student card

✅ EVENT 2 COMPLETE - Gaming behavior flagged
```

**Verify on Dashboard**:
- One student card shows **⚠️ Gaming Detected** badge
- Student profile shows adversarial summary

#### 👥 Event 3 (T+30s): Cohort Anomaly - MECH-2023
```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                  👥 EVENT 3: COHORT ANOMALY (MECH-2023 BATCH)                       ║
╚═════════════════════════════════════════════════════════════════════════════════════╝

🔍 RUNNING: Cohort scan on MECH-2023 batch
   ├─ Batch size: 12 students
   ├─ Students below baseline: 8/12 (66.7%)
   ├─ Threshold: 50%
   └─→ COHORT ALERT TRIGGERED!
   
🎯 INSTITUTIONAL INTERVENTION:
   ├─ Level 4: Institutional Report
   ├─ Alert type: cohort_wide_baseline_drop
   ├─ Report generated with affected student list
   └─ Banner appears on dashboard

✅ EVENT 3 COMPLETE - Batch-level alert active
```

**Verify on Dashboard**:
- Refresh page
- Yellow **Cohort Alert Banner** appears at top
- Shows "MECH-2023 - 8 students affected (66.7%)"
- Overview stats show "1 Active Cohort Alert"

#### 📋 Event 4 (T+45s): Action Log Summary
```
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                       📋 EVENT 4: ACTION LOG SUMMARY                                ║
╚═════════════════════════════════════════════════════════════════════════════════════╝

📊 RECENT AUTONOMOUS DECISIONS:

1. [Level 3] Priya Kumar - Crisis Intervention
   └─ Reasoning: "Consecutive low mood scores, immediate escalation required"
   └─ Action: Emergency email sent to counsellor
   
2. [Level 1] Gaming Student - Adversarial Flag
   └─ Reasoning: "Perfect consistency pattern indicates masking behavior"
   └─ Action: Warning logged, monitoring increased
   
3. [Level 4] MECH-2023 Cohort - Institutional Alert
   └─ Reasoning: "66.7% of batch below baseline, systemic issue detected"
   └─ Action: Report generated for institutional review

✅ EVENT 4 COMPLETE - Full audit trail visible
```

**Verify on Dashboard**:
- Click **"Action Log"** in navigation
- See all 3 interventions listed
- Expand any entry to view full AI reasoning
- Each shows: trigger reason, action taken, message sent, outcome

---

## 📊 WHAT EACH `--` COMMAND DOES

### `python demo_runner.py --reset`
**Purpose**: Clean slate for rehearsal

**What it does**:
- ❌ Deletes all students, check-ins, interventions, state assessments
- ✅ **PRESERVES** institution (UUID: `88353031-000c-4b80-b091-89fe65849734`)
- ✅ Resets database to blank state

**When to use**: Before each rehearsal or when data is corrupted

---

### `python demo_runner.py --setup`
**Purpose**: Create realistic demo dataset

**What it does**:
- ✅ Creates 50 diverse students across 5 batches
- ✅ Generates 14 days of check-in history for each
- ✅ Priya Kumar gets **STABLE** history (scores: 4,4,5,3,4... positive one-words)
- ✅ Other students get mixed histories (some stable, some at-risk, some crisis)
- ✅ Runs HMM engine to assess initial states
- ✅ Creates baseline interventions

**When to use**: After `--reset`, before `--live` or dashboard viewing

---

### `python demo_runner.py --live`
**Purpose**: Execute the 4 autonomous events in sequence

**What it does**:
- ✅ **Event 1**: Injects Priya's crisis check-in through **real webhook pipeline**
  - Actually calls `/api/webhook` endpoint
  - Triggers real HMM engine analysis
  - Fires real intervention orchestrator
  - Sends real email (if SMTP configured)
  
- ✅ **Event 2**: Simulates gaming detection
  - Creates student with perfect 14-day streak
  - Adversarial validator flags masking
  - Logs gaming alert
  
- ✅ **Event 3**: Runs cohort scan
  - Analyzes MECH-2023 batch
  - Detects 66.7% below baseline
  - Triggers institutional alert
  
- ✅ **Event 4**: Summarizes action log
  - Displays all autonomous decisions
  - Shows full reasoning chains
  - Proves transparency

**When to use**: During live demo presentation (after --setup)

---

## ✅ ALL 4 EVENTS ARE FUNCTIONAL

### Status: ✅ All events work with `--reset`, `--setup`, `--live`

**Event 1**: ✅ Fully functional
- Uses real webhook pipeline
- Actual HMM + Intervention pipeline
- Beautiful terminal output
- Sends real email (if configured)

**Event 2**: ✅ Fully functional
- Adversarial validator catches gaming
- Beautiful terminal output
- Shows on dashboard

**Event 3**: ✅ Fully functional
- Cohort detector scans batches
- Beautiful terminal output
- Banner appears on dashboard

**Event 4**: ✅ Fully functional
- Action log shows all interventions
- Beautiful terminal output
- Full reasoning visible in dashboard

---

## 🎬 RECOMMENDED DEMO FLOW

### Before Demo:
1. Run `--reset` and `--setup`
2. Open dashboard and show Priya is GREEN
3. Navigate around to show features

### During Demo:
1. Explain "Now watch AI detect crisis in real-time"
2. Run `--live` in terminal
3. Show terminal output as events happen
4. Refresh dashboard to show changes
5. Navigate to Action Log to show reasoning

### After Demo:
- Answer questions while showing student profiles
- Demonstrate transparency via action log
- Show cohort alert details

---

## 🐛 TROUBLESHOOTING

### Frontend still showing blank screen?
1. Check browser console for errors
2. Hard refresh: `Ctrl+Shift+R` (or `Cmd+Shift+R` on Mac)
3. Clear browser cache
4. Restart frontend: `npm run dev` again

### Backend not responding?
1. Check backend is running: `http://localhost:8000/docs`
2. Check `.env` file has `DATABASE_URL`
3. Restart backend: `python main.py`

### Email not sending?
1. Check `.env` has `SMTP_*` settings
2. Set `DEMO_MODE=true` to see emails in terminal instead
3. Gmail requires app password, not regular password

### Database errors?
1. Run `python nuclear_reset.py` for complete wipe
2. Then run `--setup` again

---

## 📝 NOTES FOR REHEARSAL

1. **Timing**: Each `--live` event has 3-second delays between them
2. **Dashboard Refresh**: After `--live`, refresh browser to see changes
3. **Email**: Set `DEMO_MODE=true` in `.env` to print emails to terminal instead of sending
4. **Multiple Runs**: You can run `--live` multiple times (creates duplicate interventions)
5. **Clean Slate**: Always run `--reset` + `--setup` before important rehearsals

---

## ✅ CHECKLIST BEFORE DEMO

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000/3001
- [ ] Dashboard loads without errors
- [ ] Can login with demo button
- [ ] Priya Kumar visible and GREEN
- [ ] Run `--live` successfully
- [ ] Priya turns RED after Event 1
- [ ] Cohort alert banner appears
- [ ] Action Log shows 3+ interventions
- [ ] Can navigate to student profiles

---

**Ready to rehearse!** 🎭

Run through the flow 2-3 times to get comfortable with timing and narration.
