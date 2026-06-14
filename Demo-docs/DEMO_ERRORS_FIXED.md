# ✅ Demo Runner Errors Fixed

## Problems Found & Fixed

### ❌ Issue 1: Duplicate Key Error on Setup
```
duplicate key value violates unique constraint "students_phone_key"
DETAIL: Key (phone)=(+919876500001) already exists.
```

**Cause:** Old demo data still in database from previous run

**Solution:** Always run `reset` before `setup`

```bash
# WRONG (causes duplicate key error)
.\run_demo.bat --scenario setup  # Data already exists!

# RIGHT (clean slate first)
.\run_demo.bat --scenario reset  # Clear old data
.\run_demo.bat --scenario setup  # Create fresh data
```

---

### ❌ Issue 2: Sentiment Score Type Error
```
invalid input for query argument $8: 'score' (must be real number, not str)
```

**Cause:** `analyze_sentiment()` returns a dict, not a tuple

**Fixed in:** `backend/utils/demo_runner.py`

**Before:**
```python
sentiment, sentiment_score = analyze_sentiment(one_word)  # ❌ Wrong!
```

**After:**
```python
sentiment_result = analyze_sentiment(one_word)
sentiment = sentiment_result["sentiment"]
sentiment_score = sentiment_result["score"]
```

---

### ⚠️ Issue 3: Datetime Deprecation Warning
```
datetime.datetime.utcnow() is deprecated
```

**Fixed in:** `backend/utils/demo_runner.py`

**Before:**
```python
"checked_in_at": datetime.utcnow(),  # ⚠️ Deprecated
```

**After:**
```python
"checked_in_at": datetime.now(datetime.UTC) if hasattr(datetime, 'UTC') else datetime.utcnow(),
```

---

## ✅ How to Run Demo Now

### Step 1: Reset Database (If You've Run Before)
```bash
.\run_demo.bat --scenario reset
```
Type `yes` when prompted.

### Step 2: Setup Fresh Data
```bash
.\run_demo.bat --scenario setup
```

### Step 3: Run Live Demo
```bash
.\run_demo.bat --scenario live
```

---

## 🔄 Complete Workflow

**First Time:**
```bash
.\run_demo.bat --scenario setup
.\run_demo.bat --scenario live
```

**Testing Multiple Times:**
```bash
.\run_demo.bat --scenario live  # Adds more events to existing data
.\run_demo.bat --scenario live  # Keeps adding...
```

**Before Judge Demo (Fresh Start):**
```bash
.\run_demo.bat --scenario reset   # ← THE KEY!
.\run_demo.bat --scenario setup
.\run_demo.bat --scenario live
```

---

## 🎯 What Each Command Does

### `reset`
- **Drops** all tables
- **Recreates** empty tables
- **Clears** all demo data
- **Duration:** 2 seconds
- **Safety:** Requires typing "yes"

### `setup`
- **Creates** 50 students
- **Generates** 700 check-ins (14 days)
- **Inserts** burnout states
- **Adds** pre-existing interventions
- **Duration:** 5-10 seconds
- **Result:** Institution ID displayed

### `live`
- **Simulates** 4 real-time events
- **Duration:** ~60 seconds
- **Events:** Crisis, gaming, cohort, action log
- **Result:** New data added to database

---

## 📊 Database State

**After reset:**
```
Students: 0
Check-ins: 0
Interventions: 0
```

**After setup:**
```
Students: 50
Check-ins: ~700
Interventions: ~15
```

**After live:**
```
Students: 50 (same)
Check-ins: ~702 (+2)
Interventions: ~16 (+1)
Cohort alerts: 1 (+1)
```

---

## 🚨 Common Errors & Solutions

### "duplicate key value violates"
**Solution:**
```bash
.\run_demo.bat --scenario reset
.\run_demo.bat --scenario setup
```

### "Demo data not found"
**Solution:**
```bash
.\run_demo.bat --scenario setup
```

### "OpenAI API key not found"
**This is OK!** Demo uses fallback templates.

To use GPT-4o-mini, add to `.env`:
```
OPENAI_API_KEY=sk-...
```

### "No gaming students found"
**This is OK!** Event 2 will skip gracefully.

Gaming patterns are created randomly by data_generator.

---

## ✅ Verification Steps

**After setup, check:**
```bash
# Should show 50
psql -d SaviorAI -c "SELECT COUNT(*) FROM students;"

# Should exist
psql -d SaviorAI -c "SELECT name FROM students WHERE name='Priya Sharma';"
```

**After live, check:**
```bash
# Should show ~702 (700 from setup + 2 from live)
psql -d SaviorAI -c "SELECT COUNT(*) FROM checkins;"

# Should show ~16 (15 from setup + 1 from live)
psql -d SaviorAI -c "SELECT COUNT(*) FROM interventions;"
```

---

## 🎬 Ready for Demo!

**Now you can run:**
```bash
# Test as many times as you want
.\run_demo.bat --scenario live

# Reset before judges
.\run_demo.bat --scenario reset
.\run_demo.bat --scenario setup
.\run_demo.bat --scenario live
```

---

## 📝 What Was Fixed

1. ✅ Sentiment analysis tuple unpacking → dict access
2. ✅ Datetime deprecation warning → timezone-aware datetime
3. ✅ Documentation on reset workflow

---

**All errors fixed! Demo runner is now fully functional.** 🚀

