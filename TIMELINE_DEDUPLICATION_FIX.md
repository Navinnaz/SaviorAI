# Timeline Deduplication Fix

## Issue
Student profile timeline showed multiple bars with same percentage (e.g., three "CRISIS 95%" bars for Priya Sharma).

## Root Cause
When running demo scenarios, multiple HMM assessments can be triggered for the same student on the same day:
1. Initial demo setup runs historical assessments
2. `--scenario live` triggers a crisis check-in → new assessment
3. Any additional check-ins trigger more assessments

**Example (Priya Sharma):**
- 2026-06-13: CRISIS 95% (Trend -1.8, 6 consec low days)
- 2026-06-13: CRISIS 95% (Trend -2.4, 9 consec low days) ← after live demo
- 2026-06-13: CRISIS 95% (Trend -2.6, 10 consec low days) ← after another event

All three are **technically valid** assessments, but visually confusing to see 3 identical bars.

## Solution
Modified `frontend/src/pages/StudentProfile.jsx` to show **only the most recent assessment per day**.

### Implementation:
```javascript
// Show only the most recent assessment per day for cleaner timeline
state_history.reduce((acc, state) => {
  const date = new Date(state.assessed_at).toLocaleDateString()
  // Keep only the last assessment for each date
  const existingIndex = acc.findIndex(s => 
    new Date(s.assessed_at).toLocaleDateString() === date
  )
  if (existingIndex >= 0) {
    // Replace with later assessment
    if (new Date(state.assessed_at) > new Date(acc[existingIndex].assessed_at)) {
      acc[existingIndex] = state
    }
  } else {
    acc.push(state)
  }
  return acc
}, [])
```

### Visual Improvement:
**Before:**
```
2026-06-13: CRISIS (95%)
2026-06-13: CRISIS (95%)
2026-06-13: CRISIS (95%)
```

**After:**
```
2026-06-13: CRISIS (95%)
```

Added footer text: `"Showing most recent assessment per day. Total assessments: X"`

## Verification

### Check No Duplicate Students:
```powershell
python check_duplicates.py
```
✅ Result: 50 unique students, no duplicates

### Check Priya's Assessments:
```powershell
python check_priya_states.py
```
Result: 3 assessments on 2026-06-13 (all CRISIS, slightly different trends)

### Frontend Display:
- **Before**: 3 bars on same date
- **After**: 1 bar per date (most recent)
- Timeline now clearly shows progression over multiple days

## When This Happens
Multiple assessments on same day occur when:
1. Running `--scenario live` after `--scenario setup` (adds real-time check-in)
2. Manual check-ins via WhatsApp while demo is running
3. Testing intervention flows (which trigger reassessment)

## Production Behavior
In production with real students:
- Students check in once per day (morning prompt)
- One HMM assessment per check-in
- Timeline naturally shows one bar per day
- This deduplication is a safety measure for demo scenarios

## Files Changed
- ✅ `frontend/src/pages/StudentProfile.jsx` - Timeline deduplication logic

## Testing
1. Refresh frontend (Ctrl+Shift+R)
2. Click Priya Sharma's profile
3. Timeline should show 1-2 bars (one per unique date)
4. Footer shows total assessment count
5. Each bar represents the most recent state for that day

## Alternative Approach (Not Implemented)
Could also deduplicate at backend level in `dashboard.py`:
```python
# In get_student_profile endpoint
# Group by date and take max(assessed_at) per day
from sqlalchemy import func, and_
state_history_result = await db.execute(
    select(models.BurnoutState)
    .where(...)
    .group_by(func.date(models.BurnoutState.assessed_at))
    .having(models.BurnoutState.assessed_at == func.max(models.BurnoutState.assessed_at))
)
```

Chose frontend deduplication for simplicity and to preserve full data access for debugging.

## Impact
- ✅ Cleaner visual timeline (no duplicate bars)
- ✅ Preserves all assessment data (visible in footer count)
- ✅ Shows state progression across different days
- ✅ Most recent assessment per day (highest fidelity)
- ✅ No database changes needed

