# SaviorAI Demo Quick Commands

## 🎬 Complete Demo Workflow

### Before Demo
```bash
# 1. Reset database
python -m backend.utils.demo_runner --scenario reset
# Type: yes

# 2. Setup demo data (Priya STABLE + 50 students)
python -m backend.utils.demo_runner --scenario setup

# 3. Start backend (Terminal 1)
python -m backend.main

# 4. Start frontend (Terminal 2)
cd frontend
npm run dev
```

### During Demo
```bash
# Open browser
http://localhost:5173/

# Click "Demo Login" button

# Run live demo (Terminal 3)
python -m backend.utils.demo_runner --scenario live
```

### After Demo (to reset for next run)
```bash
# Ctrl+C both services
# Run reset again
python -m backend.utils.demo_runner --scenario reset
```

---

## 📧 Email Setup (One-Time)

Add to `.env`:
```bash
DEMO_MODE=true
DEMO_COUNSELLOR_EMAIL=your.email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.gmail@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

Get Gmail app password:
1. https://myaccount.google.com/apppasswords
2. Enable 2FA first
3. Create app password for "Mail"
4. Copy 16-character password (no spaces)

---

## 🎯 What to Show Judges

1. **Dashboard (before live):** Priya is GREEN at bottom
2. **Run --live command:** Show terminal output
3. **Event 1 output:** Crisis detection with AI reasoning
4. **Refresh dashboard:** Priya turns RED
5. **Event 2 output:** Gaming detection with flags
6. **Event 3 output:** Cohort alert with recommendations
7. **Event 4 output:** Action log summary
8. **Open email:** Show beautiful emergency alert
9. **Open action log:** Show complete audit trail

---

## ⚡ Quick Troubleshooting

**Problem:** No students on dashboard
**Fix:** Run `python -m backend.utils.demo_runner --scenario setup`

**Problem:** Priya already RED
**Fix:** Run `--reset` then `--setup` again

**Problem:** Email not sending
**Fix:** Check `.env` has all SMTP settings, verify Gmail app password

**Problem:** Dashboard won't load
**Fix:** Check institutionId in localStorage (should be `88353031-000c-4b80-b091-89fe65849734`)

---

## 📊 Expected Results

**After --setup:**
- 50 students created
- Priya Sharma is GREEN (stable)
- Risk score: 20-35
- No interventions logged

**After --live:**
- Priya turns RED (crisis)
- Risk score: 90%+
- 1 gaming student has ⚠️ badge
- Cohort banner appears
- 3+ interventions in action log
- Email received

---

## 🔄 Repeatable Cycle

```bash
reset → setup → start services → live demo
  ↑                                    ↓
  └────────────────────────────────────┘
        (Repeat for multiple demos)
```

**Time per cycle:**
- Reset: 5 seconds
- Setup: 10 seconds
- Start services: 5 seconds
- Live demo: 15 seconds
- **Total: 35 seconds to reset and re-run**

---

## 💡 Demo Day Checklist

**Before judges arrive:**
- [ ] .env configured with email settings
- [ ] Database reset and setup completed
- [ ] Both services running
- [ ] Dashboard showing Priya as GREEN
- [ ] Email inbox open in browser tab
- [ ] Terminal ready for --live command

**During presentation:**
- [ ] Explain the problem (mental health monitoring)
- [ ] Show stable dashboard
- [ ] Run --live command
- [ ] Point to each terminal output
- [ ] Show dashboard updates
- [ ] Show email alert
- [ ] Show action log
- [ ] Emphasize: autonomous, explainable, real-time

**After demo:**
- [ ] Answer questions
- [ ] Show code if asked
- [ ] Explain multi-agent architecture
- [ ] Discuss production deployment

---

**Demo UUID (permanent):** `88353031-000c-4b80-b091-89fe65849734`

**Dashboard:** http://localhost:5173/  
**Action Log:** http://localhost:5173/action-log

**Demo ready:** ✅ All 4 events functional with beautiful output
