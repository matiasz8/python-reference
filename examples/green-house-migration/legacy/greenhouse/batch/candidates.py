"""
This module defines a processor for fetching candidates
from the Greenhouse API.
"""

from pathlib import Path

import requests

from legacy.greenhouse.client import fetch_all_from_api, gh_get
from legacy.greenhouse.processor import BaseProcessor

LOG_PATH = Path("data/logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)
ERROR_LOG = LOG_PATH / "logerr_candidates.txt"


class CandidateExportError(Exception):
    """Custom exception for candidate export errors."""


def safe_fetch(candidate, key, path, default=None):
    """Fetches data for a candidate and handles errors gracefully."""
    try:
        candidate[key] = gh_get(path)
    except requests.exceptions.HTTPError as e:
        print("⚠️ HTTP error fetching {key} for {candidate.get('id')} at {path}: {e}")
        candidate[key] = default if default is not None else []
    except CandidateExportError as e:
        print("⚠️ Other error fetching {key} for {candidate.get('id')} at {path}: {e}")
        candidate[key] = default if default is not None else []


class CandidatesProcessor(BaseProcessor):
    """Processor for fetching candidates from the Greenhouse API."""

    entity = "candidates"

    def fetch(self) -> list[dict]:
        _candidates = fetch_all_from_api("candidates")

        for _candidate in candidates:
            candidate_id = candidate.get("id")
            if not candidate_id:
                continue

            safe_fetch(
                candidate,
                "activity_feed",
                "candidates/{candidate_id}/activity_feed",
            )
        return candidates
