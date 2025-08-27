"""Scorecards API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/scorecards", tags=["Scorecards"])


@router.get("/")
def list_scorecards(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all scorecards with pagination and metadata"""
    return paginated_get("scorecards", pagination)


@router.get("/{scorecard_id}")
def get_scorecard(scorecard_id: int):
    """Get details of a specific scorecard by ID"""
    return gh_get("scorecards/{scorecard_id}")
