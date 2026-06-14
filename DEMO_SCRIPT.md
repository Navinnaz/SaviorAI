# 🎭 SaviorAI Live Demo Script (5 Minutes)

## Setup (Before Demo)
- Backend running: `python -m backend.main`
- Frontend running: `npm run dev` (port 3001)
- Demo data loaded: `python -m backend.utils.demo_runner --setup`
- Dashboard open: http://localhost:3001

---

## PART 1: Introduction (30 seconds)

**[Show Dashboard]**

> "This is SaviorAI - an autonomous mental health monitoring system for educational institutions. We're monitoring 50 students at IIT Delhi in real-time."

**[Point to screen]**

> "Green cards are stable students. Yellow are at-risk. Red are crisis cases requiring immediate intervention. This isn't just data visualization - this is a fully autonomous AI system making life-saving decisions."

---

## PART 2: The Problem (30 seconds)

> "Student mental health is in crisis. Traditional counseling can't scale - one counselor for 1000+ students. Students hide their struggles until it's too late. We needed an AI system that could:"

**[Count on fingers]**

1. **Detect** - Spot declining mental health early
2. **Decide** - Autonomously escalate when needed  
3. **Act** - Intervene before crisis hits
4. **Explain** - Show complete reasoning for every decision

> "Let me show you all four in action."

---

## PART 3: Autonomous Event Demo (2 minutes)

**[Switch to Terminal]**

> "I'm going to run our live demo scenario. Watch the terminal - you'll see four autonomous events unfold in real-time."

**[Run command]**
```bash
python -m backend.utils.demo_runner --live
```

### Event 1: Crisis Detection (15 seconds)

**[As terminal shows Event 1]**

> "Event 1: A student named Priya just sent a check-in - mood score of 1, didn't eat, one-word: 'empty'. Watch the AI pipeline:"

**[Point to terminal output]**

- "Sentiment analysis: -0.90 (highly concerning)"
- "HMM assessment: AT_RISK state detected"
- "Adversarial validator: Confirms this is genuine, not gaming"
- "Decision: Level 1 peer intervention triggered"

> "That's detection, decision, and action - all autonomous, all in 3 seconds."

### Event 2: Gaming Detection (15 seconds)

**[As Event 2 runs]**

> "Event 2: Another student has 14 consecutive perfect scores. Statistically impossible. Our adversarial AI catches students trying to game the system:"

**[Point to terminal]**

- "Zero variance - 70% confidence it's masking"
- "System flags for counselor follow-up"

> "This prevents false negatives that could miss real crisis."

### Event 3: Cohort Anomaly (15 seconds)

**[As Event 3 runs]**

> "Event 3: Now zooming out - the AI detects 100% of MECH-2023 batch declining simultaneously. This isn't individual burnout:"

**[Point to terminal]**

- "12 out of 12 students below baseline"
- "Average drop: 1.89 points"
- "Likely cause: Mid-semester exam stress"

> "System automatically generates institutional report for systemic intervention. One counselor can't fix a curriculum problem."

### Event 4: Action Log (15 seconds)

**[As Event 4 runs]**

> "Event 4: Complete audit trail. Every decision, every intervention, full AI reasoning visible. This is explainable AI - no black boxes."

---

## PART 4: Dashboard Impact (30 seconds)

**[Switch to Dashboard, Refresh]**

> "Now look at the dashboard..."

**[Point to changes]**

- "Priya's card - now showing at-risk assessment"
- "Gaming student - warning badge visible"  
- "Cohort alert banner - '12 students affected (100%)'"

**[Click Action Log]**

> "Here's the action log - 4 autonomous decisions made. Click any one..."

**[Expand an intervention]**

> "Full reasoning chain. Input data, sentiment score, HMM assessment, adversarial check, escalation logic, message sent. Complete transparency."

---

## PART 5: Live WhatsApp Demo (1 minute)

**[Switch to Terminal]**

> "Now for the live demo with my actual phone number."

**[Run command]**
```bash
python add_my_number.py
```

**[Show terminal output]**

> "System just added me and sent a WhatsApp check-in..."

**[Show phone - WhatsApp message received]**

> "Here's the message. I'll reply with a crisis signal..."

**[Type on phone]** `1 no terrible`

**[Send, then immediately switch to Dashboard]**

> "The webhook is processing... HMM analyzing... adversarial validating... and..."

**[Refresh Dashboard - your card appears RED]**

> "There's my card. Crisis detected in real-time."

**[Click your card]**

> "Full profile - my check-in, sentiment analysis, state assessment, intervention reasoning. This is the same pipeline processing 50 students daily."

---

## PART 6: Technical Deep-Dive (Optional, 30 seconds)

**[If time allows]**

> "Under the hood: Hidden Markov Model for burnout probability, GPT-4o for sentiment analysis, adversarial validator to catch gaming, cohort detector for systemic issues, intervention orchestrator making escalation decisions. All running autonomously, 24/7."

---

## CLOSING (30 seconds)

> "This is AI with agency. Not a chatbot. Not a dashboard. A system that detects, decides, acts, and explains - autonomously saving lives at scale."

**[Final screen - Dashboard with all students]**

> "One counselor, 1000 students, zero students falling through the cracks. That's SaviorAI."

---

## BACKUP: If Things Go Wrong

### Dashboard blank?
> "Let me restart the frontend... [Ctrl+Shift+R]"

### WhatsApp not arriving?
> "While the message sends, let me show you the action log from our automated tests..." [Skip to existing interventions]

### Terminal crashes?
> "The system already processed 50 students this morning. Let me show you the results..." [Just show dashboard]

---

## KEY TALKING POINTS

✅ **Autonomous**: Not supervised - makes decisions itself  
✅ **Real-time**: 3-second pipeline from check-in to intervention  
✅ **Scalable**: One system monitors 1000+ students  
✅ **Explainable**: Every decision has full reasoning chain  
✅ **Multi-level**: Peer nudges, counselor alerts, emergency escalation  
✅ **Anti-gaming**: Adversarial AI catches masking behavior  
✅ **Systemic**: Detects institutional problems, not just individual  

---

## TIMING BREAKDOWN

| Section | Duration | Critical? |
|---------|----------|-----------|
| Intro | 30s | Yes |
| Problem | 30s | Yes |
| --live demo | 2m | YES |
| Dashboard | 30s | Yes |
| WhatsApp | 1m | If time |
| Technical | 30s | Optional |
| Closing | 30s | Yes |

**Total: 5 minutes** (3.5 min minimum without WhatsApp/technical)

---

**Practice this 3 times. Memorize transitions. You've got this! 🚀**
