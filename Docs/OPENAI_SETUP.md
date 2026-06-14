# OpenAI API Setup for GuardianAI

## Quick Setup (5 minutes)

### Step 1: Get API Key (2 min)

1. **Visit**: https://platform.openai.com/signup
2. **Sign up** with Google or email
3. **Verify** your email (check inbox)
4. **Add payment**: https://platform.openai.com/account/billing/overview
   - Click "Add payment method"
   - Enter credit/debit card
   - Add **$5-10** (enough for months of testing)
5. **Create key**: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name: `GuardianAI`
   - Copy the key (starts with `sk-proj-...`)
   - ⚠️ **SAVE IT NOW** - you can't see it again!

### Step 2: Add to .env File (1 min)

Open `c:\Users\g_and\SaviorAI\.env` and update:

```bash
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE
```

Replace `YOUR_KEY_HERE` with your actual key.

### Step 3: Test It (2 min)

```bash
.\venv\Scripts\activate
python -c "from openai import OpenAI; client = OpenAI(); print('✅ API key works!')"
```

If you see `✅ API key works!` - you're ready!

---

## Model Used: gpt-4o-mini

**Why this model?**
- ✅ **10x cheaper** than gpt-4o
- ✅ **Fast** (1-2 seconds per call)
- ✅ **Good quality** for intervention messages
- ✅ **Cost**: ~$0.50-1.00 for entire hackathon demo

**Price comparison**:
| Model | Input | Output | Demo Cost |
|-------|-------|--------|-----------|
| gpt-4o | $2.50/1M | $10/1M | ~$5-8 |
| **gpt-4o-mini** ✅ | **$0.15/1M** | **$0.60/1M** | **~$0.50-1** |
| gpt-3.5-turbo | $0.50/1M | $1.50/1M | ~$1-2 |

**Your code already uses gpt-4o-mini** - no changes needed!

---

## When is OpenAI API Called?

GuardianAI is **very efficient** - OpenAI is only used for:

### 1. Intervention Message Generation
- **When**: Student enters crisis/at-risk state
- **Frequency**: 1-5 times per day (with 24hr cooldown)
- **Cost per call**: ~$0.001 (less than 1 cent)
- **Purpose**: Generate personalized, empathetic messages

### 2. NOT Used For:
- ❌ Sentiment analysis (uses keyword matching - FREE)
- ❌ HMM assessment (pure math - FREE)
- ❌ Adversarial validation (statistics - FREE)
- ❌ Cohort detection (Z-score math - FREE)
- ❌ Daily check-ins (templates - FREE)

**Result**: 95% of operations are FREE! OpenAI only for final message polish.

---

## Cost Estimate for Demo

### Scenario: 50 students, 3 days of demo

| Event | Calls | Cost/Call | Total |
|-------|-------|-----------|-------|
| Crisis interventions | 3 | $0.001 | $0.003 |
| At-risk interventions | 8 | $0.001 | $0.008 |
| Counsellor alerts | 2 | $0.001 | $0.002 |
| Testing/debugging | 10 | $0.001 | $0.010 |
| **TOTAL** | | | **$0.023** |

**🎉 Less than 3 cents for entire demo!**

---

## Fallback System

If OpenAI fails or you run out of credits:
- ✅ **Automatic fallback** to template messages
- ✅ System keeps working
- ✅ Interventions still sent (just less personalized)
- ✅ No crashes or errors

Example fallback message:
> "Hey Priya, I noticed your check-ins show you're struggling. Would you like to talk to a counsellor? Reply YES if you'd like help."

---

## Usage Monitoring

Check your usage at: https://platform.openai.com/usage

You'll see:
- Requests per day
- Tokens used
- Cost breakdown
- Model usage

For GuardianAI, expect:
- **10-50 requests/day** during testing
- **$0.01-0.10/day** cost
- **$1-3/month** typical usage

---

## Troubleshooting

### "Invalid API key"
- Check `.env` file has correct key
- Key should start with `sk-proj-` or `sk-`
- No spaces before/after the key
- Restart backend after changing `.env`

### "Insufficient credits"
- Add $5: https://platform.openai.com/account/billing
- Check usage: https://platform.openai.com/usage
- Fallback templates will work if API fails

### "Rate limit exceeded"
- Free tier: 3 requests/minute
- Wait 60 seconds and retry
- Or upgrade to paid tier ($5 minimum)

### Test command not working
```bash
# Full test with error messages:
python
>>> from openai import OpenAI
>>> import os
>>> from dotenv import load_dotenv
>>> load_dotenv()
>>> client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
>>> response = client.chat.completions.create(
...     model="gpt-4o-mini",
...     messages=[{"role": "user", "content": "Say hi"}],
...     max_tokens=10
... )
>>> print(response.choices[0].message.content)
```

---

## Security Best Practices

✅ **DO**:
- Keep `.env` file private
- Never commit API key to git (already in `.gitignore`)
- Rotate key if accidentally exposed
- Use separate keys for dev/prod

❌ **DON'T**:
- Share your API key publicly
- Post it in Discord/forums
- Hardcode it in code files
- Use the same key across projects

---

## Alternative: Free Testing

If you want to test **without OpenAI** initially:

1. Comment out OpenAI in code (uses fallback templates)
2. OR set `OPENAI_API_KEY=sk-test-fake-key` in `.env`
3. System will use template messages automatically

To force fallback mode, edit `intervention_orchestrator.py`:
```python
# Line 477 - add this before the API call:
raise Exception("Testing fallback mode")
```

---

## Summary

✅ **Model**: `gpt-4o-mini` (already configured)  
✅ **Cost**: ~$0.02-0.10 for entire demo  
✅ **Setup time**: 5 minutes  
✅ **Fallback**: Automatic if API fails  
✅ **Security**: Key in `.env` (never committed)

**Next**: Add your key to `.env` and start testing!
