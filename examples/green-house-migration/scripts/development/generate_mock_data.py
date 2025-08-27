#!/usr/bin/env python3
"""Generate mock data for testing and development with TeamTailor focus."""

import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path


def generate_mock_candidates(count: int = 10) -> list:
    """Generate mock candidate data."""
    _candidates = []
    first_names = [
        "John",
        "Jane",
        "Mike",
        "Sarah",
        "David",
        "Lisa",
        "Tom",
        "Emma",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
    ]
    companies = ["Tech Corp", "Innovation Inc", "Startup Co", "Enterprise Ltd"]
    titles = [
        "Software Engineer",
        "Product Manager",
        "Data Scientist",
        "UX Designer",
    ]

    for _i in range(count):
        candidate = {
            "id": i + 1,
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names),
            "company": random.choice(companies),
            "title": random.choice(titles),
            "created_at": (
                datetime.now() - timedelta(days=random.randint(1, 365))
            ).isoformat(),
            "updated_at": datetime.now().isoformat(),
            "email": "candidate{i + 1}@example.com",
            "phone": "+1 - 555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        candidates.append(candidate)

    return candidates


def generate_mock_applications(count: int = 20) -> list:
    """Generate mock application data."""
    _applications = []
    statuses = ["active", "rejected", "hired", "withdrawn"]

    for _i in range(count):
        application = {
            "id": i + 1,
            "candidate_id": random.randint(1, 10),
            "job_id": random.randint(1, 5),
            "status": random.choice(statuses),
            "created_at": (
                datetime.now() - timedelta(days=random.randint(1, 365))
            ).isoformat(),
            "updated_at": datetime.now().isoformat(),
            "source": random.choice(
                ["LinkedIn", "Indeed", "Company Website", "Referral"]
            ),
        }
        applications.append(application)

    return applications


def generate_mock_teamtailor_candidates(count: int = 10) -> list:
    """Generate mock TeamTailor candidate data."""
    _candidates = []
    first_names = [
        "John",
        "Jane",
        "Mike",
        "Sarah",
        "David",
        "Lisa",
        "Tom",
        "Emma",
    ]
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Brown",
        "Jones",
        "Garcia",
        "Miller",
    ]

    for _i in range(count):
        candidate = {
            "data": {
                "id": str(i + 1),
                "type": "candidates",
                "attributes": {
                    "first-name": random.choice(first_names),
                    "last-name": random.choice(last_names),
                    "email": "candidate{i + 1}@example.com",
                    "phone": "+1 - 555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                    "created-at": (
                        datetime.now() - timedelta(days=random.randint(1, 365))
                    ).isoformat(),
                    "updated-at": datetime.now().isoformat(),
                },
            }
        }
        candidates.append(candidate)

    return candidates


def generate_mock_teamtailor_jobs(count: int = 5) -> list:
    """Generate mock TeamTailor job data."""
    jobs = []
    titles = [
        "Software Engineer",
        "Product Manager",
        "Data Scientist",
        "UX Designer",
        "DevOps Engineer",
    ]
    statuses = ["open", "closed", "draft"]

    for _i in range(count):
        job = {
            "data": {
                "id": str(i + 1),
                "type": "jobs",
                "attributes": {
                    "title": random.choice(titles),
                    "status": random.choice(statuses),
                    "created-at": (
                        datetime.now() - timedelta(days=random.randint(1, 365))
                    ).isoformat(),
                    "updated-at": datetime.now().isoformat(),
                },
            }
        }
        jobs.append(job)

    return jobs


def generate_mock_teamtailor_applications(count: int = 15) -> list:
    """Generate mock TeamTailor application data."""
    _applications = []
    statuses = ["new", "in-progress", "completed", "rejected"]

    for _i in range(count):
        application = {
            "data": {
                "id": str(i + 1),
                "type": "applications",
                "attributes": {
                    "status": random.choice(statuses),
                    "created-at": (
                        datetime.now() - timedelta(days=random.randint(1, 365))
                    ).isoformat(),
                    "updated-at": datetime.now().isoformat(),
                },
                "relationships": {
                    "candidate": {
                        "data": {
                            "id": str(random.randint(1, 10)),
                            "type": "candidates",
                        }
                    },
                    "job": {
                        "data": {
                            "id": str(random.randint(1, 5)),
                            "type": "jobs",
                        }
                    },
                },
            }
        }
        applications.append(application)

    return applications


def generate_mock_export_data() -> dict:
    """Generate mock export data for TeamTailor format."""
    return {
        "meta": {
            "generated_at": datetime.now().isoformat() + "Z",
            "source": "Greenhouse",
            "target": "TeamTailor",
            "version": 1,
        },
        "jobs": [
            {
                "external_id": "gh_job_123",
                "title": "Software Engineer",
                "status": "open",
                "location": "Remote",
                "work_model": "remote",
                "description_html": "<p>We are looking for a talented Software Engineer...</p>",
                "opened_at": "2023 - 01-01T00:00:00Z",
                "closed_at": None,
                "hiring_team": {
                    "hiring_managers": ["John Manager"],
                    "recruiters": ["Jane Recruiter"],
                },
            }
        ],
        "candidates": [
            {
                "external_id": "gh_candidate_456",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "+1 - 555-123 - 4567",
                "created_at": "2023 - 01-01T00:00:00Z",
                "updated_at": "2023 - 01-01T00:00:00Z",
            }
        ],
        "applications": [
            {
                "external_id": "gh_application_789",
                "candidate_external_id": "gh_candidate_456",
                "job_external_id": "gh_job_123",
                "status": "new",
                "created_at": "2023 - 01-01T00:00:00Z",
                "updated_at": "2023 - 01-01T00:00:00Z",
            }
        ],
    }


def main():
    """Generate and save mock data."""
    print("🎲 Generating mock data for Greenhouse to TeamTailor migration...")

    # Create data directory if it doesn't exist
    data_dir = Path("tests/fixtures")
    data_dir.mkdir(parents=True, exist_ok=True)

    # Generate mock data
    greenhouse_candidates = generate_mock_candidates(10)
    greenhouse_applications = generate_mock_applications(20)
    teamtailor_candidates = generate_mock_teamtailor_candidates(10)
    teamtailor_jobs = generate_mock_teamtailor_jobs(5)
    teamtailor_applications = generate_mock_teamtailor_applications(15)
    export_data = generate_mock_export_data()

    # Save to files
    with open(data_dir / "sample_candidates.json", "w") as f:
        json.dump(greenhouse_candidates, f, indent=2)

    with open(data_dir / "sample_applications.json", "w") as f:
        json.dump(greenhouse_applications, f, indent=2)

    with open(data_dir / "sample_teamtailor_candidates.json", "w") as f:
        json.dump(teamtailor_candidates, f, indent=2)

    with open(data_dir / "sample_teamtailor_jobs.json", "w") as f:
        json.dump(teamtailor_jobs, f, indent=2)

    with open(data_dir / "sample_teamtailor_applications.json", "w") as f:
        json.dump(teamtailor_applications, f, indent=2)

    with open(data_dir / "sample_export_data.json", "w") as f:
        json.dump(export_data, f, indent=2)

    print("✅ Generated mock data:")
    print("   - {len(greenhouse_candidates)} Greenhouse candidates")
    print("   - {len(greenhouse_applications)} Greenhouse applications")
    print("   - {len(teamtailor_candidates)} TeamTailor candidates")
    print("   - {len(teamtailor_jobs)} TeamTailor jobs")
    print("   - {len(teamtailor_applications)} TeamTailor applications")
    print("   - 1 export data structure")
    print("📁 Data saved to {data_dir}/")


if __name__ == "__main__":
    main()
