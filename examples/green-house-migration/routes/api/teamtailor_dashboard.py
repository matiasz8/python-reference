"""
TeamTailor Dashboard API

API endpoints for TeamTailor dashboard data.
"""

import os
import sys
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from teamtailor.management.tag_manager import CandidateTagManager

router = APIRouter(prefix="/api/teamtailor", tags=["teamtailor-dashboard"])


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
            {"page[size]": 25, "page[number]": page}
        )

        if not candidates_data:
            return {
                "success": True,
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

                # Enhanced language detection
                language_tags = []
                for tag in candidate_tags:
                    tag_lower = tag.lower()
                    if tag_lower in [
                        "python",
                        "javascript",
                        "java",
                        "react",
                        "vue",
                        "angular",
                        "backend",
                        "frontend",
                        "full-stack",
                        "node.js",
                        "django",
                        "flask",
                        "spring",
                        "laravel",
                        "express",
                        "next.js",
                        "nuxt.js",
                        "svelte",
                        "ember",
                        "typescript",
                        "c#",
                        "c++",
                        "php",
                        "ruby",
                        "go",
                        "rust",
                        "swift",
                        "kotlin",
                        "scala",
                    ]:
                        language_tags.append(tag)

                processed_candidate = {
                    "id": candidate.get("id"),
                    "first_name": attributes.get("first-name", ""),
                    "last_name": attributes.get("last-name", ""),
                    "email": attributes.get("email", ""),
                    "pitch": (
                        (attributes.get("pitch", "")[:200] + "...")
                        if attributes.get("pitch")
                        and len(attributes.get("pitch", "")) > 200
                        else (attributes.get("pitch", "") or "")
                    ),
                    "tags": candidate_tags,
                    "created_at": attributes.get("created-at"),
                    "updated_at": attributes.get("updated-at"),
                    "languages": language_tags,
                }
                processed_candidates.append(processed_candidate)
            except Exception as candidate_error:
                # Skip problematic candidates silently
                continue

        return {
            "success": True,
            "data": processed_candidates,
            "pagination": {
                "page": page,
                "page_size": len(processed_candidates),
                "total": len(processed_candidates),
            },
        }

    except Exception as e:
        return {
            "success": True,
            "data": [],
            "pagination": {"page": page, "page_size": 0, "total": 0},
            "message": "Error fetching candidates",
        }


@router.get("/stats")
async def get_teamtailor_stats() -> Dict[str, Any]:
    """Get TeamTailor statistics."""
    try:
        tag_manager = CandidateTagManager()

        # Get more candidates for better statistics
        all_candidates = []
        page = 1
        page_size = 25
        max_candidates = 500  # Increased from 100 to 500

        # Get candidates for statistics (limited to avoid performance issues)
        while len(all_candidates) < max_candidates:
            try:
                candidates_data = tag_manager.client.get_candidates(
                    {"page[size]": page_size, "page[number]": page}
                )

                candidates = candidates_data.get("data", [])
                if not candidates:
                    break

                all_candidates.extend(candidates)
                page += 1

                # Add small delay to avoid rate limiting
                import asyncio

                await asyncio.sleep(0.1)

            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break

        # Calculate statistics
        total_candidates = len(all_candidates)

        # Tag statistics with improved language detection
        tag_counts = {}
        language_tags = {
            "python",
            "javascript",
            "java",
            "c#",
            "c++",
            "php",
            "ruby",
            "go",
            "rust",
            "swift",
            "kotlin",
            "scala",
            "typescript",
            "react",
            "vue",
            "angular",
            "node.js",
            "django",
            "flask",
            "spring",
            "laravel",
            "express",
            "next.js",
            "nuxt.js",
            "svelte",
            "ember",
        }

        for candidate in all_candidates:
            tags = candidate.get("attributes", {}).get("tags", [])
            for tag in tags:
                tag_lower = tag.lower()
                # Only count the original tag, not the language_ prefixed version
                if not tag_lower.startswith("language_"):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

        # Top tags
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:15]

        # Tag categories with improved detection
        tag_categories = {
            "languages": [
                "python",
                "javascript",
                "java",
                "c#",
                "c++",
                "php",
                "ruby",
                "go",
                "rust",
                "swift",
                "kotlin",
                "scala",
                "typescript",
            ],
            "frameworks": [
                "react",
                "vue",
                "angular",
                "django",
                "flask",
                "spring",
                "laravel",
                "express",
                "next.js",
                "nuxt.js",
                "svelte",
                "ember",
            ],
            "roles": ["senior", "junior", "lead", "manager", "architect", "consultant"],
            "specialties": [
                "backend",
                "frontend",
                "full-stack",
                "devops",
                "qa",
                "data-science",
                "mobile",
                "ui-ux",
            ],
            "status": [
                "prospect",
                "imported-from-greenhouse",
                "remote",
                "onsite",
                "hybrid",
            ],
        }

        category_stats = {}
        for category, tags in tag_categories.items():
            category_count = sum(tag_counts.get(tag, 0) for tag in tags)
            category_stats[category] = {
                "count": category_count,
                "percentage": (
                    round((category_count / total_candidates) * 100, 2)
                    if total_candidates > 0
                    else 0
                ),
            }

        return {
            "success": True,
            "data": {
                "total_candidates": total_candidates,
                "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags],
                "tag_categories": category_stats,
                "tag_distribution": tag_counts,
                "sample_size": max_candidates,
                "languages_detected": len(
                    [tag for tag in tag_counts.keys() if tag.startswith("language_")]
                ),
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching TeamTailor stats: {str(e)}"
        )


@router.get("/tags")
async def get_teamtailor_tags() -> Dict[str, Any]:
    """Get all available tags from TeamTailor."""
    try:
        tag_manager = CandidateTagManager()

        # Get available tags from tag manager
        available_tags = tag_manager.list_available_tags()

        # Get tag definitions
        tag_definitions = {}
        for tag in available_tags:
            definition = tag_manager.get_tag_definition(tag)
            if definition:
                tag_definitions[tag] = {
                    "category": definition.category.value,
                    "description": definition.description,
                    "examples": definition.examples,
                }

        return {
            "success": True,
            "data": {
                "available_tags": available_tags,
                "tag_definitions": tag_definitions,
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching TeamTailor tags: {str(e)}"
        )


@router.get("/search")
async def search_teamtailor_candidates(
    query: str = Query(..., description="Search query"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    limit: int = Query(50, ge=1, le=200, description="Maximum results"),
) -> Dict[str, Any]:
    """Search candidates in TeamTailor."""
    try:
        tag_manager = CandidateTagManager()

        # Get candidates for search
        all_candidates = []
        page = 1
        page_size = 25

        # Get candidates for search (limit to avoid performance issues)
        while len(all_candidates) < limit:
            try:
                candidates_data = tag_manager.client.get_candidates(
                    {"page[size]": page_size, "page[number]": page}
                )

                candidates = candidates_data.get("data", [])
                if not candidates:
                    break

                all_candidates.extend(candidates)
                page += 1

            except Exception as e:
                break

        # Search in candidates
        search_results = []
        query_lower = query.lower()

        for candidate in all_candidates:
            attributes = candidate.get("attributes", {})

            # Search in name, email, pitch
            name = f"{attributes.get('first-name', '')} {attributes.get('last-name', '')}".lower()
            email = attributes.get("email", "").lower()
            pitch = attributes.get("pitch", "").lower()

            if query_lower in name or query_lower in email or query_lower in pitch:
                # Apply tag filtering if specified
                if tags:
                    tag_list = [tag.strip() for tag in tags.split(",")]
                    candidate_tags = [tag.lower() for tag in attributes.get("tags", [])]
                    if not any(tag.lower() in candidate_tags for tag in tag_list):
                        continue

                search_results.append(
                    {
                        "id": candidate.get("id"),
                        "first_name": attributes.get("first-name", ""),
                        "last_name": attributes.get("last-name", ""),
                        "email": attributes.get("email", ""),
                        "pitch": attributes.get("pitch", ""),
                        "tags": attributes.get("tags", []),
                    }
                )

        # Limit results
        search_results = search_results[:limit]

        return {
            "success": True,
            "data": {
                "query": query,
                "results": search_results,
                "total": len(search_results),
            },
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching TeamTailor candidates: {str(e)}"
        )


@router.get("/test")
async def test_teamtailor_connection() -> Dict[str, Any]:
    """Test TeamTailor connection and return basic info."""
    try:
        tag_manager = CandidateTagManager()

        # Try to get just one page of candidates
        candidates_data = tag_manager.client.get_candidates(
            {"page[size]": 5, "page[number]": 1}
        )

        candidates = candidates_data.get("data", [])

        return {
            "success": True,
            "message": "TeamTailor connection successful",
            "data": {
                "connection": "OK",
                "candidates_found": len(candidates),
                "sample_candidates": [
                    {
                        "id": candidate.get("id"),
                        "name": f"{candidate.get('attributes', {}).get('first-name', '')} {candidate.get('attributes', {}).get('last-name', '')}",
                        "tags": candidate.get("attributes", {}).get("tags", []),
                    }
                    for candidate in candidates[:3]
                ],
            },
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"TeamTailor connection failed: {str(e)}",
            "data": {"connection": "ERROR", "error": str(e)},
        }


@router.get("/local/stats")
async def get_local_stats() -> Dict[str, Any]:
    """Get local statistics for dashboard."""
    try:
        import os
        from pathlib import Path

        # Get data directory
        data_dir = Path("data")

        # Count JSON files
        json_files = list(data_dir.rglob("*.json"))
        total_files = len(json_files)

        # Count unique candidates (not total lines)
        unique_candidates = set()
        total_items = 0

        # Only check a few files to avoid performance issues
        for json_file in json_files[:5]:  # Limit to first 5 files
            try:
                import json

                with open(json_file, encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        # Count unique candidates by ID or email
                        for item in data:
                            if isinstance(item, dict):
                                candidate_id = (
                                    item.get("id") or item.get("email") or str(item)
                                )
                                unique_candidates.add(candidate_id)
                    elif isinstance(data, dict):
                        # Single candidate
                        candidate_id = data.get("id") or data.get("email") or str(data)
                        unique_candidates.add(candidate_id)
            except Exception:
                continue

        # Estimate total unique candidates
        estimated_unique = (
            len(unique_candidates) * (total_files // 5)
            if total_files > 5
            else len(unique_candidates)
        )

        return {
            "success": True,
            "data": {
                "total_files": total_files,
                "total_items": estimated_unique,
                "last_update": "N/A",
                "success_rate": 100,
            },
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": {
                "total_files": 0,
                "total_items": 0,
                "last_update": "N/A",
                "success_rate": 0,
            },
        }


@router.get("/local/candidates")
async def get_local_candidates() -> Dict[str, Any]:
    """Get local candidates from JSON files."""
    try:
        import json
        import os
        from pathlib import Path

        # Get data directory
        data_dir = Path("data")

        # Look for specific candidate files first
        candidate_files = [
            data_dir / "json" / "candidates.json",
            data_dir / "csv" / "candidates.csv",
        ]

        all_candidates = []

        # Process candidate files
        for candidate_file in candidate_files:
            if candidate_file.exists() and candidate_file.suffix == ".json":
                try:
                    with open(candidate_file, encoding="utf-8") as f:
                        data = json.load(f)

                        if isinstance(data, dict) and "data" in data:
                            # TeamTailor format
                            candidates_data = data["data"]
                            for candidate in candidates_data:
                                if (
                                    isinstance(candidate, dict)
                                    and "attributes" in candidate
                                ):
                                    attrs = candidate["attributes"]
                                    candidate_info = {
                                        "id": candidate.get("id", ""),
                                        "first_name": attrs.get("first-name", ""),
                                        "last_name": attrs.get("last-name", ""),
                                        "email": attrs.get("email", ""),
                                        "pitch": attrs.get("pitch", ""),
                                        "tags": attrs.get("tags", []),
                                        "created_at": attrs.get("created-at", ""),
                                        "updated_at": attrs.get("updated-at", ""),
                                    }
                                    all_candidates.append(candidate_info)
                        elif isinstance(data, list):
                            # Direct list format
                            for candidate in data:
                                if isinstance(candidate, dict):
                                    candidate_info = {
                                        "id": candidate.get("id", ""),
                                        "first_name": candidate.get(
                                            "first_name",
                                            (
                                                candidate.get("name", "").split()[0]
                                                if candidate.get("name")
                                                else ""
                                            ),
                                        ),
                                        "last_name": candidate.get(
                                            "last_name",
                                            (
                                                " ".join(
                                                    candidate.get("name", "").split()[
                                                        1:
                                                    ]
                                                )
                                                if candidate.get("name")
                                                and len(
                                                    candidate.get("name", "").split()
                                                )
                                                > 1
                                                else ""
                                            ),
                                        ),
                                        "email": candidate.get("email", ""),
                                        "pitch": candidate.get(
                                            "pitch", candidate.get("summary", "")
                                        ),
                                        "tags": candidate.get("tags", []),
                                        "created_at": candidate.get("created_at", ""),
                                        "updated_at": candidate.get("updated_at", ""),
                                    }
                                    all_candidates.append(candidate_info)

                except Exception as e:
                    print(f"Error processing {candidate_file}: {e}")
                    continue

        # If no candidates found in specific files, try other JSON files
        if not all_candidates:
            json_files = list(data_dir.rglob("*.json"))
            for json_file in json_files[:5]:  # Limit to first 5 files for performance
                try:
                    with open(json_file, encoding="utf-8") as f:
                        data = json.load(f)

                        if isinstance(data, list):
                            for item in data:
                                if isinstance(item, dict) and "attributes" in item:
                                    attrs = item["attributes"]
                                    if attrs.get("first-name") or attrs.get(
                                        "email"
                                    ):  # Only process if it looks like a candidate
                                        candidate_info = {
                                            "id": item.get("id", ""),
                                            "first_name": attrs.get("first-name", ""),
                                            "last_name": attrs.get("last-name", ""),
                                            "email": attrs.get("email", ""),
                                            "pitch": attrs.get("pitch", ""),
                                            "tags": attrs.get("tags", []),
                                            "created_at": attrs.get("created-at", ""),
                                            "updated_at": attrs.get("updated-at", ""),
                                        }
                                        all_candidates.append(candidate_info)

                except Exception as e:
                    continue

        # Limit to first 50 candidates for performance
        limited_candidates = all_candidates[:50]

        return {
            "success": True,
            "data": limited_candidates,
            "pagination": {
                "page": 1,
                "page_size": len(limited_candidates),
                "total": len(all_candidates),
            },
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "pagination": {"page": 1, "page_size": 0, "total": 0},
        }


@router.get("/debug")
async def debug_teamtailor_api() -> Dict[str, Any]:
    """Debug endpoint to test TeamTailor API calls."""
    try:
        tag_manager = CandidateTagManager()

        # Test basic API call
        candidates_data = tag_manager.client.get_candidates(
            {"page[size]": 5, "page[number]": 1}
        )

        if not candidates_data:
            return {
                "success": False,
                "error": "No data returned from API",
                "data": None,
            }

        candidates = candidates_data.get("data", [])

        return {
            "success": True,
            "api_response": candidates_data,
            "candidates_count": len(candidates),
            "sample_candidate": candidates[0] if candidates else None,
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        return {"success": False, "error": str(e), "traceback": traceback.format_exc()}
