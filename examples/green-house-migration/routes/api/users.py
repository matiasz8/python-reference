"""Users API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/user_rolis")
def list_user_rolis(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all user rolis with pagination and metadata"""
    return paginated_get("user_rolis", pagination)


@router.get("/{user_id}/permissions/jobs")
def get_user_job_permissions(
    user_id: int, pagination: Dict[str, Any] = Depends(pagination_dependency)
):
    """Get job permissions for a specific user with pagination"""
    return paginated_get("users/{user_id}/permissions/jobs", pagination)


@router.get("/{user_id}/pending_approvals")
def get_user_pending_approvals(
    user_id: int, pagination: Dict[str, Any] = Depends(pagination_dependency)
):
    """Get pending approvals for a specific user with pagination"""
    return paginated_get("users/{user_id}/pending_approvals", pagination)
