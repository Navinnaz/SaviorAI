# GuardianAI

**The autonomous agent that catches student burnout before it becomes a tragedy.**

## Overview

GuardianAI is an autonomous student mental health triage agent built for the FAR AWAY 2026 hackathon. One student dies by suicide every 40 minutes in India. GuardianAI watches what counsellors can't — 24/7, at scale, before the crisis.

## System Architecture

- **Student Layer**: WhatsApp check-ins via Twilio
- **Agent Core**: HMM burnout detection, adversarial validation, cohort anomaly detection
- **Intervention Layer**: 4-level autonomous intervention system
- **Dashboard Layer**: React PWA for counsellors
- **Data Layer**: PostgreSQL on Railway

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key
- Twilio account (for WhatsApp)

### Installation

1. Clone the repository:
```bash
cd SaviorAI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
copy .env.example .env
# Edit .env with your credentials
```

4. Run the application:
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── main.py                    # FastAPI app entry
├── database/
│   ├── connection.py          # PostgreSQL connection pool
│   └── models.py              # SQLAlchemy models
├── agents/
│   ├── hmm_engine.py          # HMM burnout detection
│   ├── adversarial_validator.py
│   ├── cohort_detector.py
│   └── intervention_orchestrator.py
├── routes/
│   ├── webhook.py             # WhatsApp webhook
│   ├── students.py
│   ├── dashboard.py
│   ├── interventions.py
│   └── cohorts.py
├── services/
│   ├── whatsapp.py
│   ├── scheduler.py
│   └── sentiment.py
└── utils/
```

## Key Features

1. **Hidden Markov Model**: Probabilistic burnout state detection
2. **Adversarial Validation**: Detects students gaming the system
3. **Cohort Anomaly Detection**: Identifies systemic stressors
4. **4-Level Intervention System**: Autonomous escalation
5. **GPT-4o Reasoning**: Context-aware message generation

## License

Built for FAR AWAY 2026 Hackathon - Agentic & Autonomous Systems Theme
