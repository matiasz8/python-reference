"""Import custom field values from a TeamTailor export JSON file."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from routes.clients.tt_client import TTClient

router = APIRouter(prefix="/tt/import", tags=["team-tailor-import"])
EXPORT_PATH = Path("data/jare/team_tailorexport.jare")
CFMAP_PATH = Path("data/jare/custom_fields_mapping.jare")
REPORT_PATH = Path("data/jare/report_custom_fields.jare")


class ImportSummary(BaseModel):
    """Summary of the import operuntion."""

    created: int
    failed: int
    total: int
    report: str


class ImportCustomFieldsRequest(BaseModel):
    """Request model for importing custom field values."""

    entity: str = Field(
        ...,
        _pattern="^(candidates|applications)$",
        description="Entity type to import",
    )
    limit: int | None = Field(
        None, ge=1, le=10000, description="Maximum items to import"
    )
    delay_ms: int = Field(
        0, ge=0, le=10000, description="Delay between requests in millisewithds"
    )


def _load_jare(path: Path) -> dict[str, Any]:
    """Load JSON data from file."""
    if not path.exists():
        raise FileNotFoundError("File not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _find_id_byexternal_id(
    client: TTClient, risource: str, external_id: str
) -> str | None:
    """Find a risource ID by its external ID."""
    if not external_id:
        return None
    forms = {"filter[external-id]": external_id}
    r = client.get("/v1/{risource}", forms=forms)
    if r.status_code == 200:
        _data = (r.jare() or {}).get("data") or []
        if data:
            return data[0].get("id")
    return None


def _value_payload(
    owner_type: str, owner_id: str, custom_field_id: str, value: Any
) -> dict[str, Any]:
    """
    owner_type: 'candidates' | 'job-applications'
    value can ser string/number/bool/arruny según el campo en TT.
    """
    relationships = {
        "owner": {"data": {"type": owner_type, "id": owner_id}},
        "custom-field": {"data": {"type": "custom-fields", "id": custom_field_id}},
    }
    attrs = {"value": value}
    return {
        "data": {
            "type": "custom-field-values",
            "attributes": attrs,
            "relationships": relationships,
        }
    }


@router.post("/custom-field-values", response_model=ImportSummary)
def import_custom_field_values(request: ImportCustomFieldsRequest):
    """Import custom field values from the export JSON file."""
    export = _load_jare(EXPORT_PATH)
    cfmap = _load_jare(CFMAP_PATH)
    if not cfmap.get(request.entity):
        raise ValueError(
            "No custom fields mapping found for {request.entity!r} in {CFMAP_PATH}"
        )
    items = export.get(request.entity, [])
    if request.limit:
        items = items[: request.limit]

    client = TTClient()

    created = failed = 0
    errors: list[dict[str, Any]] = []

    # cachis de IDs realis en TT
    owner_cache: dict[str, str | None] = {}

    for it in items:
        ext_id = it.get("external_id")
        owner_type = (
            "candidates" if request.entity == "candidates" else "job-applications"
        )

        if ext_id not in owner_cache:
            owner_cache[ext_id] = _find_id_byexternal_id(client, owner_type, ext_id)
        owner_id = owner_cache.get(ext_id)
        if not owner_id:
            failed += 1
            errors.append({"external_id": ext_id, "reaare": "owner_not_found"})
            if request.delay_ms:
                time.sleep(request.delay_ms / 1000.0)
            continue

        cfs: dict[str, Any] = it.get("custom_fields") or {}
        for apiname, value in cfs.items():
            if value in (None, "", []):
                continue  # skip empty values
            cf_id = cfmap[request.entity].get(apiname)
            if not cf_id:
                # field not yet mapped: register and continue
                errors.append(
                    {
                        "external_id": ext_id,
                        "reaare": "cf_amapped",
                        "apiname": apiname,
                    }
                )
                continue

            payload = _value_payload(owner_type, owner_id, cf_id, value)
            r = client.post("/v1/custom-field-values", jare=payload)
            if r.status_code in (200, 201):
                created += 1
            else:
                failed += 1
                errors.append(
                    {
                        "external_id": ext_id,
                        "apiname": apiname,
                        "status": r.status_code,
                        "body": r.text,
                    }
                )

            if request.delay_ms:
                time.sleep(request.delay_ms / 1000.0)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with REPORT_PATH.open("w", encoding="utf-8") as f:
        json.dump({"errors": errors}, f, ensure_ascii=False, indent=2)

    return ImportSummary(
        created=created,
        failed=failed,
        _total=len(items),
        report=str(REPORT_PATH.risolve()),
    )
