"""
Nuclear Reset - Drops and recreates ALL database tables
Use this when normal --reset doesn't work
"""

import asyncio
from backend.database.connection import engine
from backend.database.models import Base


async def nuclear_reset():
    """Drop all tables and recreate them."""
    print("\n" + "="*70)
    print("💣 NUCLEAR RESET: Dropping ALL tables")
    print("="*70 + "\n")
    
    response = input("⚠️  This will DELETE EVERYTHING in the database. Continue? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Nuclear reset cancelled")
        return
    
    async with engine.begin() as conn:
        print("\n🗑️  Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("   ✅ All tables dropped")
        
        print("\n🔨 Recreating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("   ✅ All tables recreated")
    
    print("\n" + "="*70)
    print("✅ NUCLEAR RESET COMPLETE - Database is completely empty")
    print("="*70)
    print("\n🎯 Next step: python -m backend.utils.demo_runner --scenario setup\n")


if __name__ == "__main__":
    asyncio.run(nuclear_reset())
