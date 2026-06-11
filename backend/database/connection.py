"""
GuardianAI Database Connection Manager
Async PostgreSQL connection pool using asyncpg and SQLAlchemy 2.0
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please configure your PostgreSQL connection string."
    )

# Create async engine
# asyncpg is the async driver for PostgreSQL
engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("DEBUG", "false").lower() == "true",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for SQLAlchemy models
Base = declarative_base()


async def init_db():
    """
    Initialize database connection pool.
    Called on application startup.
    """
    # Import models to ensure they're registered with Base
    from database import models
    
    # Create tables if they don't exist
    # In production, use Alembic for migrations instead
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print(f"✅ Database initialized: {engine.url.database}")


async def close_db():
    """
    Close database connection pool.
    Called on application shutdown.
    """
    await engine.dispose()
    print("🔌 Database connection pool closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI routes.
    Provides async database session.
    
    Usage:
        @app.get("/students")
        async def get_students(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Student))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_db_session():
    """
    Context manager for database sessions (non-FastAPI usage).
    
    Usage:
        async with get_db_session() as db:
            student = await crud.get_student_by_phone(db, phone)
    """
    return AsyncSessionLocal()
