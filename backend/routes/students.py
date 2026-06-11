"""
GuardianAI - Students API Routes
CRUD operations for student management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from database import get_db
from database.models import Student, Institution

router = APIRouter()


@router.get("/")
async def get_all_students(
    institution_id: str = None,
    batch: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all students, optionally filtered by institution or batch."""
    query = select(Student)
    
    if institution_id:
        query = query.where(Student.institution_id == UUID(institution_id))
    
    if batch:
        query = query.where(Student.batch == batch)
    
    result = await db.execute(query)
    students = result.scalars().all()
    
    return {
        "students": [
            {
                "id": str(s.id),
                "name": s.name,
                "phone": s.phone,
                "batch": s.batch,
                "year_of_study": s.year_of_study,
                "baseline_score": s.baseline_score,
                "is_active": s.is_active
            }
            for s in students
        ]
    }


@router.get("/{student_id}")
async def get_student(student_id: str, db: AsyncSession = Depends(get_db)):
    """Get a single student by ID."""
    result = await db.execute(
        select(Student).where(Student.id == UUID(student_id))
    )
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return {
        "id": str(student.id),
        "name": student.name,
        "phone": student.phone,
        "email": student.email,
        "batch": student.batch,
        "year_of_study": student.year_of_study,
        "baseline_score": student.baseline_score,
        "is_active": student.is_active,
        "enrolled_at": student.enrolled_at.isoformat()
    }
