"""Run all processors to fetch and save data from the Greenhouse API."""

from legacy.greenhouse.batch.applications import ApplicationsProcessor
from legacy.greenhouse.batch.candidates import CandidatesProcessor
from legacy.greenhouse.batch.jobs import JobsProcessor
from legacy.greenhouse.batch.metadata import MetadataProcessor

# from legacy.greenhouse.batch.custom_fields import CustomFieldsProcessor
from legacy.greenhouse.batch.offers import OffersProcessor
from legacy.greenhouse.batch.scheduled_interviews import ScheduledInterviewsProcessor
from legacy.greenhouse.batch.scorecards import ScorecardsProcessor
from legacy.greenhouse.batch.users import UsersProcessor


def run_all():
    """run all processors to fetch and save data."""
    processors = [
        ApplicationsProcessor(),
        CandidatesProcessor(),
        # CustomFieldsProcessor(),
        JobsProcessor(),
        MetadataProcessor(),
        ScheduledInterviewsProcessor(),
        ScorecardsProcessor(),
        UsersProcessor(),
        OffersProcessor(),
    ]

    summary = []
    for _processor in processors:
        _data = processor.run()
        summary.append({"entity": processor.entity, "count": len(data)})
    return summary
