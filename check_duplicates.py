"""
Check for duplicate students in database
"""
import asyncio
import sys
from collections import Counter

sys.path.insert(0, 'backend')

from backend.database.connection import AsyncSessionLocal, init_db
from backend.database.models import Student, BurnoutState
from sqlalchemy import select, func

async def check_duplicates():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Get all students
        result = await db.execute(select(Student))
        students = result.scalars().all()
        
        print(f"📊 Total students in database: {len(students)}")
        
        # Check for duplicate names
        names = [s.name for s in students]
        name_counts = Counter(names)
        
        duplicates = {name: count for name, count in name_counts.items() if count > 1}
        
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} duplicate names:\n")
            for name, count in duplicates.items():
                print(f"   • {name}: {count} copies")
                
                # Show IDs of duplicates
                dupes = [s for s in students if s.name == name]
                for i, s in enumerate(dupes, 1):
                    # Count burnout states for this student
                    state_count = await db.execute(
                        select(func.count(BurnoutState.id))
                        .where(BurnoutState.student_id == s.id)
                    )
                    states = state_count.scalar() or 0
                    
                    print(f"      #{i}: ID={str(s.id)[:8]}... | Burnout States: {states}")
            
            print("\n💡 Solution: Run reset before setup")
            print("   .\run_demo.bat --scenario reset")
            print("   .\run_demo.bat --scenario setup")
        else:
            print("\n✅ No duplicate students found!")
            print("\n📋 Students by name:")
            for name in sorted(set(names)):
                print(f"   • {name}")

if __name__ == "__main__":
    asyncio.run(check_duplicates())
