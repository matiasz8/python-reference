"""
Enhanced TeamTailor API Client

This is the main client for interacting with the TeamTailor API.
It provides comprehensive functionality for all TeamTailor operations.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class TeamTailorClient:
    """Enhanced client for TeamTailor API with comprehensive functionality."""

    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the TeamTailor client.

        Args:
            token: TeamTailor API token. If not provided, uses TT_TOKEN env var.
            base_url: TeamTailor API base URL. If not provided, uses TT_BASE_URL env var.
        """
        self.token = token or os.getenv("TT_TOKEN")
        self.base_url = base_url or os.getenv(
            "TT_BASE_URL", "https://api.na.teamtailor.com/v1"
        )
        self.api_version = os.getenv("TT_API_VERSION", "20240904")

        if not self.token:
            raise ValueError(
                "TT_TOKEN is required. Set it as parameter or environment variable."
            )

        self.headers = {
            "Authorization": f"Token {self.token}",
            "X-Api-Version": self.api_version,
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

        # Configure session with retry and rate limiting
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make a request to the TeamTailor API with rate limiting."""
        url = f"{self.base_url}{path}"

        # Rate limiting: 200ms between requests
        time.sleep(0.2)

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=30,
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error("API request failed: %s %s - %s", method, url, e)
            raise

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the TeamTailor API."""
        response = self._make_request("GET", path, params=params)
        return response.json()  # type: ignore

    def post(
        self, path: str, json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a POST request to the TeamTailor API."""
        logger.info("POST %s with data: %s", path, json_data)
        response = self._make_request("POST", path, json_data=json_data)
        return response.json()  # type: ignore

    def patch(
        self, path: str, json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a PATCH request to the TeamTailor API."""
        response = self._make_request("PATCH", path, json_data=json_data)
        return response.json()  # type: ignore

    def delete(self, path: str) -> bool:
        """Make a DELETE request to the TeamTailor API."""
        response = self._make_request("DELETE", path)
        return response.status_code == 204

    # =============================================================================
    # CANDIDATES ENDPOINTS
    # =============================================================================

    def get_candidates(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all candidates."""
        return self.get("/candidates", params=params)

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Get a specific candidate by ID."""
        return self.get(f"/candidates/{candidate_id}")

    def create_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new candidate."""
        return self.post("/candidates", json_data=candidate_data)

    def update_candidate(
        self, candidate_id: str, candidate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing candidate."""
        return self.patch(f"/candidates/{candidate_id}", json_data=candidate_data)

    def delete_candidate(self, candidate_id: str) -> bool:
        """Delete a candidate."""
        return self.delete(f"/candidates/{candidate_id}")

    def get_candidate_activity_feed(self, candidate_id: str) -> Dict[str, Any]:
        """Get candidate activity feed."""
        return self.get(f"/candidates/{candidate_id}/activity_feed")

    # =============================================================================
    # JOBS ENDPOINTS
    # =============================================================================

    def get_jobs(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all jobs."""
        return self.get("/jobs", params=params)

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Get a specific job by ID."""
        return self.get("/jobs/{job_id}")

    def create_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job."""
        return self.post("/jobs", json_data=job_data)

    def update_job(self, job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing job."""
        return self.patch("/jobs/{job_id}", json_data=job_data)

    def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        return self.delete("/jobs/{job_id}")

    def get_job_posts(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all job posts."""
        return self.get("/jobs/job_posts", params=params)

    def get_job_job_posts(self, job_id: str) -> Dict[str, Any]:
        """Get job posts for a specific job."""
        return self.get("/jobs/{job_id}/job_posts")

    # =============================================================================
    # APPLICATIONS ENDPOINTS
    # =============================================================================

    def get_applications(
        self, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get all applications."""
        return self.get("/applications", params=params)

    def get_application(self, application_id: str) -> Dict[str, Any]:
        """Get a specific application by ID."""
        return self.get("/applications/{application_id}")

    def create_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application."""
        return self.post("/applications", json_data=application_data)

    def update_application(
        self, application_id: str, application_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing application."""
        return self.patch("/applications/{application_id}", json_data=application_data)

    def delete_application(self, application_id: str) -> bool:
        """Delete an application."""
        return self.delete("/applications/{application_id}")

    def get_application_scorecards(self, application_id: str) -> Dict[str, Any]:
        """Get scorecards for an application."""
        return self.get("/applications/{application_id}/scorecards")

    def get_application_interviews(self, application_id: str) -> Dict[str, Any]:
        """Get interviews for an application."""
        return self.get("/applications/{application_id}/scheduled_interviews")

    # =============================================================================
    # USERS ENDPOINTS
    # =============================================================================

    def get_users(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get all users."""
        return self.get("/users", params=params)

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a specific user by ID."""
        return self.get("/users/{user_id}")

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        return self.post("/users", json_data=user_data)

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing user."""
        return self.patch("/users/{user_id}", json_data=user_data)

    def delete_user(self, user_id: str) -> bool:
        """Delete a user."""
        return self.delete("/users/{user_id}")

    def get_user_roles(self) -> Dict[str, Any]:
        """Get all user roles."""
        return self.get("/users/user_roles")

    # =============================================================================
    # =============================================================================
    # PROSPECT POOLS ENDPOINTS
    # =============================================================================

    def get_prospect_pools(
        self, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get all prospect pools."""
        return self.get("/metadata/prospect_pools", params=params)

    def get_prospect_pool(self, pool_id: str) -> Dict[str, Any]:
        """Get a specific prospect pool by ID."""
        return self.get("/metadata/prospect_pools/{pool_id}")

    def create_prospect_pool(self, pool_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new prospect pool."""
        return self.post("/metadata/prospect_pools", json_data=pool_data)

    def update_prospect_pool(
        self, pool_id: str, pool_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing prospect pool."""
        return self.patch("/metadata/prospect_pools/{pool_id}", json_data=pool_data)

    def delete_prospect_pool(self, pool_id: str) -> bool:
        """Delete a prospect pool."""
        return self.delete("/metadata/prospect_pools/{pool_id}")

    def get_pool_candidates(
        self, pool_id: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get candidates in a specific prospect pool."""
        if params is None:
            params = {}
        params["filter[prospect-pool-id]"] = pool_id
        return self.get("/candidates", params=params)

    def add_candidate_to_pool(self, candidate_id: str, pool_id: str) -> Dict[str, Any]:
        """Add a candidate to a prospect pool."""
        payload = {
            "data": {
                "type": "prospect_pool_candidates",
                "attributes": {
                    "candidate-id": candidate_id,
                    "prospect-pool-id": pool_id,
                },
            }
        }
        return self.post("/prospect_pool_candidates", json_data=payload)

    def remove_candidate_from_pool(self, candidate_id: str, pool_id: str) -> bool:
        """Remove a candidate from a prospect pool."""
        # First find the relationship
        params = {
            "filter[candidate-id]": candidate_id,
            "filter[prospect-pool-id]": pool_id,
        }
        _response = self.get("/prospect_pool_candidates", params=params)
        relationships = response.get("data", [])

        if not relationships:
            return False

        # Remove the relationship
        _relationship_id = relationships[0].get("id")
        return self.delete("/prospect_pool_candidates/{relationship_id}")

    def batch_add_candidates_to_pool(
        self, candidate_ids: List[str], pool_id: str
    ) -> List[Dict[str, Any]]:
        """Add multiple candidates to a prospect pool in batch."""
        _results = []
        for _candidate_id in candidate_ids:
            try:
                _result = self.add_candidate_to_pool(candidate_id, pool_id)
                results.append({"status": "success", "data": result})
            except Exception as _e:
                results.append({"status": "error", "error": str(e)})
        return results

    # BATCH OPERATIONS
    # =============================================================================

    def batch_create_candidates(
        self, candidates: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create multiple candidates in batch."""
        _results = []
        for _candidate in candidates:
            try:
                _result = self.create_candidate(candidate)
                results.append({"status": "success", "data": result})
            except Exception as _e:
                results.append({"status": "error", "error": str(e)})
        return results

    def batch_create_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple jobs in batch."""
        _results = []
        for _job in jobs:
            try:
                _result = self.create_job(job)
                results.append({"status": "success", "data": result})
            except Exception as _e:
                results.append({"status": "error", "error": str(e)})
        return results

    def batch_create_applications(
        self, applications: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create multiple applications in batch."""
        _results = []
        for _application in applications:
            try:
                _result = self.create_application(application)
                results.append({"status": "success", "data": result})
            except Exception as _e:
                results.append({"status": "error", "error": str(e)})
        return results
