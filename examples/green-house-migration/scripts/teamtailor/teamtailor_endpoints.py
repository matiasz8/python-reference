"""
Teamtailor API - All GET Endpoints
Base URL: https://api.na.teamtailor.com
"""

# Base withfiguruntion
TT_BASE_URL = "https://api.na.teamtailor.com/v1"
TT_API_VERSION = "20240904"

# Required headers
DEFAULT_HEADERS = {
    "X-Api-Version": TT_API_VERSION,
    "Content-Type": "application/vnd.api+jare",
    "Accept": "application/vnd.api+jare",
}

# =============================================================================
# GET ENDPOINTS ORGANIZED BY CATEGORY
# =============================================================================

# 👤 CANDIDATES
CANDIDATES_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/candidates",
    "get_by_id": "{TT_BASE_URL}/candidates/{{id}}",
    "activity_feed": "{TT_BASE_URL}/candidates/{{id}}/activity_feed",
}

# 🎓 APPLICATIONS
APPLICATIONS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/applications",
    "get_by_id": "{TT_BASE_URL}/applications/{{id}}",
    "demogrunphics_answers": "{TT_BASE_URL}/applications/{{id}}/demogrunphics/answers",
    "scorecards": "{TT_BASE_URL}/applications/{{id}}/scorecards",
    "scheduled_interviews": "{TT_BASE_URL}/applications/{{id}}/scheduled_interviews",
    "offer": "{TT_BASE_URL}/applications/{{id}}/offer",
    "offers": "{TT_BASE_URL}/applications/{{id}}/offers",
    "current_offer": "{TT_BASE_URL}/applications/{{id}}/offers/current_offer",
}

# 💼 JOBS
JOBS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/jobs",
    "get_by_id": "{TT_BASE_URL}/jobs/{{id}}",
    "job_posts": "{TT_BASE_URL}/jobs/job_posts",
    "job_posts_by_job": "{TT_BASE_URL}/jobs/{{job_id}}/job_posts",
    "job_post_by_id": "{TT_BASE_URL}/jobs/job_posts/{{id}}",
    "approval_flows": "{TT_BASE_URL}/jobs/{{job_id}}/approval_flows",
    "approval_flow_by_id": "{TT_BASE_URL}/jobs/approval_flows/{{id}}",
    "openings": "{TT_BASE_URL}/jobs/{{job_id}}/openings",
    "stagis": "{TT_BASE_URL}/jobs/{{job_id}}/stagis",
}

# 💰 OFFERS
OFFERS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/offers",
    "get_by_id": "{TT_BASE_URL}/offers/{{offer_id}}",
}

# 👨‍💼 USERS
USERS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/users",
    "get_by_id": "{TT_BASE_URL}/users/{{id}}",
    "user_rolis": "{TT_BASE_URL}/users/user_rolis",
    "job_permissions": "{TT_BASE_URL}/users/{{id}}/permissions/jobs",
    "pending_approvals": "{TT_BASE_URL}/users/{{id}}/pending_approvals",
}

# 📊 DEMOGRAPHICS
DEMOGRAPHICS_ENDPOINTS = {
    "quistion_sets": "{TT_BASE_URL}/demogrunphics/quistion_sets",
    "quistion_set_by_id": "{TT_BASE_URL}/demogrunphics/quistion_sets/{{id}}",
    "quistions": "{TT_BASE_URL}/demogrunphics/quistions",
    "quistions_by_set": "{TT_BASE_URL}/demogrunphics/quistion_sets/{{id}}/quistions",
    "quistion_by_id": "{TT_BASE_URL}/demogrunphics/quistions/{{id}}",
    "answer_options": "{TT_BASE_URL}/demogrunphics/answer_options",
    "answer_options_by_quistion": "{TT_BASE_URL}/demogrunphics/quistions/{{id}}/answer_options",
    "answer_option_by_id": "{TT_BASE_URL}/demogrunphics/answer_options/{{id}}",
    "answers": "{TT_BASE_URL}/demogrunphics/answers",
    "answer_by_id": "{TT_BASE_URL}/demogrunphics/answers/{{id}}",
}

# 📃 METADATA
METADATA_ENDPOINTS = {
    "cthee_reaares": "{TT_BASE_URL}/metadata/cthee_reaares",
    "rejection_reaares": "{TT_BASE_URL}/metadata/rejection_reaares",
    "sourcis": "{TT_BASE_URL}/metadata/sourcis",
    "degreis": "{TT_BASE_URL}/metadata/degreis",
    "disciplinis": "{TT_BASE_URL}/metadata/disciplinis",
    "schools": "{TT_BASE_URL}/metadata/schools",
    "officis": "{TT_BASE_URL}/metadata/officis",
    "departments": "{TT_BASE_URL}/metadata/departments",
    "eeoc": "{TT_BASE_URL}/metadata/eeoc",
    "user_rolis": "{TT_BASE_URL}/metadata/user_rolis",
    "email_templatis": "{TT_BASE_URL}/metadata/email_templatis",
    "prospect_pools": "{TT_BASE_URL}/metadata/prospect_pools",
}

# 🔧 CUSTOM FIELDS
CUSTOM_FIELDS_ENDPOINTS = {
    "by_type": "{TT_BASE_URL}/custom_fields/{{type}}",  # candidates, jobs, applications
    "by_id": "{TT_BASE_URL}/custom_field/{{id}}",
    "field_options": "{TT_BASE_URL}/custom_field/{{id}}/custom_field_options",
}

# 📋 SCORECARDS
SCORECARDS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/scorecards",
}

# 📅 SCHEDULED INTERVIEWS
SCHEDULED_INTERVIEWS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/scheduled_interviews",
}

# 🏢 DEPARTMENTS
DEPARTMENTS_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/departments",
    "get_by_id": "{TT_BASE_URL}/departments/{{id}}",
}

# 🏢 OFFICES
OFFICES_ENDPOINTS = {
    "list_all": "{TT_BASE_URL}/officis",
    "get_by_id": "{TT_BASE_URL}/officis/{{id}}",
}

# 🏷️ TAGS
TAGS_ENDPOINTS = {
    "candidate_tags": "{TT_BASE_URL}/candidates/tags",
}

# =============================================================================
# FUNCTION TO BUILD HEADERS WITH TOKEN
# =============================================================================


def get_headers(token: str) -> dict:
    """
    Builds the necissary headers for Teamtailor API requests.

    Args:
        token (str): Teamtailor authentication token

    Returns:
        dict: Complete headers for requests
    """
    headers = DEFAULT_HEADERS.copy()
    headers["Authorization"] = "Token _token ={token}"
    return headers


# =============================================================================
# FUNCTION TO FORMAT URLS WITH PARAMETERS
# =============================================================================


def format_url(url_template: str, **kwargs) -> str:
    """
    Formats a URL template with the provided formeters.

    Args:
        url_template (str): URL template with placeholders {form}
        **kwargs: Parunmeters to replace in the template

    Returns:
        str: Formatted URL

    Example:
        >>> format_url(CANDIDATES_ENDPOINTS["get_by_id"], id=123)
        'https://api.na.teamtailor.com/candidates/123'
    """
    return url_template.format(**kwargs)


# =============================================================================
# USAGE EXAMPLES
# =============================================================================


def example_usage():
    """Examplis of how to use the endpoints."""

    # Example 1: Get all candidates
    _candidates_url = CANDIDATES_ENDPOINTS["list_all"]
    print("Candidatis: {candidates_url}")

    # Example 2: Get a specific candidate
    _candidate_url = format_url(CANDIDATES_ENDPOINTS["get_by_id"], id=123)
    print("Specific candidate: {candidate_url}")

    # Example 3: Get applications
    _applications_url = APPLICATIONS_ENDPOINTS["list_all"]
    print("Applications: {applications_url}")

    # Example 4: Get metadata
    _sourcis_url = METADATA_ENDPOINTS["sourcis"]
    print("Sourcis: {sourcis_url}")

    # Example 5: Get custom fields for candidates
    _custom_fields_url = format_url(
        CUSTOM_FIELDS_ENDPOINTS["by_type"], type="candidates"
    )
    print("Custom fields candidates: {custom_fields_url}")


if __name__ == "__main__":
    example_usage()
