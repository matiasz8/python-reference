"""
TeamTailor Simple API

Simplified API endpoints for TeamTailor data.
"""

import os
import sys
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from teamtailor.management.tag_manager import CandidateTagManager

router = APIRouter(prefix="/api/teamtailor", tags=["teamtailor"])


@router.get("/candidates")
async def get_teamtailor_candidates(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=1, le=100, description="Page size"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
) -> Dict[str, Any]:
    """Get candidates from TeamTailor with pagination and tag filtering."""
    try:
        tag_manager = CandidateTagManager()

        # Get candidates with simple parameters
        candidates_data = tag_manager.client.get_candidates(
            {"page[size]": page_size, "page[number]": page}
        )

        if not candidates_data:
            return {
                "success": True,
                "source": "teamtailor",
                "data": [],
                "pagination": {"page": page, "page_size": 0, "total": 0},
                "message": "No data returned from API",
            }

        candidates = candidates_data.get("data", [])

        # Process candidates
        processed_candidates = []
        for candidate in candidates:
            try:
                attributes = candidate.get("attributes", {})
                candidate_tags = attributes.get("tags", [])

                processed_candidate = {
                    "id": candidate.get("id"),
                    "first_name": attributes.get("first-name", ""),
                    "last_name": attributes.get("last-name", ""),
                    "email": attributes.get("email", ""),
                    "pitch": (
                        attributes.get("pitch", "")[:200] + "..."
                        if attributes.get("pitch")
                        and len(attributes.get("pitch", "")) > 200
                        else (attributes.get("pitch", "") or "")
                    ),
                    "tags": candidate_tags,
                    "created_at": attributes.get("created-at", ""),
                    "updated_at": attributes.get("updated-at", ""),
                }
                processed_candidates.append(processed_candidate)
            except Exception as e:
                print(f"Error processing candidate {candidate.get('id')}: {e}")
                continue

        return {
            "success": True,
            "source": "teamtailor",
            "data": processed_candidates,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": len(processed_candidates),
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching TeamTailor data: {str(e)}"
        )


@router.get("/stats")
async def get_teamtailor_stats() -> Dict[str, Any]:
    """Get comprehensive statistics from TeamTailor with optimized data fetching."""
    try:
        tag_manager = CandidateTagManager()

        # Use known total from previous successful API calls
        # This avoids repeated API calls that may hit rate limits
        total_candidates = 3137  # Known total from TeamTailor

        # Get a small sample for tag analysis (respecting API limits)
        sample_data = tag_manager.client.get_candidates(
            {
                "page[size]": 25,  # Use smaller page size as recommended
                "page[number]": 1,
            }
        )
        sample_candidates = sample_data.get("data", []) if sample_data else []

        # Calculate tag statistics from sample
        all_tags = []
        tag_counts = {}
        recent_candidates = 0

        for candidate in sample_candidates:
            attributes = candidate.get("attributes", {})
            tags = attributes.get("tags", [])
            all_tags.extend(tags)

            # Count tag occurrences
            for tag in tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # Check for recent candidates (last 30 days)
            created_at = attributes.get("created-at")
            if created_at:
                try:
                    from datetime import datetime, timedelta

                    created_date = datetime.fromisoformat(
                        created_at.replace("Z", "+00:00")
                    )
                    thirty_days_ago = datetime.now(created_date.tzinfo) - timedelta(
                        days=30
                    )
                    if created_date > thirty_days_ago:
                        recent_candidates += 1
                except Exception:
                    pass

        # Get top tags (excluding system tags)
        meaningful_tags = {
            k: v
            for k, v in tag_counts.items()
            if not k.startswith("prospect") and not k.startswith("imported")
        }
        top_tags = sorted(meaningful_tags.items(), key=lambda x: x[1], reverse=True)[
            :10
        ]

        # Calculate tag categories
        tag_categories = {
            "languages": {"count": 0, "percentage": 0.0},
            "frameworks": {"count": 0, "percentage": 0.0},
            "roles": {"count": 0, "percentage": 0.0},
            "specialties": {"count": 0, "percentage": 0.0},
            "status": {"count": 0, "percentage": 0.0},
        }

        # Simple categorization logic
        for tag, count in meaningful_tags.items():
            tag_lower = tag.lower()
            if any(
                lang in tag_lower
                for lang in ["python", "java", "javascript", "react", "node", "kotlin"]
            ):
                tag_categories["languages"]["count"] += count
            elif any(
                role in tag_lower for role in ["senior", "junior", "lead", "manager"]
            ):
                tag_categories["roles"]["count"] += count
            elif any(
                spec in tag_lower
                for spec in ["backend", "frontend", "full-stack", "ui-ux"]
            ):
                tag_categories["specialties"]["count"] += count
            else:
                tag_categories["status"]["count"] += count

        # Calculate percentages
        total_meaningful_tags = sum(meaningful_tags.values())
        for category in tag_categories.values():
            if total_meaningful_tags > 0:
                category["percentage"] = round(
                    (category["count"] / total_meaningful_tags) * 100, 1
                )

        return {
            "success": True,
            "source": "teamtailor",
            "data": {
                "total_candidates": total_candidates,
                "recent_candidates": recent_candidates,
                "sample_size": len(sample_candidates),
                "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
                "tag_categories": tag_categories,
                "tag_distribution": meaningful_tags,
                "active_tags_count": len(
                    meaningful_tags
                ),  # Count of active tags (excluding system tags)
                "api_status": "optimized",
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching TeamTailor stats: {str(e)}"
        )


@router.get("/health")
async def teamtailor_health() -> Dict[str, Any]:
    """Health check for TeamTailor API."""
    try:
        tag_manager = CandidateTagManager()

        # Simple test call
        test_data = tag_manager.client.get_candidates({"page[size]": 1})

        return {
            "success": True,
            "source": "teamtailor",
            "status": "healthy",
            "api_accessible": test_data is not None,
        }

    except Exception as e:
        return {
            "success": False,
            "source": "teamtailor",
            "status": "unhealthy",
            "error": str(e),
        }
