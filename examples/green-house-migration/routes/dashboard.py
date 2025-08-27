"""
Dashboard routes for serving the prospects analytics dashboard.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Get the dashboard directory
dashboard_dir = Path(__file__).parent.parent / "dashboard"

# Mount static files
if dashboard_dir.exists():
    static_files = StaticFiles(directory=str(dashboard_dir))
else:
    static_files = None


@router.get("/", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the main dashboard HTML page."""
    try:
        html_file = dashboard_dir / "index.html"
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            raise HTTPException(status_code=404, detail="Dashboard not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading dashboard: {str(e)}"
        )


@router.get("/unified", response_class=HTMLResponse)
async def get_unified_dashboard():
    """Serve the unified dashboard HTML page."""
    try:
        html_file = dashboard_dir / "unified_dashboard.html"
        if html_file.exists():
            with open(html_file, encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            raise HTTPException(status_code=404, detail="Unified dashboard not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error loading unified dashboard: {str(e)}"
        )


@router.get("/static/{file_path:path}")
async def get_static_file(file_path: str):
    """Serve static files for the dashboard."""
    try:
        file_path_obj = dashboard_dir / "static" / file_path
        if file_path_obj.exists() and file_path_obj.is_file():
            return FileResponse(str(file_path_obj))
        else:
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")


@router.get("/test")
async def test_dashboard():
    """Test dashboard page for debugging."""
    return FileResponse("dashboard/test.html")


@router.get("/simple-test")
async def simple_test_dashboard():
    """Simple test dashboard page for debugging."""
    return FileResponse("dashboard/simple_test.html")


@router.get("/health")
async def dashboard_health():
    """Health check for dashboard."""
    return {
        "status": "healthy",
        "service": "prospects-dashboard",
        "dashboard_dir": str(dashboard_dir),
        "dashboard_exists": dashboard_dir.exists(),
    }
