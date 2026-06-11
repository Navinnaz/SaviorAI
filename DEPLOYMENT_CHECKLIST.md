# GuardianAI - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Environment Setup
- [ ] Python 3.11+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created from `.env.example`
- [ ] PostgreSQL database created

### 2. Required Credentials
- [ ] **DATABASE_URL** configured (PostgreSQL with asyncpg driver)
- [ ] **OPENAI_API_KEY** added (GPT-4o access required)
- [ ] **TWILIO_ACCOUNT_SID** added
- [ ] **TWILIO_AUTH_TOKEN** added
- [ ] **TWILIO_WHATSAPP_NUMBER** configured

### 3. Database Setup
- [ ] Database `guardianai` created
- [ ] Connection string uses `postgresql+asyncpg://` (not just `postgresql://`)
- [ ] Database accessible from application server
- [ ] Tables will auto-create on first run

### 4. Local Testing
- [ ] Run `python backend/main.py` successfully
- [ ] Health check responds at `http://localhost:8000/`
- [ ] API docs accessible at `http://localhost:8000/docs`
- [ ] No errors in console logs

## 🚀 Railway Deployment (Recommended)

### Step 1: Create Railway Project
1. Sign up at https://railway.app
2. Create new project
3. Add PostgreSQL service
4. Add Python service (from GitHub or local)

### Step 2: Configure Database
1. Railway auto-provides `DATABASE_URL`
2. **IMPORTANT**: Change the URL format:
   - Railway gives: `postgresql://user:pass@host:port/db`
   - You need: `postgresql+asyncpg://user:pass@host:port/db`
3. Add as environment variable in Railway

### Step 3: Add Environment Variables
In Railway dashboard, add:
```
DATABASE_URL=postgresql+asyncpg://[from Railway but modified]
OPENAI_API_KEY=sk-your-key
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
FRONTEND_URL=https://your-frontend-url.railway.app
ENVIRONMENT=production
DEBUG=false
```

### Step 4: Configure Build
Railway should auto-detect Python and install from `requirements.txt`

Start command:
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Configure Twilio Webhook
1. Deploy to Railway (get your URL: `https://your-app.railway.app`)
2. In Twilio console, set WhatsApp webhook to:
   ```
   https://your-app.railway.app/api/webhook/whatsapp
   ```
3. Method: POST

### Step 6: Test Deployment
- [ ] Visit `https://your-app.railway.app/` - should show health check
- [ ] Visit `https://your-app.railway.app/docs` - API documentation loads
- [ ] Send test WhatsApp message to Twilio number
- [ ] Check Railway logs for incoming webhook

## 🔒 Security Checklist

- [ ] All API keys in environment variables (not hardcoded)
- [ ] `.env` file in `.gitignore`
- [ ] Database uses SSL in production
- [ ] CORS configured for your frontend domain only
- [ ] Debug mode disabled in production (`DEBUG=false`)

## 📊 Monitoring Setup

### Railway Logs
Monitor for:
- ✅ Database connections successful
- ✅ HMM assessments running
- ✅ Interventions triggered
- ❌ Any error traces

### Key Metrics to Track
- Daily check-in completion rate
- Intervention accuracy (false positive rate)
- Response time to crisis states
- Cohort anomaly detection rate

## 🎯 Demo Day Preparation

### 1. Seed Demo Data
Create 50 synthetic students with realistic patterns:
- 8 students in crisis (declining trajectory)
- 5 students gaming the system (flat responses)
- 37 students with normal variation

### 2. Prepare Demo Scenarios
**Scenario 1: Individual Crisis Detection**
- Show student "Priya" with declining scores
- HMM detects crisis state
- Agent autonomously triggers intervention
- Display reasoning and message generated

**Scenario 2: Gaming Detection**
- Show student with suspiciously flat scores (all 4s)
- Adversarial validator flags behavior
- Different intervention path (counselor alert, not peer nudge)

**Scenario 3: Cohort Anomaly**
- 60% of CSE-2022 batch declining together
- Cohort detector identifies systemic stressor
- Institutional alert generated

### 3. Dashboard Highlights
Prepare to show:
- Risk heatmap with color-coded students
- Real-time state transitions (Stable → At-Risk → Crisis)
- Intervention history with agent reasoning
- Cohort analytics showing batch trends

### 4. Technical Deep Dive (If Judges Ask)
Be ready to explain:
- **HMM**: Viterbi algorithm, transition probabilities
- **Autonomy**: No human in loop, agent decides intervention level
- **Adversarial**: Gaming detection via variance analysis
- **Scalability**: Async PostgreSQL, can handle 10K+ students
- **Privacy**: No conversation content stored, only structured metrics

## 🐛 Troubleshooting

### Issue: Database connection fails
```
sqlalchemy.exc.OperationalError: connection failed
```
**Fix**: 
1. Verify PostgreSQL is running
2. Check DATABASE_URL format (must use `postgresql+asyncpg://`)
3. Ensure database `guardianai` exists

### Issue: OpenAI API errors
```
openai.error.AuthenticationError: Invalid API key
```
**Fix**:
1. Verify `OPENAI_API_KEY` in `.env`
2. Ensure GPT-4o access enabled on your account
3. Check API quota not exceeded

### Issue: WhatsApp webhook not receiving
**Fix**:
1. Verify Twilio webhook URL is correct
2. Check webhook logs in Twilio console
3. Ensure POST method is selected
4. Test with Twilio's webhook tester

### Issue: Import errors
```
ModuleNotFoundError: No module named 'agents'
```
**Fix**: Run from correct directory:
```bash
cd c:\Users\g_and\SaviorAI\backend
python main.py
```

## 📞 Support During Demo

If something breaks during demo:
1. **Database down**: Switch to mock data mode (show static dashboard)
2. **OpenAI down**: Explain that message generation uses GPT-4o, show pre-generated examples
3. **WhatsApp down**: Demonstrate with Postman/curl to webhook endpoint directly

## 🎓 Key Talking Points

1. **Autonomous**: Agent decides intervention level, no human approval
2. **Proactive**: Detects burnout BEFORE crisis, not after
3. **Context-aware**: Personal baselines, not one-size-fits-all thresholds
4. **Gaming-resistant**: Adversarial validation catches masking behavior
5. **Systemic view**: Cohort detection finds institutional problems
6. **Privacy-first**: Structured metrics only, no conversation storage
7. **Scalable**: Async architecture, handles thousands of students

---

**For FAR AWAY 2026 Hackathon**
*"One student dies by suicide every 40 minutes in India. GuardianAI is the autonomous agent that watches what counsellors can't — 24/7, at scale, before the crisis."*
