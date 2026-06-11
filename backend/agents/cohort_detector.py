"""
GuardianAI - Cohort Anomaly Detector

Detects systemic stressors affecting groups of students simultaneously.

This is what individual wellness apps CANNOT do.
When 60% of a batch declines together — it's not individual burnout.
It's a bad professor, an unfair exam, a hostel incident.
The institution needs to know, not just the individual counsellor.

Japan context: Maps directly to 'examination hell' (juken jigoku) where
entire cohorts deteriorate simultaneously before entrance exams.
"""

from typing import List, Dict, Literal
from datetime import datetime, timedelta
import statistics
import os
import logging
from uuid import UUID

logger = logging.getLogger(__name__)


class CohortAnomalyDetector:
    """
    Detects systemic stressors affecting groups of students simultaneously.
    
    This detector identifies when a significant portion of a batch (cohort)
    shows declining mental health patterns simultaneously, indicating a
    systemic stressor rather than individual burnout.
    
    Examples of systemic stressors:
    - Difficult exam period
    - Problematic professor/course
    - Hostel/campus incident
    - Administrative policy changes
    - Placement/job search pressure
    """
    
    def __init__(self):
        """Initialize detector with configurable thresholds from environment."""
        # Allow threshold configuration via environment variable
        self.COHORT_THRESHOLD = float(os.getenv("COHORT_THRESHOLD", "0.40"))
        self.SCORE_DROP_THRESHOLD = float(os.getenv("SCORE_DROP_THRESHOLD", "1.0"))
        self.MIN_BATCH_SIZE = int(os.getenv("MIN_BATCH_SIZE", "5"))
        
        logger.info(
            f"CohortAnomalyDetector initialized: "
            f"threshold={self.COHORT_THRESHOLD:.0%}, "
            f"drop={self.SCORE_DROP_THRESHOLD}, "
            f"min_size={self.MIN_BATCH_SIZE}"
        )
    
    def detect(
        self, 
        batch_data: List[Dict]   # [{"student_id": ..., "recent_avg": ..., "baseline": ...}]
    ) -> Dict:
        """
        Analyse a batch of students for cohort-level anomaly.
        
        Args:
            batch_data: List of dicts with keys:
                - student_id: str or UUID
                - recent_avg: float (average of recent 7 days)
                - baseline: float (personal baseline)
                - name: str (optional, for logging)
        
        Returns:
            Dict with:
            - anomaly_detected: bool
            - affected_count: int (if detected)
            - total_count: int (if detected)
            - affected_percentage: float (always)
            - average_score_drop: float (if detected)
            - severity: "high" | "medium" (if detected)
            - institutional_action: str (if detected)
            - reason: str (if not detected)
        """
        logger.info(f"Analyzing cohort of {len(batch_data)} students")
        
        if len(batch_data) < self.MIN_BATCH_SIZE:
            logger.debug(
                f"Insufficient batch size: {len(batch_data)} < {self.MIN_BATCH_SIZE}"
            )
            return {"anomaly_detected": False, "reason": "insufficient_batch_size"}
        
        # Calculate who's declining relative to their personal baseline
        declining = [
            s for s in batch_data 
            if (s["baseline"] - s["recent_avg"]) >= self.SCORE_DROP_THRESHOLD
        ]
        
        affected_pct = len(declining) / len(batch_data)
        
        logger.info(
            f"Cohort analysis: {len(declining)}/{len(batch_data)} declining "
            f"({affected_pct:.0%}), threshold={self.COHORT_THRESHOLD:.0%}"
        )
        
        if affected_pct < self.COHORT_THRESHOLD:
            logger.debug("Below cohort threshold - no anomaly detected")
            return {
                "anomaly_detected": False,
                "affected_percentage": round(affected_pct * 100, 1)
            }
        
        # Cohort anomaly confirmed
        avg_drop = statistics.mean([
            s["baseline"] - s["recent_avg"] for s in declining
        ])
        
        severity = "high" if affected_pct > 0.6 else "medium"
        
        logger.warning(
            f"COHORT ANOMALY DETECTED: {severity.upper()} - "
            f"{affected_pct:.0%} affected, avg drop {avg_drop:.2f}"
        )
        
        return {
            "anomaly_detected": True,
            "affected_count": len(declining),
            "total_count": len(batch_data),
            "affected_percentage": round(affected_pct * 100, 1),
            "average_score_drop": round(avg_drop, 2),
            "severity": severity,
            "institutional_action": self._recommend_action(affected_pct, avg_drop)
        }
    
    def _recommend_action(self, pct: float, avg_drop: float) -> str:
        """Generate institutional action recommendation based on severity."""
        if pct > 0.6 and avg_drop > 1.5:
            return (
                "URGENT: Over 60% of this batch shows significant decline. "
                "Recommend immediate batch-level intervention — group counselling session, "
                "faculty review meeting, or workload assessment within 48 hours."
            )
        elif pct > 0.4:
            return (
                "ATTENTION: Systemic stress pattern detected in this batch. "
                "Recommend proactive faculty communication and optional "
                "group check-in session this week."
            )
        return "Monitor closely. Consider reaching out to batch representatives."
    
    def detect_trend(
        self,
        batch_data_current: List[Dict],
        batch_data_previous: List[Dict]
    ) -> Literal["improving", "stable", "declining"]:
        """
        Detect whether cohort is improving, stable, or declining over time.
        
        Compares current week vs previous week to identify trajectory.
        
        Args:
            batch_data_current: Current week's data [{"student_id": ..., "recent_avg": ...}]
            batch_data_previous: Previous week's data [{"student_id": ..., "recent_avg": ...}]
        
        Returns:
            "improving" - Cohort average is rising
            "stable" - Cohort average unchanged (within 0.3 points)
            "declining" - Cohort average is falling
        """
        if not batch_data_current or not batch_data_previous:
            logger.warning("Insufficient data for trend detection")
            return "stable"
        
        # Calculate cohort averages
        current_avg = statistics.mean([s["recent_avg"] for s in batch_data_current])
        previous_avg = statistics.mean([s["recent_avg"] for s in batch_data_previous])
        
        trend_change = current_avg - previous_avg
        
        logger.info(
            f"Cohort trend: current={current_avg:.2f}, "
            f"previous={previous_avg:.2f}, change={trend_change:+.2f}"
        )
        
        # Threshold: 0.3 points is considered meaningful change
        if trend_change > 0.3:
            return "improving"
        elif trend_change < -0.3:
            return "declining"
        else:
            return "stable"
    
    async def run_daily_cohort_scan(
        self,
        db,  # AsyncSession
        institution_id: UUID
    ) -> List[Dict]:
        """
        Scan all batches in an institution for cohort anomalies.
        
        This is the daily scheduled job that runs autonomously to detect
        systemic stressors across all batches in an institution.
        
        Args:
            db: Async database session
            institution_id: UUID of institution to scan
        
        Returns:
            List of detected anomalies (saved to cohort_alerts table)
        
        Process:
            1. Get all unique batches in institution
            2. For each batch, get student data
            3. Run cohort anomaly detection
            4. If anomaly detected, save to cohort_alerts table
            5. Return summary of detected anomalies
        """
        from database.crud import (
            get_all_students_by_institution,
            get_cohort_data_by_batch,
            save_cohort_alert
        )
        
        logger.info(f"Starting daily cohort scan for institution {institution_id}")
        
        # Get all students in institution
        students = await get_all_students_by_institution(db, institution_id)
        
        # Group by batch
        batches = {}
        for student in students:
            batch = student.batch or "Unknown"
            if batch not in batches:
                batches[batch] = []
            batches[batch].append(student)
        
        logger.info(f"Found {len(batches)} batches to scan")
        
        detected_anomalies = []
        
        # Scan each batch
        for batch_name, batch_students in batches.items():
            if len(batch_students) < self.MIN_BATCH_SIZE:
                logger.debug(
                    f"Skipping batch {batch_name}: "
                    f"only {len(batch_students)} students (min {self.MIN_BATCH_SIZE})"
                )
                continue
            
            # Get cohort data for this batch
            batch_data = await get_cohort_data_by_batch(
                db, institution_id, batch_name
            )
            
            if not batch_data:
                logger.warning(f"No data for batch {batch_name}")
                continue
            
            # Run detection
            result = self.detect(batch_data)
            
            if result["anomaly_detected"]:
                logger.warning(
                    f"COHORT ANOMALY DETECTED: {batch_name} - "
                    f"{result['affected_percentage']}% affected"
                )
                
                # Save to database
                alert_data = {
                    "institution_id": institution_id,
                    "batch": batch_name,
                    "detected_at": datetime.utcnow(),
                    "affected_students": result["affected_count"],
                    "affected_percentage": result["affected_percentage"],
                    "avg_score_drop": result["average_score_drop"],
                    "likely_cause": "Systemic stressor detected - requires investigation",
                    "institutional_action_recommended": result["institutional_action"],
                    "acknowledged": False
                }
                
                await save_cohort_alert(db, alert_data)
                detected_anomalies.append(result)
        
        logger.info(
            f"Cohort scan complete: {len(detected_anomalies)} anomalies detected "
            f"across {len(batches)} batches"
        )
        
        return detected_anomalies
