"""
Add your phone to database and trigger WhatsApp check-in for live demo
"""

import asyncio
import sys
import re
from uuid import uuid4
from datetime import datetime

sys.path.insert(0, 'backend')

from database.connection import AsyncSessionLocal, init_db
from database.models import Student, Institution
from sqlalchemy import select
from services.whatsapp import send_checkin_prompt

# Configure your details here
YOUR_PHONE = "+919944906759"
YOUR_NAME = "Navin Nazerine"

def validate_phone(phone: str) -> bool:
    """Validate phone format (+country code + number)."""
    pattern = r'^\+\d{10,15}$'
    return bool(re.match(pattern, phone))

async def add_and_notify():
    await init_db()
    
    if not validate_phone(YOUR_PHONE):
        print(f"❌ Invalid phone format: {YOUR_PHONE}")
        print("   Expected: +91XXXXXXXXXX or +[country][number]")
        return
    
    async with AsyncSessionLocal() as db:
        # Get institution
        inst_result = await db.execute(
            select(Institution).where(Institution.name == 'IIT Delhi')
        )
        institution = inst_result.scalar_one_or_none()
        
        if not institution:
            print("❌ IIT Delhi institution not found. Run --setup first.")
            return
        
        # Check if already exists (upsert)
        result = await db.execute(
            select(Student).where(Student.phone == YOUR_PHONE)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"✅ Student already exists: {existing.name}")
            student = existing
        else:
            # Add new student
            student = Student(
                id=uuid4(),
                name=YOUR_NAME,
                phone=YOUR_PHONE,
                email=f"{YOUR_NAME.lower().replace(' ', '.')}@iitd.ac.in",
                institution_id=institution.id,
                batch="DEMO-LIVE",
                year_of_study=3,
                is_active=True,
                baseline_score=3.5,
                consent_given=True
            )
            
            db.add(student)
            await db.commit()
            print(f"✅ Added student: {student.name}")
        
        print(f"   Phone: {student.phone}")
        print(f"   Batch: DEMO-LIVE")
        print(f"   Student ID: {student.id}")
    
    # Send WhatsApp check-in prompt
    print(f"\n📱 Sending WhatsApp check-in prompt to {YOUR_PHONE}...")
    
    success = send_checkin_prompt(YOUR_PHONE)
    
    if success:
        print(f"✅ Check-in message sent to {YOUR_PHONE}")
        print("\n" + "="*70)
        print("⏳ Waiting for your reply...")
        print("="*70)
        print("\n📲 On your phone, reply to the WhatsApp message:")
        print("   Format: [1-5] [yes/no] [one word]")
        print("   Example: 1 no terrible")
        print("\n🔄 Once you reply:")
        print("   1. The webhook will process your message automatically")
        print("   2. Refresh the dashboard to see your card appear")
        print("   3. Click your card to see the real-time check-in")
        print("\n� Dashboard: http://localhost:3001")
        print("="*70)
    else:
        print(f"⚠️  Failed to send WhatsApp message")
        print("   Check Twilio credentials in .env")

if __name__ == "__main__":
    asyncio.run(add_and_notify())
