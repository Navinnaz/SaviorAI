# Dashboard API Quick Reference

## Base URL
```
http://localhost:8000/api/dashboard
```

## Authentication
```
X-API-Key: guardianai_dev_key_2024
```

---

## Endpoints

### 1️⃣ Overview
```bash
GET /dashboard/{institution_id}/overview
```
**Returns:** Total students, risk counts, check-in rate, interventions today

### 2️⃣ Heatmap
```bash
GET /dashboard/{institution_id}/heatmap
```
**Returns:** Array of all students with risk state, score, trend

### 3️⃣ Student Profile
```bash
GET /dashboard/student/{student_id}/profile
```
**Returns:** Full history - check-ins, states, interventions, gaming detection

### 4️⃣ Cohorts
```bash
GET /dashboard/{institution_id}/cohorts
```
**Returns:** Batch-level analytics with risk distribution

### 5️⃣ Recent Interventions
```bash
GET /dashboard/interventions/recent?limit=20
```
**Returns:** Last N interventions with full reasoning

### 6️⃣ Health Check
```bash
GET /dashboard/health
```
**Returns:** Service status (no auth required)

---

## Quick Test

```bash
# 1. Health (no auth)
curl http://localhost:8000/api/dashboard/health

# 2. Overview
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/YOUR_INST_UUID/overview

# 3. Heatmap
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/YOUR_INST_UUID/heatmap | jq

# 4. Profile
curl -H "X-API-Key: guardianai_dev_key_2024" \
  http://localhost:8000/api/dashboard/student/YOUR_STUDENT_UUID/profile | jq

# 5. Interventions
curl -H "X-API-Key: guardianai_dev_key_2024" \
  "http://localhost:8000/api/dashboard/interventions/recent?limit=5" | jq
```

---

## Python Quick Start

```python
import requests

API = "http://localhost:8000/api/dashboard"
KEY = {"X-API-Key": "guardianai_dev_key_2024"}

# Get overview
overview = requests.get(f"{API}/YOUR_INST_UUID/overview", headers=KEY).json()
print(f"Crisis: {overview['crisis_count']}")

# Get heatmap
heatmap = requests.get(f"{API}/YOUR_INST_UUID/heatmap", headers=KEY).json()
print(f"Students: {len(heatmap)}")
```

---

## Status Codes

- **200** OK - Success
- **400** Bad Request - Invalid UUID
- **401** Unauthorized - Missing API key
- **403** Forbidden - Invalid API key
- **404** Not Found - Institution/student not found

---

## Risk States

- `stable` - HMM prob < 0.4
- `at_risk` - HMM prob 0.4-0.7
- `crisis` - HMM prob > 0.7

## Trends

- `improving` - trend_score > 0.5
- `stable` - -0.5 to 0.5
- `declining` - < -0.5

---

**Full Docs:** `backend/routes/README_DASHBOARD.md`
