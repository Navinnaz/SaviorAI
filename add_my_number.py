"""
Add your real phone number to database for testing
"""

import asyncio
import sys
from uuid import uuid4

sys.path.insert(0, 'backend')

from database.connection import AsyncSessionLocal, init_db
from database.models import Student
from sqlalchemy import select

async def add_student():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Check if already exists
        result = await db.execute(
            select(Student).where(Student.phone == '+919944906759')
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print(f"✅ Student already exists: {existing.name}")
            return
        
        # Get institution ID
        from database.models import Institution
        inst_result = await db.execute(
            select(Institution).where(Institution.name == 'IIT Delhi')
        )
        institution = inst_result.scalar_one()
        
        # Add new student with YOUR number
        new_student = Student(
            id=uuid4(),
            name="Navin Nazerine",  # Your name from WhatsApp
            phone="+919944906759",  # Your number
            email="navin.nazerine@iitd.ac.in",
            institution_id=institution.id,
            batch="CSE-2023",
            year_of_study=3,
            is_active=True,
            baseline_score=3.5,
            consent_given=True
        )
        
        db.add(new_student)
        await db.commit()
        
        print(f"✅ Added student: {new_student.name}")
        print(f"   Phone: {new_student.phone}")
        print(f"   Student ID: {new_student.id}")
        print("\n🎉 You can now send WhatsApp check-ins!")

if __name__ == "__main__":
    asyncio.run(add_student())
