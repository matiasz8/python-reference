#!/usr/bin/env python3
"""
Retry Failed Migration

Retry migration for candidates that failed in previous runs.
"""

import os
import sys
import time
from typing import Any, Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from teamtailor.management.tag_manager import CandidateTagManager


def get_candidate_name(candidate_data: Dict[str, Any]) -> str:
    """Extract candidate name from candidate data."""
    attributes = candidate_data.get("attributes", {})
    first_name = attributes.get("first-name", "")
    last_name = attributes.get("last-name", "")
    return f"{first_name} {last_name}".strip()


def analyze_candidate_for_tags(candidate_data: Dict[str, Any]) -> List[str]:
    """Analyze candidate data and suggest tags."""
    suggested_tags = ["prospect", "imported-from-greenhouse"]

    # Get candidate information
    attributes = candidate_data.get("attributes", {})
    pitch = attributes.get("pitch", "")
    custom_fields = attributes.get("custom-fields", {})

    # Create text to analyze
    text_to_analyze = ""
    if pitch:
        text_to_analyze += pitch.lower()
    if custom_fields:
        text_to_analyze += (
            " " + " ".join(str(v) for v in custom_fields.values()).lower()
        )

    # Simple pattern matching
    if (
        "python" in text_to_analyze
        or "django" in text_to_analyze
        or "flask" in text_to_analyze
    ):
        suggested_tags.append("python")

    if (
        "javascript" in text_to_analyze
        or "react" in text_to_analyze
        or "vue" in text_to_analyze
    ):
        suggested_tags.append("javascript")

    if "java" in text_to_analyze or "spring" in text_to_analyze:
        suggested_tags.append("java")

    if "full" in text_to_analyze and "stack" in text_to_analyze:
        suggested_tags.append("full-stack")

    if "frontend" in text_to_analyze or "front-end" in text_to_analyze:
        suggested_tags.append("frontend")

    if "backend" in text_to_analyze or "back-end" in text_to_analyze:
        suggested_tags.append("backend")

    if "senior" in text_to_analyze or "lead" in text_to_analyze:
        suggested_tags.append("senior")

    if "remote" in text_to_analyze or "remoto" in text_to_analyze:
        suggested_tags.append("remote")

    return list(set(suggested_tags))  # Remove duplicates


def retry_failed_candidates(
    failed_ids: List[str], tag_manager: CandidateTagManager, dry_run: bool = False
) -> Dict[str, Any]:
    """Retry migration for failed candidate IDs."""
    print(f"🔄 Reintentando {len(failed_ids)} candidatos fallidos...")

    success_count = 0
    failed_count = 0
    errors = []

    for i, candidate_id in enumerate(failed_ids, 1):
        try:
            # Get candidate data
            candidate_data = tag_manager.client.get_candidate(candidate_id)
            candidate_name = get_candidate_name(candidate_data)

            # Get current tags
            current_tags = candidate_data.get("attributes", {}).get("tags", [])

            # Analyze and suggest new tags
            suggested_tags = analyze_candidate_for_tags(candidate_data)

            # Find tags to add (not already present)
            tags_to_add = [tag for tag in suggested_tags if tag not in current_tags]

            if not tags_to_add:
                print(
                    f"   [{i}/{len(failed_ids)}] ⏭️ {candidate_name}: Sin cambios necesarios"
                )
                continue

            if dry_run:
                print(
                    f"   [{i}/{len(failed_ids)}] 🔍 {candidate_name}: Se agregarían {tags_to_add}"
                )
                success_count += 1
            else:
                # Actually add tags
                result = tag_manager.add_tags_to_candidate(
                    candidate_id, tags_to_add, validate=True
                )

                if result["success"]:
                    print(
                        f"   [{i}/{len(failed_ids)}] ✅ {candidate_name}: Tags agregados"
                    )
                    success_count += 1
                else:
                    print(
                        f"   [{i}/{len(failed_ids)}] ❌ {candidate_name}: {result['error']}"
                    )
                    failed_count += 1
                    errors.append(f"{candidate_name}: {result['error']}")

            # Delay between retries
            if not dry_run:
                time.sleep(0.5)

        except Exception as e:
            print(f"   [{i}/{len(failed_ids)}] ❌ ID {candidate_id}: {str(e)}")
            failed_count += 1
            errors.append(f"ID {candidate_id}: {str(e)}")

    return {"success": success_count, "failed": failed_count, "errors": errors}


def main():
    """Main function."""
    import argparse

    parser = argparse.ArgumentParser(description="Retry failed migration")
    parser.add_argument(
        "--dry-run", action="store_true", default=True, help="Dry run mode"
    )
    parser.add_argument("--live", action="store_true", help="Live mode")
    parser.add_argument(
        "--auto-confirm", action="store_true", help="Auto confirm without asking"
    )

    args = parser.parse_args()

    # Determine mode
    dry_run = not args.live

    print("🔄 Retry Failed Migration")
    print("=" * 50)

    if dry_run:
        print("🔍 DRY RUN - No cambios reales")
    else:
        print("🚀 LIVE - Cambios reales")
        if not args.auto_confirm:
            confirm = input("¿Continuar? (y/N): ")
            if confirm.lower() != "y":
                print("Cancelado")
                return

    # Failed candidate IDs from previous run
    failed_ids = [
        "4558712",
        "4558715",
        "4558716",
        "4558717",
        "4558746",
        "4558748",
        "4558750",
        "4558764",
        "4558768",
        "4558777",
        "4558780",
    ]

    print(f"📋 Candidatos fallidos a reintentar: {len(failed_ids)}")
    print()

    try:
        # Initialize tag manager
        tag_manager = CandidateTagManager()
        print("✅ Conectado a TeamTailor")

        # Retry failed candidates
        result = retry_failed_candidates(failed_ids, tag_manager, dry_run)

        # Summary
        print("\n" + "=" * 50)
        print("📊 RESUMEN DEL REINTENTO")
        print("=" * 50)
        print(f"Total reintentados: {len(failed_ids)}")
        print(f"✅ Exitosos: {result['success']}")
        print(f"❌ Fallidos: {result['failed']}")

        if result["errors"]:
            print(f"\n❌ Errores ({len(result['errors'])}):")
            for error in result["errors"][:5]:
                print(f"   • {error}")
            if len(result["errors"]) > 5:
                print(f"   ... y {len(result['errors']) - 5} más")

        print("\n🎉 ¡Reintento completado!")

        if dry_run:
            print("\n💡 Para aplicar cambios: --live --auto-confirm")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
