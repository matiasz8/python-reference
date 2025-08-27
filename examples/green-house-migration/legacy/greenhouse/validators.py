"""Centralized validation utilities for the Greenhouse API Proxy."""

from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class PaginationParams(BaseModel):
    """Pagination parameters with validation."""

    per_page: int = Field(100, ge=1, le=1000, description="Items per page")
    page: int = Field(1, ge=1, description="Page number")

    @field_validator("per_page")
    @classmethod
    def validate_per_page(cls, v):
        """Validate per_page parameter."""
        if v > 1000:
            raise ValueError("per_page cannot exceed 1000")
        return v


class ImportParams(BaseModel):
    """Common import parameters with validation."""

    limit: Optional[int] = Field(
        None, ge=1, le=10000, description="Maximum items to import"
    )
    delay_ms: int = Field(
        0, ge=0, le=10000, description="Delay between requests in milliseconds"
    )

    @field_validator("delay_ms")
    @classmethod
    def validate_delay(cls, v):
        """Validate delay_ms parameter."""
        if v > 10000:
            raise ValueError("delay_ms cannot exceed 10000ms (10 seconds)")
        return v


class SearchParams(BaseModel):
    """Search parameters with validation."""

    query: str = Field(..., min_length=1, max_length=200, description="Search query")
    filters: Optional[dict[str, Any]] = Field(None, description="Additional filters")


def validate_limit(limit: Optional[int]) -> Optional[int]:
    """Validate limit parameter."""
    if limit is not None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if limit > 10000:
            raise ValueError("limit cannot exceed 10000")
    return limit


def validate_delay_ms(delay_ms: int) -> int:
    """Validate delay_ms parameter."""
    if delay_ms < 0:
        raise ValueError("delay_ms must be >= 0")
    if delay_ms > 10000:
        raise ValueError("delay_ms cannot exceed 10000ms (10 seconds)")
    return delay_ms


def validate_page(page: int) -> int:
    """Validate page parameter."""
    if page < 1:
        raise ValueError("page must be >= 1")
    return page


def validate_per_page(per_page: int) -> int:
    """Validate per_page parameter."""
    if per_page < 1:
        raise ValueError("per_page must be >= 1")
    if per_page > 1000:
        raise ValueError("per_page cannot exceed 1000")
    return per_page
