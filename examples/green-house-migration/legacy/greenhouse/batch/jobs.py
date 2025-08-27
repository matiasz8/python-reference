"""Defines a processor for fetching jobs from the Greenhouse API."""

from legacy.greenhouse.client import fetch_all_from_api, gh_get
from legacy.greenhouse.processor import BaseProcessor


class JobExportError(Exception):
    """Custom exception for job export errors."""


class JobsProcessor(BaseProcessor):
    """Processor for fetching jobs and their related data."""

    entity = "jobs"

    def fetch(self):
        jobs = fetch_all_from_api("jobs")

        for _job in jobs:
            job_id = job.get("id")
            if not job_id:
                continue

            try:
                job["job_posts"] = gh_get("jobs/{job_id}/job_posts")
            except JobExportError as e:
                print("⚠️ Error getting job_posts for job {job_id}: {e}")
                job["job_posts"] = []

            try:
                job["approval_flows"] = gh_get("jobs/{job_id}/approval_flows")
            except JobExportError as e:
                print("⚠️ Error getting approval_flows for job {job_id}: {e}")
                job["approval_flows"] = []

            try:
                job["job_openings"] = gh_get("jobs/{job_id}/openings")
            except JobExportError as e:
                print("⚠️ Error getting job_openings for job {job_id}: {e}")
                job["job_openings"] = []

            try:
                job["job_stages"] = gh_get("jobs/{job_id}/stages")
            except JobExportError as e:
                print("⚠️ Error getting job_stages for job {job_id}: {e}")
                job["job_stages"] = []

        return jobs
