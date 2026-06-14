## SECTION 8 — SYNTHETIC DEMO DATA GENERATOR

```python
# backend/utils/data_generator.py
"""
Generates 50 realistic synthetic students for demo.
Three persona archetypes with distinct trajectories.
Run this before demo: python data_generator.py
"""

import random
from datetime import datetime, timedelta

def generate_demo_students(db_session):
    
    # PERSONA TYPE A: Student in crisis (8 students)
    # Clear declining trajectory judges will see immediately
    crisis_pattern = [4, 4, 3, 4, 3, 3, 2, 2, 2, 1, 2, 1, 1, 2]
    
    # PERSONA TYPE B: Student gaming the system (5 students)
    # Suspiciously flat scores — adversarial validation flags this
    gaming_pattern = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    
    # PERSONA TYPE C: Normal variation (37 students)
    # Healthy variance, occasional dips, recoveries
    def normal_pattern():
        base = 3.5
        return [max(1, min(5, round(base + random.gauss(0, 0.8)))) for _ in range(14)]
    
    # One-word response pools per persona
    crisis_words = [
        "okay", "tired", "stressed", "exhausted", 
        "overwhelmed", "lost", "empty", "struggling"
    ]
    gaming_words = ["fine", "good", "great", "good", "fine", "okay"]
    normal_words = [
        "good", "tired", "okay", "happy", "stressed",
        "focused", "anxious", "motivated", "calm", "busy"
    ]
    
    # Demo flagship student: "Priya" — your main demo
    flagship = {
        "name": "Priya Sharma",
        "batch": "CSE-2022",
        "year": 2,
        "scores": crisis_pattern,
        "onewords": crisis_words[-len(crisis_pattern):],
        "persona": "crisis"
    }
    
    return flagship  # + rest of 50 students
```
