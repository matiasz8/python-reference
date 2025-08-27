"""Scheduled Interviews API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/scheduled_interviews", tags=["Scheduled Interviews"])


@router.get("/")
def list_scheduled_interviews(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all scheduled interviews with pagination and metadata"""
    return paginated_get("scheduled_interviews", pagination)


@router.get("/{interview_id}")
def get_scheduled_interview(interview_id: int):
    """Get details of a specific scheduled interview by ID"""
    return gh_get("scheduled_interviews/{interview_id}")
