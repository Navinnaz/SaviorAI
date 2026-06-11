# GuardianAI - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Python Dependencies

```bash
cd c:\Users\g_and\SaviorAI
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

```bash
copy .env.example .env
```

Edit `.env` and add your credentials:
- **DATABASE_URL**: Your PostgreSQL connection string
- **OPENAI_API_KEY**: Your OpenAI API key (for GPT-4o)
- **TWILIO credentials**: For WhatsApp integration (optional for testing)

### Step 3: Set Up PostgreSQL Database

**Option A: Local PostgreSQL**
```sql
CREATE DATABASE guardianai;
```

**Option B: Railway.app (Recommended for demo)**
1. Go to https://railway.app
2. Create new project → Add PostgreSQL
3. Copy the connection string to `.env` as `DATABASE_URL`
   - Change `postgresql://` to `postgresql+asyncpg://`

### Step 4: Run the Application

```bash
cd backend
python main.py
```

You should see:
```
✅ GuardianAI database connection pool initialized
✅ Database initialized: guardianai
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Test the API

Open your browser:
- **Health check**: http://localhost:8000/
- **API docs**: http://localhost:8000/docs

You should see:
```json
{
  "status": "operational",
  "agent": "GuardianAI",
  "tagline": "The autonomous agent that catches student burnout before it becomes a tragedy."
}
```

## 🧪 Testing Without WhatsApp

The system works in "demo mode" without Twilio credentials:
- WhatsApp messages will be logged to console instead of sent
- All other functionality works normally

## 📊 Key API Endpoints

### Health & Status
- `GET /` - Health check
- `GET /health` - Detailed system status

### Students
- `GET /api/students` - List all students
- `GET /api/students/{id}` - Get student details

### Dashboard
- `GET /api/dashboard/overview` - Risk statistics
- `GET /api/dashboard/risk-heatmap` - Student risk visualization

### Interventions
- `GET /api/interventions` - Intervention history

### WhatsApp Webhook
- `POST /api/webhook/whatsapp` - Receives WhatsApp messages (Twilio)

## 🎯 Testing the Agent Core

You can test the agent components independently:

```python
from agents import BurnoutHMM, AdversarialValidator, CohortAnomalyDetector

# Test HMM with sample scores
hmm = BurnoutHMM()
scores = [4, 4, 3, 2, 2, 1, 2, 1]  # Declining pattern
assessment = hmm.assess(scores, baseline=3.5)
print(f"State: {assessment.state}")
print(f"Probability: {assessment.probability}")
print(f"Reasoning: {assessment.reasoning}")

# Test adversarial validator
validator = AdversarialValidator()
flat_scores = [4, 4, 4, 4, 4, 4, 4, 4]  # Suspiciously flat
validation = validator.validate(flat_scores)
print(f"Suspicious: {validation['is_suspicious']}")
print(f"Flags: {validation['flags']}")
```

## 🔧 Common Issues

### Issue: Database connection error
**Solution**: Make sure:
1. PostgreSQL is running
2. Database `guardianai` exists
3. Connection string in `.env` is correct (use `postgresql+asyncpg://`)

### Issue: Import errors
**Solution**: Make sure you're running from the correct directory:
```bash
cd c:\Users\g_and\SaviorAI\backend
python main.py
```

### Issue: OpenAI API errors
**Solution**: 
1. Verify your API key in `.env`
2. Ensure you have GPT-4o access
3. Check your API quota

## 📝 Next Steps

1. **Add Demo Data**: Create synthetic students for testing
2. **Test WhatsApp Flow**: Set up Twilio sandbox
3. **Deploy to Railway**: Use the deployment guide
4. **Build Frontend**: Create React PWA dashboard

## 🎓 Understanding the Agent

The autonomous decision pipeline:
1. Student sends check-in via WhatsApp
2. HMM analyzes burnout state (Stable/At-Risk/Crisis)
3. Adversarial validator checks for gaming
4. Orchestrator autonomously selects intervention level
5. GPT-4o generates empathetic message
6. Action executed (peer nudge, counsellor alert, or emergency)

**No human approval needed** - the agent decides and acts autonomously.

## 📚 Documentation

- `README.md` - Overview and features
- `PROJECT_STRUCTURE.md` - Complete file structure
- `Section*.md` - Detailed architecture documents

---

**Built for FAR AWAY 2026 Hackathon**
*Theme: Agentic & Autonomous Systems*
