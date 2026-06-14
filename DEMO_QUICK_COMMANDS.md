# 🎯 Demo Quick Reference Card

## ⚡ One-Page Cheat Sheet

### START SERVERS (One Time)

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Frontend  
cd frontend && npm run dev

# Open: http://localhost:3001
```

---

### REHEARSAL COMMANDS (Each Time)

```bash
# Terminal 3
cd backend/utils

# 1. Reset (type 'yes')
python demo_runner.py --reset

# 2. Setup (wait ~20sec)
python demo_runner.py --setup

# 3. Verify: Open http://localhost:3001
#    → Click "Demo Login"
#    → Priya card should be GREEN

# 4. Run demo (watch magic happen)
python demo_runner.py --live

# 5. Verify: Refresh browser
#    → Priya card now RED
#    → Cohort banner appears
#    → Check Action Log
```

---

### WHAT TO EXPECT

#### After `--setup`:
✅ 50 students created  
✅ Priya Kumar: **GREEN** (stable)  
✅ Dashboard loads normally

#### After `--live` (60 seconds):
✅ Event 1: Crisis detected → Priya RED  
✅ Event 2: Gaming flagged → ⚠️ badge  
✅ Event 3: Cohort alert → 🔔 banner  
✅ Event 4: Action log → 3+ decisions

---

### TROUBLESHOOTING

**Blank screen?**
```bash
cd frontend
npm run dev
# Hard refresh: Ctrl+Shift+R
```

**Database error?**
```bash
cd backend/utils
python nuclear_reset.py
python demo_runner.py --setup
```

**Email not sending?**
Add to `.env`:
```
DEMO_MODE=true
```

---

### KEY URLs

- **Dashboard**: http://localhost:3001
- **Action Log**: http://localhost:3001/action-log
- **Backend API**: http://localhost:8000/docs
- **Demo Login**: Click "🎭 Demo Login (IIT Delhi)" button

---

### TIMING

| Step | Duration |
|------|----------|
| `--reset` | 5 sec |
| `--setup` | 20 sec |
| Verify dashboard | 10 sec |
| `--live` | 60 sec |
| Show results | 90 sec |
| **Total** | **3 min** |

---

### SUCCESS CHECKLIST

- [ ] Backend running (port 8000)
- [ ] Frontend running (port 3001)  
- [ ] Dashboard loads (no blank)
- [ ] Login works
- [ ] Priya starts GREEN
- [ ] `--live` shows 4 beautiful events
- [ ] Priya turns RED
- [ ] Cohort banner appears
- [ ] Action Log shows reasoning

---

### NARRATION ONE-LINER

> "Watch SaviorAI's autonomous pipeline detect crisis, flag gaming, identify cohort stress, and log every decision with complete transparency - all in 60 seconds."

---

**Print this. Keep it visible during demo. 🎬**
