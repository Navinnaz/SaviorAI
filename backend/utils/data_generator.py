"""
SaviorAI Demo Data Generator

Generates realistic synthetic data for demo purposes with distinct personas:
- Persona A: Crisis student (Priya Sharma) - flagship demo
- Persona B: Gaming students (3) - adversarial detection
- Persona C: Cohort anomaly (12 students in MECH-2023)
- Persona D: Normal students (rest) - realistic variance
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from uuid import uuid4, UUID


# Indian names for realistic demo
INDIAN_FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Sai", "Ayaan", "Aryan", "Reyansh",
    "Ananya", "Diya", "Aadhya", "Saanvi", "Pari", "Myra", "Anika", "Sara",
    "Kavya", "Riya", "Navya", "Prisha", "Ishaan", "Rohan", "Karan", "Dev",
    "Advait", "Vihaan", "Atharv", "Krishna", "Avani", "Kiara", "Shanaya",
    "Aarohi", "Krisha", "Nisha", "Tanvi", "Sneha", "Pooja", "Rahul", "Amit",
    "Nikhil", "Abhishek", "Siddharth", "Varun", "Akash", "Vikas", "Deepak"
]

INDIAN_LAST_NAMES = [
    "Kumar", "Singh", "Sharma", "Patel", "Gupta", "Reddy", "Rao", "Iyer",
    "Menon", "Nair", "Pillai", "Verma", "Joshi", "Desai", "Shah", "Mehta",
    "Agarwal", "Bansal", "Chopra", "Malhotra", "Khanna", "Bhatia", "Kapoor",
    "Sethi", "Dutta", "Ghosh", "Mukherjee", "Chatterjee", "Roy", "Das"
]

# PERMANENT DEMO INSTITUTION UUID
# This UUID is hardcoded and MUST match frontend/src/config.js DEMO_INSTITUTION_ID
# It will persist across --reset runs and should NEVER be deleted from the database
DEMO_INSTITUTION_UUID = UUID("88353031-000c-4b80-b091-89fe65849734")


class DemoDataGenerator:
    """Generate realistic demo data for SaviorAI."""
    
    def __init__(self):
        # Use the permanent demo institution UUID
        self.institution_id = DEMO_INSTITUTION_UUID
        self.students_data = []
        self.checkins_data = []
        self.burnout_states_data = []
        self.interventions_data = []
        self.cohort_alerts_data = []
        
    def generate_all(self, num_students: int = 50) -> Dict:
        """
        Generate all demo data.
        
        Returns dict with institution, students, check-ins, states, interventions.
        """
        print(f"🎭 Generating demo data for {num_students} students...")
        
        # Create institution
        institution = self._generate_institution()
        
        # Generate different persona types
        self._generate_persona_a_crisis()  # 1 student
        self._generate_persona_b_gaming(3)  # 3 students
        self._generate_persona_c_cohort(12)  # 12 students
        self._generate_persona_d_normal(num_students - 16)  # Rest
        
        print(f"✅ Generated {len(self.students_data)} students")
        print(f"✅ Generated {len(self.checkins_data)} check-ins")
        print(f"✅ Generated {len(self.burnout_states_data)} burnout states")
        print(f"✅ Generated {len(self.interventions_data)} interventions")
        print(f"✅ Generated {len(self.cohort_alerts_data)} cohort alerts")
        
        return {
            "institution": institution,
            "students": self.students_data,
            "checkins": self.checkins_data,
            "burnout_states": self.burnout_states_data,
            "interventions": self.interventions_data,
            "cohort_alerts": self.cohort_alerts_data
        }
    
    def _generate_institution(self) -> Dict:
        """Generate demo institution."""
        return {
            "id": self.institution_id,
            "name": "IIT Delhi",
            "type": "college",
            "city": "New Delhi",
            "state": "Delhi",
            "counsellor_phone": "+919876543210",
            "counsellor_email": "counsellor@iitd.ac.in"
        }
    
    def _generate_persona_a_crisis(self):
        """
        PERSONA A: Priya Sharma - Flagship demo student.
        
        STABLE 14-day pattern for demo initialization.
        Will transition to crisis during --live scenario.
        """
        student_id = uuid4()
        
        # Student info
        student = {
            "id": student_id,
            "name": "Priya Sharma",
            "phone": "+919876500001",
            "email": "priya.sharma@iitd.ac.in",
            "institution_id": self.institution_id,
            "batch": "CSE-2022",
            "year_of_study": 3,
            "is_active": True,
            "baseline_score": 3.8,
            "consent_given": True
        }
        self.students_data.append(student)
        
        # STABLE 14-day pattern - GREEN card on dashboard
        scores = [4, 4, 5, 3, 4, 4, 3, 4, 5, 4, 3, 4, 4, 3]
        onewords = [
            "good", "okay", "great", "tired", "good", "focused", "okay",
            "good", "amazing", "calm", "tired", "good", "okay", "fine"
        ]
        sentiments = [
            "positive", "neutral", "positive", "neutral", "positive", "positive", "neutral",
            "positive", "positive", "positive", "neutral", "positive", "neutral", "neutral"
        ]
        ate_properly = [
            "yes", "yes", "yes", "mostly", "yes", "yes", "mostly",
            "yes", "yes", "yes", "mostly", "yes", "yes", "yes"
        ]
        
        # Generate check-ins
        for i in range(14):
            checkin = {
                "id": uuid4(),
                "student_id": student_id,
                "checked_in_at": datetime.utcnow() - timedelta(days=13-i, hours=20),
                "mood_score": scores[i],
                "ate_properly": ate_properly[i],
                "one_word": onewords[i],
                "sentiment": sentiments[i],
                "sentiment_score": self._sentiment_to_score(sentiments[i]),
                "raw_message": f"{scores[i]} {ate_properly[i]} {onewords[i]}",
                "skipped": False
            }
            self.checkins_data.append(checkin)
        
        # Burnout state: STABLE (will be computed properly after setup)
        # Calculate proper state based on stable scores
        avg_score = sum(scores) / len(scores)  # Should be ~3.9
        trend = avg_score - student["baseline_score"]  # ~0.1
        
        burnout_state = {
            "id": uuid4(),
            "student_id": student_id,
            "assessed_at": datetime.utcnow() - timedelta(minutes=10),
            "state": "stable",
            "hmm_probability": 0.15,  # Low probability of burnout
            "trend_score": trend,
            "consecutive_low_days": 0,
            "variance_flag": False,
            "cohort_flag": False
        }
        self.burnout_states_data.append(burnout_state)
        
        # NO pre-created interventions - she's stable!
        # Intervention will be triggered during --live scenario
        
        print("  ✅ Persona A: Priya Sharma (STABLE) - demo ready for live crisis injection")
    
    def _generate_persona_b_gaming(self, count: int):
        """
        PERSONA B: Gaming students - adversarial detection demo.
        
        Always report perfect scores to game the system.
        """
        for i in range(count):
            student_id = uuid4()
            name = f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}"
            
            student = {
                "id": student_id,
                "name": name,
                "phone": f"+91987650{100+i:04d}",
                "email": f"{name.lower().replace(' ', '.')}@iitd.ac.in",
                "institution_id": self.institution_id,
                "batch": random.choice(["CSE-2022", "ECE-2023", "CSE-2023"]),
                "year_of_study": random.randint(2, 4),
                "is_active": True,
                "baseline_score": 4.0,
                "consent_given": True
            }
            self.students_data.append(student)
            
            # Perfectly flat pattern - obvious gaming
            for day in range(14):
                checkin = {
                    "id": uuid4(),
                    "student_id": student_id,
                    "checked_in_at": datetime.utcnow() - timedelta(days=13-day, hours=20),
                    "mood_score": 4,
                    "ate_properly": "yes",
                    "one_word": random.choice(["fine", "good", "fine", "good"]),
                    "sentiment": "positive",
                    "sentiment_score": 0.5,
                    "raw_message": "4 yes fine",
                    "skipped": False
                }
                self.checkins_data.append(checkin)
            
            # Burnout state with variance flag
            burnout_state = {
                "id": uuid4(),
                "student_id": student_id,
                "assessed_at": datetime.utcnow() - timedelta(hours=2),
                "state": "stable",
                "hmm_probability": 0.15,
                "trend_score": 0.0,  # No variance at all
                "consecutive_low_days": 0,
                "variance_flag": True,  # FLAGGED by adversarial validator
                "cohort_flag": False
            }
            self.burnout_states_data.append(burnout_state)
            
            # Level 1 intervention for gaming detection
            intervention = {
                "id": uuid4(),
                "student_id": student_id,
                "triggered_at": datetime.utcnow() - timedelta(hours=2),
                "level": 1,
                "trigger_reason": (
                    f"Adversarial gaming detected for {name}. "
                    "Pattern analysis: Zero variance in 14-day scores (all 4/5). "
                    "Statistical impossibility: σ²=0.00 (expected >0.5). "
                    "One-word responses show no emotional variation. "
                    "Likely masking true mental state."
                ),
                "action_taken": "send_masking_alert",
                "message_sent": (
                    f"Hi {name.split()[0]}, we noticed your check-ins have been consistently high. "
                    "That's great if you're genuinely doing well! 😊\n\n"
                    "However, we also know that sometimes students feel pressure to report "
                    "positive scores even when they're struggling.\n\n"
                    "Remember: This system is here to help, not judge. "
                    "It's okay to be honest about difficult days. "
                    "Your responses are confidential and help us provide better support.\n\n"
                    "If you'd like to talk to someone, our counsellor is available."
                ),
                "recipient": "student",
                "was_acknowledged": False,
                "outcome": "pending"
            }
            self.interventions_data.append(intervention)
        
        print(f"  ✅ Persona B: {count} gaming students (adversarial detection)")
    
    def _generate_persona_c_cohort(self, count: int):
        """
        PERSONA C: Cohort anomaly - examination hell scenario.
        
        All 12 students in MECH-2023 declined simultaneously in last 5 days.
        """
        for i in range(count):
            student_id = uuid4()
            name = f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}"
            baseline = random.uniform(3.5, 4.2)
            
            student = {
                "id": student_id,
                "name": name,
                "phone": f"+91987650{200+i:04d}",
                "email": f"{name.lower().replace(' ', '.')}@iitd.ac.in",
                "institution_id": self.institution_id,
                "batch": "MECH-2023",  # Same batch for cohort detection
                "year_of_study": 2,
                "is_active": True,
                "baseline_score": baseline,
                "consent_given": True
            }
            self.students_data.append(student)
            
            # First 9 days: normal around baseline
            # Last 5 days: sudden 1.5+ point drop (examination stress)
            for day in range(14):
                if day < 9:
                    # Normal period
                    score = int(baseline + random.uniform(-0.5, 0.5))
                    score = max(1, min(5, score))
                    oneword = random.choice(["okay", "good", "fine", "tired", "busy"])
                    sentiment = "neutral"
                    ate = "yes"
                else:
                    # Examination hell - sudden decline
                    score = max(1, int(baseline - random.uniform(1.5, 2.5)))
                    oneword = random.choice(["stressed", "overwhelmed", "exhausted", "anxious", "drained", "worried"])
                    sentiment = "negative"
                    ate = random.choice(["mostly", "no", "mostly"])
                
                checkin = {
                    "id": uuid4(),
                    "student_id": student_id,
                    "checked_in_at": datetime.utcnow() - timedelta(days=13-day, hours=20),
                    "mood_score": score,
                    "ate_properly": ate,
                    "one_word": oneword,
                    "sentiment": sentiment,
                    "sentiment_score": self._sentiment_to_score(sentiment),
                    "raw_message": f"{score} {ate} {oneword}",
                    "skipped": False
                }
                self.checkins_data.append(checkin)
            
            # Burnout state: at_risk with cohort flag
            current_avg = (baseline - 1.8)  # Average after decline
            burnout_state = {
                "id": uuid4(),
                "student_id": student_id,
                "assessed_at": datetime.utcnow() - timedelta(hours=1),
                "state": "at_risk",
                "hmm_probability": random.uniform(0.55, 0.75),
                "trend_score": -1.8,
                "consecutive_low_days": random.randint(3, 5),
                "variance_flag": False,
                "cohort_flag": True  # Part of cohort anomaly
            }
            self.burnout_states_data.append(burnout_state)
        
        # Create cohort alert
        cohort_alert = {
            "id": uuid4(),
            "institution_id": self.institution_id,
            "batch": "MECH-2023",
            "detected_at": datetime.utcnow() - timedelta(hours=1),
            "affected_students": count,
            "affected_percentage": 100.0,  # All students in batch
            "avg_score_drop": 1.8,
            "likely_cause": (
                "Batch-wide stress pattern detected. Analysis:\n\n"
                "• 100% of MECH-2023 students showed simultaneous decline\n"
                "• Average score drop: 1.8 points from baseline\n"
                "• Timing: Last 5 days (corresponds to mid-semester examination period)\n"
                "• Common keywords: 'stressed', 'overwhelmed', 'exhausted'\n"
                "• Eating pattern disruption in 75% of students\n\n"
                "Likely cause: Mid-semester examination stress\n\n"
                "This is a systemic issue affecting the entire cohort, "
                "not individual student problems."
            ),
            "institutional_action_recommended": (
                "INSTITUTIONAL INTERVENTION RECOMMENDED:\n\n"
                "1. IMMEDIATE (24-48 hours):\n"
                "   • Counsellor group session for MECH-2023\n"
                "   • Stress management workshop\n"
                "   • Extend assignment deadlines if possible\n\n"
                "2. SHORT-TERM (1 week):\n"
                "   • Review examination schedule for bunching\n"
                "   • Provide study resources and peer mentoring\n"
                "   • Set up office hours with faculty\n\n"
                "3. LONG-TERM (this semester):\n"
                "   • Review MECH-2023 curriculum load\n"
                "   • Schedule wellness check-ins\n"
                "   • Consider workload redistribution\n\n"
                "This requires department-level action, not just counselling."
            ),
            "acknowledged": False
        }
        
        # Store as special field
        self.cohort_alerts_data.append(cohort_alert)
        
        print(f"  ✅ Persona C: {count} students in MECH-2023 (cohort anomaly)")
    
    def _generate_persona_d_normal(self, count: int):
        """
        PERSONA D: Normal students with realistic variance.
        
        Mix of improving, stable, and occasional dips.
        """
        batches = ["CSE-2022", "CSE-2023", "ECE-2023", "CSE-2024"]
        
        for i in range(count):
            student_id = uuid4()
            name = f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}"
            baseline = random.uniform(2.8, 4.0)
            batch = random.choice(batches)
            
            student = {
                "id": student_id,
                "name": name,
                "phone": f"+91987650{300+i:04d}",
                "email": f"{name.lower().replace(' ', '.')}@iitd.ac.in",
                "institution_id": self.institution_id,
                "batch": batch,
                "year_of_study": random.randint(1, 4),
                "is_active": True,
                "baseline_score": baseline,
                "consent_given": True
            }
            self.students_data.append(student)
            
            # Generate realistic variance pattern
            trajectory = random.choice(["improving", "stable", "dip_and_recover"])
            
            for day in range(14):
                if trajectory == "improving":
                    # Gradual improvement
                    score = baseline + (day * 0.1) + random.uniform(-0.5, 0.5)
                elif trajectory == "stable":
                    # Stable with normal variance
                    score = baseline + random.uniform(-0.7, 0.7)
                else:  # dip_and_recover
                    # Dip in middle, then recover
                    if 5 <= day <= 9:
                        score = baseline - 1.0 + random.uniform(-0.5, 0.5)
                    else:
                        score = baseline + random.uniform(-0.5, 0.5)
                
                score = int(max(1, min(5, score)))
                
                # Generate realistic one-word based on score
                if score >= 4:
                    oneword = random.choice(["good", "happy", "motivated", "energized", "focused"])
                    sentiment = "positive"
                    ate = "yes"
                elif score == 3:
                    oneword = random.choice(["okay", "fine", "tired", "busy", "alright"])
                    sentiment = "neutral"
                    ate = random.choice(["yes", "mostly"])
                elif score == 2:
                    oneword = random.choice(["stressed", "tired", "overwhelmed", "anxious", "worried"])
                    sentiment = "negative"
                    ate = random.choice(["mostly", "no"])
                else:  # score == 1
                    oneword = random.choice(["exhausted", "drained", "lost", "hopeless", "empty"])
                    sentiment = "concerning"
                    ate = "no"
                
                checkin = {
                    "id": uuid4(),
                    "student_id": student_id,
                    "checked_in_at": datetime.utcnow() - timedelta(days=13-day, hours=20),
                    "mood_score": score,
                    "ate_properly": ate,
                    "one_word": oneword,
                    "sentiment": sentiment,
                    "sentiment_score": self._sentiment_to_score(sentiment),
                    "raw_message": f"{score} {ate} {oneword}",
                    "skipped": False
                }
                self.checkins_data.append(checkin)
            
            # Calculate current state
            recent_avg = sum([c["mood_score"] for c in self.checkins_data[-7:]]) / 7
            trend = recent_avg - baseline
            
            if recent_avg >= baseline + 0.3:
                state = "stable"
                prob = random.uniform(0.1, 0.3)
            elif recent_avg >= baseline - 0.5:
                state = "stable"
                prob = random.uniform(0.2, 0.4)
            elif recent_avg >= baseline - 1.0:
                state = "at_risk"
                prob = random.uniform(0.4, 0.6)
            else:
                state = "at_risk"
                prob = random.uniform(0.6, 0.7)
            
            burnout_state = {
                "id": uuid4(),
                "student_id": student_id,
                "assessed_at": datetime.utcnow() - timedelta(minutes=30),
                "state": state,
                "hmm_probability": prob,
                "trend_score": trend,
                "consecutive_low_days": max(0, int((baseline - recent_avg) * 2)),
                "variance_flag": False,
                "cohort_flag": False
            }
            self.burnout_states_data.append(burnout_state)
        
        print(f"  ✅ Persona D: {count} normal students (realistic variance)")
    
    def _sentiment_to_score(self, sentiment: str) -> float:
        """Convert sentiment to numerical score."""
        mapping = {
            "positive": 0.6,
            "neutral": 0.0,
            "negative": -0.5,
            "concerning": -0.8
        }
        return mapping.get(sentiment, 0.0)


def generate_demo_data(num_students: int = 50) -> Dict:
    """
    Generate complete demo dataset.
    
    Args:
        num_students: Total number of students to generate (default 50)
    
    Returns:
        Dict with institution, students, check-ins, states, interventions
    """
    generator = DemoDataGenerator()
    return generator.generate_all(num_students)

