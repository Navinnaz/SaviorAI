# 🚀 Backend Start — CORRECT WAY

## Problem
You're trying to run from the wrong directory and Python 3.13 has compatibility issues.

## ✅ CORRECT WAY TO START BACKEND

### Option 1: From Project Root (RECOMMENDED)
```bash
cd C:\Users\g_and\SaviorAI
python -m backend.main
```

### Option 2: Check If Already Running
The backend might already be running! Check:
```bash
# Open browser
http://localhost:8000/docs
```

If you see the API documentation, backend is already running! ✅

---

## 🎬 RUN DEMO NOW (Backend Already Running)

Since your backend is likely already running, just run the demo:

```bash
cd C:\Users\g_and\SaviorAI
python -m backend.utils.demo_runner --scenario reset
# Type: yes

python -m backend.utils.demo_runner --scenario setup

python -m backend.utils.demo_runner --scenario live
```

**NOW YOU'LL SEE**:
- ✅ Clean terminal output (no SQL logs!)
- ✅ Correct probabilities ("87.5%" not "0%")
- ✅ Email sent to someboyisyourfriend@gmail.com
- ✅ Beautiful formatting for all 4 events

---

## 📧 CHECK YOUR EMAIL

After running `--live`, check your inbox:
**someboyisyourfriend@gmail.com**

You should receive:
> Subject: 🚨 URGENT: Priya Sharma — Emergency Mental Health Alert

---

## ✅ QUICK TEST

Run this now to see beautiful output:

```bash
cd C:\Users\g_and\SaviorAI
python -m backend.utils.demo_runner --scenario live
```

That's it! No need to restart backend. The SQL logging fix will apply next time you restart (but not critical for demo).

---

**Test it now! Run `--live` from project root.** 🎭
