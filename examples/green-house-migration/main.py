"""Greenhouse API Proxy - Main Application."""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from legacy.greenhouse.logger import app_logger
from routes.api import (
    applications,
    candidate_tags,
    candidates,
    jobs,
    legacy_data,
    metadata,
    offers,
    prospects,
    scheduled_interviews,
    scorecards,
    stats,
    teamtailor_dashboard,
    teamtailor_simple,
    users,
    users_mapping,
)
from routes.dashboard import router as dashboard_router
from routes.export import export, export_team_tailor
from routes.import_ import (
    import_applications,
    import_candidates,
    import_comments,
    import_custom_fields,
    import_interviews,
    import_jobs,
    import_offers,
)


@asynccontextmanager
async def lifespan(_):
    """Application lifespan manager."""
    # Startup
    app_logger.info("Starting Greenhouse API Proxy...")
    start_time = time.time()
    yield

    # Shutdown
    uptime = time.time() - start_time
    app_logger.info("Shutting down Greenhouse API Proxy. Uptime: %.2fs", uptime)


app = FastAPI(
    _title="Greenhouse API Proxy",
    description=(
        "A FastAPI application that acts as an intermediate layer"
        " between the Greenhouse API and external clients."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidates.router)
app.include_router(applications.router)
app.include_router(jobs.router)
app.include_router(users.router)
app.include_router(metadata.router)
app.include_router(export.router)
app.include_router(scheduled_interviews.router)
app.include_router(scorecards.router)
app.include_router(stats.router)
app.include_router(offers.router)
app.include_router(export_team_tailor.router)
app.include_router(import_jobs.router)
app.include_router(import_candidates.router)
app.include_router(import_applications.router)
app.include_router(import_comments.router)
app.include_router(import_custom_fields.router)
app.include_router(import_interviews.router)
app.include_router(import_offers.router)
app.include_router(prospects.router)
app.include_router(users_mapping.router)
app.include_router(candidate_tags.router)
app.include_router(dashboard_router)
app.include_router(teamtailor_dashboard.router)
app.include_router(teamtailor_simple.router)
app.include_router(legacy_data.router)


@app.get("/", tags=["root"])
async def read_root():
    """Root endpoint with application information."""
    return {
        "message": "Welcome to the Greenhouse API Proxy!",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    try:
        # Basic health check - could be extended with database checks, etc.
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "service": "greenhouse-api-proxy",
        }
    except Exception as e:
        app_logger.error("Health check failed: %s", e)
        raise HTTPException(status_code=503, detail="Service unhealthy") from e


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    app_logger.error("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
