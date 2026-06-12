# GuardianAI Dashboard API Documentation

Complete API reference for institutional monitoring and analytics endpoints.

---

## Authentication

All dashboard endpoints (except `/health`) require API key authentication.

**Header:**
```
X-API-Key: your_api_key_here
```

**Default Dev Key:** `guardianai_dev_key_2024` (set in `.env` as `DASHBOARD_API_KEY`)

**Production:** Store hashed API keys in database with institution mapping.

---

## Endpoints

### 1. Institution Overview

**GET** `/api/dashboard/{institution_id}/overview`

High-level dashboard statistics for an institution.

**Headers:**
```
X-API-Key: guardianai_dev_key_2024
```

**Response:**
```json
{
  "total_students": 156,
  "stable_count": 120,
  "at_risk_count": 28,
  "crisis_count": 8,
  "check_in_rate_7d": 87.2,
  "interventions_today": 3,
  "cohort_alerts_active": 2
}
```

**Use Cases:**
- Main dashboard KPI tiles
- Real-time monitoring
- Alert counts

---

### 2. Student Heatmap

**GET** `/api/dashboard/{institution_id}/heatmap`

Grid data for visual risk heatmap of all students.

**Headers:**
```
X-API-Key: guardianai_dev_key_2024
```

**Response:**
```json
[
  {
    "student_id": "123e4567-e89b-12d3-a456-426614174001",
    "name": "Arjun Kumar",
    "batch": "CSE-2022",
    "state": "at_risk",
    "risk_score": 72,
    "last_checkin": "2026-06-11T19:30:00Z",
    "trend": "declining"
  },
  {
    "student_id": "123e4567-e89b-12d3-a456-426614174002",
    "name": "Priya Sharma",
    "batch": "CSE-2022",
    "state": "stable",
    "risk_score": 15,
    "last_checkin": "2026-06-12T08:15:00Z",
    "trend": "improving"
  }
]
```

**Fields:**
- `state`: `"stable"` | `"at_risk"` | `"crisis"`
- `risk_score`: 0-100 (HMM probability * 100)
- `trend`: `"improving"` | `"stable"` | `"declining"` (based on trend_score)
- `last_checkin`: ISO 8601 datetime or `null`

**Use Cases:**
- Color-coded grid visualization
- Quick identification of high-risk students
- Batch-level patterns

---

### 3. Student Profile

**GET** `/api/dashboard/student/{student_id}/profile`

Complete student mental health profile with full history.

**Headers:**
```
X-API-Key: guardianai_dev_key_2024
```

**Response:**
```json
{
  "basic_info": {
    "id": "456e4567-e89b-12d3-a456-426614174111",
    "name": "Arjun Kumar",
    "phone": "+919876543210",
    "email": "arjun@example.com",
    "batch": "CSE-2022",
    "year_of_study": 3,
    "baseline_score": 3.2,
    "enrolled_at": "2024-08-01T10:00:00Z",
    "institution": {
      "id": "789e4567-e89b-12d3-a456-426614174000",
      "name": "IIT Delhi",
      "type": "college",
      "city": "New Delhi"
    }
  },
  "checkins_14d": [
    {
      "checked_in_at": "2026-06-01T20:00:00Z",
      "mood_score": 3,
      "ate_properly": "yes",
      "one_word": "focused",
      "sentiment": "neutral",
      "sentiment_score": 0.1
    },
    {
      "checked_in_at": "2026-06-02T20:05:00Z",
      "mood_score": 2,
      "ate_properly": "mostly",
      "one_word": "overwhelmed",
      "sentiment": "negative",
      "sentiment_score": -0.6
    }
  ],
  "state_history": [
    {
      "assessed_at": "2026-06-01T20:01:00Z",
      "state": "stable",
      "hmm_probability": 0.85,
      "trend_score": 0.1,
      "consecutive_low_days": 0,
      "variance_flag": false,
      "cohort_flag": false
    },
    {
      "assessed_at": "2026-06-02T20:06:00Z",
      "state": "at_risk",
      "hmm_probability": 0.68,
      "trend_score": -0.7,
      "consecutive_low_days": 1,
      "variance_flag": false,
      "cohort_flag": false
    }
  ],
  "interventions": [
    {
      "id": "abc12345-e89b-12d3-a456-426614174222",
      "triggered_at": "2026-06-03T08:30:00Z",
      "level": 1,
      "trigger_reason": "2 consecutive days of mood score <= 2, declining trend detected",
      "action_taken": "send",
      "message_sent": "Hey Arjun! We noticed you've been feeling a bit low. Remember, it's okay to take breaks...",
      "recipient": "student",
      "was_acknowledged": true,
      "acknowledged_at": "2026-06-03T09:15:00Z",
      "outcome": "recovered"
    }
  ],
  "adversarial_summary": {
    "total_assessments": 45,
    "gaming_detected_count": 2,
    "gaming_percentage": 4.4,
    "last_gaming_detected": "2026-05-15T20:10:00Z"
  }
}
```

**Use Cases:**
- Student detail page
- Timeline visualization of mental health journey
- Intervention effectiveness tracking
- Anomaly detection (gaming behavior)

---

### 4. Cohort Analytics

**GET** `/api/dashboard/{institution_id}/cohorts`

Batch-level aggregated analytics for cohort monitoring.

**Headers:**
```
X-API-Key: guardianai_dev_key_2024
```

**Response:**
```json
[
  {
    "batch": "CSE-2022",
    "total_students": 68,
    "avg_mood_7d": 3.4,
    "risk_distribution": {
      "stable": 52,
      "at_risk": 12,
      "crisis": 4
    },
    "active_alerts": 1
  },
  {
    "batch": "CSE-2023",
    "total_students": 72,
    "avg_mood_7d": 3.8,
    "risk_distribution": {
      "stable": 65,
      "at_risk": 6,
      "crisis": 1
    },
    "active_alerts": 0
  }
]
```

**Use Cases:**
- Batch comparison
- Cohort anomaly detection
- Year-wise mental health trends
- Resource allocation planning

---

### 5. Recent Interventions

**GET** `/api/dashboard/interventions/recent`

Recent autonomous interventions with full reasoning chains.

**Query Parameters:**
- `institution_id` (optional): Filter by institution UUID
- `limit` (default 20, max 100): Number of interventions to return

**Headers:**
```
X-API-Key: guardianai_dev_key_2024
```

**Example:**
```
GET /api/dashboard/interventions/recent?institution_id=789e4567&limit=10
```

**Response:**
```json
[
  {
    "id": "int-001",
    "triggered_at": "2026-06-12T10:30:00Z",
    "student": {
      "id": "stud-001",
      "name": "Arjun Kumar",
      "batch": "CSE-2022",
      "institution": "IIT Delhi"
    },
    "level": 2,
    "level_name": "Counsellor Soft Alert",
    "trigger_reason": "Student in 'at_risk' state for 5 consecutive days. HMM probability: 0.72. Trend score: -0.8 (declining). Recent onewords: 'exhausted', 'hopeless', 'numb'.",
    "action_taken": "send",
    "message_sent": "Dear Counsellor, Arjun Kumar (CSE-2022) has been showing signs of burnout...",
    "recipient": "counsellor",
    "was_acknowledged": false,
    "acknowledged_at": null,
    "outcome": "pending"
  }
]
```

**Intervention Levels:**
1. **Peer Nudge** - Gentle message to student
2. **Counsellor Soft Alert** - Notify counsellor for outreach
3. **Emergency Escalation** - Immediate crisis intervention
4. **Institutional Action** - Cohort-wide systemic changes

**Use Cases:**
- Audit trail of agent decisions
- Intervention effectiveness analysis
- Debugging autonomous reasoning
- Compliance and accountability

---

### 6. Health Check

**GET** `/api/dashboard/health`

Dashboard service health check (no auth required).

**Response:**
```json
{
  "status": "healthy",
  "service": "guardianai-dashboard",
  "version": "1.0.0",
  "timestamp": "2026-06-12T12:00:00Z"
}
```

**Use Cases:**
- Monitoring dashboards
- Load balancer health checks
- Service discovery

---

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Missing API key. Include X-API-Key header."
}
```

### 403 Forbidden
```json
{
  "detail": "Invalid API key"
}
```

### 404 Not Found
```json
{
  "detail": "Institution not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid institution ID format"
}
```

---

## Data Models

### Risk States
- `stable`: HMM probability < 0.4, no concerning patterns
- `at_risk`: HMM probability 0.4-0.7, declining trend
- `crisis`: HMM probability > 0.7, critical intervention needed

### Trend Classification
- `improving`: trend_score > 0.5 (scores rising relative to baseline)
- `stable`: -0.5 ≤ trend_score ≤ 0.5
- `declining`: trend_score < -0.5 (scores falling)

### Intervention Outcomes
- `pending`: Just triggered, awaiting response
- `recovered`: Student returned to stable state
- `escalated`: Required higher-level intervention
- `no_change`: No observable improvement

---

## Rate Limiting

**Current:** No rate limiting (development)

**Production Recommendations:**
- 100 requests/minute per API key
- 1000 requests/hour per institution
- Implement Redis-based rate limiting

---

## Security Best Practices

### Production Deployment

1. **API Key Management:**
   ```python
   # Store hashed keys in database
   CREATE TABLE api_keys (
       id UUID PRIMARY KEY,
       institution_id UUID REFERENCES institutions(id),
       key_hash TEXT NOT NULL,
       created_at TIMESTAMP,
       last_used TIMESTAMP,
       is_active BOOLEAN DEFAULT true
   );
   ```

2. **HTTPS Only:**
   - Enforce TLS 1.3
   - HSTS headers
   - Certificate pinning for mobile apps

3. **Request Validation:**
   - Input sanitization
   - SQL injection prevention (SQLAlchemy ORM)
   - Rate limiting per institution

4. **Audit Logging:**
   ```python
   # Log all API access
   logger.info(f"Dashboard access: institution={inst_id}, endpoint={endpoint}, api_key={key[:8]}...")
   ```

5. **Data Privacy:**
   - PII encryption at rest
   - Anonymized exports
   - GDPR/HIPAA compliance checks

---

## Example Frontend Integration

### React/Next.js

```typescript
// lib/dashboard-api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL;
const API_KEY = process.env.DASHBOARD_API_KEY;

export async function getInstitutionOverview(institutionId: string) {
  const response = await fetch(
    `${API_BASE}/api/dashboard/${institutionId}/overview`,
    {
      headers: {
        'X-API-Key': API_KEY,
        'Content-Type': 'application/json'
      }
    }
  );
  
  if (!response.ok) {
    throw new Error(`Dashboard API error: ${response.status}`);
  }
  
  return response.json();
}

export async function getStudentProfile(studentId: string) {
  const response = await fetch(
    `${API_BASE}/api/dashboard/student/${studentId}/profile`,
    {
      headers: { 'X-API-Key': API_KEY }
    }
  );
  
  if (!response.ok) {
    throw new Error(`Failed to fetch student profile`);
  }
  
  return response.json();
}
```

### Python Client

```python
import requests

class GuardianAIDashboard:
    def __init__(self, api_url: str, api_key: str):
        self.base_url = api_url
        self.headers = {"X-API-Key": api_key}
    
    def get_overview(self, institution_id: str):
        response = requests.get(
            f"{self.base_url}/api/dashboard/{institution_id}/overview",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_heatmap(self, institution_id: str):
        response = requests.get(
            f"{self.base_url}/api/dashboard/{institution_id}/heatmap",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
dashboard = GuardianAIDashboard(
    api_url="http://localhost:8000",
    api_key="guardianai_dev_key_2024"
)

overview = dashboard.get_overview("123e4567-e89b-12d3-a456-426614174000")
print(f"Total students: {overview['total_students']}")
print(f"Crisis count: {overview['crisis_count']}")
```

---

## Testing

### cURL Examples

**1. Get Overview:**
```bash
curl -X GET "http://localhost:8000/api/dashboard/123e4567-e89b-12d3-a456-426614174000/overview" \
  -H "X-API-Key: guardianai_dev_key_2024"
```

**2. Get Heatmap:**
```bash
curl -X GET "http://localhost:8000/api/dashboard/123e4567-e89b-12d3-a456-426614174000/heatmap" \
  -H "X-API-Key: guardianai_dev_key_2024" | jq
```

**3. Get Student Profile:**
```bash
curl -X GET "http://localhost:8000/api/dashboard/student/456e4567-e89b-12d3-a456-426614174111/profile" \
  -H "X-API-Key: guardianai_dev_key_2024" | jq
```

**4. Get Recent Interventions:**
```bash
curl -X GET "http://localhost:8000/api/dashboard/interventions/recent?limit=5" \
  -H "X-API-Key: guardianai_dev_key_2024" | jq
```

### Pytest

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_dashboard_overview():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/dashboard/123e4567-e89b-12d3-a456-426614174000/overview",
            headers={"X-API-Key": "guardianai_dev_key_2024"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "total_students" in data
    assert "stable_count" in data
    assert data["total_students"] >= 0

@pytest.mark.asyncio
async def test_auth_required():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/api/dashboard/123e4567/overview"
        )
    
    assert response.status_code == 401
```

---

## Performance Optimization

### Current Performance
- Overview endpoint: ~200-300ms (N+1 query issue)
- Heatmap endpoint: ~500ms for 100 students
- Student profile: ~150ms

### Optimization Strategies

1. **Database Indexing:**
   ```sql
   CREATE INDEX idx_student_institution ON students(institution_id) WHERE is_active = true;
   CREATE INDEX idx_checkin_student_time ON checkins(student_id, checked_in_at DESC);
   CREATE INDEX idx_burnout_student_time ON burnout_states(student_id, assessed_at DESC);
   ```

2. **Caching (Redis):**
   ```python
   @router.get("/{institution_id}/overview")
   @cache(expire=60)  # Cache for 60 seconds
   async def get_institution_overview(...):
       ...
   ```

3. **Batch Queries:**
   ```python
   # Instead of N+1 queries
   for student in students:
       state = await get_latest_burnout_state(student.id)
   
   # Use batch query
   states = await get_latest_states_batch([s.id for s in students])
   ```

4. **Materialized Views:**
   ```sql
   CREATE MATERIALIZED VIEW institution_overview AS
   SELECT 
       institution_id,
       COUNT(*) as total_students,
       SUM(CASE WHEN state = 'stable' THEN 1 ELSE 0 END) as stable_count,
       ...
   FROM students_with_latest_state
   GROUP BY institution_id;
   
   REFRESH MATERIALIZED VIEW CONCURRENTLY institution_overview;
   ```

---

## Changelog

### v1.0.0 (2026-06-12)
- Initial dashboard API release
- 5 core endpoints + health check
- API key authentication
- Full HMM state history
- Adversarial validation summary
- Cohort-level analytics

---

## Support

**Issues:** Check logs for detailed error traces
**API Key Reset:** Contact your institution administrator
**Rate Limit Increase:** Email support@guardianai.io (production only)

---

Built with ❤️ for FAR AWAY 2026 - Agentic & Autonomous Systems
