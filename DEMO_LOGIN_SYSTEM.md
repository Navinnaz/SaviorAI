# Demo Institution Login System

## Overview

SaviorAI now has a permanent demo institution login system that eliminates the need to manually set `institutionId` in localStorage. The demo institution has a **fixed UUID** that persists across all `--reset` operations.

## Key Features

### 1. Login Page at Root Route
- Navigate to `http://localhost:5173/` to see the login page
- Two login options:
  - **Manual Login**: Enter any institution UUID
  - **Demo Login**: One-click access to the IIT Delhi demo with 50 students

### 2. Permanent Demo Institution UUID
```
88353031-000c-4b80-b091-89fe65849734
```

This UUID is:
- **Hardcoded** in `frontend/src/config.js` as `DEMO_INSTITUTION_ID`
- **Hardcoded** in `backend/utils/data_generator.py` as `DEMO_INSTITUTION_UUID`
- **Preserved** during `--reset` operations (only students are deleted)
- **Reused** when running `--setup` after a reset

### 3. Protected Dashboard Routes
All dashboard routes now require authentication:
- `/` - Login page (public)
- `/dashboard` - Main dashboard (protected)
- `/student/:studentId` - Student profile (protected)
- `/action-log` - Action log (protected)

If you try to access a protected route without being logged in, you'll be redirected to the login page.

### 4. Logout Functionality
Click the "Logout" button in the navigation bar to:
- Clear `institutionId` from localStorage
- Redirect to the login page

## Usage Workflow

### For Demo Day Presentations

1. **Initial Setup**
```bash
python -m backend.utils.demo_runner --scenario setup
```
- Creates or reuses the permanent demo institution
- Populates 50 students with 14 days of history

2. **Start Services**
```bash
# Terminal 1: Backend
python -m backend.main

# Terminal 2: Frontend
cd frontend
npm run dev
```

3. **Access Dashboard**
- Open browser to `http://localhost:5173/`
- Click **"🎭 Demo Login (IIT Delhi)"** button
- Dashboard loads immediately with all 50 students

4. **Between Demos (Reset)**
```bash
python -m backend.utils.demo_runner --scenario reset
```
- Deletes all students and related data
- **Preserves** the demo institution record
- Ready for fresh setup without changing UUID

5. **Fresh Setup After Reset**
```bash
python -m backend.utils.demo_runner --scenario setup
```
- Reuses the existing demo institution
- Creates fresh set of 50 students
- Same UUID works in frontend without changes

## Technical Details

### Frontend Configuration
**File**: `frontend/src/config.js`
```javascript
export const DEMO_INSTITUTION_ID = "88353031-000c-4b80-b091-89fe65849734";
export const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
```

### Backend Configuration
**File**: `backend/utils/data_generator.py`
```python
from uuid import UUID

DEMO_INSTITUTION_UUID = UUID("88353031-000c-4b80-b091-89fe65849734")

class DemoDataGenerator:
    def __init__(self):
        # Use the permanent demo institution UUID
        self.institution_id = DEMO_INSTITUTION_UUID
```

### Reset Behavior
**File**: `backend/utils/demo_runner.py`

The `--reset` scenario now:
1. Checks for the demo institution UUID
2. Deletes all `Student` records (CASCADE deletes handle related records)
3. Deletes all `CohortAlert` records
4. **Preserves** the `Institution` record with the demo UUID

### Setup Behavior
The `--setup` scenario now:
1. Checks if institution with demo UUID exists
2. If exists: reuses it
3. If not: creates new institution with the demo UUID
4. Creates fresh students linked to this institution

## Benefits

### Before (Manual localStorage Setup)
```javascript
// Required in browser console after every setup:
localStorage.setItem('institutionId', 'a8353031-000c-4b80-b091-89fe65849734')
location.reload()
```
- Tedious for demo presentations
- Easy to forget
- UUID changes on full reset
- Not user-friendly

### After (Demo Login System)
- Click one button to login
- UUID never changes
- Works across all resets
- Professional demo experience
- No console manipulation needed

## Files Modified

1. **Frontend**
   - `frontend/src/config.js` (NEW) - Configuration constants
   - `frontend/src/pages/Login.jsx` (NEW) - Login page component
   - `frontend/src/App.jsx` - Routing and authentication
   
2. **Backend**
   - `backend/utils/data_generator.py` - Fixed UUID constant
   - `backend/utils/demo_runner.py` - Preserve institution on reset

## Testing the System

1. **Test Login Flow**
```bash
# Start services
python -m backend.main
cd frontend && npm run dev

# Open http://localhost:5173/
# Should see login page, not dashboard
```

2. **Test Demo Login**
```bash
# Click "Demo Login" button
# Should redirect to /dashboard
# Should show 50 students
```

3. **Test Reset Persistence**
```bash
# Run reset
python -m backend.utils.demo_runner --scenario reset

# Run setup again
python -m backend.utils.demo_runner --scenario setup

# Refresh browser at /dashboard
# Same institution, fresh students
# No need to re-login!
```

4. **Test Logout**
```bash
# Click "Logout" in navigation
# Should redirect to login page
# localStorage.institutionId should be cleared
```

## Troubleshooting

### "No students found" after demo login
- Run: `python -m backend.utils.demo_runner --scenario setup`
- Institution exists but students were deleted

### "Cannot access /dashboard" 
- Check localStorage in browser console
- Should have `institutionId` key
- If missing, go to `/` and login again

### Different UUID in database
- Check `backend/utils/data_generator.py` has correct UUID
- Check `frontend/src/config.js` has matching UUID
- Run `--reset` and `--setup` to recreate with correct UUID

## Summary

The demo login system provides:
- ✅ Professional login experience
- ✅ Permanent demo institution UUID
- ✅ No manual localStorage manipulation
- ✅ Survives `--reset` operations
- ✅ One-click demo access
- ✅ Protected routes
- ✅ Logout functionality

Perfect for demo presentations where you need to reset and re-setup multiple times without losing the institution UUID or requiring manual browser configuration!
