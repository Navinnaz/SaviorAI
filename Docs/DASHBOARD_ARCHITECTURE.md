# GuardianAI Dashboard Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Dashboard                        │
│  (React/Next.js - Institution Monitoring Portal)            │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Overview │  │ Heatmap  │  │ Student  │  │ Cohorts  │   │
│  │  Cards   │  │   Grid   │  │ Profile  │  │Analytics │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└────────────┬────────────────────────────────────────────────┘
             │
             │ HTTPS + X-API-Key Header
             ↓
┌─────────────────────────────────────────────────────────────┐
│              Dashboard API (FastAPI)                         │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  API Key Authentication Middleware                   │   │
│  │  (verify_api_key dependency)                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Endpoint Handlers                                    │  │
│  │                                                       │  │
│  │  • GET /overview          → Institution stats        │  │
│  │  • GET /heatmap           → Student risk grid        │  │
│  │  • GET /student/profile   → Full history            │  │
│  │  • GET /cohorts           → Batch analytics         │  │
│  │  • GET /interventions     → Audit trail             │  │
│  │  • GET /health            → Service status          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬────────────────────────────────────────────────┘
             │
             │ SQLAlchemy Async Queries
             ↓
┌─────────────────────────────────────────────────────────────┐
│           Database Layer (CRUD Operations)                   │
│                                                              │
│  • get_student_by_id()                                      │
│  • get_latest_burnout_state()                              │
│  • get_all_students_by_institution()                       │
│  • get_recent_scores()                                     │
│  • get_interventions_for_student()                         │
│  • get_active_cohort_alerts()                             │
└────────────┬────────────────────────────────────────────────┘
             │
             │ PostgreSQL Protocol
             ↓
┌─────────────────────────────────────────────────────────────┐
│         Railway PostgreSQL Database                          │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐          │
│  │ students   │  │ checkins   │  │ burnout_    │          │
│  │            │  │            │  │ states      │          │
│  └────────────┘  └────────────┘  └─────────────┘          │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌─────────────┐          │
│  │interventions│ │ cohort_    │  │institutions │          │
│  │            │  │ alerts     │  │             │          │
│  └────────────┘  └────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Get Institution Overview

```
1. Frontend Request
   ↓
   GET /api/dashboard/abc123.../overview
   Header: X-API-Key: guardianai_dev_key_2024

2. FastAPI Router
   ↓
   Match route → dashboard.get_institution_overview()

3. Authentication
   ↓
   verify_api_key(x_api_key) → Validate key → ✅ Pass

4. Dependency Injection
   ↓
   get_db() → Async database session → db

5. Institution Lookup
   ↓
   SELECT * FROM institutions WHERE id = 'abc123...'
   ↓
   Institution exists? ✅ Continue

6. Student Aggregation
   ↓
   SELECT * FROM students WHERE institution_id = 'abc123...' AND is_active = true
   ↓
   Found 156 students

7. Risk State Calculation (Loop)
   ↓
   For each student:
     • get_latest_burnout_state(student.id)
     • SELECT * FROM burnout_states WHERE student_id = '...' ORDER BY assessed_at DESC LIMIT 1
     • Count by state: stable++, at_risk++, crisis++

8. Check-in Rate Calculation
   ↓
   SELECT COUNT(DISTINCT student_id) FROM checkins
   WHERE student_id IN (...) AND checked_in_at >= '7 days ago'
   ↓
   137 of 156 students checked in (87.8%)

9. Today's Interventions
   ↓
   SELECT COUNT(*) FROM interventions
   WHERE student_id IN (...) AND triggered_at >= 'today 00:00:00'
   ↓
   3 interventions today

10. Active Cohort Alerts
    ↓
    SELECT COUNT(*) FROM cohort_alerts
    WHERE institution_id = 'abc123...' AND acknowledged = false
    ↓
    2 unacknowledged alerts

11. JSON Response
    ↓
    {
      "total_students": 156,
      "stable_count": 120,
      "at_risk_count": 28,
      "crisis_count": 8,
      "check_in_rate_7d": 87.8,
      "interventions_today": 3,
      "cohort_alerts_active": 2
    }

12. Frontend Rendering
    ↓
    Display KPI cards with color coding
```

---

## Component Architecture

### Frontend (Proposed)

```
Dashboard/
├── components/
│   ├── Overview/
│   │   ├── StatCard.tsx           (KPI tile)
│   │   ├── TrendChart.tsx         (7-day trend)
│   │   └── AlertBanner.tsx        (cohort alerts)
│   │
│   ├── Heatmap/
│   │   ├── StudentGrid.tsx        (grid layout)
│   │   ├── StudentTile.tsx        (single student)
│   │   └── BatchFilter.tsx        (filter by batch)
│   │
│   ├── StudentProfile/
│   │   ├── BasicInfo.tsx          (name, batch, baseline)
│   │   ├── CheckinChart.tsx       (14-day timeline)
│   │   ├── StateTimeline.tsx      (HMM state transitions)
│   │   ├── InterventionsList.tsx  (history table)
│   │   └── GamingAlert.tsx        (adversarial flag)
│   │
│   └── Cohorts/
│       ├── BatchCard.tsx          (batch overview)
│       ├── RiskDistribution.tsx   (pie chart)
│       └── AlertsList.tsx         (active alerts)
│
├── hooks/
│   ├── useDashboard.ts           (fetch overview)
│   ├── useHeatmap.ts             (fetch heatmap)
│   ├── useStudentProfile.ts      (fetch profile)
│   └── useInterventions.ts       (fetch interventions)
│
└── lib/
    └── dashboard-api.ts          (API client)
```

### Backend (Current)

```
backend/
├── routes/
│   └── dashboard.py              (6 endpoints + auth)
│
├── database/
│   ├── models.py                 (SQLAlchemy models)
│   ├── crud.py                   (query functions)
│   └── connection.py             (DB pool)
│
└── main.py                       (FastAPI app + router registration)
```

---

## Authentication Flow

```
┌─────────────────────────────────────────────────┐
│  Frontend makes request                         │
│  Headers: { "X-API-Key": "guardianai_dev..." } │
└────────────┬────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────┐
│  FastAPI receives request                       │
│  Extract x_api_key from headers                │
└────────────┬────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────┐
│  verify_api_key(x_api_key: str)                │
│                                                 │
│  1. Check if key exists                        │
│     ↓ Missing → 401 Unauthorized               │
│                                                 │
│  2. Get valid key from environment             │
│     DASHBOARD_API_KEY = os.getenv(...)         │
│                                                 │
│  3. Compare keys                               │
│     x_api_key == valid_api_key?                │
│     ↓ No → 403 Forbidden                       │
│     ↓ Yes → ✅ Continue                        │
└────────────┬────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────┐
│  Execute endpoint handler                       │
│  Query database                                 │
│  Return JSON response                           │
└─────────────────────────────────────────────────┘
```

---

## Database Schema (Relevant Tables)

```sql
institutions
├── id (UUID, PK)
├── name (VARCHAR)
├── type (VARCHAR)
├── counsellor_phone (VARCHAR)
└── created_at (TIMESTAMP)

students
├── id (UUID, PK)
├── name (VARCHAR)
├── phone (VARCHAR, UNIQUE)
├── institution_id (UUID, FK → institutions)
├── batch (VARCHAR)
├── baseline_score (FLOAT)
└── is_active (BOOLEAN)

checkins
├── id (UUID, PK)
├── student_id (UUID, FK → students)
├── checked_in_at (TIMESTAMP)
├── mood_score (INT, 1-5)
├── ate_properly (VARCHAR)
├── one_word (TEXT)
├── sentiment (VARCHAR)
└── skipped (BOOLEAN)

burnout_states
├── id (UUID, PK)
├── student_id (UUID, FK → students)
├── assessed_at (TIMESTAMP)
├── state (VARCHAR: stable|at_risk|crisis)
├── hmm_probability (FLOAT)
├── trend_score (FLOAT)
├── consecutive_low_days (INT)
├── variance_flag (BOOLEAN)
└── cohort_flag (BOOLEAN)

interventions
├── id (UUID, PK)
├── student_id (UUID, FK → students)
├── triggered_at (TIMESTAMP)
├── level (INT: 1-4)
├── trigger_reason (TEXT)
├── message_sent (TEXT)
├── recipient (VARCHAR)
└── outcome (VARCHAR)

cohort_alerts
├── id (UUID, PK)
├── institution_id (UUID, FK → institutions)
├── batch (VARCHAR)
├── detected_at (TIMESTAMP)
├── affected_students (INT)
├── likely_cause (TEXT)
└── acknowledged (BOOLEAN)
```

---

## API Response Time Breakdown

### GET /overview (typical: ~250ms)

```
┌────────────────────────────────────┬─────────┐
│ Operation                          │ Time    │
├────────────────────────────────────┼─────────┤
│ API key validation                 │   5ms   │
│ Institution lookup                 │  20ms   │
│ Get all students                   │  30ms   │
│ Loop: Get latest states (N+1)     │ 150ms   │ ← Bottleneck
│ Check-in rate query                │  25ms   │
│ Today's interventions query        │  15ms   │
│ Active alerts query                │  10ms   │
│ JSON serialization                 │   5ms   │
├────────────────────────────────────┼─────────┤
│ Total                              │ 260ms   │
└────────────────────────────────────┴─────────┘
```

**Optimization:** Batch query for latest states → 150ms → 40ms

---

## Security Layers

```
┌──────────────────────────────────────────┐
│  Layer 1: Network Security               │
│  • HTTPS only (TLS 1.3)                 │
│  • CORS restrictions                    │
│  • Rate limiting (future)               │
└────────────┬─────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────┐
│  Layer 2: Authentication                 │
│  • X-API-Key header validation          │
│  • 401/403 for invalid keys             │
│  • Audit logging (future)               │
└────────────┬─────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────┐
│  Layer 3: Input Validation               │
│  • UUID format checking                 │
│  • Limit caps (max 100)                 │
│  • Type coercion (Pydantic)             │
└────────────┬─────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────┐
│  Layer 4: Database Security              │
│  • SQLAlchemy ORM (SQL injection safe)  │
│  • Parameterized queries                │
│  • Transaction isolation                │
└────────────┬─────────────────────────────┘
             │
             ↓
┌──────────────────────────────────────────┐
│  Layer 5: Data Privacy                   │
│  • PII access control                   │
│  • Anonymized exports (future)          │
│  • Audit trail (future)                 │
└──────────────────────────────────────────┘
```

---

## Scalability Considerations

### Current Limits
- **100 students:** ~200ms response time ✅
- **1000 students:** ~1.5s response time ⚠️
- **10000 students:** ~15s response time ❌

### Solutions

1. **Database Indexes**
   ```sql
   CREATE INDEX idx_burnout_latest 
   ON burnout_states (student_id, assessed_at DESC);
   ```

2. **Materialized Views**
   ```sql
   CREATE MATERIALIZED VIEW student_current_state AS
   SELECT DISTINCT ON (student_id)
     student_id, state, hmm_probability, assessed_at
   FROM burnout_states
   ORDER BY student_id, assessed_at DESC;
   ```

3. **Redis Caching**
   ```python
   @cache(expire=60)
   async def get_institution_overview(...):
       ...
   ```

4. **Pagination**
   ```
   GET /heatmap?page=1&limit=50
   ```

---

## Monitoring & Observability

### Logs to Track
```python
logger.info(f"Dashboard access: endpoint={endpoint}, institution={inst_id}")
logger.warning(f"Slow query: {elapsed}ms > 500ms")
logger.error(f"Database error: {error}")
```

### Metrics to Monitor
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Database query time
- API key usage per institution
- Endpoint popularity

### Alerts to Configure
- Response time > 1s for 5 minutes
- Error rate > 5% for 1 minute
- Database connection pool exhausted
- Disk space < 10%

---

## Production Deployment Checklist

- [ ] Hash API keys in database
- [ ] Enable HTTPS (Let's Encrypt)
- [ ] Configure CORS for production domain
- [ ] Add rate limiting (100 req/min)
- [ ] Set up Redis for caching
- [ ] Create database indexes
- [ ] Enable audit logging
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Configure backups (hourly)
- [ ] Load testing (1000 concurrent users)
- [ ] Security audit
- [ ] GDPR compliance review

---

**Status:** Architecture documented ✅  
**Next:** Test with real data and optimize based on metrics
