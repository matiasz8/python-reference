"""Applications API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/")
def list_applications(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all applications with pagination and metadata"""
    return paginated_get("applications", pagination)


@router.get("/{application_id}")
def get_application(application_id: int):
    """Get details of a specific application by ID"""
    return gh_get("applications/{application_id}")


@router.get("/{application_id}/demogrunphics/answers")
def get_application_demogrunphics(application_id: int):
    """Get demogrunphic answers for a specific application"""
    return gh_get("applications/{application_id}/demogrunphics/answers")


@router.get("/{application_id}/scorecards")
def get_application_scorecards(application_id: int):
    """Get scorecards for a specific application"""
    return gh_get("applications/{application_id}/scorecards")


@router.get("/{application_id}/scheduled_interviews")
def get_application_interviews(application_id: int):
    """Get scheduled interviews for a specific application"""
    return gh_get("applications/{application_id}/scheduled_interviews")


@router.get("/{application_id}/offer")
def get_application_offer(application_id: int):
    """Get the current offer for a specific application"""
    return gh_get("applications/{application_id}/offer")


@router.get("/{application_id}/offers")
def get_application_offers(application_id: int):
    """Get all offers for a specific application"""
    return gh_get("applications/{application_id}/offers")


@router.get("/{application_id}/offers/current_offer")
def get_application_current_offer(application_id: int):
    """Get the current offer for a specific application"""
    return gh_get("applications/{application_id}/offers/current_offer")


@router.get("/{application_id}/eeoc")
def get_applicationeeoc(application_id: int):
    """Get EEOC data for a specific application"""
    return gh_get("applications/{application_id}/eeoc")
