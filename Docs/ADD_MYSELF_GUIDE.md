# Adding Yourself to SaviorAI for Live WhatsApp Demo

## Quick Steps

### 1. Ensure Backend is Running
```powershell
# In terminal 1 (if not already running)
.\venv\Scripts\activate
python -m backend.main
```

### 2. Add Your Phone Number to Database
```powershell
# In terminal 2
.\venv\Scripts\activate
python add_my_number.py
```

**Expected Output:**
```
✅ Added student: Navin Nazerine
   Phone: +919944906759
   Student ID: <some-uuid>

🎉 You can now send WhatsApp check-ins!
```

**If Already Exists:**
```
✅ Student already exists: Navin Nazerine
```

### 3. Get Your Student ID
```powershell
python get_test_ids.py
```

This will show all students including yours with their IDs.

### 4. Send Test WhatsApp Message

**Format:**
```
<mood_score> <ate_properly> <one_word>
```

**Examples:**

**Good Day:**
```
5 yes happy
```

**Bad Day (Crisis):**
```
1 no empty
```

**Medium Day:**
```
3 yes tired
```

### 5. Check Dashboard
1. Refresh frontend (http://localhost:3000)
2. Look for your card: "Navin Nazerine"
3. Click to see your profile with check-in history

---

## Full WhatsApp Integration Test Flow

### Step 1: Set Up ngrok (if not already)
```powershell
# Start ngrok in terminal 3
.\ngrok http 8000
```

Copy the https URL (e.g., `https://abc123.ngrok.io`)

### Step 2: Update Webhook in Twilio
1. Go to [Twilio Console](https://console.twilio.com/us1/develop/sms/services)
2. Find your WhatsApp sender
3. Update webhook to: `https://abc123.ngrok.io/webhook/whatsapp`

### Step 3: Send WhatsApp Message
Send to: **WhatsApp Business number (your Twilio WhatsApp number)**

Message: `1 no empty`

### Step 4: Verify Processing
**Check Backend Logs:**
```
[INFO] Received WhatsApp message from +919944906759
[INFO] Parsed: mood=1, ate=no, word=empty
[INFO] Sentiment: concerning (score: -0.9)
[INFO] Check-in saved: <checkin-id>
[INFO] HMM assessment: CRISIS (probability: 4.8e-08)
[INFO] Intervention triggered: Level 2 - Counsellor Alert
```

**Check Dashboard:**
- Your card should show updated risk score
- State should change to "at_risk" or "crisis" (depending on history)
- Last check-in should show "just now" or "1m ago"

**Check Database:**
```powershell
python check_my_checkins.py
```

This shows all your check-ins with sentiments and HMM states.

---

## Demo Presentation Flow

### Setup (Before Presentation):
1. Run `.\run_demo.bat --scenario reset`
2. Run `.\run_demo.bat --scenario setup`
3. Update localStorage in browser console
4. Add yourself: `python add_my_number.py`
5. Start ngrok: `.\ngrok http 8000`
6. Update Twilio webhook to ngrok URL

### During Presentation:

**Part 1: Show Existing Data (5 min)**
- "Here's our SaviorAI dashboard monitoring 50 students"
- Show risk heatmap with Priya Sharma at top (crisis state)
- Click Priya's card → show her profile with timeline
- "She's scored 1-2 for 9 consecutive days, trend declining -2.4"
- Show intervention history (autonomous actions taken)

**Part 2: Simulate Real-Time Crisis (5 min)**
- Run `.\run_demo.bat --scenario live` in separate terminal
- Show logs as events happen:
  - Crisis check-in from Priya
  - HMM assessment runs
  - Intervention triggers
  - Counsellor alert sent
- Refresh dashboard → Priya's card updates
- "All of this happened autonomously, no human needed to intervene"

**Part 3: Live WhatsApp Demo (FINALE - 3 min)**
- "Now let me show you the real WhatsApp integration"
- Pull out your phone
- Send WhatsApp message: `1 no empty`
- Show backend logs processing in real-time
- Show Twilio webhook activity log
- Refresh dashboard → your card appears/updates
- "This is the actual system working end-to-end"
- Show your profile with the check-in that just came in

**Closing:**
- "Three-layer AI: HMM for state detection, Adversarial validator for gaming detection, Cohort detector for group patterns"
- "All autonomous, explainable, and ready for real deployment"

---

## Troubleshooting Live Demo

### Issue: Message Not Received
**Check:**
1. Backend running? (`python -m backend.main`)
2. ngrok running? (`.\ngrok http 8000`)
3. Twilio webhook updated with ngrok URL?
4. Phone number format correct? (+91XXXXXXXXXX)

**Debug:**
```powershell
# Check ngrok inspector
# Open http://localhost:4040 in browser
# See all incoming webhook requests
```

### Issue: Message Received But Not Processed
**Check Backend Logs:**
```
[ERROR] Student not found for phone +919944906759
```

**Solution:**
```powershell
python add_my_number.py
```

### Issue: Dashboard Not Updating
**Try:**
1. Hard refresh: Ctrl+Shift+R
2. Check localStorage has correct institutionId
3. Check API key in `frontend/src/utils/api.js`

### Issue: Risk Score Still Shows 0%
**Make sure:**
1. Backend restarted after code changes
2. Changes saved to `backend/routes/dashboard.py`
3. No syntax errors: `python -m py_compile backend/routes/dashboard.py`

---

## Scripts Reference

### `add_my_number.py`
Adds your phone number (+919944906759) to database as student

### `get_test_ids.py`
Shows all students with IDs (useful for testing)

### `check_my_checkins.py`
Shows all YOUR check-ins with details

### `run_demo.bat`
Main demo runner:
- `--scenario reset` - Wipe database
- `--scenario setup` - Add 50 students with 14 days history
- `--scenario live` - Simulate 4 real-time events

---

## Testing Checklist

Before presentation:
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] ngrok running and Twilio webhook updated
- [ ] Database reset and setup complete
- [ ] localStorage updated with institution ID
- [ ] Your number added: `python add_my_number.py`
- [ ] Test WhatsApp message sent and received
- [ ] Dashboard shows your card with check-in
- [ ] Risk scores displaying correctly (crisis = 85-95%)
- [ ] Heatmap sorted by risk (highest first)
- [ ] Student profile timeline shows percentages

Emergency backup:
- [ ] Screenshots of dashboard ready
- [ ] Video recording of WhatsApp demo as fallback
- [ ] Know how to restart backend if it crashes

---

## Post-Demo Next Steps

### If Demo Goes Well:
1. Clean up database: `.\run_demo.bat --scenario reset`
2. Keep your number in for testing: `python add_my_number.py`
3. Document any questions/feedback received
4. Note any features requested

### For Production Readiness:
1. Set up proper API key management (not hardcoded)
2. Add rate limiting to webhook endpoint
3. Set up error monitoring (Sentry/DataDog)
4. Add health check monitoring
5. Set up proper logging/alerting
6. Database backups and migration strategy
7. SSL/TLS for all endpoints
8. GDPR compliance review for student data

---

## You're All Set! 🎉

With these fixes:
- ✅ Risk scores display correctly (85-95% for crisis)
- ✅ Heatmap sorted automatically
- ✅ Student profiles show accurate timelines
- ✅ Your number ready for live WhatsApp demo
- ✅ Full autonomous agent pipeline working

**Break a leg with your presentation! 🚀**

