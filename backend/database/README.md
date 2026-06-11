# GuardianAI Database Layer

## Overview

Complete async database layer for GuardianAI using SQLAlchemy 2.0 and asyncpg.

## Files

### `connection.py`
- Async PostgreSQL connection pool using asyncpg driver
- SQLAlchemy async engine configuration
- `get_db()` dependency for FastAPI routes
- `init_db()` and `close_db()` lifecycle management

### `models.py`
- Complete SQLAlchemy declarative models for all 6 tables:
  - `Institution` - Organizations using GuardianAI
  - `Student` - Enrolled students with personal baselines
  - `CheckIn` - Daily check-in responses
  - `BurnoutState` - HMM state transitions
  - `Intervention` - Autonomous actions taken
  - `CohortAlert` - Batch-level anomalies
- All relationships configured
- `__repr__()` methods for debugging
- `to_dict()` methods for JSON serialization

### `crud.py`
Complete set of async CRUD operations:

#### Student Operations
- `get_student_by_phone(db, phone)` - Find student by WhatsApp number
- `get_student_by_id(db, student_id)` - Get student with institution
- `get_all_students_by_institution(db, institution_id)` - List all students
- `update_student_baseline(db, student_id, new_baseline)` - Weekly baseline update

#### Check-in Operations
- `save_checkin(db, checkin_data)` - Save new check-in
- `get_recent_scores(db, student_id, days=14)` - Get mood score history
- `get_recent_onewords(db, student_id, days=7)` - Get one-word responses
- `get_all_checkins_for_student(db, student_id, days=30)` - Full check-in history

#### Burnout State Operations
- `save_burnout_state(db, student_id, assessment, validation)` - Save HMM result
- `get_latest_burnout_state(db, student_id)` - Get current state

#### Intervention Operations
- `get_last_intervention(db, student_id)` - Get most recent intervention
- `save_intervention(db, intervention_data)` - Log autonomous action
- `get_interventions_for_student(db, student_id, limit=10)` - Intervention history

#### Cohort Operations
- `get_cohort_data_by_batch(db, institution_id, batch)` - Get batch data for anomaly detection
- `save_cohort_alert(db, alert_data)` - Save cohort anomaly alert
- `get_active_cohort_alerts(db, institution_id)` - Get unacknowledged alerts

#### Analytics Operations
- `get_institution_statistics(db, institution_id)` - Dashboard stats

## Database Schema

All tables match the schema defined in `Section3.md`:
- Proper UUID primary keys
- Foreign key relationships with cascade delete
- Check constraints on scores (1-5)
- Indexes on frequently queried columns
- Timestamps with timezone support

## Usage Example

```python
from database import get_db
from database.crud import get_student_by_phone, get_recent_scores
from database.models import Student

# In a FastAPI route
@router.post("/webhook/whatsapp")
async def webhook(phone: str, db: AsyncSession = Depends(get_db)):
    # Get student
    student = await get_student_by_phone(db, phone)
    
    # Get their check-in history
    scores = await get_recent_scores(db, student.id, days=14)
    
    # All operations are async
    await db.commit()
```

## Type Hints

All functions include complete type hints using Python 3.11+ style:
- `AsyncSession` for database sessions
- `UUID` for all ID fields
- `List[T]`, `Optional[T]`, `Dict[str, Any]` for return types
- Proper dataclass types for agent assessments

## Performance Notes

- Connection pooling configured (10 connections, 20 max overflow)
- Indexes on frequently queried columns
- `selectinload()` used to prevent N+1 queries
- All queries use async/await for non-blocking I/O

## Testing

Test database operations with:
```bash
pytest backend/tests/test_crud.py -v
```

## Next Steps

After setting up models and CRUD:
1. Configure DATABASE_URL in `.env`
2. Run `python backend/main.py` to auto-create tables
3. Use `backend/utils/data_generator.py` to seed demo data
