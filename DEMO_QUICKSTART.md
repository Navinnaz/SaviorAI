# SaviorAI Demo Quick Start

## 🚀 One-Time Setup

### 1. Install Dependencies
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 2. Configure Environment
```bash
# Copy .env.example to .env
copy .env.example .env

# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-...
```

### 3. Initialize Database
```bash
python -m backend.utils.demo_runner --scenario setup
```
✅ Creates permanent demo institution: **88353031-000c-4b80-b091-89fe65849734**  
✅ Populates 50 students with 14 days of history

## 🎬 Running the Demo

### Start Services (2 terminals)
```bash
# Terminal 1: Backend
python -m backend.main

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### Access Dashboard
1. Open browser: **http://localhost:5173/**
2. Click **"🎭 Demo Login (IIT Delhi)"** button
3. Dashboard loads with 50 students ✨

## 🔄 Reset Between Demos

```bash
# Stop both services (Ctrl+C in terminals)

# Reset data (preserves institution)
python -m backend.utils.demo_runner --scenario reset
# Type: yes

# Setup fresh data
python -m backend.utils.demo_runner --scenario setup

# Restart services and refresh browser
```

## 🎯 Demo Features to Showcase

### 1. Crisis Detection (Priya Sharma)
- Find "Priya Sharma" card (RED - Crisis state)
- Click to view profile
- Show 14-day declining pattern
- Point out Level 3 Emergency intervention in Action Log

### 2. Gaming Detection  
- Look for cards with ⚠️ WARNING badge
- These students report perfect scores (attempting to game system)
- Adversarial validator caught the pattern

### 3. Cohort Anomaly (MECH-2023)
- 12 students in MECH-2023 all declined simultaneously
- Check Action Log for cohort alert
- Shows institutional-level intervention recommendation

### 4. Risk Heatmap
- Visual representation of all students
- Color coding: Green (stable), Yellow (at-risk), Red (crisis)
- Click any student for detailed view

### 5. Action Log
- Shows all autonomous interventions
- Different levels (1=Peer, 2=Counsellor, 3=Emergency)
- Decision reasoning visible for explainability

## 💡 Key Talking Points

1. **No Manual Setup**: One-click demo login (no localStorage manipulation)
2. **Permanent UUID**: Institution persists across resets
3. **Real AI**: GPT-4o-mini generates personalized intervention messages
4. **Multi-Agent System**: HMM + Adversarial + Cohort detection working together
5. **Production Ready**: WhatsApp integration, scheduled check-ins, PWA support

## 🔍 Live Demo Scenario (Optional)

```bash
# After setup, run live events simulation
python -m backend.utils.demo_runner --scenario live
```

This simulates 4 real-time events:
1. **Crisis check-in** from Priya (mood: 1, word: "empty")
2. **Gaming detection** (student with 14 perfect scores)
3. **Cohort scan** (MECH-2023 anomaly detection)
4. **Action log summary** (show all interventions)

Each event updates the dashboard in real-time!

## 🐛 Troubleshooting

### "No students found"
```bash
python -m backend.utils.demo_runner --scenario setup
```

### "Cannot access /dashboard"
- Go to http://localhost:5173/ and click "Demo Login"

### Database locked
```bash
# Windows
taskkill /F /IM python.exe
# Then restart backend
```

### Frontend not updating
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

## 📝 Demo Checklist

Before presentation:
- [ ] Both services running
- [ ] Database populated (50 students)
- [ ] Browser at login page
- [ ] Action log has interventions
- [ ] Priya Sharma is in crisis state

During presentation:
- [ ] Demo login (one click)
- [ ] Show dashboard overview
- [ ] Click Priya's profile
- [ ] Show risk heatmap
- [ ] Open action log
- [ ] Explain AI decision-making

## 🎓 Institution Details

**Demo Institution**
- Name: IIT Delhi
- UUID: 88353031-000c-4b80-b091-89fe65849734
- Students: 50
- Batches: CSE-2022, CSE-2023, ECE-2023, MECH-2023, CSE-2024

**Special Students**
- **Priya Sharma** (CSE-2022): Crisis demo - 14-day decline
- **Gaming students** (3): Adversarial detection demo
- **MECH-2023 cohort** (12): Batch-wide anomaly demo
- **Normal students** (34): Realistic variance patterns

---

**Need help?** Check DEMO_LOGIN_SYSTEM.md for detailed documentation.
