# Frontend Visual Enhancement Test Guide

**Quick 5-Minute Visual Verification**

---

## 🚀 START THE FRONTEND

```bash
cd frontend
npm run dev
```

Wait for: `Local: http://localhost:5173/`

---

## ✅ TEST CHECKLIST

### 1. LOGIN PAGE (30 seconds)

**URL**: `http://localhost:5173/`

**Look for**:
- [ ] Animated gradient background (slow moving colors)
- [ ] Tagline: "Watches. Reasons. Acts. Autonomously." in teal
- [ ] Three stat chips below Demo Login:
  - 🎓 50 Students Monitored
  - 🤖 4 Autonomous Agents
  - ⚡ Real-time WhatsApp Integration

**Action**: Click "🎭 Demo Login (IIT Delhi)"

---

### 2. DASHBOARD (60 seconds)

**URL**: `http://localhost:5173/dashboard`

**Look for**:
- [ ] Page fades in smoothly
- [ ] Stat numbers COUNT UP from 0 (watch the numbers animate!)
- [ ] Green "Live" dot PULSES in top-right navbar
- [ ] If cohort alerts present: banner has subtle shimmer effect

**Scroll to Risk Heatmap**:
- [ ] Red crisis cards PULSE with glowing border
- [ ] Crisis cards show "CRISIS" badge (top-left)
- [ ] Crisis cards show large risk score number (top-right)
- [ ] All cards have thin colored left border (red/amber/green)
- [ ] Cards are taller (100px minimum height)
- [ ] HOVER over any card: it lifts slightly

**Action**: Click on a CRISIS (red) student card

---

### 3. STUDENT PROFILE (90 seconds)

**URL**: `http://localhost:5173/student/{id}`

**Look for**:

#### Header Section:
- [ ] Large CIRCULAR GAUGE shows risk score
- [ ] Number in center of gauge (e.g., "92")
- [ ] State label below number ("CRISIS")
- [ ] If crisis: gauge ring PULSES

#### 14-Day Mood Trend Chart:
- [ ] Horizontal DASHED LINE across chart (baseline)
- [ ] Line labeled "Personal Baseline" in teal
- [ ] Student's scores plotted against baseline

#### Mental Health State Timeline:
- [ ] Bars are TALLER (48px height)
- [ ] Date text INSIDE each colored bar
- [ ] Format: "CRISIS since Jun 8" or similar

#### Emotional Keywords:
- [ ] Word size varies by frequency (larger = more frequent)
- [ ] RED WORDS stand out (sentinel words like "hopeless", "empty", "lost")
- [ ] Red words have red border

#### Intervention History:
- [ ] VERTICAL LINE connects interventions (timeline view)
- [ ] Colored circles mark each entry (L1=green, L2=amber, L3=red)
- [ ] Messages VISIBLE by default (not collapsed)
- [ ] Quote marks around messages
- [ ] Colored left border on message boxes

**Action**: Click "Back to Dashboard", then click "Action Log" in navbar

---

### 4. ACTION LOG (90 seconds)

**URL**: `http://localhost:5173/action-log`

**Look for**:

#### Top Stats Cards:
- [ ] Each level card has COLOR-CODED background
- [ ] Emergency card has red tint
- [ ] Colors: green (L1), amber (L2), red (L3), purple (L4)

#### Intervention Feed:

**Level 3 (Emergency) Entries**:
- [ ] THICK RED LEFT BORDER (4px)
- [ ] Light red background tint
- [ ] Circular badge with "L3" + "EMERGENCY" label
- [ ] Emergency entries PULSE with glow effect
- [ ] Messages EXPANDED by default (visible immediately)
- [ ] Quote marks around message content

**Level 1/2 Entries**:
- [ ] Circular badges with level number
- [ ] Full labels: "PEER NUDGE", "COUNSELLOR"
- [ ] Messages collapsed (expandable)

**NEW Badge** (if intervention triggered within last 60 seconds):
- [ ] Green "NEW" badge appears
- [ ] Badge PULSES

**Action**: Test complete!

---

## 🎯 CRITICAL VISUAL MOMENTS

These are the **"wow"** moments judges will notice:

1. **Dashboard Load**: Numbers counting up from 0
2. **Crisis Cards**: Pulsing red borders that demand attention
3. **Student Profile Gauge**: Large circular risk indicator
4. **Baseline Chart**: Drop below personal baseline is dramatic
5. **Action Log Level 3**: Auto-expanded with red border - unmissable
6. **Live Indicator**: Pulsing green dot reinforces real-time

---

## 🐛 TROUBLESHOOTING

### "I don't see the animations"

**Check**:
1. Hard refresh: `Ctrl+Shift+R` (Chrome) or `Cmd+Shift+R` (Mac)
2. Clear browser cache
3. Check browser console for errors: `F12`

### "Crisis cards aren't pulsing"

**Verify**:
- Student state is actually "crisis" (risk score >80)
- CSS loaded correctly: inspect element → check for `crisis-pulse` class
- Try different crisis student

### "Stat numbers don't animate"

**Reason**: Animation runs once on mount
**Solution**: Refresh page to see animation again

### "NEW badge doesn't appear"

**Reason**: No interventions triggered in last 60 seconds
**Solution**: 
1. Run demo: `python backend/utils/demo_runner.py`
2. Trigger intervention
3. Check Action Log within 60 seconds

---

## 📊 COMPARISON TEST

### Open Two Tabs Side-by-Side:

**Tab 1**: Dashboard with crisis cards  
**Tab 2**: Action Log with Level 3 entries

**Observe**: Both use the same red pulsing animation - visual consistency reinforces crisis severity across the app.

---

## ⚡ QUICK DEMO SCRIPT (30 seconds)

Perfect for showing judges:

1. **Login** (3s): "Notice the animated background - this is a live system."

2. **Dashboard** (5s): "These red cards pulse - crisis students are impossible to miss."

3. **Click Crisis Student** (10s): "This gauge gives instant context. 92% risk. The baseline shows her dramatic drop."

4. **Scroll to Keywords** (3s): "Red words - hopeless, empty, lost - our AI flags these as critical."

5. **Action Log** (8s): "Level 3 emergencies auto-expand with red borders. In a crisis, every second counts."

6. **Wrap** (1s): "This system doesn't just monitor. It watches, reasons, and acts."

---

## 🎨 ANIMATION REFERENCE

All animations are subtle and professional:

| Element | Animation | Duration | Effect |
|---------|-----------|----------|--------|
| Crisis cards | Pulse border | 2s | Draws eye to high-risk |
| Risk gauge (crisis) | Pulse ring | 2s | Reinforces severity |
| Live indicator | Pulse dot | 1.5s | Shows real-time |
| NEW badge | Pulse scale | 1.5s | Highlights fresh data |
| Level 3 entries | Pulse glow | 2s | Emergency emphasis |
| Page load | Fade in | 0.2s | Smooth transition |
| Stat numbers | Count up | 0.8s | Engaging first impression |
| Cohort banner | Shimmer | 3s | Subtle attention draw |
| Login background | Gradient shift | 15s | Ambient intelligence feel |

---

## ✅ SUCCESS CRITERIA

After testing, you should feel:

- ✅ Crisis students are **unmissable**
- ✅ Emergency actions are **obvious**
- ✅ The system feels **alive** and **autonomous**
- ✅ First impression is **professional**
- ✅ Navigation is **smooth**
- ✅ Visual hierarchy is **clear**

If any of these aren't true, report the issue!

---

## 🎯 READY FOR DEMO

When all checkboxes are ticked:

1. ✅ Visual enhancements verified
2. ✅ Animations working smoothly
3. ✅ No console errors
4. ✅ Crisis cards pulse
5. ✅ Gauge displays correctly
6. ✅ Action log Level 3 stands out

**Status**: Frontend is judge-ready! 🏆

---

**Next Steps**:
1. Run full demo rehearsal with `demo_runner.py`
2. Test WhatsApp integration live
3. Practice talking points with animations
4. Take screenshots for presentation backup

**Estimated Test Time**: 5-10 minutes for full verification
