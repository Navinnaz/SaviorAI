# ✅ WhatsApp Live Demo — READY

## What Was Added

### 1. Modified `add_my_number.py`:
- ✅ Phone validation (+91XXXXXXXXXX format)
- ✅ Upsert logic (update if exists)
- ✅ Sets batch="DEMO-LIVE", year=3
- ✅ **Sends WhatsApp check-in prompt automatically**
- ✅ Beautiful terminal output with instructions

### 2. Added to `backend/services/whatsapp.py`:
- ✅ `send_checkin_prompt()` function
- ✅ Sends formatted check-in message via Twilio

---

## 🎬 Live Demo Flow (Part 4 of Presentation)

### Step 1: Run Script
```bash
cd C:\Users\g_and\SaviorAI
python add_my_number.py
```

**Output**:
```
✅ Added student: Navin Nazerine
   Phone: +919944906759
   Batch: DEMO-LIVE
   Student ID: xxx-xxx-xxx

📱 Sending WhatsApp check-in prompt to +919944906759...
✅ Check-in message sent to +919944906759

======================================================================
⏳ Waiting for your reply...
======================================================================

📲 On your phone, reply to the WhatsApp message:
   Format: [1-5] [yes/no] [one word]
   Example: 1 no terrible

🔄 Once you reply:
   1. The webhook will process your message automatically
   2. Refresh the dashboard to see your card appear
   3. Click your card to see the real-time check-in

🎯 Dashboard: http://localhost:3001
======================================================================
```

### Step 2: WhatsApp Message Arrives
Your phone receives:
```
Hey! 👋 SaviorAI checking in.

Please reply in this format:
[1-5] [yes/mostly/no] [one word]

Example: 3 yes tired

• How was your day? (1=terrible, 5=amazing)
• Did you eat properly today?
• One word for how you're feeling?
```

### Step 3: Reply on WhatsApp
Send: `1 no terrible`

### Step 4: Webhook Fires (Automatic)
```
Incoming WhatsApp → Twilio → ngrok → POST /api/webhook
→ Parse "1 no terrible"
→ Sentiment analysis (GPT-4o)
→ HMM assessment
→ Adversarial validation
→ Intervention decision
→ Save to database
```

### Step 5: Dashboard Updates
1. Refresh: http://localhost:3001
2. Your card appears: "Navin Nazerine" (RED - crisis)
3. Click card → see full profile with check-in
4. Action Log shows intervention decision

---

## 🎤 Presentation Script

**Say**: "Now for the live demo. I'll add my actual phone number..."

**Do**: `python add_my_number.py`

**Say**: "The system just sent me a WhatsApp check-in. Let me reply with a crisis message..."

**Do**: Send `1 no terrible` on phone

**Say**: "The webhook is processing... [wait 2-3 seconds]... and there's my card on the dashboard!"

**Do**: Refresh dashboard, click your card

**Say**: "You can see the AI detected my crisis state in real-time, ran sentiment analysis, and logged the full reasoning chain. This is the same pipeline that processes 50 students daily."

---

## ⚙️ Prerequisites

### 1. Backend Running:
```bash
cd C:\Users\g_and\SaviorAI
python -m backend.main
```

### 2. Twilio Configured (Already Done):
```env
TWILIO_ACCOUNT_SID=AC7a333a2ff095b17c5526089df152d912
TWILIO_AUTH_TOKEN=efd529c263063458a879d1ced8809249
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### 3. Institution Exists:
Run if needed:
```bash
python -m backend.utils.demo_runner --scenario setup
```

---

## 🐛 Troubleshooting

### "Institution not found"
```bash
python -m backend.utils.demo_runner --scenario setup
```

### "Failed to send WhatsApp"
- Check `.env` has Twilio credentials
- Check backend is running
- Test with: `curl http://localhost:8000/health`

### "Webhook not receiving messages"
- Ensure ngrok is running (if testing locally)
- Check Twilio webhook URL is configured
- Test webhook: `POST http://localhost:8000/api/webhook`

### "Card not appearing on dashboard"
- Refresh browser (F5)
- Check Action Log for intervention
- Verify backend processed message (check logs)

---

## 📱 To Change Phone Number

Edit `add_my_number.py`:
```python
YOUR_PHONE = "+91YOURNUMBER"
YOUR_NAME = "Your Name"
```

Then run: `python add_my_number.py`

---

## ✅ Ready to Demo!

1. Run `add_my_number.py`
2. Reply on WhatsApp
3. Show dashboard update
4. Explain autonomous pipeline

**Total time**: 30 seconds 🚀
