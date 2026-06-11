"""
GuardianAI - Autonomous Student Mental Health Triage Agent
FastAPI Application Entry Point

The agent that catches burnout before it becomes a tragedy.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database connection
from database.connection import init_db, close_db

# Import routers
from routes import webhook, students, dashboard, interventions, cohorts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Initializes database connection pool on startup.
    Closes connections on shutdown.
    """
    # Startup
    await init_db()
    print("✅ GuardianAI database connection pool initialized")
    
    yield
    
    # Shutdown
    await close_db()
    print("🔌 GuardianAI database connections closed")


# Initialize FastAPI application
app = FastAPI(
    title="GuardianAI API",
    description="Autonomous student mental health triage agent - FAR AWAY 2026",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("FRONTEND_URL", "http://localhost:3000"),
        "http://localhost:3000",
        "http://localhost:5173",  # Vite default
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """
    Health check endpoint.
    Returns system status and agent readiness.
    """
    return {
        "status": "operational",
        "agent": "GuardianAI",
        "version": "1.0.0",
        "tagline": "The autonomous agent that catches student burnout before it becomes a tragedy.",
        "theme": "Agentic & Autonomous Systems",
        "hackathon": "FAR AWAY 2026"
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check for monitoring.
    """
    from database.connection import engine
    
    db_status = "connected" if engine else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "agent_core": "ready",
        "hmm_engine": "loaded",
        "adversarial_validator": "loaded",
        "cohort_detector": "loaded",
        "intervention_orchestrator": "ready"
    }


# Register routers
app.include_router(
    webhook.router,
    prefix="/api",
    tags=["Webhook"]
)

app.include_router(
    students.router,
    prefix="/api/students",
    tags=["Students"]
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"]
)

app.include_router(
    interventions.router,
    prefix="/api/interventions",
    tags=["Interventions"]
)

app.include_router(
    cohorts.router,
    prefix="/api/cohorts",
    tags=["Cohorts"]
)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
