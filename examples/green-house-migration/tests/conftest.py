"""Test configuration and fixtures."""

import os
from unittest.mock import patch

import pytest

# Set up test environment variables
os.environ["GREENHOUSE_API_KEY"] = "test:password"
os.environ["GREENHOUSE_API_URL"] = "https://harvest.greenhouse.io/v1"
os.environ["TEAMTAILOR_API_KEY"] = "test_teamtailor_key"
os.environ["TEAMTAILOR_API_URL"] = "https://api.teamtailor.com/v1"
os.environ["DEBUG"] = "False"
os.environ["LOG_LEVEL"] = "INFO"
os.environ["DATA_DIR"] = "data"
os.environ["BATCH_SIZE"] = "100"
os.environ["TEST_MODE"] = "true"
os.environ["MOCK_DATA"] = "true"


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment for all tests."""
    # Mock external API calls to avoid real network requests
    with patch("requests.Session.get") as mock_get, patch(
        "requests.Session.post"
    ) as mock_post, patch("requests.Session.put") as mock_put, patch(
        "requests.Session.delete"
    ) as mock_delete:

        # Configure mock responses
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": [], "meta": {}}
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"data": {}, "meta": {}}
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {"data": {}, "meta": {}}
        mock_delete.return_value.status_code = 200
        mock_delete.return_value.json.return_value = {"data": {}, "meta": {}}

        yield


@pytest.fixture
def mock_teamtailor_client():
    """Mock TeamTailor client for testing."""
    with patch("teamtailor.api.client.TeamTailorClient") as mock_client:
        mock_client.return_value.get_candidate.return_value = {
            "data": {"id": "1", "type": "candidates"}
        }
        mock_client.return_value.get_candidates.return_value = {"data": [], "meta": {}}
        mock_client.return_value.search_candidates.return_value = {
            "data": [],
            "meta": {},
        }
        mock_client.return_value.get_tags.return_value = {"data": [], "meta": {}}
        yield mock_client


@pytest.fixture
def mock_greenhouse_client():
    """Mock Greenhouse client for testing."""
    with patch("legacy.greenhouse.client.gh_get") as mock_get:
        mock_get.return_value = {"data": [], "meta": {}}
        yield mock_get


@pytest.fixture
def test_app():
    """Create test app with proper exception handling."""
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="Test API")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


@pytest.fixture
def sample_candidate_data():
    """Sample candidate data for testing."""
    return {
        "id": "1",
        "type": "candidates",
        "attributes": {
            "first-name": "John",
            "last-name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "created-at": "2024-01-01T00:00:00Z",
            "updated-at": "2024-01-01T00:00:00Z",
        },
    }


@pytest.fixture
def sample_application_data():
    """Sample application data for testing."""
    return {
        "id": "1",
        "type": "applications",
        "attributes": {
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "status": "active",
        },
    }


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "id": "1",
        "type": "jobs",
        "attributes": {
            "title": "Software Engineer",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "status": "open",
        },
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "1",
        "type": "users",
        "attributes": {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
    }


@pytest.fixture
def sample_tag_data():
    """Sample tag data for testing."""
    return {
        "id": "1",
        "type": "tags",
        "attributes": {
            "name": "python",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
    }


@pytest.fixture
def sample_prospect_pool_data():
    """Sample prospect pool data for testing."""
    return {
        "id": "1",
        "type": "prospect-pools",
        "attributes": {
            "name": "Engineering Candidates",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
        },
    }


@pytest.fixture
def sample_analytics_data():
    """Sample analytics data for testing."""
    return {
        "total_candidates": 100,
        "unique_tags": 25,
        "average_tags_per_candidate": 2.5,
        "categories": [
            {"name": "Engineering", "count": 50, "engagement_rate": 0.75},
            {"name": "Product", "count": 30, "engagement_rate": 0.65},
        ],
        "migration_success_rate": 0.85,
        "average_engagement_rate": 0.70,
    }


@pytest.fixture
def sample_duplicates_data():
    """Sample duplicates analysis data for testing."""
    return {
        "total_candidates": 100,
        "duplicate_groups": 5,
        "duplicate_candidates": 15,
        "duplicate_rate": 0.15,
        "groups": [
            {
                "group_id": "1",
                "candidates": [
                    {"id": "1", "name": "John Doe", "email": "john.doe@example.com"},
                    {"id": "2", "name": "John Doe", "email": "john.doe@company.com"},
                ],
                "confidence": 0.95,
            }
        ],
    }


@pytest.fixture
def sample_export_data():
    """Sample export data for testing."""
    return {
        "candidates": [
            {
                "id": "1",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "tags": ["python", "react"],
            }
        ],
        "applications": [
            {"id": "1", "candidate_id": "1", "job_id": "1", "status": "active"}
        ],
        "jobs": [{"id": "1", "title": "Software Engineer", "status": "open"}],
        "users": [
            {
                "id": "1",
                "first_name": "Admin",
                "last_name": "User",
                "email": "admin@example.com",
            }
        ],
    }


@pytest.fixture
def sample_stats_data():
    """Sample statistics data for testing."""
    return {
        "total_candidates": 100,
        "total_applications": 150,
        "total_jobs": 25,
        "total_users": 10,
        "active_jobs": 15,
        "recent_applications": 20,
        "average_applications_per_job": 6.0,
        "candidate_engagement_rate": 0.75,
    }


@pytest.fixture
def sample_metadata_data():
    """Sample metadata data for testing."""
    return {
        "departments": [
            {"id": "1", "name": "Engineering"},
            {"id": "2", "name": "Product"},
        ],
        "offices": [
            {"id": "1", "name": "San Francisco"},
            {"id": "2", "name": "New York"},
        ],
        "sources": [{"id": "1", "name": "LinkedIn"}, {"id": "2", "name": "Indeed"}],
        "tags": [{"id": "1", "name": "python"}, {"id": "2", "name": "react"}],
    }
