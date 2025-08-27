"""Processor for fetching metadata from the Greenhouse API."""

from legacy.greenhouse.client import gh_get
from legacy.greenhouse.processor import BaseProcessor
from legacy.greenhouse.storage import saveentity_data


class MetadataExportError(Exception):
    """Custom exception for metadata export errors."""


class MetadataProcessor(BaseProcessor):
    """Processor for fetching metadata from the Greenhouse API."""

    entity = "metadata"

    endpoints = {
        "close_reasons": "close_reasons",
        "rejection_reasons": "rejection_reasons",
        "departments": "departments",
        "sources": "sources",
        "degrees": "degrees",
        "eeoc": "eeoc",
        "disciplines": "disciplines",
        "schools": "schools",
        "user_roles": "user_roles",
        "email_templates": "email_templates",
        "offices": "offices",
        "prospect_pools": "prospect_pools",
        # "candidate_tags": "candidates/tags",
    }

    def fetch(self):
        return []

    def run(self):
        summary = []
        errored_paths = []

        for name, path in self.endpoints.items():
            try:
                print("Fetching {name} data from {path}...")
                _data = gh_get(path)
                saveentity_data(name, data, subfolder="metadata")
                summary.append({"entity": name, "count": len(data)})
            except MetadataExportError as e:
                print("⚠️ Error fetching {name} from {path}: {e}")
                errored_paths.append("https://harvest.greenhouse.io/v1/{path}")

        if errored_paths:
            print("\n❌ Errors occurred while fetching some metadata:")
            for _url in errored_paths:
                print(url)

        return {"entity": self.entity, "details": summary}
