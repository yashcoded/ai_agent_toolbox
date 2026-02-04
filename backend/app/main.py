"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.api import agents, tools, evals, metrics
from app.core.config import settings
from app.db.session import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup and cleanup on shutdown."""
    # Initialize database
    await init_db()
    yield
    # Cleanup


app = FastAPI(
    title="AI Agent Toolbox",
    description="LangChain-powered agent system with tool calling, evals, and observability",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(evals.router, prefix="/api/evals", tags=["evals"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])


@app.get("/")
async def root():
    """Root endpoint."""
    return JSONResponse(
        content={
            "name": "AI Agent Toolbox",
            "version": "0.1.0",
            "status": "running",
        }
    )


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse(content={"status": "healthy"})
