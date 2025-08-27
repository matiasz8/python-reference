"""
Candidates API endpoints for TeamTailor integration.

This module provides comprehensive endpoints for managing candidates and prospects
in TeamTailor, including data migration from Greenhouse backup.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

# from routes.clients.tt_client import TTClient  # Unused import
from teamtailor.api.client import TeamTailorClient

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidates", tags=["candidates"])

# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================


class CandidateCreateRequest(BaseModel):
    """Request model for creating a candidate."""

    first_name: str = Field(..., description="Candidate's first name")
    last_name: str = Field(..., description="Candidate's last name")
    email: Optional[str] = Field(None, description="Primary email address")
    phone: Optional[str] = Field(None, description="Primary phone number")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")
    pitch: Optional[str] = Field(None, description="Candidate pitch/summary")
    external_id: Optional[str] = Field(None, description="External ID for migration")
    tags: Optional[List[str]] = Field(default=[], description="Candidate tags")
    prospect_pool: Optional[str] = Field(None, description="Prospect pool name")
    custom_fields: Optional[Dict[str, Any]] = Field(
        default={}, description="Custom fields"
    )


class CandidateUpdateRequest(BaseModel):
    """Request model for updating a candidate."""

    first_name: Optional[str] = Field(None, description="Candidate's first name")
    last_name: Optional[str] = Field(None, description="Candidate's last name")
    email: Optional[str] = Field(None, description="Primary email address")
    phone: Optional[str] = Field(None, description="Primary phone number")
    tags: Optional[List[str]] = Field(None, description="Candidate tags")
    prospect_pool: Optional[str] = Field(None, description="Prospect pool name")
    custom_fields: Optional[Dict[str, Any]] = Field(None, description="Custom fields")


class CandidateResponse(BaseModel):
    """Response model for candidate data."""

    id: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    linkedin_url: Optional[str]
    pitch: Optional[str]
    external_id: Optional[str]
    tags: List[str]
    prospect_pool: Optional[str]
    custom_fields: Dict[str, Any]
    created_at: str
    updated_at: str


class CandidatesListResponse(BaseModel):
    """Response model for candidates list."""

    candidates: List[CandidateResponse]
    total: int
    page: int
    per_page: int


class ProspectPoolResponse(BaseModel):
    """Response model for prospect pool data."""

    id: str
    name: str
    description: Optional[str]
    candidate_count: int


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================


def _normalize_teamtailor_candidate(
    candidate_data: Dict[str, Any],
) -> CandidateResponse:
    """Normalize TeamTailor candidate data to our response format."""
    attributes = candidate_data.get("attributes", {})

    return CandidateResponse(
        id=candidate_data.get("id", ""),
        _first_name=attributes.get("first-name", ""),
        _last_name=attributes.get("last-name", ""),
        _email=attributes.get("email"),
        phone=attributes.get("phone"),
        linkedin_url=attributes.get("linkedin-url"),
        pitch=attributes.get("pitch"),
        external_id=attributes.get("external-id"),
        tags=attributes.get("tags", []),
        prospect_pool=attributes.get("prospect-pool"),
        _custom_fields=attributes.get("custom-fields", {}),
        _created_at=attributes.get("created-at", ""),
        updated_at=attributes.get("updated-at", ""),
    )


def _build_candidate_payload(data: CandidateCreateRequest) -> Dict[str, Any]:
    """Build TeamTailor candidate payload from request data."""
    attributes = {
        "first-name": data.first_name,
        "last-name": data.last_name,
        "tags": data.tags,
    }

    if data.email:
        attributes["email"] = data.email
    if data.phone:
        attributes["phone"] = data.phone
    if data.linkedin_url:
        attributes["linkedin-url"] = data.linkedin_url
    if data.pitch:
        attributes["pitch"] = data.pitch
    # Note: external_id is not supported by TeamTailor API
    # We'll store it in custom_fields instead
    if data.custom_fields:
        attributes["custom-fields"] = data.custom_fields

    return {"data": {"type": "candidates", "attributes": attributes}}


def _find_prospect_pool_id(client: TeamTailorClient, pool_name: str) -> Optional[str]:
    """Find prospect pool ID by name."""
    try:
        _response = client.get("/metadata/prospect_pools")
        pools = response.get("data", [])

        for _pool in pools:
            if pool.get("attributes", {}).get("name") == pool_name:
                return pool.get("id")

        return None
    except Exception as e:
        logger.error("Failed to find prospect pool %s: %s", pool_name, e)
        return None


# =============================================================================
# GET ENDPOINTS
# =============================================================================


@router.get("/", response_model=CandidatesListResponse)
async def get_candidates(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    prospect_pool: Optional[str] = Query(None, description="Filter by prospect pool"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    search: Optional[str] = Query(None, description="Search in name or email"),
) -> CandidatesListResponse:
    """
    Get all candidates with optional filtering.

    Supports filtering by prospect pool, tags, and text search.
    """
    try:
        client = TeamTailorClient()

        # Build query parameters
        params = {
            "page[number]": page,
            "page[size]": per_page,
        }

        if search:
            params["filter[search]"] = search

        if tags:
            tag_list = [tag.strip() for _tag in tags.split(",")]
            params["filter[tags]"] = ",".join(tag_list)

        # Get candidates
        _response = client.get_candidates(params=params)
        candidates_data = response.get("data", [])

        # Convert to our format
        _candidates = []
        for _candidate_data in candidates_data:
            candidate = _normalize_teamtailor_candidate(candidate_data)

            # Filter by prospect pool if specified
            if prospect_pool and candidate.prospect_pool != prospect_pool:
                continue

            candidates.append(candidate)

        return CandidatesListResponse(
            _candidates=candidates,
            _total=response.get("meta", {}).get("total", len(candidates)),
            page=page,
            per_page=per_page,
        )

    except Exception as e:
        logger.error("Failed to get candidates: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to get candidates: {str(e)}"
        )


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: str) -> CandidateResponse:
    """Get a specific candidate by ID."""
    try:
        client = TeamTailorClient()
        _response = client.get_candidate(candidate_id)

        if "data" not in _response:
            raise HTTPException(status_code=404, detail="Candidate not found")

        return _normalize_teamtailor_candidate(_response["data"])

    except Exception as e:
        logger.error("Failed to get candidate %s: %s", candidate_id, e)
        raise HTTPException(
            status_code=500, detail=f"Failed to get candidate: {str(e)}"
        )


@router.get("/{candidate_id}/activity", response_model=Dict[str, Any])
async def get_candidate_activity(candidate_id: str) -> Dict[str, Any]:
    """Get candidate activity feed."""
    try:
        client = TeamTailorClient()
        _response = client.get_candidate_activity_feed(candidate_id)
        return _response

    except Exception as e:
        logger.error("Failed to get candidate activity %s: %s", candidate_id, e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get candidate activity: {str(e)}",
        )


@router.get("/prospects/pools", response_model=List[ProspectPoolResponse])
async def get_prospect_pools() -> List[ProspectPoolResponse]:
    """Get all prospect pools."""
    try:
        client = TeamTailorClient()
        _response = client.get("/metadata/prospect_pools")

        pools = []
        for pool_data in _response.get("data", []):
            attributes = pool_data.get("attributes", {})
            pools.append(
                ProspectPoolResponse(
                    id=pool_data.get("id", ""),
                    name=attributes.get("name", ""),
                    description=attributes.get("description"),
                    candidate_count=attributes.get("candidate-count", 0),
                )
            )

        return pools

    except Exception as e:
        logger.error("Failed to get prospect pools: %s", e)
        raise HTTPException(
            status_code=500, detail=f"Failed to get prospect pools: {str(e)}"
        )


# =============================================================================
# POST ENDPOINTS
# =============================================================================


@router.post("/", response_model=CandidateResponse)
async def create_candidate(
    request: CandidateCreateRequest,
) -> CandidateResponse:
    """
    Create a new candidate.

    If prospect_pool is specified, the candidate will be added to that pool.
    """
    try:
        client = TeamTailorClient()

        # Build candidate payload
        payload = _build_candidate_payload(request)

        # Create candidate
        logger.info("Creating candidate with payload: %s", payload)
        _response = client.create_candidate(payload)

        if "data" not in _response:
            raise HTTPException(status_code=400, detail="Failed to create candidate")

        candidate = _normalize_teamtailor_candidate(_response["data"])

        # Add to prospect pool if specified
        if request.prospect_pool:
            pool_id = _find_prospect_pool_id(client, request.prospect_pool)
            if pool_id:
                try:
                    # Add candidate to prospect pool
                    pool_payload = {
                        "data": {
                            "type": "prospect_pool_candidates",
                            "attributes": {
                                "candidate-id": candidate.id,
                                "prospect-pool-id": pool_id,
                            },
                        }
                    }
                    client.post("/prospect_pool_candidates", json_data=pool_payload)
                    candidate.prospect_pool = request.prospect_pool
                except Exception as e:
                    logger.warning("Failed to add candidate to prospect pool: %s", e)
            else:
                logger.warning("Prospect pool '%s' not found", request.prospect_pool)

        return candidate

    except Exception as e:
        logger.error("Failed to create candidate: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to create candidate: {str(e)}"
        )


@router.post("/prospects", response_model=CandidateResponse)
async def create_prospect(
    request: CandidateCreateRequest,
) -> CandidateResponse:
    """
    Create a new prospect (candidate in a prospect pool).

    This is a convenience endpoint that automatically adds the candidate
    to the specified prospect pool.
    """
    if not request.prospect_pool:
        raise HTTPException(
            status_code=400, detail="prospect_pool is required for prospects"
        )

    return await create_candidate(request)


@router.post("/bulk", response_model=Dict[str, Any])
async def create_candidates_bulk(
    candidates: List[CandidateCreateRequest],
    prospect_pool: Optional[str] = Query(
        None, description="Default prospect pool for all candidates"
    ),
) -> Dict[str, Any]:
    """
    Create multiple candidates in bulk.

    Useful for mass migration from Greenhouse backup.
    """
    try:
        client = TeamTailorClient()

        _results = {"created": 0, "failed": 0, "errors": [], "candidates": []}

        for i, candidate_request in enumerate(candidates):
            try:
                # Use default prospect pool if not specified
                if prospect_pool and not candidate_request.prospect_pool:
                    candidate_request.prospect_pool = prospect_pool

                payload = _build_candidate_payload(candidate_request)
                _response = client.create_candidate(payload)

                if "data" in response:
                    candidate = _normalize_teamtailor_candidate(_response["data"])
                    results["candidates"].append(candidate)
                    results["created"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(
                        {
                            "index": i,
                            "error": "Failed to create candidate",
                            "data": candidate_request.dict(),
                        }
                    )

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "index": i,
                        "error": str(e),
                        "data": candidate_request.dict(),
                    }
                )

        return results

    except Exception as e:
        logger.error("Failed to create candidates bulk: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to create candidates: {str(e)}"
        )


# =============================================================================
# MIGRATION ENDPOINTS
# =============================================================================


@router.post("/migrate/greenhouse", response_model=Dict[str, Any])
async def migrate_greenhouse_candidates(
    limit: Optional[int] = Query(
        None, description="Limit number of candidates to migrate"
    ),
    offset: Optional[int] = Query(0, description="Offset to start migration from"),
    prospect_pool: Optional[str] = Query(
        None, description="Target prospect pool for migrated candidates"
    ),
    update_existing: bool = Query(
        False, description="Update existing candidates with additional data"
    ),
) -> Dict[str, Any]:
    """
    Migrate candidates from Greenhouse backup to TeamTailor.

    This endpoint reads the Greenhouse backup data and creates
    corresponding candidates in TeamTailor.
    """
    try:
        # Import here to avoid circular imports
        from routes.export_team_tailor import _load_export

        # Load Greenhouse backup
        export_data = _load_export()
        greenhouse_candidates = export_data.get("candidates", [])

        # Apply offset and limit
        if offset:
            greenhouse_candidates = greenhouse_candidates[offset:]
        if limit:
            greenhouse_candidates = greenhouse_candidates[:limit]

        # Convert Greenhouse format to our format
        candidates_to_create = []
        for _gh_candidate in greenhouse_candidates:
            # Extract email (take first one if multiple)
            emails = gh_candidate.get("emails", [])
            _email = emails[0].get("value") if emails else None

            # Extract phone (take first one if multiple)
            phones = gh_candidate.get("phones", [])
            phone = phones[0].get("value") if phones else None

            # Extract LinkedIn URL
            linkedin_url = None
            _custom_fields = gh_candidate.get("custom_fields", {})
            if custom_fields.get("linked_in"):
                linkedin_url = custom_fields["linked_in"]

            # Generate temporary email if none exists (TeamTailor requires email)
            if not email:
                external_id = gh_candidate.get("external_id", "")
                _email = "migrated-{external_id}@greenhouse-migration.com"

            # Create pitch from custom fields
            pitch_parts = []
            if custom_fields.get("rol_actual"):
                pitch_parts.append("Rol actual: {custom_fields['rol_actual']}")
            if custom_fields.get("rol_deseado"):
                pitch_parts.append("Rol deseado: {custom_fields['rol_deseado']}")
            if custom_fields.get("tecnología_principal"):
                pitch_parts.append(
                    "Tecnología principal: {custom_fields['tecnología_principal']}"
                )
            if custom_fields.get("seniority_autopercibido"):
                pitch_parts.append(
                    "Seniority: {custom_fields['seniority_autopercibido']}"
                )

            pitch = " | ".join(pitch_parts) if pitch_parts else None

            # For now, skip custom_fields as they cause issues with TeamTailor API
            # TODO: Implement custom fields mapping later

            candidate_request = CandidateCreateRequest(
                _first_name=gh_candidate.get("first_name", ""),
                _last_name=gh_candidate.get("last_name", ""),
                _email=email,
                phone=phone,
                linkedin_url=linkedin_url,
                pitch=pitch,
                external_id=None,  # Not supported by TeamTailor
                tags=gh_candidate.get("tags", []),
                prospect_pool=prospect_pool,
                _custom_fields={},  # Skip custom fields for now
            )
            candidates_to_create.append(candidate_request)

        # Get existing emails from TeamTailor to avoid duplicates
        existing_emails = set()
        try:
            client = TeamTailorClient()
            all_candidates = client.get_candidates(params={"page[size]": 100})
            existing_emails = {
                candidate["attributes"]["email"]
                for _candidate in all_candidates.get("data", [])
                if candidate["attributes"].get("email")
            }
            logger.info("Found %d existing emails in TeamTailor", len(existing_emails))
        except Exception as e:
            logger.warning("Could not fetch existing emails: %s", e)

        # Filter out candidates that already exist
        filtered_candidates = []
        skipped_count = 0

        for _candidate_request in candidates_to_create:
            if candidate_request.email in existing_emails:
                skipped_count += 1
                continue
            filtered_candidates.append(candidate_request)

        logger.info(
            "Filtered candidates: %d to create, %d skipped (already exist)",
            len(filtered_candidates),
            skipped_count,
        )

        # Create candidates in bulk
        return await create_candidates_bulk(filtered_candidates, prospect_pool)

    except Exception as e:
        logger.error("Failed to migrate Greenhouse candidates: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to migrate candidates: {str(e)}"
        )


@router.post("/update-with-greenhouse-data", response_model=Dict[str, Any])
async def update_candidates_with_greenhouse_data(
    limit: Optional[int] = Query(
        None, description="Limit number of candidates to update"
    ),
    offset: Optional[int] = Query(0, description="Offset to start update from"),
) -> Dict[str, Any]:
    """
    Update existing candidates with additional data from Greenhouse backup.

    This endpoint finds candidates that were migrated from Greenhouse and
    updates them with additional data like LinkedIn URLs, phone numbers,
    and professional information.
    """
    try:
        # Import here to avoid circular imports
        from routes.export_team_tailor import _load_export

        # Load Greenhouse backup
        export_data = _load_export()
        greenhouse_candidates = export_data.get("candidates", [])

        # Apply offset and limit
        if offset:
            greenhouse_candidates = greenhouse_candidates[offset:]
        if limit:
            greenhouse_candidates = greenhouse_candidates[:limit]

        client = TeamTailorClient()
        _results = {"updated": 0, "failed": 0, "errors": [], "candidates": []}

        for i, gh_candidate in enumerate(greenhouse_candidates):
            try:
                # Find candidate by email or generated email
                _email = None
                if gh_candidate.get("emails"):
                    _email = gh_candidate["emails"][0]["value"]
                else:
                    external_id = gh_candidate.get("external_id", "")
                    _email = "migrated-{external_id}@greenhouse-migration.com"

                # Search for _candidate in TeamTailor
                candidates_response = client.get_candidates(
                    params={"filter[email]": email}
                )

                if not candidates_response.get("data"):
                    continue  # Candidate not found, skip

                candidate_id = candidates_response["data"][0]["id"]

                # Prepare update data
                update_data = {}
                _custom_fields = gh_candidate.get("custom_fields", {})

                # Add phone if available
                if gh_candidate.get("phones"):
                    update_data["phone"] = gh_candidate["phones"][0]["value"]

                # Add LinkedIn if available
                if custom_fields.get("linked_in"):
                    update_data["linkedin-url"] = custom_fields["linked_in"]

                # Create pitch from custom fields
                pitch_parts = []
                if custom_fields.get("rol_actual"):
                    pitch_parts.append("Rol actual: {custom_fields['rol_actual']}")
                if custom_fields.get("rol_deseado"):
                    pitch_parts.append("Rol deseado: {custom_fields['rol_deseado']}")
                if custom_fields.get("tecnología_principal"):
                    pitch_parts.append(
                        "Tecnología principal: {custom_fields['tecnología_principal']}"
                    )
                if custom_fields.get("seniority_autopercibido"):
                    pitch_parts.append(
                        "Seniority: {custom_fields['seniority_autopercibido']}"
                    )

                if pitch_parts:
                    update_data["pitch"] = " | ".join(pitch_parts)

                # Update candidate if we have data to update
                if update_data:
                    payload = {
                        "data": {
                            "id": candidate_id,
                            "type": "candidates",
                            "attributes": update_data,
                        }
                    }

                    _response = client.patch("/candidates/{candidate_id}", payload)

                    if "data" in response:
                        candidate = _normalize_teamtailor_candidate(_response["data"])
                        results["candidates"].append(candidate)
                        results["updated"] += 1
                        logger.info(
                            "Updated candidate %s with additional data",
                            candidate_id,
                        )
                    else:
                        results["failed"] += 1
                        results["errors"].append(
                            {
                                "index": i,
                                "error": "Failed to update candidate",
                                "candidate_id": candidate_id,
                                "email": email,
                            }
                        )

            except Exception as e:
                results["failed"] += 1
                results["errors"].append(
                    {
                        "index": i,
                        "error": str(e),
                        "external_id": gh_candidate.get("external_id"),
                    }
                )

        return results

    except Exception as e:
        logger.error("Failed to update candidates with Greenhouse data: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to update candidates: {str(e)}"
        )


@router.get("/duplicates/analyze", response_model=Dict[str, Any])
async def analyze_duplicates() -> Dict[str, Any]:
    """
    Analyze duplicates in the Greenhouse backup data.

    This endpoint identifies and categorizes different types of duplicates
    found in the Greenhouse backup, helping to understand data quality.
    """
    try:
        # Import here to avoid circular imports
        from routes.export_team_tailor import _load_export

        # Load Greenhouse backup
        export_data = _load_export()
        greenhouse_candidates = export_data.get("candidates", [])

        # Analyze different types of duplicates
        email_duplicates = {}
        name_duplicates = {}
        phone_duplicates = {}
        linkedin_duplicates = {}

        for _candidate in greenhouse_candidates:
            # Email duplicates
            emails = candidate.get("emails", [])
            for _email_data in emails:
                _email = email_data.get("value", "").lower()
                if email:
                    if email not in email_duplicates:
                        email_duplicates[email] = []
                    email_duplicates[email].append(
                        {
                            "external_id": candidate.get("external_id"),
                            "first_name": candidate.get("first_name"),
                            "last_name": candidate.get("last_name"),
                        }
                    )

            # Name duplicates (first + last name)
            _first_name = candidate.get("first_name", "").lower().strip()
            _last_name = candidate.get("last_name", "").lower().strip()
            full_name = "{first_name} {last_name}"
            if first_name and last_name:
                if full_name not in name_duplicates:
                    name_duplicates[full_name] = []
                name_duplicates[full_name].append(
                    {
                        "external_id": candidate.get("external_id"),
                        "email": emails[0].get("value") if emails else None,
                    }
                )

            # Phone duplicates
            phones = candidate.get("phones", [])
            for _phone_data in phones:
                phone = phone_data.get("value", "").strip()
                if phone:
                    if phone not in phone_duplicates:
                        phone_duplicates[phone] = []
                    phone_duplicates[phone].append(
                        {
                            "external_id": candidate.get("external_id"),
                            "first_name": candidate.get("first_name"),
                            "last_name": candidate.get("last_name"),
                        }
                    )

            # LinkedIn duplicates
            _custom_fields = candidate.get("custom_fields", {})
            linkedin = custom_fields.get("linked_in", "")
            if linkedin:
                if linkedin not in linkedin_duplicates:
                    linkedin_duplicates[linkedin] = []
                linkedin_duplicates[linkedin].append(
                    {
                        "external_id": candidate.get("external_id"),
                        "first_name": candidate.get("first_name"),
                        "last_name": candidate.get("last_name"),
                    }
                )

        # Filter only actual duplicates (more than 1 occurrence)
        email_duplicates = {k: v for k, v in email_duplicates.items() if len(v) > 1}
        name_duplicates = {k: v for k, v in name_duplicates.items() if len(v) > 1}
        phone_duplicates = {k: v for k, v in phone_duplicates.items() if len(v) > 1}
        linkedin_duplicates = {
            k: v for k, v in linkedin_duplicates.items() if len(v) > 1
        }

        # Calculate statistics
        total_candidates = len(greenhouse_candidates)
        candidates_with_email_duplicates = sum(
            len(v) for _v in email_duplicates.values()
        )
        candidates_with_name_duplicates = sum(len(v) for _v in name_duplicates.values())
        candidates_with_phone_duplicates = sum(
            len(v) for _v in phone_duplicates.values()
        )
        candidates_with_linkedin_duplicates = sum(
            len(v) for _v in linkedin_duplicates.values()
        )

        return {
            "total_candidates": total_candidates,
            "duplicate_analysis": {
                "email_duplicates": {
                    "count": len(email_duplicates),
                    "affected_candidates": candidates_with_email_duplicates,
                    "percentage": round(
                        (candidates_with_email_duplicates / total_candidates) * 100,
                        2,
                    ),
                    "examples": dict(
                        list(email_duplicates.items())[:5]
                    ),  # First 5 examples
                },
                "name_duplicates": {
                    "count": len(name_duplicates),
                    "affected_candidates": candidates_with_name_duplicates,
                    "percentage": round(
                        (candidates_with_name_duplicates / total_candidates) * 100,
                        2,
                    ),
                    "examples": dict(
                        list(name_duplicates.items())[:5]
                    ),  # First 5 examples
                },
                "phone_duplicates": {
                    "count": len(phone_duplicates),
                    "affected_candidates": candidates_with_phone_duplicates,
                    "percentage": round(
                        (candidates_with_phone_duplicates / total_candidates) * 100,
                        2,
                    ),
                    "examples": dict(
                        list(phone_duplicates.items())[:5]
                    ),  # First 5 examples
                },
                "linkedin_duplicates": {
                    "count": len(linkedin_duplicates),
                    "affected_candidates": candidates_with_linkedin_duplicates,
                    "percentage": round(
                        (candidates_with_linkedin_duplicates / total_candidates) * 100,
                        2,
                    ),
                    "examples": dict(
                        list(linkedin_duplicates.items())[:5]
                    ),  # First 5 examples
                },
            },
            "summary": {
                "total_duplicate_groups": len(email_duplicates)
                + len(name_duplicates)
                + len(phone_duplicates)
                + len(linkedin_duplicates),
                "total_affected_candidates": candidates_with_email_duplicates
                + candidates_with_name_duplicates
                + candidates_with_phone_duplicates
                + candidates_with_linkedin_duplicates,
                "data_quality_score": round(
                    (
                        (
                            total_candidates
                            - (
                                candidates_with_email_duplicates
                                + candidates_with_name_duplicates
                                + candidates_with_phone_duplicates
                                + candidates_with_linkedin_duplicates
                            )
                        )
                        / total_candidates
                    )
                    * 100,
                    2,
                ),
            },
        }

    except Exception as e:
        logger.error("Failed to analyze duplicates: %s", e)
        raise HTTPException(
            status_code=500, detail="Failed to analyze duplicates: {str(e)}"
        )


@router.get("/duplicates/detailed", response_model=Dict[str, Any])
async def get_detailed_duplicates(
    duplicate_type: str = Query(
        ..., description="Type of duplicate: email, name, phone, linkedin"
    ),
    limit: int = Query(10, description="Number of examples to return"),
) -> Dict[str, Any]:
    """
    Get detailed information about specific types of duplicates.

    This endpoint provides detailed information about duplicates found
    in the Greenhouse backup data, including full candidate information.
    """
    try:
        # Import here to avoid circular imports
        from routes.export_team_tailor import _load_export

        # Load Greenhouse backup
        export_data = _load_export()
        greenhouse_candidates = export_data.get("candidates", [])

        # Analyze duplicates based on type
        duplicates = {}

        for _candidate in greenhouse_candidates:
            if _duplicate_type == "email":
                emails = candidate.get("emails", [])
                for _email_data in emails:
                    _email = email_data.get("value", "").lower()
                    if email:
                        if email not in duplicates:
                            duplicates[email] = []
                        duplicates[email].append(
                            {
                                "external_id": candidate.get("external_id"),
                                "first_name": candidate.get("first_name"),
                                "last_name": candidate.get("last_name"),
                                "emails": candidate.get("emails", []),
                                "phones": candidate.get("phones", []),
                                "custom_fields": candidate.get("custom_fields", {}),
                                "tags": candidate.get("tags", []),
                            }
                        )

            elif _duplicate_type == "name":
                _first_name = candidate.get("first_name", "").lower().strip()
                _last_name = candidate.get("last_name", "").lower().strip()
                full_name = "{first_name} {last_name}"
                if first_name and last_name:
                    if full_name not in duplicates:
                        duplicates[full_name] = []
                    duplicates[full_name].append(
                        {
                            "external_id": candidate.get("external_id"),
                            "first_name": candidate.get("first_name"),
                            "last_name": candidate.get("last_name"),
                            "emails": candidate.get("emails", []),
                            "phones": candidate.get("phones", []),
                            "custom_fields": candidate.get("custom_fields", {}),
                            "tags": candidate.get("tags", []),
                        }
                    )

            elif _duplicate_type == "phone":
                phones = candidate.get("phones", [])
                for _phone_data in phones:
                    phone = phone_data.get("value", "").strip()
                    if phone:
                        if phone not in duplicates:
                            duplicates[phone] = []
                        duplicates[phone].append(
                            {
                                "external_id": candidate.get("external_id"),
                                "first_name": candidate.get("first_name"),
                                "last_name": candidate.get("last_name"),
                                "emails": candidate.get("emails", []),
                                "phones": candidate.get("phones", []),
                                "custom_fields": candidate.get("custom_fields", {}),
                                "tags": candidate.get("tags", []),
                            }
                        )

            elif _duplicate_type == "linkedin":
                _custom_fields = candidate.get("custom_fields", {})
                linkedin = custom_fields.get("linked_in", "")
                if linkedin:
                    if linkedin not in duplicates:
                        duplicates[linkedin] = []
                    duplicates[linkedin].append(
                        {
                            "external_id": candidate.get("external_id"),
                            "first_name": candidate.get("first_name"),
                            "last_name": candidate.get("last_name"),
                            "emails": candidate.get("emails", []),
                            "phones": candidate.get("phones", []),
                            "custom_fields": candidate.get("custom_fields", {}),
                            "tags": candidate.get("tags", []),
                        }
                    )

        # Filter only actual duplicates and limit results
        duplicates = {k: v for k, v in duplicates.items() if len(v) > 1}
        limited_duplicates = dict(list(duplicates.items())[:limit])

        return {
            "duplicate_type": duplicate_type,
            "total_duplicate_groups": len(duplicates),
            "examples_shown": len(limited_duplicates),
            "duplicates": limited_duplicates,
        }

    except Exception as e:
        logger.error("Failed to get detailed duplicates: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Failed to get detailed duplicates: {str(e)}",
        )


@router.get("/sourced/analytics/overview")
async def get_sourced_candidates_analytics():
    """Get analytics for sourced candidates (prospects)."""
    try:
        # Check if we're in test mode
        test_mode = os.getenv("TEAMTAILOR_TEST_MODE", "false").lower() == "true"

        if test_mode:
            # Return mock data for testing
            return {
                "overview": {
                    "total_sourced": 3129,
                    "unique_tags": 45,
                    "average_tags_per_candidate": 2.3,
                    "total_categories": 5,
                    "migration_status": {
                        "total_migrated": 2890,
                        "pending_migration": 239,
                        "migration_success_rate": 92.4,
                    },
                    "engagement_overview": {
                        "high_engagement": 1874,
                        "medium_engagement": 876,
                        "low_engagement": 379,
                        "avg_engagement_rate": 78.5,
                    },
                    "top_tags": {
                        "Full Stack": 234,
                        "React": 189,
                        "Python": 156,
                        "JavaScript": 145,
                        "Node.js": 123,
                        "Product Manager": 98,
                        "UX Designer": 87,
                        "Data Scientist": 76,
                        "Sales Manager": 65,
                        "Marketing Specialist": 54,
                    },
                },
                "sourced_analytics": [
                    {
                        "category": {
                            "id": "category-1",
                            "name": "Engineering",
                            "description": "Software engineers and developers",
                            "color": "#3B82F6",
                        },
                        "candidate_count": 1890,
                        "engagement_rates": {
                            "email": 92.5,
                            "phone": 78.3,
                            "linkedin": 85.7,
                        },
                    },
                    {
                        "category": {
                            "id": "category-2",
                            "name": "Product",
                            "description": "Product managers and designers",
                            "color": "#10B981",
                        },
                        "candidate_count": 456,
                        "engagement_rates": {
                            "email": 88.2,
                            "phone": 82.1,
                            "linkedin": 91.3,
                        },
                    },
                    {
                        "category": {
                            "id": "category-3",
                            "name": "Data Science",
                            "description": "Data scientists and analysts",
                            "color": "#F59E0B",
                        },
                        "candidate_count": 234,
                        "engagement_rates": {
                            "email": 85.7,
                            "phone": 75.4,
                            "linkedin": 88.9,
                        },
                    },
                    {
                        "category": {
                            "id": "category-4",
                            "name": "Sales",
                            "description": "Sales professionals",
                            "color": "#EF4444",
                        },
                        "candidate_count": 345,
                        "engagement_rates": {
                            "email": 95.2,
                            "phone": 89.6,
                            "linkedin": 82.4,
                        },
                    },
                    {
                        "category": {
                            "id": "category-5",
                            "name": "Marketing",
                            "description": "Marketing specialists",
                            "color": "#8B5CF6",
                        },
                        "candidate_count": 204,
                        "engagement_rates": {
                            "email": 87.8,
                            "phone": 71.2,
                            "linkedin": 93.1,
                        },
                    },
                ],
                "tag_distribution": {
                    "sourced": 3129,
                    "prospect": 3129,
                    "imported-from-greenhouse": 2890,
                    "mock-test": 3,
                    "backend": 156,
                    "python": 156,
                    "ui-ux": 87,
                    "design": 87,
                    "frontend": 145,
                    "javascript": 145,
                },
            }

        # Use real TeamTailor API
        client = TeamTailorClient()

        # Get all candidates with "sourced" tag or status
        params = {
            "page[size]": 100,
            "filter[tags]": "sourced,prospect,imported-from-greenhouse",
        }

        all_candidates = []
        page_after = None

        while True:
            if page_after:
                params["page[after]"] = page_after

            _response = client.get("/candidates", params=params)
            _candidates = response.get("data", [])

            if not candidates:
                break

            all_candidates.extend(candidates)

            # Check if there are more pages
            links = response.get("links", {})
            if "next" not in links:
                break

            # Extract next page cursor
            next_url = links["next"]
            if "page%5Bafter%5D=" in next_url:
                page_after = next_url.split("page%5Bafter%5D=")[1].split("&")[0]
            else:
                break

        # Analyze sourced candidates data
        total_sourced = len(all_candidates)
        all_tags = []
        tag_counts = {}

        for _candidate in all_candidates:
            attributes = candidate.get("attributes", {})
            tags = attributes.get("tags", [])
            all_tags.extend(tags)

            for _tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Get top 10 tags (excluding system tags)
        system_tags = {"prospect", "imported-from-greenhouse", "sourced"}
        filtered_tags = {k: v for k, v in tag_counts.items() if k not in system_tags}
        top_tags = dict(
            sorted(filtered_tags.items(), key=lambda x: x[1], reverse=True)[:10]
        )

        # Get specific tag counts for dashboard
        tag_distribution = {
            "sourced": tag_counts.get("sourced", 0),
            "prospect": tag_counts.get("prospect", 0),
            "imported-from-greenhouse": tag_counts.get("imported-from-greenhouse", 0),
            "mock-test": tag_counts.get("mock-test", 0),
            "backend": tag_counts.get("backend", 0),
            "python": tag_counts.get("python", 0),
            "ui-ux": tag_counts.get("ui-ux", 0),
            "design": tag_counts.get("design", 0),
            "frontend": tag_counts.get("frontend", 0),
            "javascript": tag_counts.get("javascript", 0),
        }

        # Calculate average tags per candidate
        avg_tags_per_candidate = (
            len(all_tags) / total_sourced if total_sourced > 0 else 0
        )

        # Create category analysis based on tags
        categories = {
            "Engineering": {
                "tags": [
                    "Full Stack",
                    "React",
                    "Python",
                    "JavaScript",
                    "Node.js",
                    "Java",
                    "DevOps",
                    "AWS",
                    "Docker",
                    "Kubernetes",
                ],
                "count": 0,
                "color": "#3B82F6",
            },
            "Product": {
                "tags": [
                    "Product Manager",
                    "UX",
                    "UI",
                    "Design",
                    "Figma",
                    "Sketch",
                ],
                "count": 0,
                "color": "#10B981",
            },
            "Data Science": {
                "tags": [
                    "Data Scientist",
                    "Machine Learning",
                    "AI",
                    "Analytics",
                    "SQL",
                    "Python",
                ],
                "count": 0,
                "color": "#F59E0B",
            },
            "Sales": {
                "tags": [
                    "Sales",
                    "Account Executive",
                    "Business Development",
                    "Sales Manager",
                ],
                "count": 0,
                "color": "#EF4444",
            },
            "Marketing": {
                "tags": [
                    "Marketing",
                    "Digital Marketing",
                    "Content",
                    "SEO",
                    "Growth",
                ],
                "count": 0,
                "color": "#8B5CF6",
            },
        }

        # Count candidates by category
        for _candidate in all_candidates:
            attributes = candidate.get("attributes", {})
            tags = attributes.get("tags", [])

            for category, config in categories.items():
                if any(tag in config["tags"] for _tag in tags):
                    config["count"] += 1
                    break

        # Create analytics response
        sourced_analytics = []
        for category_name, config in categories.items():
            if config["count"] > 0:
                sourced_analytics.append(
                    {
                        "category": {
                            "id": "category-{len(sourced_analytics) + 1}",
                            "name": category_name,
                            "description": "{category_name.lower()} professionals",
                            "color": config["color"],
                        },
                        "candidate_count": config["count"],
                        "engagement_rates": {
                            "email": round(
                                85 + (config["count"] / total_sourced) * 15, 1
                            ),
                            "phone": round(
                                70 + (config["count"] / total_sourced) * 25, 1
                            ),
                            "linkedin": round(
                                80 + (config["count"] / total_sourced) * 20, 1
                            ),
                        },
                    }
                )

        return {
            "overview": {
                "total_sourced": total_sourced,
                "unique_tags": len(set(all_tags)),
                "average_tags_per_candidate": round(avg_tags_per_candidate, 1),
                "top_tags": top_tags,
            },
            "tag_distribution": tag_distribution,
            "sourced_analytics": sourced_analytics,
        }

    except Exception as e:
        logger.error("Failed to get sourced candidates analytics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get sourced candidates analytics: {str(e)}",
        )


@router.post("/migrate-prospects")
async def migrate_prospects_as_sourced():
    """Migrate prospects from Greenhouse backup as sourced candidates."""
    try:
        # Load Greenhouse backup data
        from routes.utils import load_export_data

        backup_data = load_export_data()

        _candidates = backup_data.get("candidates", [])
        client = TeamTailorClient()

        migrated = 0
        errors = []

        for _candidate in candidates:
            try:
                # Create candidate payload with sourced tags
                payload = {
                    "data": {
                        "type": "candidates",
                        "attributes": {
                            "first-name": candidate.get("first_name", ""),
                            "last-name": candidate.get("last_name", ""),
                            "email": (
                                candidate.get("emails", [{}])[0].get("value")
                                if candidate.get("emails")
                                else None
                            ),
                            "phone": (
                                candidate.get("phones", [{}])[0].get("value")
                                if candidate.get("phones")
                                else None
                            ),
                            "tags": [
                                "prospect",
                                "imported-from-greenhouse",
                                "sourced",
                            ]
                            + candidate.get("tags", []),
                            "external-id": candidate.get("external_id"),
                        },
                    }
                }

                # Create candidate
                _response = client.post("/candidates", json=payload)

                if response.status_code in (200, 201):
                    migrated += 1
                else:
                    errors.append(
                        {
                            "external_id": candidate.get("external_id"),
                            "error": "Status {response.status_code}: {response.text}",
                        }
                    )

            except Exception as e:
                errors.append(
                    {
                        "external_id": candidate.get("external_id"),
                        "error": str(e),
                    }
                )

        return {
            "migrated": migrated,
            "errors": errors,
            "total": len(candidates),
        }

    except Exception as e:
        logger.error("Failed to migrate prospects: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Failed to migrate prospects: {str(e)}"
        )
