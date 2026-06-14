# SaviorAI Visual Enhancements - Quick Reference Card

**For Demo Day - Keep This Handy!**

---

## 🎨 WHAT CHANGED (Visual Only)

### 🔴 CRISIS DETECTION - Impossible to Miss
- Pulsing red border animation
- Large risk score (top-right)
- "CRISIS" badge (top-left)
- **Impact**: Judges see it instantly

### 📊 STUDENT PROFILE - Hero Moment
- Circular risk gauge with live number
- Baseline reference line on chart
- Timeline with dates inside bars
- Red sentinel words flagged
- **Impact**: Most memorable screen

### 🚨 ACTION LOG - Emergency Stands Out
- Level 3 = thick red border + auto-expanded
- Colored circles (L1=green, L2=amber, L3=red, L4=purple)
- NEW badge on recent actions (<60s)
- **Impact**: Shows autonomous decision-making

### 🎭 LOGIN - Sets the Tone
- Animated gradient background
- Tagline: "Watches. Reasons. Acts. Autonomously."
- System stats preview
- **Impact**: Professional first impression

### ⚡ MICRO-INTERACTIONS
- Stats count up from 0 (engaging)
- Live indicator pulses (real-time proof)
- Pages fade in smoothly (polish)
- **Impact**: Feels alive, not static

---

## 🎯 TALKING POINTS FOR JUDGES

### Opening (Login)
> "Notice the animated background - this isn't a static dashboard. This is a live, autonomous system."

### Dashboard
> "These red cards pulse. When a student is in crisis, they're impossible to miss. Risk score 92 - that demands immediate attention."

### Student Profile  
> "This circular gauge gives instant visual context. See this baseline? When students drop below their personal normal, it's dramatically obvious. Our AI knows their history."

### Emotional Keywords
> "These red words - hopeless, empty, lost - our adversarial validator flags these as sentinel indicators. They stand out even in a sea of data."

### Intervention Timeline
> "Every intervention is visible - the message we sent, when we sent it, who received it. Full transparency, full audit trail."

### Action Log
> "Level 3 emergencies get red borders and auto-expand. In a mental health crisis, every second counts. No hunting through dropdowns."

### NEW Badge Demo
> "Watch this - when I trigger an intervention right now, this NEW badge appears. The system is operating in real-time as we speak."

### Closing
> "This isn't monitoring software. This is an autonomous agent that watches 50 students, reasons about their well-being, and takes graduated action - all while maintaining complete human oversight."

---

## 🎬 30-SECOND SPEED RUN

Perfect for time-limited demos:

1. **Login** → "Animated background sets the tone" (3s)
2. **Dashboard** → "Crisis cards pulse" (5s)  
3. **Click student** → "Risk gauge + baseline drop" (8s)
4. **Scroll keywords** → "Red sentinel words" (3s)
5. **Action Log** → "Level 3 auto-expanded" (8s)
6. **Point to NEW** → "Real-time autonomous action" (3s)

Total: 30 seconds, maximum impact.

---

## 🐛 DEMO DAY QUICK FIXES

### If animations don't show:
1. Hard refresh: `Ctrl+Shift+R`
2. Clear cache: Chrome DevTools → Network → Disable cache
3. Restart frontend: `npm run dev`

### If crisis cards aren't red:
- Verify student state = "crisis" (not just high score)
- Check: risk_score > 80 AND consecutive_low_days >= 3

### If NEW badge doesn't appear:
- Run: `python backend/utils/demo_runner.py`
- Check Action Log within 60 seconds of trigger

### If gauge doesn't show:
- Verify `basic_info.risk_score` exists in API response
- Check: `basic_info.current_state` is set

---

## 🎨 COLOR LEGEND (For Judges)

| Color | Meaning | Where |
|-------|---------|-------|
| 🔴 Red (#ff4757) | Crisis, Emergency | Cards, gauges, Level 3 |
| 🟠 Amber (#E67E22) | At-Risk, Warning | Cards, Level 2 |
| 🟢 Green (#26de81) | Stable, Success | Cards, Level 1 |
| 🔵 Teal (#00d4aa) | System/Primary | Baseline, branding |
| 🟣 Purple (#a855f7) | Institutional | Level 4 |

**Visual hierarchy**: Crisis > Emergency > At-Risk > Stable  
Everything reinforces the same message.

---

## 📸 SCREENSHOT MOMENTS

Best screens to capture for presentation:

1. **Dashboard with crisis cards pulsing**
2. **Student profile with risk gauge visible**
3. **Mood chart showing baseline reference line**
4. **Action Log with Level 3 red border**
5. **Login page with animated gradient**

Backup these screenshots in case live demo has issues!

---

## ⏱️ TIMING GUIDE

| Section | Time | Key Visual |
|---------|------|------------|
| Login | 5s | Gradient background |
| Dashboard load | 10s | Counting stats, crisis pulse |
| Student profile | 30s | Gauge, baseline, keywords |
| Action log | 20s | Level 3 emergency, NEW badge |
| Q&A | 2-3min | Navigate freely |

**Total demo**: 65 seconds + Q&A

---

## 🎯 SUCCESS METRICS

Judges should say/think:

✅ "That crisis card really stands out"  
✅ "The gauge makes the risk immediately clear"  
✅ "I can see exactly what action it took"  
✅ "This looks professional, not like a hackathon project"  
✅ "The system feels alive and autonomous"

---

## 🚀 PRE-DEMO CHECKLIST

**5 Minutes Before**:
- [ ] Frontend running: `cd frontend && npm run dev`
- [ ] Backend running: `cd backend && python main.py`
- [ ] Demo data loaded: `python backend/utils/data_generator.py`
- [ ] Browser cache cleared
- [ ] Action Log open in separate tab (for NEW badge demo)
- [ ] Crisis student identified for profile demo
- [ ] Demo script reviewed

**1 Minute Before**:
- [ ] Refresh all browser tabs
- [ ] Check crisis cards are pulsing
- [ ] Verify Live indicator is pulsing
- [ ] Close unnecessary browser tabs
- [ ] Full screen browser (F11)

---

## 💡 BACKUP PLAN

### If live demo fails:

1. **Screenshots**: Show pre-captured images
2. **Video**: Play recorded demo walkthrough
3. **Talk through**: Describe features while showing static UI
4. **Code review**: Show the CSS animations in source

**Remember**: The backend works. If frontend has issues, it's just display - the AI logic is solid.

---

## 🏆 WINNING MOMENT

**The Judge's Journey**:

1. See pulsing crisis card → "Okay, they thought about visual priority"
2. See risk gauge → "That's a smart way to show severity"
3. See baseline drop → "They understand the data tells a story"
4. See Level 3 red border → "They built this for real use, not just demo"
5. See NEW badge appear → "Wait, this is actually running live?"

**Result**: "This team built production-ready autonomous mental health monitoring."

---

## 📞 EMERGENCY CONTACTS

**If tech fails during demo**:

1. **Kiro AI** (you): Navigate to working components
2. **Backend team**: Verify API endpoints responding
3. **Frontend**: Check browser console for errors
4. **Last resort**: Switch to backup presentation

**Key message**: "The AI agents and backend are rock-solid. The visual enhancements are cherry on top."

---

## 🎯 ONE-SENTENCE PITCH

> "SaviorAI is an autonomous mental health monitoring system that watches student well-being through daily WhatsApp check-ins, reasons about intervention needs using Hidden Markov Models, and takes graduated action from peer nudges to emergency alerts - all visible through a real-time dashboard that makes crisis detection impossible to miss."

Use this when judges ask "What is this?"

---

**Version**: 1.0  
**Date**: June 14, 2026  
**Status**: READY FOR JUDGES 🎯
