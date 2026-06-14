# SaviorAI Dashboard - React PWA

Dark, clinical-grade mental health monitoring interface built for FAR AWAY 2026.

---

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

**Access:** http://localhost:3000

---

## Features

### 🏠 Dashboard (Home)
- **Real-time Overview**: KPI stats with 30-second polling
- **Risk Heatmap**: Color-coded student grid (green/yellow/red)
- **Cohort Alerts**: Banner notifications for batch-wide issues
- **Quick Navigation**: Click any student card → full profile

### 👤 Student Profile
- **14-Day Mood Trend**: Recharts line graph
- **HMM State Timeline**: Visual state transitions with probabilities
- **Adversarial Badge**: Gaming detection indicator
- **Intervention History**: Full autonomous action log per student
- **Word Cloud**: Emotional keywords with frequency sizing
- **Agent Reasoning**: Expandable AI decision explanations

### 📋 Action Log
- **Complete Audit Trail**: Every autonomous intervention
- **Filter Controls**: By level, date range, outcome
- **Expandable Details**: Full reasoning + message content
- **Judge-Ready**: Proof of agentic behavior

---

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Styling (dark theme)
- **Recharts** - Charts & visualizations
- **React Router v6** - Client-side routing

**No external UI libraries** - Pure custom components

---

## Design System

### Colors
```css
Background:    #0f0f1a
Card:          #1a1a2e
Border:        #2a2a3e

Accent:        #00d4aa (primary)
Success:       #26de81 (stable)
Warning:       #ffa502 (at-risk)
Danger:        #ff4757 (crisis)
```

### Typography
- Font: Inter (Google Fonts)
- Clinical-grade minimal UI
- Mobile-first responsive design

---

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Home.jsx              # Dashboard overview + heatmap
│   │   ├── StudentProfile.jsx    # Individual student details
│   │   └── ActionLog.jsx         # Intervention audit trail
│   │
│   ├── components/
│   │   └── RiskHeatmap.jsx       # Student grid with filters
│   │
│   ├── utils/
│   │   └── api.js                # API client functions
│   │
│   ├── App.jsx                   # Router + navigation
│   ├── main.jsx                  # React entry point
│   └── index.css                 # Tailwind + global styles
│
├── package.json
├── vite.config.js                # Vite config (API proxy)
├── tailwind.config.js            # Custom theme colors
└── index.html                    # HTML shell
```

---

## API Integration

### Configuration
- **Base URL**: `/api/dashboard` (proxied to `http://localhost:8000`)
- **API Key**: `SaviorAI_dev_key_2024`
- **Institution ID**: Auto-detected or from localStorage

### Endpoints Used
```javascript
GET /api/dashboard/{institution_id}/overview
GET /api/dashboard/{institution_id}/heatmap
GET /api/dashboard/student/{student_id}/profile
GET /api/dashboard/{institution_id}/cohorts
GET /api/dashboard/interventions/recent
```

### Polling
- Dashboard auto-refreshes every 30 seconds
- Live indicator in navigation bar
- Error handling with retry button

---

## Component Guide

### Home.jsx
**Purpose**: Main dashboard with overview metrics and student heatmap

**Features**:
- 7 KPI stat cards (total, stable, at-risk, crisis, check-in rate, interventions, alerts)
- Cohort alert banner (auto-hides if none active)
- Integrated RiskHeatmap component
- 30-second polling with last update timestamp

**State**:
- `overview` - Overview metrics
- `heatmap` - Array of student objects
- `cohorts` - Batch data for alert detection

---

### RiskHeatmap.jsx
**Purpose**: Responsive grid of color-coded student cards

**Features**:
- Color coding: green (stable), yellow (at-risk), red (crisis)
- Hover effect: Shows risk score overlay
- Sort options: Risk level, batch, last check-in
- Filter: By batch
- Click: Navigate to student profile

**Props**:
- `students` - Array from heatmap API

---

### StudentProfile.jsx
**Purpose**: Deep-dive into individual student mental health journey

**Features**:
- Basic info header with adversarial badge
- 14-day mood trend (Recharts LineChart)
- HMM state timeline (colored bars with probabilities)
- Word cloud from one-word responses
- Intervention history with expandable reasoning
- Back button to dashboard

**URL**: `/student/:studentId`

---

### ActionLog.jsx
**Purpose**: Audit trail of all autonomous interventions (for judges)

**Features**:
- Chronological feed of interventions
- Level badges (1-4) with color coding
- Filter by intervention level
- Expandable reasoning sections
- Student name links to profile
- Judge-friendly info box explaining agentic behavior

**Intervention Levels**:
1. **Peer Nudge** (cyan)
2. **Counsellor Alert** (yellow)
3. **Emergency** (red)
4. **Institutional** (purple)

---

## Mobile Responsiveness

All screens tested on:
- ✅ Desktop (1920x1080)
- ✅ Tablet (768x1024)
- ✅ Mobile (375x667)

**Breakpoints**:
- `sm:` 640px
- `md:` 768px
- `lg:` 1024px
- `xl:` 1280px

**Mobile optimizations**:
- Single column layouts on mobile
- Touch-friendly card sizes
- Readable font sizes
- Collapsible sections
- Horizontal scrolling where needed

---

## Development Tips

### Hot Reload
Vite provides instant HMR. Edit any file and see changes immediately.

### API Proxy
Vite proxies `/api/*` to backend. Ensure backend is running on port 8000.

### Change Institution
```javascript
import { setInstitutionId } from './utils/api'
setInstitutionId('your-institution-uuid')
```

### Debug Mode
Check browser console for:
- API fetch logs
- Error messages
- State updates

---

## Production Build

```bash
npm run build
```

Output: `dist/` folder ready for deployment

**Optimizations**:
- Code splitting
- Minification
- Asset optimization
- Lazy loading

---

## Deployment Options

### Vercel (Recommended)
```bash
vercel deploy
```

### Netlify
```bash
netlify deploy
```

### Manual (Static Host)
1. Build: `npm run build`
2. Upload `dist/` folder
3. Configure rewrites for SPA routing

**Environment Variables**:
- Set backend URL if not using proxy
- Update API key for production

---

## Testing Checklist

- [ ] Dashboard loads with demo data
- [ ] All 7 stat cards show correct numbers
- [ ] Cohort alert banner appears if alerts exist
- [ ] Student cards color-coded correctly
- [ ] Click student card → navigate to profile
- [ ] Profile chart renders with 14 days data
- [ ] HMM timeline shows state transitions
- [ ] Word cloud displays top 10 words
- [ ] Interventions expandable
- [ ] Action log shows all interventions
- [ ] Filter works in action log
- [ ] Mobile view renders correctly
- [ ] 30-second polling works
- [ ] Error handling shows retry button

---

## Troubleshooting

### "Cannot GET /api/dashboard/..."
**Solution**: Backend not running. Start with `python backend/main.py`

### Blank Screen
**Solution**: Check browser console. Likely CORS or API key issue.

### Charts Not Rendering
**Solution**: Install recharts: `npm install recharts`

### Styles Not Applied
**Solution**: Run `npm install` to ensure Tailwind is configured

### 404 on Refresh
**Solution**: Configure your host for SPA routing (all routes → index.html)

---

## Demo Flow (For Presentations)

1. **Start on Dashboard**
   - Point out real-time KPI stats
   - Show color-coded heatmap
   - Explain cohort alert banner

2. **Click Priya Sharma (Red Card)**
   - Show 14-day declining trend
   - Point to crisis state in timeline
   - Highlight concerning words in word cloud
   - Expand Level 3 intervention
   - Read AI reasoning aloud

3. **Navigate to Action Log**
   - Filter to show only Level 3
   - Expand Priya's intervention
   - Show full reasoning chain
   - Emphasize autonomous behavior
   - Point to judge info box

4. **Mobile Demo**
   - Open on phone/tablet
   - Show responsive layout
   - Navigate through all screens
   - Demonstrate touch interactions

---

## Key Selling Points

✅ **Fully Autonomous**: AI decides interventions without human input  
✅ **Transparent**: Every decision has visible reasoning  
✅ **Real-time**: 30-second polling for live monitoring  
✅ **Clinical Grade**: Healthcare-appropriate dark theme  
✅ **Mobile Ready**: Works perfectly on judge's phones  
✅ **Audit Trail**: Complete log for compliance/accountability  

---

## Next Steps

1. **Install dependencies**: `npm install`
2. **Start backend**: `python backend/main.py` (port 8000)
3. **Generate demo data**: `python -m backend.utils.demo_runner`
4. **Start frontend**: `npm run dev` (port 3000)
5. **Open browser**: http://localhost:3000

---

## Credits

Built for **FAR AWAY 2026** - Agentic & Autonomous Systems

SaviorAI: The autonomous agent that catches student burnout before it becomes a tragedy.

