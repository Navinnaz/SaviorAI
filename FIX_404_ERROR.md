# ✅ Fix 404 Error - Institution ID Mismatch

## Problem

```
GET /api/dashboard/06d5af82-b343-4ccc-a5e9-6f01bebfaf41/overview HTTP/1.1" 404 Not Found
```

**Cause:** Frontend is using OLD institution ID, but database was reset and has NEW institution ID.

---

## ✅ Quick Fix (Do This Now!)

**Open your browser console (press F12) and run these 2 commands:**

```javascript
localStorage.setItem('institutionId', 'b913b940-18b2-4bd4-9055-80a042717b17')
location.reload()
```

**Or in one line:**

```javascript
localStorage.setItem('institutionId', 'b913b940-18b2-4bd4-9055-80a042717b17'); location.reload()
```

---

## What Happened

1. **Old setup:** Created institution with ID `06d5af82-b343-4ccc-a5e9-6f01bebfaf41`
2. **You ran:** `.\run_demo.bat --scenario reset` (deleted everything)
3. **You ran:** `.\run_demo.bat --scenario setup` (created NEW institution with NEW ID)
4. **New ID:** `b913b940-18b2-4bd4-9055-80a042717b17`
5. **Frontend:** Still looking for OLD ID → 404 error

---

## How localStorage Works

The frontend stores the institution ID in browser localStorage:

```javascript
// frontend/src/utils/api.js
const getInstitutionId = () => {
  return localStorage.getItem('institutionId') || '06d5af82-...'
}
```

When you reset the database, the OLD ID is deleted, but the frontend still has it cached in localStorage.

---

## Alternative: Clear All localStorage

**Option 1: Clear everything (loses all browser cache)**

```javascript
localStorage.clear()
location.reload()
```

**Option 2: Just update institution ID (recommended)**

```javascript
localStorage.setItem('institutionId', 'b913b940-18b2-4bd4-9055-80a042717b17')
location.reload()
```

---

## For Future Demos

**Every time you run `--scenario reset` + `--scenario setup`, you need to update the institution ID in the browser!**

**The setup script now prints the exact command to run:**

```
🎯 Next steps:
   4. ⚠️  IMPORTANT: Update institution ID in browser:
      Open browser console (F12) and run:
      localStorage.setItem('institutionId', 'b913b940-18b2-4bd4-9055-80a042717b17')
      location.reload()
```

Just copy-paste those two lines into your browser console after every reset+setup!

---

## Verify It Works

**After updating localStorage, the dashboard should load without 404 errors.**

**Check the browser console for:**
```
✅ No more "API Error: 404"
✅ Dashboard shows student cards
✅ Overview statistics visible
```

---

## Complete Workflow for Judges

```bash
# 1. Reset database
.\run_demo.bat --scenario reset

# 2. Create fresh data
.\run_demo.bat --scenario setup
# ↑ Copy the institution ID from output!

# 3. Update browser (open console - F12)
# Paste these two lines:
localStorage.setItem('institutionId', '<paste-institution-id-here>')
location.reload()

# 4. Run live demo
.\run_demo.bat --scenario live
```

---

## Why This Happens

UUIDs are generated randomly, so every time you run `--scenario setup`, you get a **new** random institution ID. This is intentional for database isolation, but requires updating the frontend reference.

**Alternative approaches (not implemented):**
- Use fixed UUID in setup script (loses isolation benefit)
- Auto-update frontend config file (requires file write permissions)
- API endpoint to list institutions (current approach with localStorage is simpler)

---

## ✅ Do This Now

1. **Open browser console** (F12 in Chrome/Edge/Firefox)
2. **Paste and run:**
   ```javascript
   localStorage.setItem('institutionId', 'b913b940-18b2-4bd4-9055-80a042717b17')
   location.reload()
   ```
3. **Dashboard should load** without 404 errors
4. **You'll see:** Student cards, overview stats, heatmap, cohorts

---

**That's it! The 404 error will be gone.** 🎉
