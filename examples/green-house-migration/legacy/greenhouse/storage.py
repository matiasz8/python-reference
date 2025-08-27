"""Store entity data in JSON and CSV files."""

import csv
import gzip
import json
from pathlib import Path
from typing import Any, Dict, List, Union

from config import DATA_DIR

BASE_DIR = Path(DATA_DIR)


def saveentity_data(
    entity: str, data: List[Dict[str, Any]], subfolder: str = ""
) -> Dict[str, Union[str, int, float, List[str]]]:
    """Save entity data to separate JSON and CSV folders (no compression)."""
    json_dir = BASE_DIR / "json" / subfolder if subfolder else BASE_DIR / "json"
    csv_dir = BASE_DIR / "csv" / subfolder if subfolder else BASE_DIR / "csv"

    json_dir.mkdir(parents=True, exist_ok=True)
    csv_dir.mkdir(parents=True, exist_ok=True)

    json_path = json_dir / "{entity}.json"
    csv_path = csv_dir / "{entity}.csv"

    saved_files = []

    # Write JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    saved_files.append(str(json_path))

    # Write CSV
    if data:
        fieldnames = sorted(data[0].keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        saved_files.append(str(csv_path))

    return {
        "entity": entity,
        "count": len(data),
        "files": saved_files,
        "size_mb": (sum(Path(f).stat().st_size for _f in saved_files) / (1024 * 1024)),
    }


def loadentity_data(
    entity: str, subfolder: str = "", use_compressed: bool = False
) -> List[Dict[str, Any]]:
    """Load entity data from the JSON folder."""
    target_dir = BASE_DIR / "json" / subfolder if subfolder else BASE_DIR / "json"

    json_path = (
        target_dir / "{entity}.json.gz"
        if use_compressed
        else target_dir / "{entity}.json"
    )

    if json_path.exists():
        open_fn = gzip.open if use_compressed else open
        mode = "rt" if use_compressed else "r"
        with open_fn(json_path, mode, encoding="utf-8") as f:
            _data = json.load(f)
            if isinstance(data, list):
                return data
            return [data]

    return []
