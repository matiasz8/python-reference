"""
Legacy Data API

API endpoints for local/legacy data sources.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/legacy", tags=["legacy-data"])


@router.get("/candidates")
async def get_legacy_candidates(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=1, le=100, description="Page size"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
) -> Dict[str, Any]:
    """Get candidates from local/legacy data sources."""
    try:
        # Import here to avoid circular imports
        from routes.api.candidates import get_candidates

        # Use existing logic but with legacy prefix
        result = await get_candidates(page=page, per_page=page_size)

        return {
            "success": True,
            "source": "legacy",
            "data": result.get("candidates", []),
            "pagination": result.get("pagination", {}),
            "stats": result.get("stats", {}),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching legacy data: {str(e)}"
        )


@router.get("/stats")
async def get_legacy_stats() -> Dict[str, Any]:
    """Get statistics from legacy data sources."""
    try:
        # Import here to avoid circular imports
        from routes.api.candidates import get_sourced_candidates_analytics

        result = await get_sourced_candidates_analytics()

        return {
            "success": True,
            "source": "legacy",
            "overview": result.get("overview", {}),
            "sourced_analytics": result.get("sourced_analytics", []),
            "tag_distribution": result.get("tag_distribution", {}),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching legacy stats: {str(e)}"
        )


@router.get("/tags")
async def get_legacy_tags() -> Dict[str, Any]:
    """Get available tags from legacy data."""
    try:
        # Import here to avoid circular imports
        from routes.api.candidate_tags import get_candidate_tags

        result = await get_candidate_tags()

        return {
            "success": True,
            "source": "legacy",
            "tags": result.get("tags", []),
            "categories": result.get("categories", []),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching legacy tags: {str(e)}"
        )
