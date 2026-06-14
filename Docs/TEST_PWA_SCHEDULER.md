# Testing GuardianAI PWA & Scheduler

## Quick Test Guide for FAR AWAY 2026 Demo

---

## 🚀 START THE SYSTEM

### 1. Activate Virtual Environment
```bash
.\venv\Scripts\activate
```

### 2. Install New Dependencies
```bash
pip install pytz==2024.1
```

### 3. Start Backend (with Scheduler)
```bash
cd backend
python main.py
```

**Expected Output:**
```
✅ Database initialized: railway
✅ GuardianAI database connection pool initialized
✅ GuardianAI Scheduler started with 3 jobs:
  📱 Daily check-in blast: 7:30 PM IST
  🔍 Morning risk scan: 8:00 AM IST
  📈 Weekly baseline update: Sunday midnight IST
INFO:     Application startup complete.
```

### 4. Start Frontend (in new terminal)
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x ready in X ms
➜  Local:   http://localhost:5173/
```

---

## 🧪 TEST PWA FEATURES

### Test 1: Service Worker Registration
1. Open browser console (F12)
2. Go to http://localhost:5173
3. Look for: `✅ GuardianAI Service Worker registered`
4. Check Application tab → Service Workers → should show active worker

### Test 2: Install as PWA
**Desktop (Chrome):**
1. Visit http://localhost:5173
2. Look for install icon in address bar (⊕)
3. Click "Install GuardianAI"
4. App opens in standalone window

**Mobile:**
1. Visit app on phone
2. Browser menu → "Add to Home Screen"
3. Tap app icon → opens fullscreen

### Test 3: Push Notification
1. Install the PWA
2. You should see notification: "GuardianAI is watching"
3. Check browser notification permissions

### Test 4: Offline Mode
1. Install PWA
2. Open DevTools → Network tab
3. Check "Offline" mode
4. Refresh app → should still load (cached)
5. API calls will fail (expected) but UI stays functional

### Test 5: Manifest Loading
1. DevTools → Application tab → Manifest
2. Verify:
   - Name: "GuardianAI"
   - Theme color: #0f0f1a
   - Display: standalone
   - All icon sizes listed (even if missing)

---

## 🤖 TEST SCHEDULER JOBS

### Option A: Wait for Real Scheduled Times
- **7:30 PM IST**: Check backend logs for daily check-in blast
- **8:00 AM IST next day**: Check logs for morning risk scan
- **Sunday midnight**: Check logs for baseline update

### Option B: Test Immediately (Recommended)

#### Modify scheduler.py temporarily:
```python
# In start_scheduler() function, replace:

# JOB 1: Test check-in in 2 minutes
scheduler.add_job(
    daily_checkin_blast,
    trigger="interval",
    minutes=2,
    id="daily_checkin_blast",
    replace_existing=True
)

# JOB 2: Test risk scan in 3 minutes
scheduler.add_job(
    morning_risk_scan,
    trigger="interval",
    minutes=3,
    id="morning_risk_scan",
    replace_existing=True
)

# JOB 3: Test baseline update in 5 minutes
scheduler.add_job(
    weekly_baseline_update,
    trigger="interval",
    minutes=5,
    id="weekly_baseline_update",
    replace_existing=True
)
```

Then restart backend and wait 2-5 minutes to see logs.

#### Expected Logs:

**Check-in Blast:**
```
🚀 Starting daily check-in blast...
✅ Daily check-in blast complete: 50/50 sent
```

**Morning Risk Scan:**
```
🔍 Starting morning risk scan...
📊 GuardianAI Morning Risk Scan
Date: 2026-06-12 08:00
Students Assessed: 48/50
New At-Risk: 2
New Crisis: 1
Cohort Alerts: 1
🚨 CRISIS: Priya Sharma
⚠️  AT RISK: Student A, Student B
👥 COHORT ALERTS: MECH-2023
✅ Morning risk scan complete
```

**Baseline Update:**
```
📈 Starting weekly baseline update...
Updated Priya Sharma: 3.8 → 2.1
Updated Student X: 3.2 → 3.6
✅ Weekly baseline update complete: 12/50 updated
```

---

## 📱 TEST WHATSAPP INTEGRATION

### If Twilio is configured:
After check-in blast runs, verify:
1. Students receive WhatsApp message
2. Check Twilio console for message logs
3. Test format: "Hey {name}! 👋 Quick check-in..."

### If Twilio NOT configured:
Logs will show errors but scheduler continues:
```
Failed to send to Student Name: [Twilio Error]
```

---

## 🎯 DEMO FLOW FOR JUDGES

### 1. Show PWA Installation (30 seconds)
- Open app in browser
- Click install icon
- App opens as standalone application
- Point out notification: "GuardianAI is watching"

### 2. Show Backend Logs (30 seconds)
- Terminal showing scheduler started
- 3 jobs listed with times
- "Fully autonomous system"

### 3. Show Dashboard (1 minute)
- Real-time monitoring (30s polling)
- Risk heatmap with color coding
- Stats: total, at-risk, crisis counts
- Click student → profile with HMM timeline

### 4. Show Scheduler in Action (1 minute)
- If testing with intervals: show live logs
- Explain: "7:30 PM - sends check-ins autonomously"
- Explain: "8 AM - processes responses, triggers interventions"
- Explain: "Sunday - adapts baselines automatically"

### 5. Show Autonomous Intervention (1 minute)
- Open Action Log page
- Show intervention entries with reasoning
- Point out: "No human in the loop - fully autonomous"
- Explain: HMM → Validate → Orchestrate → Act

### 6. Highlight Agentic Features
- ✅ Scheduled autonomous check-ins
- ✅ Automated risk assessment (HMM)
- ✅ Gaming detection (adversarial validation)
- ✅ Cohort anomaly detection
- ✅ Autonomous intervention triggering
- ✅ Self-adapting baselines
- ✅ PWA for 24/7 monitoring

---

## ⚠️ TROUBLESHOOTING

### "Service Worker registration failed"
- Must use localhost or HTTPS
- Check if serviceWorker.js is in public directory
- Try hard refresh (Ctrl+Shift+R)

### "Scheduler started" but no logs
- Jobs scheduled for future times (7:30 PM, 8 AM)
- Use interval trigger for immediate testing
- Check system time vs IST

### "Database connection failed"
- Verify .env has DATABASE_URL
- Check Railway database is running
- Test connection: `python -c "from database.connection import init_db; import asyncio; asyncio.run(init_db())"`

### "WhatsApp messages not sending"
- Check TWILIO_ACCOUNT_SID in .env
- Verify TWILIO_AUTH_TOKEN
- Check TWILIO_WHATSAPP_FROM phone number
- Review Twilio console for errors

### PWA icons not showing
- Icons not generated yet (expected)
- App still installs with default icon
- Generate with: `npx pwa-asset-generator logo.png ./public/icons`

---

## 📋 FINAL CHECKLIST

Before demo:
- [ ] Backend running with scheduler logs visible
- [ ] Frontend running on localhost:5173
- [ ] PWA installed successfully
- [ ] Service worker active in DevTools
- [ ] Dashboard loading with data
- [ ] Risk heatmap showing students
- [ ] Action Log showing interventions
- [ ] Student profile page working
- [ ] Demo data populated (50 students)
- [ ] Priya Sharma showing as crisis student

---

## 🎓 KEY TALKING POINTS

1. **Fully Autonomous**: No human trigger needed - system operates 24/7
2. **Adaptive**: Self-adjusting baselines every week
3. **Intelligent**: HMM + adversarial validation + cohort detection
4. **Proactive**: Catches burnout before crisis (early intervention)
5. **Scalable**: Scheduled jobs handle thousands of students
6. **PWA**: Works offline, installable, push notifications
7. **Real-time**: Dashboard polls every 30 seconds
8. **Transparent**: Every action logged with reasoning (Action Log)

---

**Ready for Demo**: YES ✅  
**Autonomy Level**: MAXIMUM 🤖  
**Impact**: POTENTIALLY LIFE-SAVING 💚
