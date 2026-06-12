"""
GuardianAI - WhatsApp Service

Handles all WhatsApp messaging via Twilio API.
Provides high-level functions for sending various message types.
"""

import os
import logging
from typing import Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)


class WhatsAppService:
    """
    WhatsApp messaging service using Twilio API.
    
    Handles:
    - Outbound messages to students
    - Check-in prompts (daily scheduled)
    - Counsellor alerts
    - Emergency notifications
    - Phone number formatting
    """
    
    def __init__(self):
        """Initialize Twilio client with credentials from environment."""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            logger.error("Missing Twilio credentials in environment variables")
            raise ValueError(
                "Required environment variables: TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER"
            )
        
        self.client = Client(self.account_sid, self.auth_token)
        logger.info(f"WhatsAppService initialized with number {self.whatsapp_number}")
    
    def format_phone(self, phone: str) -> str:
        """
        Ensure phone number has whatsapp: prefix for Twilio.
        
        Args:
            phone: Phone number (can be +919876543210 or whatsapp:+919876543210)
        
        Returns:
            Formatted phone with whatsapp: prefix
        
        Examples:
            >>> service.format_phone("+919876543210")
            "whatsapp:+919876543210"
            >>> service.format_phone("whatsapp:+919876543210")
            "whatsapp:+919876543210"
        """
        if not phone:
            raise ValueError("Phone number cannot be empty")
        
        phone = phone.strip()
        
        # Already has whatsapp: prefix
        if phone.startswith("whatsapp:"):
            return phone
        
        # Add prefix
        return f"whatsapp:{phone}"
    
    def send_message(self, to_phone: str, message: str) -> bool:
        """
        Send a WhatsApp message to a phone number.
        
        Args:
            to_phone: Recipient phone number (will be formatted automatically)
            message: Message text to send
        
        Returns:
            True if message sent successfully, False otherwise
        
        Example:
            >>> service.send_message("+919876543210", "Hello from GuardianAI!")
            True
        """
        try:
            to_phone = self.format_phone(to_phone)
            
            logger.info(f"Sending WhatsApp message to {to_phone[:20]}... ({len(message)} chars)")
            
            message_obj = self.client.messages.create(
                from_=self.whatsapp_number,
                body=message,
                to=to_phone
            )
            
            logger.info(f"Message sent successfully: SID={message_obj.sid}, status={message_obj.status}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"Twilio API error sending message: {e.code} - {e.msg}")
            return False
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    def send_check_in_prompt(self, to_phone: str, student_name: str) -> bool:
        """
        Send daily check-in prompt to a student.
        
        Args:
            to_phone: Student phone number
            student_name: Student's first name for personalization
        
        Returns:
            True if sent successfully, False otherwise
        
        Message format:
            "Good morning, [Name]! 🌅
            
            How are you feeling today?
            Please reply with:
            1️⃣ Your mood score (1-5)
            2️⃣ Did you eat properly? (yes/mostly/no)
            3️⃣ One word describing your day
            
            Example: 4 yes hopeful"
        """
        message = f"""Good morning, {student_name}! 🌅

How are you feeling today?

Please reply with:
1️⃣ Your mood score (1-5, where 1=struggling, 5=great)
2️⃣ Did you eat properly? (yes/mostly/no)
3️⃣ One word describing your day

Example: 4 yes hopeful

Your response helps us support you better. 💙"""
        
        logger.info(f"Sending check-in prompt to {student_name} at {to_phone[:20]}...")
        return self.send_message(to_phone, message)
    
    def send_counsellor_alert(
        self, 
        counsellor_phone: str, 
        student_name: str, 
        alert_message: str
    ) -> bool:
        """
        Send alert to counsellor about a student.
        
        Args:
            counsellor_phone: Counsellor's phone number
            student_name: Student requiring attention
            alert_message: Detailed alert message from intervention orchestrator
        
        Returns:
            True if sent successfully, False otherwise
        """
        message = f"""🔔 GuardianAI Counsellor Alert

Student: {student_name}

{alert_message}

---
Reply DETAILS for full student history.
Reply ACK to acknowledge this alert."""
        
        logger.warning(f"Sending counsellor alert for student {student_name}")
        return self.send_message(counsellor_phone, message)
    
    def send_emergency_alert(
        self,
        emergency_phone: str,
        student_name: str,
        alert_message: str
    ) -> bool:
        """
        Send emergency alert to emergency contact.
        
        Args:
            emergency_phone: Emergency contact phone number
            student_name: Student in crisis
            alert_message: Urgent alert message
        
        Returns:
            True if sent successfully, False otherwise
        """
        message = f"""🚨 URGENT: GuardianAI Emergency Alert

Student: {student_name}

{alert_message}

This is an automated alert from the student wellbeing monitoring system.
Please contact the student immediately.

For support: Contact campus counselling center or call 1800-XXX-XXXX (Helpline)"""
        
        logger.critical(f"Sending EMERGENCY alert for student {student_name}")
        return self.send_message(emergency_phone, message)
    
    def send_confirmation(self, to_phone: str, score: int) -> bool:
        """
        Send check-in confirmation back to student.
        
        Args:
            to_phone: Student phone number
            score: Their mood score (1-5)
        
        Returns:
            True if sent successfully, False otherwise
        """
        # Personalized responses based on score
        if score >= 4:
            response = "Thanks for checking in! 💙 Glad to hear you're doing well. Keep it up!"
        elif score == 3:
            response = "Thanks for checking in! 💙 Remember, we're here if you need support."
        else:  # score <= 2
            response = "Thanks for checking in. 💙 We're here for you. Don't hesitate to reach out if you need someone to talk to."
        
        logger.debug(f"Sending check-in confirmation (score={score})")
        return self.send_message(to_phone, response)
    
    def send_institutional_report(
        self,
        institution_email: str,
        batch: str,
        report_message: str
    ) -> bool:
        """
        Send institutional report about cohort anomaly.
        
        Note: This would typically send an email, not WhatsApp.
        For MVP, we log it and could send to a designated WhatsApp number.
        
        Args:
            institution_email: Institution contact (for future email integration)
            batch: Batch identifier (e.g., "CSE-2023")
            report_message: Full institutional report
        
        Returns:
            True (logged, actual email integration pending)
        """
        logger.critical(
            f"INSTITUTIONAL REPORT for batch {batch}:\n"
            f"Contact: {institution_email}\n"
            f"{report_message}"
        )
        
        # TODO: Integrate with email service (SendGrid, AWS SES)
        # For now, just log it
        return True


# Singleton instance
_whatsapp_service: Optional[WhatsAppService] = None


def get_whatsapp_service() -> WhatsAppService:
    """
    Get or create singleton WhatsApp service instance.
    
    Returns:
        WhatsAppService instance
    """
    global _whatsapp_service
    if _whatsapp_service is None:
        _whatsapp_service = WhatsAppService()
    return _whatsapp_service
