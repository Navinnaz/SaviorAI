# GuardianAI Frontend - Complete Setup Guide

## ✅ Files Created

### Core Configuration
- ✅ `frontend/package.json` - Dependencies & scripts
- ✅ `frontend/vite.config.js` - Vite config with API proxy
- ✅ `frontend/tailwind.config.js` - Dark theme colors
- ✅ `frontend/postcss.config.js` - PostCSS setup
- ✅ `frontend/index.html` - HTML shell with Inter font

### React Application
- ✅ `frontend/src/main.jsx` - React entry point
- ✅ `frontend/src/App.jsx` - Router & navigation
- ✅ `frontend/src/index.css` - Global styles + Tailwind

### Utilities
- ✅ `frontend/src/utils/api.js` - API client functions

### Pages
- ✅ `frontend/src/pages/Home.jsx` - Dashboard with overview & heatmap
- ✅ `frontend/src/pages/StudentProfile.jsx` - Individual student details
- ✅ `frontend/src/pages/ActionLog.jsx` - Intervention audit trail

### Components
- ✅ `frontend/src/components/RiskHeatmap.jsx` - Student grid

---

## 🚀 Installation Steps

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

This will install:
- React 18.2.0
- React Router v6.20.0
- Recharts 2.10.3
- Tailwind CSS 3.3.6
- Vite 5.0.8

### 3. Ensure backend is running
```bash
# In another terminal, from project root:
cd ..
.\venv\Scripts\activate
python backend\main.py
```

Backend should be running on http://localhost:8000

### 4. Start frontend dev server
```bash
npm run dev
```

Frontend will start on http://localhost:3000

---

## 📱 Testing the Dashboard

### Step 1: Access Dashboard
Open http://localhost:3000 in your browser

### Step 2: Verify Overview
You should see:
- ✅ Navigation bar with "GuardianAI" logo
- ✅ 7 stat cards showing demo data
- ✅ Risk heatmap with 50 student cards
- ✅ Cards colored green/yellow/red by risk state

### Step 3: Test Priya Sharma Profile
1. Find the red card labeled "Priya Sharma"
2. Click it
3. Verify you see:
   - ✅ 14-day declining trend chart
   - ✅ Crisis state in HMM timeline
   - ✅ Word cloud with "hopeless", "empty", "lost"
   - ✅ Level 3 emergency intervention

### Step 4: Test Action Log
1. Click "Action Log" in navigation
2. Verify you see:
   - ✅ 4 interventions (1 crisis + 3 gaming)
   - ✅ Level badges colored correctly
   - ✅ Expandable reasoning sections
   - ✅ Judge info box at bottom

### Step 5: Test Mobile View
1. Open DevTools (F12)
2. Click device toggle (Ctrl+Shift+M)
3. Select "iPhone 12 Pro"
4. Verify responsive layout works

---

## 🎨 Design Verification

### Color Scheme
- Background: `#0f0f1a` (dark blue-black)
- Cards: `#1a1a2e` (slightly lighter)
- Accent: `#00d4aa` (cyan)
- Success: `#26de81` (green)
- Warning: `#ffa502` (yellow)
- Danger: `#ff4757` (red)

### Typography
- Font: Inter (loaded from Google Fonts)
- Clean, clinical aesthetic
- High contrast for readability

### Components
- All components use Tailwind classes
- No external UI libraries
- Custom hover effects
- Smooth transitions

---

## 🐛 Common Issues & Solutions

### Issue: "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Issue: "Cannot GET /api/dashboard/..."
**Solution**: Backend not running. Start with `python backend/main.py`

### Issue: Blank screen
**Solution**: 
1. Check browser console for errors
2. Verify backend is on port 8000
3. Check institution ID in localStorage

### Issue: CORS errors
**Solution**: Vite proxy should handle this. Check `vite.config.js` proxy settings.

### Issue: Charts not rendering
**Solution**: Recharts may not be installed. Run `npm install recharts`

### Issue: Styles not applied
**Solution**: 
1. Ensure Tailwind is in `package.json`
2. Run `npm install`
3. Check `tailwind.config.js` exists

---

## 📊 Demo Data Quick Test

### Expected Stat Cards:
- Total Students: 50
- Stable: ~36 (72%)
- At Risk: ~13 (26%)
- Crisis: 1 (2%)
- Check-in Rate: 100%
- Interventions Today: 4
- Active Alerts: 1

### Key Demo Personas:
1. **Priya Sharma** - Red card (crisis)
2. **3 Gaming Students** - Flagged with warning badge
3. **12 MECH-2023 Students** - Cohort anomaly (yellow cards)
4. **Rest** - Normal variance (mostly green)

---

## 🎯 Judge Presentation Checklist

### Before Demo:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Demo data populated (50 students)
- [ ] Browser cleared of console errors
- [ ] Mobile view tested

### During Demo:
- [ ] Show dashboard with real-time stats
- [ ] Click Priya Sharma to show crisis case
- [ ] Expand intervention to show AI reasoning
- [ ] Navigate to Action Log for audit trail
- [ ] Show mobile responsiveness

### Key Talking Points:
- ✅ "Fully autonomous - AI decides interventions"
- ✅ "Complete transparency - every decision explained"
- ✅ "Real-time monitoring with 30-second polling"
- ✅ "Clinical-grade UI for healthcare use"
- ✅ "Mobile-ready for on-the-go monitoring"

---

## 🔧 Development Commands

```bash
# Install dependencies
npm install

# Start dev server (with HMR)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Clean install (if issues)
rm -rf node_modules package-lock.json
npm install
```

---

## 📦 Production Deployment

### Build
```bash
npm run build
```

Output in `dist/` folder

### Deploy to Vercel
```bash
npm install -g vercel
vercel deploy
```

### Deploy to Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Environment Variables
For production, set:
- `VITE_API_URL` - Backend URL
- `VITE_API_KEY` - Dashboard API key

---

## 🎭 FAR AWAY 2026 Hackathon Notes

### Theme: Agentic & Autonomous Systems
**How GuardianAI fits:**
- ✅ Autonomous decision-making (no human in loop)
- ✅ Multi-agent system (HMM, adversarial, cohort, orchestrator)
- ✅ Real-world impact (student mental health)
- ✅ Complete audit trail (transparency)

### Judging Criteria:
1. **Technical Innovation**: Multi-agent AI pipeline
2. **Autonomous Behavior**: Self-directed interventions
3. **Real-world Applicability**: Addresses real crisis
4. **Transparency**: Full reasoning visible
5. **Demo Quality**: Polished, professional UI

### Demo Tips:
- Start with Priya Sharma (flagship crisis case)
- Show AI reasoning chain (most impressive part)
- Emphasize "catches burnout before tragedy"
- Demonstrate mobile responsiveness
- Point to Action Log as proof of autonomy

---

## ✅ All Systems Go!

Frontend is **production-ready** for FAR AWAY 2026! 🚀

**Next Steps:**
1. `cd frontend && npm install`
2. `npm run dev`
3. Open http://localhost:3000
4. Practice your demo flow

**Questions?** Check `frontend/README.md` for detailed docs.
