"""
SaviorAI SQLAlchemy Models
Maps to PostgreSQL schema defined in Section 3
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text,
    ForeignKey, CheckConstraint, UUID as SQLAlchemyUUID
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from .connection import Base


class Institution(Base):
    """Institutions using SaviorAI"""
    __tablename__ = "institutions"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    type = Column(String(50))  # 'college', 'coaching', 'school'
    city = Column(String(100))
    state = Column(String(100))
    counsellor_phone = Column(String(15))
    counsellor_email = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="institution")
    cohort_alerts = relationship("CohortAlert", back_populates="institution")
    
    def __repr__(self):
        return f"<Institution(id={self.id}, name='{self.name}', type='{self.type}')>"
    
    def to_dict(self):
        """Convert institution to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "city": self.city,
            "state": self.state,
            "counsellor_phone": self.counsellor_phone,
            "counsellor_email": self.counsellor_email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Student(Base):
    """Students enrolled in the system"""
    __tablename__ = "students"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String(100))
    institution_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("institutions.id"))
    batch = Column(String(50))  # e.g. "CSE-2022"
    year_of_study = Column(Integer)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    baseline_score = Column(Float, default=3.0)  # Personal baseline, updated weekly
    consent_given = Column(Boolean, default=False)
    consent_given_at = Column(DateTime(timezone=True))
    
    # Relationships
    institution = relationship("Institution", back_populates="students")
    checkins = relationship("CheckIn", back_populates="student", cascade="all, delete-orphan")
    burnout_states = relationship("BurnoutState", back_populates="student", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="student", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', batch='{self.batch}', active={self.is_active})>"
    
    def to_dict(self):
        """Convert student to dictionary for JSON serialization."""
        return {
            "id": str(self.id),
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "institution_id": str(self.institution_id) if self.institution_id else None,
            "batch": self.batch,
            "year_of_study": self.year_of_study,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
            "is_active": self.is_active,
            "baseline_score": self.baseline_score,
            "consent_given": self.consent_given,
            "consent_given_at": self.consent_given_at.isoformat() if self.consent_given_at else None
        }


class CheckIn(Base):
    """Every check-in response stored here"""
    __tablename__ = "checkins"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    checked_in_at = Column(DateTime(timezone=True), server_default=func.now())
    mood_score = Column(Integer, CheckConstraint("mood_score BETWEEN 1 AND 5"))
    ate_properly = Column(String(10))  # 'yes', 'mostly', 'no'
    one_word = Column(Text)  # Free text response
    sentiment = Column(String(20))  # 'positive', 'neutral', 'negative', 'concerning'
    sentiment_score = Column(Float)  # -1.0 to 1.0
    raw_message = Column(Text)  # Original WhatsApp message
    skipped = Column(Boolean, default=False)  # Did they skip today?
    
    # Relationships
    student = relationship("Student", back_populates="checkins")
    
    # Index for fast queries
    __table_args__ = (
        CheckConstraint("mood_score >= 1 AND mood_score <= 5", name="valid_mood_score"),
    )
    
    def __repr__(self):
        return f"<CheckIn(id={self.id}, student_id={self.student_id}, mood={self.mood_score}, at={self.checked_in_at})>"
    
    def to_dict(self):
        """Convert check-in to dictionary."""
        return {
            "id": str(self.id),
            "student_id": str(self.student_id),
            "checked_in_at": self.checked_in_at.isoformat() if self.checked_in_at else None,
            "mood_score": self.mood_score,
            "ate_properly": self.ate_properly,
            "one_word": self.one_word,
            "sentiment": self.sentiment,
            "sentiment_score": self.sentiment_score,
            "skipped": self.skipped
        }


class BurnoutState(Base):
    """HMM state transitions tracked here"""
    __tablename__ = "burnout_states"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
    state = Column(String(20), nullable=False)  # 'stable', 'at_risk', 'crisis'
    hmm_probability = Column(Float)  # Probability of current state
    trend_score = Column(Float)  # Recent avg vs baseline delta
    consecutive_low_days = Column(Integer)  # Days scored <= 2
    variance_flag = Column(Boolean, default=False)  # Adversarial gaming detected
    cohort_flag = Column(Boolean, default=False)  # Part of cohort anomaly
    
    # Relationships
    student = relationship("Student", back_populates="burnout_states")
    
    def __repr__(self):
        return f"<BurnoutState(id={self.id}, student_id={self.student_id}, state='{self.state}', prob={self.hmm_probability:.2f})>"
    
    def to_dict(self):
        """Convert burnout state to dictionary."""
        return {
            "id": str(self.id),
            "student_id": str(self.student_id),
            "assessed_at": self.assessed_at.isoformat() if self.assessed_at else None,
            "state": self.state,
            "hmm_probability": self.hmm_probability,
            "trend_score": self.trend_score,
            "consecutive_low_days": self.consecutive_low_days,
            "variance_flag": self.variance_flag,
            "cohort_flag": self.cohort_flag
        }


class Intervention(Base):
    """Every autonomous action taken by the agent"""
    __tablename__ = "interventions"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    level = Column(Integer, CheckConstraint("level BETWEEN 1 AND 4"), nullable=False)
    # 1=peer nudge, 2=counsellor soft, 3=emergency, 4=institutional
    trigger_reason = Column(Text)  # Agent's reasoning
    action_taken = Column(Text)  # What was sent/done
    message_sent = Column(Text)  # Actual message content
    recipient = Column(String(50))  # 'student', 'counsellor', 'emergency_contact'
    was_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True))
    outcome = Column(String(50))  # 'recovered', 'escalated', 'no_change', 'pending'
    
    # Relationships
    student = relationship("Student", back_populates="interventions")
    
    def __repr__(self):
        return f"<Intervention(id={self.id}, student_id={self.student_id}, level={self.level}, at={self.triggered_at})>"
    
    def to_dict(self):
        """Convert intervention to dictionary."""
        return {
            "id": str(self.id),
            "student_id": str(self.student_id),
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
            "level": self.level,
            "trigger_reason": self.trigger_reason,
            "action_taken": self.action_taken,
            "message_sent": self.message_sent,
            "recipient": self.recipient,
            "was_acknowledged": self.was_acknowledged,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "outcome": self.outcome
        }


class CohortAlert(Base):
    """Cohort-level anomaly events"""
    __tablename__ = "cohort_alerts"
    
    id = Column(SQLAlchemyUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institution_id = Column(SQLAlchemyUUID(as_uuid=True), ForeignKey("institutions.id"))
    batch = Column(String(50))
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    affected_students = Column(Integer)
    affected_percentage = Column(Float)
    avg_score_drop = Column(Float)
    likely_cause = Column(Text)  # GPT-4o inference
    institutional_action_recommended = Column(Text)
    acknowledged = Column(Boolean, default=False)
    
    # Relationships
    institution = relationship("Institution", back_populates="cohort_alerts")
    
    def __repr__(self):
        return f"<CohortAlert(id={self.id}, batch='{self.batch}', affected={self.affected_percentage}%, at={self.detected_at})>"
    
    def to_dict(self):
        """Convert cohort alert to dictionary."""
        return {
            "id": str(self.id),
            "institution_id": str(self.institution_id) if self.institution_id else None,
            "batch": self.batch,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
            "affected_students": self.affected_students,
            "affected_percentage": self.affected_percentage,
            "avg_score_drop": self.avg_score_drop,
            "likely_cause": self.likely_cause,
            "institutional_action_recommended": self.institutional_action_recommended,
            "acknowledged": self.acknowledged
        }

