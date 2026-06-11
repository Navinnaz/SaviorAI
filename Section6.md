## SECTION 6 — REACT PWA DASHBOARD

```
frontend/
├── public/
│   ├── manifest.json          ← PWA manifest
│   └── icons/
├── src/
│   ├── App.jsx
│   ├── pages/
│   │   ├── Home.jsx           ← Institution overview + risk heatmap
│   │   ├── Students.jsx       ← All students, filterable by risk
│   │   ├── StudentProfile.jsx ← Individual student timeline
│   │   ├── Cohorts.jsx        ← Batch-level analytics
│   │   └── ActionLog.jsx      ← Every autonomous action taken
│   ├── components/
│   │   ├── RiskHeatmap.jsx    ← Visual grid of student risk levels
│   │   ├── TrendChart.jsx     ← 14-day score trend per student
│   │   ├── StateTimeline.jsx  ← HMM state transitions visualised
│   │   ├── InterventionCard.jsx
│   │   └── CohortAlert.jsx
│   └── services/
│       └── api.js
```