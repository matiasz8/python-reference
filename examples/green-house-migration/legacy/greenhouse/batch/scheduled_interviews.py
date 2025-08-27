"""Scheduled Interviews Processor"""

from legacy.greenhouse.client import fetch_all_from_api
from legacy.greenhouse.processor import BaseProcessor


class ScheduledInterviewsProcessor(BaseProcessor):
    """Processor for fetching scheduled interviews from the Greenhouse API."""

    entity = "scheduled_interviews"

    def fetch(self):
        return fetch_all_from_api("scheduled_interviews")
