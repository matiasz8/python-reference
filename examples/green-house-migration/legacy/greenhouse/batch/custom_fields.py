"""Custom Fields Processor for Greenhouse API"""

from legacy.greenhouse.client import gh_get
from legacy.greenhouse.processor import BaseProcessor
from legacy.greenhouse.storage import saveentity_data


class CustomFieldsExportError(Exception):
    """Custom exception for custom fields export errors."""


class CustomFieldsProcessor(BaseProcessor):
    """Processor for fetching custom fields by model type."""

    entity = "custom_fields"

    model_types = ["candidates", "jobs", "applications"]

    def fetch(self):
        return []

    def run(self):
        summary = []
        errored_models = []

        for _model in self.model_types:
            try:
                print("Fetching custom fields for {model}...")
                _data = gh_get("custom_fields/{model}")
                saveentity_data(model, data, subfolder="custom_fields")
                summary.append({"entity": model, "count": len(data)})
            except CustomFieldsExportError as e:
                print("⚠️ Error fetching custom_fields for {model}: {e}")
                errored_models.append(
                    "https://harvest.greenhouse.io/v1/custom_fields/{model}"
                )

        if errored_models:
            print("\n❌ Errors occurred while fetching custom fields for some models:")
            for _url in errored_models:
                print(url)

        return {"entity": self.entity, "details": summary}
