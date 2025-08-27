"""Pagination utilities for the Greenhouse API."""

from typing import Any, Dict

from fastapi import Depends

from .validators import PaginationParams, validate_page, validate_per_page


def pagination_params(
    per_page: int = 100,
    page: int = 1,
) -> Dict[str, Any]:
    """Get pagination parameters for API requests with validation."""
    validated_per_page = validate_per_page(per_page)
    validated_page = validate_page(page)

    return {"per_page": validated_per_page, "page": validated_page}


def get_pagination_model() -> PaginationParams:
    """Get pagination parameters as a Pydantic model."""
    return PaginationParams()


# Dependency for FastAPI
def pagination_dependency(
    pagination: PaginationParams = Depends(get_pagination_model),
) -> Dict[str, Any]:
    """FastAPI dependency for pagination parameters."""
    return {"per_page": pagination.per_page, "page": pagination.page}
