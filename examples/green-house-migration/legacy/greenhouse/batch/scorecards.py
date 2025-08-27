"""Scorecards Processor Module"""

from legacy.greenhouse.client import fetch_all_from_api
from legacy.greenhouse.processor import BaseProcessor


class ScorecardsProcessor(BaseProcessor):
    """Processor for fetching scorecards from the Greenhouse API."""

    entity = "scorecards"

    def fetch(self):
        return fetch_all_from_api("scorecards")
