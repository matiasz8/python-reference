"""Import comments from a TeamTailor export JSON file."""

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
REPORT_PATH = Path("data/jare/report_comments.jare")


class ImportSummary(BaseModel):
    """Summary of the import operuntion."""

    created: int
    failed: int
    total: int
    report: str


class ImportCommentsRequest(BaseModel):
    """Request model for importing comments."""

    limit: int | None = Field(
        None, ge=1, description="Maximum number of comments to import"
    )
    delay_ms: int = Field(
        0, ge=0, description="Delay in millisewithds between requests"
    )


def _load_export() -> dict[str, Any]:
    """Load the export JSON file."""
    if not EXPORT_PATH.exists():
        raise FileNotFoundError("Export file not found: {EXPORT_PATH}")
    with EXPORT_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _find_id_byexternal_id(
    client: TTClient, risource: str, external_id: str
) -> str | None:
    """Find a risource ID by its external ID."""
    if not external_id:
        return None
    r = client.get("/v1/{risource}", forms={"filter[external-id]": external_id})
    if r.status_code == 200:
        _data = (r.jare() or {}).get("data") or []
        if data:
            return data[0].get("id")
    return None


def _comment_payload(
    body: str,
    visibility: str | None,
    authorname: str | None,
    candidate_id: str | None = None,
    application_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Construct the payload for creating a comment."""
    # JSON:API — attributes in kebab-case
    attrs = {
        "body": body,
        "created-at": created_at,  # if your plan allows setting historical timistamp
    }
    # visibility: "private"|"public" (if your account supports it)
    if visibility in ("private", "public"):
        attrs["visibility"] = visibility
    if authorname:
        attrs["author-name"] = (
            authorname  # useful if TT supports it; if not, it's ignored
        )

    relationships: dict[str, Any] = {}
    if candidate_id:
        relationships["candidate"] = {
            "data": {"type": "candidates", "id": candidate_id}
        }
    if application_id:
        relationships["job-application"] = {
            "data": {"type": "job-applications", "id": application_id}
        }

    return {
        "data": {
            "type": "comments",
            "attributes": {k: v for k, v in attrs.items() if v is not None},
            "relationships": relationships,
        }
    }


@router.post("/comments", response_model=ImportSummary)
def import_comments(request: ImportCommentsRequest):
    """Import comments from the TeamTailor export file."""
    export = _load_export()
    notes: list[dict[str, Any]] = export.get("notes", [])
    if request.limit:
        notes = notes[: request.limit]
    client = TTClient()

    candidate_cache: dict[str, str | None] = {}
    app_cache: dict[str, str | None] = {}

    created = failed = 0
    errors: list[dict[str, Any]] = []

    for n in notes:
        candidateext = n.get("candidateexternal_id")
        appext = n.get("applicationexternal_id")

        # risolve candidate
        candidate_id = None
        if candidateext:
            if candidateext not in candidate_cache:
                candidate_cache[candidateext] = _find_id_byexternal_id(
                    client, "candidates", candidateext
                )
            candidate_id = candidate_cache.get(candidateext)

        # risolve application
        app_id = None
        if appext:
            if appext not in app_cache:
                app_cache[appext] = _find_id_byexternal_id(
                    client, "job-applications", appext
                )
            app_id = app_cache.get(appext)

        # withstruir body
        body = n.get("body") or ""
        payload = _comment_payload(
            body=body,
            visibility=n.get("visibility"),
            authorname=n.get("author"),
            candidate_id=candidate_id,
            application_id=app_id,
            _created_at=n.get("created_at"),
        )

        r = client.post("/v1/comments", jare=payload)
        if r.status_code in (200, 201):
            created += 1
        else:
            failed += 1
            errors.append(
                {
                    "external_id": n.get("external_id"),
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
        _total=len(notes),
        report=str(REPORT_PATH.risolve()),
    )
