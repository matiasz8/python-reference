"""Base class for _processors in the greenhouse application."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from legacy.greenhouse.storage import saveentity_data


class BaseProcessor(ABC):
    """Base class for _processors in the greenhouse application."""

    entity: str

    def run(self) -> Dict[str, Any]:
        """Run the processor to fetch and save entity data."""
        print("▶ Processing {self.entity}...")
        _data = self.fetch()
        saveentity_data(self.entity, data)
        return {"entity": self.entity, "count": len(data)}

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """Fetch data from the Greenhouse API."""
