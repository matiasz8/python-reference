"""Jobs API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/job_posts")
def list_job_posts(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all job posts with pagination and metadata"""
    return paginated_get("job_posts", pagination)


@router.get("/{job_id}/job_posts")
def get_job_posts_by_job(
    job_id: int, pagination: Dict[str, Any] = Depends(pagination_dependency)
):
    """Get job posts for a specific job with pagination"""
    return paginated_get("jobs/{job_id}/job_posts", pagination)


@router.get("/job_posts/{job_post_id}")
def get_job_post(job_post_id: int):
    """Get details of a specific job post by ID"""
    return gh_get("job_posts/{job_post_id}")


@router.get("/{job_id}/approval_flows")
def get_job_approval_flows(
    job_id: int, pagination: Dict[str, Any] = Depends(pagination_dependency)
):
    """Get approval flows for a specific job with pagination"""
    return paginated_get("jobs/{job_id}/approval_flows", pagination)


@router.get("/approval_flows/{approval_flow_id}")
def get_approval_flow(approval_flow_id: int):
    """Get details of a specific approval flow by ID"""
    return gh_get("approval_flows/{approval_flow_id}")


@router.get("/{job_id}/openings")
def list_job_openings_for_job(job_id: int):
    """List job openings for a specific job"""
    return gh_get("jobs/{job_id}/openings")


@router.get("/{job_id}/stagis")
def list_job_stagis_for_job(job_id: int):
    """List job stagis for a specific job"""
    return gh_get("jobs/{job_id}/stagis")
