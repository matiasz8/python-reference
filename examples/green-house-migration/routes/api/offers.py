"""Offers API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.get("/")
def list_offers(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all offers with pagination and metadata"""
    return paginated_get("offers", pagination)


@router.get("/{offer_id}")
def get_offer(offer_id: int):
    """Get details of a specific offer by ID"""
    return gh_get("offers/{offer_id}")
