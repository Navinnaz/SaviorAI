## SECTION 5 — FASTAPI BACKEND STRUCTURE

```
backend/
├── main.py                    ← App entry, routes registered
├── requirements.txt
├── .env.example
├── database/
│   ├── connection.py          ← PostgreSQL connection pool
│   └── models.py              ← SQLAlchemy models
├── agents/
│   ├── __init__.py
│   ├── hmm_engine.py          ← HMM burnout states
│   ├── adversarial_validator.py
│   ├── cohort_detector.py
│   └── intervention_orchestrator.py
├── routes/
│   ├── webhook.py             ← Twilio WhatsApp webhook
│   ├── students.py            ← Student CRUD
│   ├── dashboard.py           ← Dashboard data endpoints
│   ├── interventions.py       ← Intervention history
│   └── cohorts.py             ← Cohort analytics
├── services/
│   ├── whatsapp.py            ← Twilio send/receive
│   ├── scheduler.py           ← APScheduler daily check-in jobs
│   └── sentiment.py           ← GPT-4o sentiment analysis
└── utils/
    ├── data_generator.py      ← Synthetic demo data generator
    └── demo_runner.py         ← Auto-runs demo scenarios
```

### Key Route: WhatsApp Webhook

```python
# backend/routes/webhook.py

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Receives every incoming WhatsApp message.
    Parses check-in, runs full agent pipeline, 
    autonomously decides intervention. No human in the loop.
    """
    phone = From.replace("whatsapp:", "")
    
    # 1. Find student
    student = await get_student_by_phone(db, phone)
    if not student:
        return send_whatsapp(phone, "Welcome to GuardianAI. Please register with your institution.")
    
    # 2. Parse check-in response
    checkin = await parse_checkin_response(Body, student.id)
    await save_checkin(db, checkin)
    
    # 3. Get full history
    scores = await get_recent_scores(db, student.id, days=14)
    onewords = await get_recent_onewords(db, student.id, days=7)
    
    # 4. Run HMM assessment
    hmm = BurnoutHMM()
    assessment = hmm.assess(scores, student.baseline_score)
    
    # 5. Adversarial validation
    validator = AdversarialValidator()
    validation = validator.validate(scores)
    
    # 6. Save burnout state
    await save_burnout_state(db, student.id, assessment, validation)
    
    # 7. Run intervention orchestrator — AUTONOMOUS DECISION
    orchestrator = InterventionOrchestrator(openai_client)
    last_intervention = await get_last_intervention(db, student.id)
    
    action = await orchestrator.decide_and_act(
        student=student.__dict__,
        assessment=assessment,
        recent_scores=scores,
        recent_onewords=onewords,
        validation_result=validation,
        last_intervention=last_intervention
    )
    
    # 8. Execute the action
    if action["action"] == "send" and action["level"] > 0:
        await execute_intervention(db, student, action)
    
    # 9. Confirm receipt to student
    await send_whatsapp(phone, "✅ Logged. Thank you for checking in.")
    
    return Response(status_code=200)
```
