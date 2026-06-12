"""Get institution and student IDs for testing."""
import asyncio
from sqlalchemy import select
from backend.database.connection import AsyncSessionLocal
from backend.database.models import Institution, Student

async def get_ids():
    async with AsyncSessionLocal() as db:
        # Get first institution
        inst_result = await db.execute(select(Institution).limit(1))
        institution = inst_result.scalar_one_or_none()
        
        if not institution:
            print("❌ No institutions found in database")
            return
        
        print(f"✅ Institution: {institution.name}")
        print(f"   ID: {institution.id}")
        
        # Get first student from this institution
        stud_result = await db.execute(
            select(Student).where(Student.institution_id == institution.id).limit(1)
        )
        student = stud_result.scalar_one_or_none()
        
        if student:
            print(f"✅ Student: {student.name}")
            print(f"   ID: {student.id}")
        else:
            print("⚠️  No students found for this institution")

if __name__ == "__main__":
    asyncio.run(get_ids())
