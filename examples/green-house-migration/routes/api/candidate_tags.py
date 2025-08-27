"""
Candidate Tags API endpoints for TeamTailor integration.

This module provides endpoints for managing candidate tags in TeamTailor,
allowing categorization by technologies, skills, and other criteria.
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from teamtailor.api.client import TeamTailorClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidate-tags", tags=["candidate-tags"])

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class AddTagsRequest(BaseModel):
    """Request model for adding tags to candidates."""

    candidate_ids: Optional[List[str]] = Field(
        None, description="List of candidate IDs to update"
    )
    emails: Optional[List[str]] = Field(
        None, description="List of candidate emails to update"
    )
    tags: List[str] = Field(..., description="Tags to add to candidates")
    bulk_mode: bool = Field(
        False, description="Update all candidates (use with caution)"
    )
    limit: int = Field(100, description="Limit for bulk operations")


class TagUpdateResponse(BaseModel):
    """Response model for tag update operations."""

    success: int = Field(..., description="Number of successful updates")
    failed: int = Field(..., description="Number of failed updates")
    total: int = Field(..., description="Total number of candidates processed")
    errors: List[str] = Field(default=[], description="List of error messages")


class AvailableTagsResponse(BaseModel):
    """Response model for available tags."""

    tags: List[str] = Field(..., description="List of available tags")
    total: int = Field(..., description="Total number of tags")


class CandidateTagsResponse(BaseModel):
    """Response model for candidate tags."""

    candidate_id: str = Field(..., description="Candidate ID")
    candidate_name: str = Field(..., description="Candidate full name")
    email: Optional[str] = Field(None, description="Candidate email")
    tags: List[str] = Field(..., description="Current tags")
    total_tags: int = Field(..., description="Total number of tags")


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def _get_candidate_name(candidate_data: Dict[str, Any]) -> str:
    """Extract candidate name from candidate data."""
    attributes = candidate_data.get("attributes", {})
    first_name = attributes.get("first-name", "")
    last_name = attributes.get("last-name", "")
    return f"{first_name} {last_name}".strip()


def _get_candidate_email(candidate_data: Dict[str, Any]) -> Optional[str]:
    """Extract candidate email from candidate data."""
    return candidate_data.get("attributes", {}).get("email")


# =============================================================================
# API ENDPOINTS
# =============================================================================


@router.get("/available", response_model=AvailableTagsResponse)
async def get_available_tags() -> AvailableTagsResponse:
    """Get all available tags in the system."""
    try:
        client = TeamTailorClient()

        # Get a sample of candidates to extract tags
        params = {"page[size]": 100}
        response = client.get_candidates(params=params)
        candidates = response.get("data", [])

        all_tags = set()
        for candidate in candidates:
            tags = candidate.get("attributes", {}).get("tags", [])
            all_tags.update(tags)

        tags_list = sorted(list(all_tags))

        return AvailableTagsResponse(tags=tags_list, total=len(tags_list))

    except Exception as e:
        logger.error(f"Error getting available tags: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get available tags: {str(e)}"
        )


@router.get("/candidate/{candidate_id}", response_model=CandidateTagsResponse)
async def get_candidate_tags(candidate_id: str) -> CandidateTagsResponse:
    """Get tags for a specific candidate."""
    try:
        client = TeamTailorClient()
        response = client.get_candidate(candidate_id)
        candidate_data = response.get("data")

        if not candidate_data:
            raise HTTPException(
                status_code=404, detail=f"Candidate {candidate_id} not found"
            )

        attributes = candidate_data.get("attributes", {})
        tags = attributes.get("tags", [])

        return CandidateTagsResponse(
            candidate_id=candidate_id,
            candidate_name=_get_candidate_name(candidate_data),
            email=_get_candidate_email(candidate_data),
            tags=tags,
            total_tags=len(tags),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting candidate tags: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get candidate tags: {str(e)}"
        )


@router.post("/add", response_model=TagUpdateResponse)
async def add_tags_to_candidates(request: AddTagsRequest) -> TagUpdateResponse:
    """Add tags to candidates."""
    try:
        client = TeamTailorClient()

        if not request.tags:
            raise HTTPException(status_code=400, detail="No tags provided")

        success_count = 0
        failed_count = 0
        errors = []

        # Validate that at least one identification method is provided
        if not any([request.candidate_ids, request.emails, request.bulk_mode]):
            raise HTTPException(
                status_code=400,
                detail="Must provide candidate_ids, emails, or enable bulk_mode",
            )

        candidates_to_update = []

        # Get candidates by IDs
        if request.candidate_ids:
            for candidate_id in request.candidate_ids:
                try:
                    response = client.get_candidate(candidate_id)
                    candidate_data = response.get("data")
                    if candidate_data:
                        candidates_to_update.append(candidate_data)
                    else:
                        errors.append(f"Candidate {candidate_id} not found")
                        failed_count += 1
                except Exception as e:
                    errors.append(f"Error getting candidate {candidate_id}: {str(e)}")
                    failed_count += 1

        # Get candidates by emails
        if request.emails:
            for email in request.emails:
                try:
                    params = {"filter[search]": email}
                    response = client.get_candidates(params=params)
                    candidates = response.get("data", [])

                    found = False
                    for candidate in candidates:
                        candidate_email = candidate.get("attributes", {}).get("email")
                        if candidate_email == email:
                            candidates_to_update.append(candidate)
                            found = True
                            break

                    if not found:
                        errors.append(f"Candidate with email {email} not found")
                        failed_count += 1

                except Exception as e:
                    errors.append(f"Error getting candidate by email {email}: {str(e)}")
                    failed_count += 1

        # Get candidates for bulk mode
        if request.bulk_mode:
            try:
                params = {"page[size]": request.limit}
                response = client.get_candidates(params=params)
                bulk_candidates = response.get("data", [])
                candidates_to_update.extend(bulk_candidates)
            except Exception as e:
                errors.append(f"Error getting candidates for bulk mode: {str(e)}")
                failed_count += 1

        # Update candidates with new tags
        for candidate in candidates_to_update:
            try:
                candidate_id = candidate.get("id")
                current_tags = candidate.get("attributes", {}).get("tags", [])

                # Add new tags (avoid duplicates)
                updated_tags = list(set(current_tags + request.tags))

                # Prepare update payload
                update_data = {
                    "data": {
                        "id": candidate_id,
                        "type": "candidates",
                        "attributes": {"tags": updated_tags},
                    }
                }

                # Update candidate
                client.update_candidate(candidate_id, update_data)
                success_count += 1

                logger.info(
                    f"Successfully updated candidate {candidate_id} with tags: {', '.join(updated_tags)}"
                )

            except Exception as e:
                candidate_id = candidate.get("id", "unknown")
                error_msg = f"Error updating candidate {candidate_id}: {str(e)}"
                errors.append(error_msg)
                failed_count += 1
                logger.error(error_msg)

        return TagUpdateResponse(
            success=success_count,
            failed=failed_count,
            total=success_count + failed_count,
            errors=errors,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding tags to candidates: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to add tags to candidates: {str(e)}"
        )


@router.get("/search", response_model=List[CandidateTagsResponse])
async def search_candidates_by_tags(
    tags: str = Query(..., description="Comma-separated list of tags to search for"),
    limit: int = Query(50, description="Maximum number of candidates to return"),
) -> List[CandidateTagsResponse]:
    """Search candidates by tags."""
    try:
        client = TeamTailorClient()

        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if not tag_list:
            raise HTTPException(status_code=400, detail="No valid tags provided")

        # Search for candidates with any of the specified tags
        params = {"page[size]": limit, "filter[tags]": ",".join(tag_list)}

        response = client.get_candidates(params=params)
        candidates = response.get("data", [])

        results = []
        for candidate in candidates:
            candidate_tags = candidate.get("attributes", {}).get("tags", [])

            # Only include candidates that have at least one of the searched tags
            if any(tag in candidate_tags for tag in tag_list):
                results.append(
                    CandidateTagsResponse(
                        candidate_id=candidate.get("id"),
                        candidate_name=_get_candidate_name(candidate),
                        email=_get_candidate_email(candidate),
                        tags=candidate_tags,
                        total_tags=len(candidate_tags),
                    )
                )

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching candidates by tags: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to search candidates by tags: {str(e)}"
        )


@router.delete("/remove/{candidate_id}")
async def remove_tags_from_candidate(
    candidate_id: str,
    tags: str = Query(..., description="Comma-separated list of tags to remove"),
) -> Dict[str, Any]:
    """Remove specific tags from a candidate."""
    try:
        client = TeamTailorClient()

        # Get current candidate data
        response = client.get_candidate(candidate_id)
        candidate_data = response.get("data")

        if not candidate_data:
            raise HTTPException(
                status_code=404, detail=f"Candidate {candidate_id} not found"
            )

        # Parse tags to remove
        tags_to_remove = [tag.strip() for tag in tags.split(",") if tag.strip()]
        if not tags_to_remove:
            raise HTTPException(
                status_code=400, detail="No valid tags provided for removal"
            )

        # Get current tags
        current_tags = candidate_data.get("attributes", {}).get("tags", [])

        # Remove specified tags
        updated_tags = [tag for tag in current_tags if tag not in tags_to_remove]

        # Prepare update payload
        update_data = {
            "data": {
                "id": candidate_id,
                "type": "candidates",
                "attributes": {"tags": updated_tags},
            }
        }

        # Update candidate
        client.update_candidate(candidate_id, update_data)

        removed_count = len(current_tags) - len(updated_tags)

        return {
            "message": f"Successfully removed {removed_count} tags from candidate {candidate_id}",
            "removed_tags": tags_to_remove,
            "remaining_tags": updated_tags,
            "removed_count": removed_count,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing tags from candidate: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to remove tags from candidate: {str(e)}"
        )
