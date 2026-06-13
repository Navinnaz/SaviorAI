# 🎯 START HERE - GuardianAI Demo

## All Fixed & Ready to Present! ✅

### What Was Fixed:
1. ✅ **Risk Score Display** - Crisis states now show 85-95% (was 0%)
2. ✅ **Heatmap Sorting** - Students sorted by risk, highest first
3. ✅ **Timeline Percentages** - Shows meaningful percentages (was 92%, 0%, 0%)

---

## Quick Start (5 Minutes)

### Step 1: Start Backend
```powershell
.\venv\Scripts\activate
python -m backend.main
```
**Wait for**: `Uvicorn running on http://0.0.0.0:8000`

### Step 2: Start Frontend (New Terminal)
```powershell
cd frontend
npm run dev
```
**Wait for**: `Local: http://localhost:3000`

### Step 3: Reset & Setup Demo Data (New Terminal)
```powershell
.\venv\Scripts\activate
.\run_demo.bat --scenario reset
.\run_demo.bat --scenario setup
```
**Wait for**: Institution ID printed (e.g., `88353031-000c-4b80-b091-89fe65849734`)

### Step 4: Update Browser
1. Open http://localhost:3000
2. Open console (F12)
3. Run:
```javascript
localStorage.setItem('institutionId', '88353031-000c-4b80-b091-89fe65849734')
```
4. Refresh (F5)

### Step 5: Verify
- ✅ Should see 50 students
- ✅ Priya Sharma at top with **85-95% risk score** (RED card)
- ✅ Cards sorted by risk level
- ✅ Click Priya → timeline shows "CRISIS (92% risk)"

---

## Demo Flow

### Show Dashboard (2 min)
- Overview of 50 students
- Color coding (red/yellow/green)
- Click Priya Sharma → deep dive

### Show Crisis Student (3 min)
- 14-day mood trend (declining)
- Mental health timeline (stable → at-risk → crisis)
- Intervention history (autonomous actions)
- Emotional keywords (empty, hopeless, tired)

### Run Live Simulation (3 min)
```powershell
.\run_demo.bat --scenario live
```
- Watch logs process crisis check-in
- Refresh dashboard → see updates
- Show intervention triggered

### WhatsApp Demo (OPTIONAL - 3 min)
**Setup:**
```powershell
python add_my_number.py
.\ngrok http 8000
# Update Twilio webhook
```

**Live:**
- Send WhatsApp: `1 no empty`
- Show webhook hit
- Show backend processing
- Refresh dashboard → your card appears

---

## If Something Breaks

### Dashboard Shows 404:
```javascript
localStorage.setItem('institutionId', '88353031-000c-4b80-b091-89fe65849734')
location.reload()
```

### Risk Scores Still 0%:
```powershell
# Restart backend
python -m backend.main
```

### Demo Runner Errors:
```powershell
# Reset first
.\run_demo.bat --scenario reset
# Then setup
.\run_demo.bat --scenario setup
```

---

## Key Files

### Documentation (Read These First):
- **`DEMO_READY_SUMMARY.md`** - Complete presentation guide
- **`FIXES_COMPLETE.md`** - What was fixed and why
- **`ADD_MYSELF_GUIDE.md`** - WhatsApp integration setup
- **`RISK_SCORE_FIX.md`** - Technical details of the fix

### Code Changed:
- `backend/routes/dashboard.py` - Risk score calculation
- `frontend/src/pages/StudentProfile.jsx` - Timeline display

### Helper Scripts:
- `add_my_number.py` - Add yourself as student
- `check_my_checkins.py` - View your check-ins
- `get_test_ids.py` - Show all student IDs
- `run_demo.bat` - Main demo runner

---

## You're Ready! 🚀

The system is fully functional with:
- ✅ Accurate risk scores (state-based mapping)
- ✅ Sorted heatmap (crisis students at top)
- ✅ Clear timeline percentages
- ✅ WhatsApp integration ready
- ✅ Autonomous agent pipeline working

**Next**: Read `DEMO_READY_SUMMARY.md` for full presentation script

**Good luck with your demo!** 🎉
