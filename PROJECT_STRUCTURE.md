# GuardianAI - Project Structure

## ✅ Completed Setup

### Backend Structure

```
backend/
├── main.py                              ✅ FastAPI app entry with CORS, routers, health check
├── requirements.txt                     ✅ All dependencies listed
├── .env.example                         ✅ All required environment variables
│
├── database/
│   ├── __init__.py                     ✅
│   ├── connection.py                   ✅ Async PostgreSQL with asyncpg + SQLAlchemy
│   └── models.py                       ✅ All tables: Students, CheckIns, BurnoutStates, etc.
│
├── agents/                             ✅ The Agent Core (The Brain)
│   ├── __init__.py                     ✅
│   ├── hmm_engine.py                   ✅ Hidden Markov Model burnout detection
│   ├── adversarial_validator.py        ✅ Gaming detection
│   ├── cohort_detector.py              ✅ Systemic stress detection
│   └── intervention_orchestrator.py    ✅ Autonomous decision-making
│
├── routes/                             ✅ All API Endpoints
│   ├── __init__.py                     ✅
│   ├── webhook.py                      ✅ WhatsApp webhook (CORE AUTONOMOUS PIPELINE)
│   ├── students.py                     ✅ Student CRUD
│   ├── dashboard.py                    ✅ Dashboard data
│   ├── interventions.py                ✅ Intervention history
│   └── cohorts.py                      ✅ Cohort analytics
│
├── services/                           ✅ External Services
│   ├── __init__.py                     ✅
│   ├── whatsapp.py                     ✅ Twilio WhatsApp messaging
│   ├── scheduler.py                    ✅ APScheduler daily check-ins
│   └── sentiment.py                    ✅ Sentiment analysis
│
└── utils/
    └── __init__.py                     ✅
```

### Root Files

```
SaviorAI/
├── README.md                           ✅ Project documentation
├── .env.example                        ✅ Environment variables template
├── .gitignore                          ✅ Git ignore rules
├── requirements.txt                    ✅ Python dependencies
└── PROJECT_STRUCTURE.md                ✅ This file
```

## Environment Variables Required

Create a `.env` file from `.env.example` and fill in:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/guardianai
OPENAI_API_KEY=sk-your-openai-api-key-here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
FRONTEND_URL=http://localhost:3000
```

## Next Steps

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   copy .env.example .env
   # Edit .env with your actual credentials
   ```

3. **Set Up Database**
   - Create PostgreSQL database named `guardianai`
   - Tables will be created automatically on first run

4. **Run the Application**
   ```bash
   cd backend
   python main.py
   ```

5. **Test the API**
   - Health check: http://localhost:8000/
   - Swagger docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Key Features Implemented

### 1. Autonomous Agent Core ✅
- **HMM Engine**: Probabilistic burnout state detection (Stable/At-Risk/Crisis)
- **Adversarial Validator**: Detects students gaming the system
- **Cohort Detector**: Identifies systemic stressors affecting groups
- **Intervention Orchestrator**: Autonomous decision-making with GPT-4o

### 2. WhatsApp Integration ✅
- Twilio webhook for incoming messages
- Automated daily check-in scheduling
- Multi-level intervention messaging

### 3. Database Schema ✅
- Students and Institutions
- Check-ins with sentiment analysis
- Burnout states tracking
- Interventions log
- Cohort alerts

### 4. API Routes ✅
- Student management
- Dashboard analytics
- Intervention history
- Cohort analytics
- WhatsApp webhook handler

## Database Schema

The complete schema is defined in `backend/database/models.py` with:
- `institutions` - Organizations using GuardianAI
- `students` - Enrolled students
- `checkins` - Daily check-in responses
- `burnout_states` - HMM state transitions
- `interventions` - Autonomous actions taken
- `cohort_alerts` - Batch-level anomalies

## Agent Decision Pipeline

1. **Student sends WhatsApp message** → Twilio webhook
2. **Parse check-in** → Extract mood score, eating habits, one-word
3. **Get history** → Last 14 days of scores
4. **Run HMM** → Calculate burnout state probability
5. **Adversarial check** → Detect gaming behavior
6. **Orchestrator decides** → Autonomous intervention level (0-4)
7. **GPT-4o generates message** → Context-aware, empathetic
8. **Execute action** → Send to student/counsellor/emergency

## Production Deployment

### Railway (Recommended)
- Deploy PostgreSQL database
- Deploy FastAPI backend
- Set environment variables
- Configure Twilio webhook URL

### Environment Variables for Production
Add to Railway/your hosting platform:
- `DATABASE_URL` (auto-provided by Railway PostgreSQL)
- `OPENAI_API_KEY`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_NUMBER`
- `FRONTEND_URL`
- `ENVIRONMENT=production`
- `DEBUG=false`

## Testing

Run tests with:
```bash
pytest
```

## Support

For questions about the GuardianAI system, refer to:
- `Section1&2.md` - Project identity and architecture
- `Section3.md` - Database schema
- `Section4.md` - Agent core implementation
- `Section5.md` - Backend structure
- `Section6.md` - Frontend dashboard (React PWA)
- `Section8.md` - Demo data generator

---

Built for FAR AWAY 2026 Hackathon
Theme: Agentic & Autonomous Systems
