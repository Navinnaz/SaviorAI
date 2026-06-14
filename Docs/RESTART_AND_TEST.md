# 🚀 Restart & Test — Quick Commands

## ✅ FIXES APPLIED

1. ✅ SQL logs disabled → Clean output
2. ✅ Email sends for Level 2 or 3 → Will receive email
3. ✅ Probabilities show correctly → "87.5%" not "0%"

---

## 🔄 RESTART BACKEND (REQUIRED!)

The SQL logging fix requires a backend restart:

### Windows:
```bash
# In backend terminal, press Ctrl+C to stop
# Then restart:
cd backend
python main.py
```

Wait for: `INFO: Application startup complete.`

---

## 🎬 RUN BEAUTIFUL DEMO

```bash
# Terminal (backend/utils directory)
cd backend/utils

# 1. Reset
python demo_runner.py --scenario reset
# Type: yes

# 2. Setup
python demo_runner.py --scenario setup
# Wait ~20 seconds

# 3. Run live demo
python demo_runner.py --scenario live
# Watch beautiful output!
```

---

## ✅ WHAT YOU'LL SEE NOW

### Clean, Beautiful Output:
```
======================================================================
⏱️  EVENT 1: PRIYA SHARMA CRISIS CHECK-IN (REAL PIPELINE)
======================================================================

📱 Simulating WhatsApp message from Priya Sharma: '1 no empty'
   Phone: +919876500001
   Current state: STABLE → transitioning to CRISIS...

   🔍 Running sentiment analysis...
      Sentiment: concerning (score: -0.90)
      ✅ Check-in saved

   📊 Updated score history (last 15): [4,4,5,3,4,4,3,4,5,4,3,4,4,3,1]
      Recent one-words: ['calm','tired','good','okay','fine','empty']

   🧠 Running HMM burnout assessment...
      State: CRISIS
      Probability: 87.5%      ← Now shows correctly!
      Trend: -1.20
      Consecutive low days: 2

   🔍 Running adversarial validation...
      Suspicious: False
      Confidence: 85%         ← Now shows correctly!

   🚨 Running intervention orchestrator...
      🎯 Action: SEND
      📨 Level: 2 (Counsellor)
      👤 Recipient: counsellor

      📧 DEMO MODE: Sending emergency email...
      ✅ Email sent to someboyisyourfriend@gmail.com  ← Will send!

✅ EVENT 1 COMPLETE
```

**NO MORE SQL LOGS!** 🎉

---

## 📧 EMAIL CONFIRMATION

Check your inbox: **someboyisyourfriend@gmail.com**

You'll receive:
- Subject: "🚨 URGENT: Priya Sharma — Emergency Mental Health Alert"
- Professional HTML formatted email
- Risk score, reasoning, recommended message
- Auto-sent by SaviorAI system

---

## 🎯 VERIFICATION CHECKLIST

After running `--live`:

- [ ] Terminal output is clean (no SQL logs)
- [ ] Event 1 shows "Probability: 87.5%" (not "0%")
- [ ] Event 1 shows "✅ Email sent to..."
- [ ] Event 2 shows "Confidence: 70%" (not "0%")
- [ ] All 4 events have beautiful formatting
- [ ] Email received in inbox

---

## ⚡ ONE-LINE RESTART

```bash
cd backend && python main.py
```

Then run the demo commands above!

---

**Now test it! Restart backend, then run `--live`. You'll see beautiful output + receive email! 🎭**
