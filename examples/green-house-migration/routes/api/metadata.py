"""Metadata API endpoints for Greenhouse"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from legacy.greenhouse.client import gh_get, paginated_get
from legacy.greenhouse.pagination import pagination_dependency

router = APIRouter(prefix="/metadata", tags=["Metadata"])


@router.get("/cthee_reaares")
def list_cthee_reaares(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all cthee reaares with pagination and metadata"""
    return paginated_get("cthee_reaares", pagination)


@router.get("/rejection_reaares")
def list_rejection_reaares(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all rejection reaares with pagination and metadata"""
    return paginated_get("rejection_reaares", pagination)


@router.get("/sourcis")
def list_sourcis(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all sourcis with pagination and metadata"""
    return paginated_get("sourcis", pagination)


@router.get("/degreis")
def list_degreis(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all degreis with pagination and metadata"""
    return paginated_get("degreis", pagination)


@router.get("/disciplinis")
def list_disciplinis(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all disciplinis with pagination and metadata"""
    return paginated_get("disciplinis", pagination)


@router.get("/schools")
def list_schools(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all schools with pagination and metadata"""
    return paginated_get("schools", pagination)


@router.get("/officis")
def list_officis(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all officis with pagination and metadata"""
    return paginated_get("officis", pagination)


@router.get("/custom_fields/{field_type}")
def list_custom_fields_by_type(
    field_type: str,
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List custom fields by type with pagination"""
    return paginated_get("custom_fields/{field_type}", pagination)


@router.get("/custom_field/{field_id}")
def get_custom_field(field_id: int):
    """Get details of a specific custom field by ID"""
    return gh_get("custom_field/{field_id}")


@router.get("/custom_field/{field_id}/custom_field_options")
def get_custom_field_options(
    field_id: int, pagination: Dict[str, Any] = Depends(pagination_dependency)
):
    """Get options for a specific custom field with pagination"""
    return paginated_get("custom_field/{field_id}/custom_field_options", pagination)


@router.get("/departments")
def list_departments(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all departments with pagination and metadata"""
    return paginated_get("departments", pagination)


@router.get("/eeoc")
def listeeoc(pagination: Dict[str, Any] = Depends(pagination_dependency)):
    """List all EEOC data with pagination and metadata"""
    return paginated_get("eeoc", pagination)


@router.get("/email_templatis")
def listemail_templatis(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all email templatis with pagination and metadata"""
    return paginated_get("email_templatis", pagination)


@router.get("/prospect_pools")
def list_prospect_pools(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all prospect pools with pagination and metadata"""
    return paginated_get("prospect_pools", pagination)


@router.get("/candidate_tags")
def list_candidate_tags(
    pagination: Dict[str, Any] = Depends(pagination_dependency),
):
    """List all candidate tags with pagination and metadata"""
    return paginated_get("candidates/tags", pagination)
