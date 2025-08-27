#!/usr/bin/env python3
"""
Verify Migration

Verify that the tag migration was completed successfully in TeamTailor.
"""

import os
import random
import sys
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


def verify_candidate_tags(candidate_data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify tags for a specific candidate."""
    candidate_name = get_candidate_name(candidate_data)
    candidate_id = candidate_data.get("id")

    # Get current tags
    current_tags = candidate_data.get("attributes", {}).get("tags", [])

    # Expected tags
    expected_tags = ["prospect", "imported-from-greenhouse"]

    # Check if expected tags are present
    missing_tags = [tag for tag in expected_tags if tag not in current_tags]
    extra_tags = [tag for tag in current_tags if tag not in expected_tags]

    return {
        "id": candidate_id,
        "name": candidate_name,
        "current_tags": current_tags,
        "expected_tags": expected_tags,
        "missing_tags": missing_tags,
        "extra_tags": extra_tags,
        "is_valid": len(missing_tags) == 0,
    }


def get_tag_statistics(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Get statistics about tag usage."""
    tag_counts = {}
    total_candidates = len(candidates)

    for candidate in candidates:
        tags = candidate.get("attributes", {}).get("tags", [])
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Calculate percentages
    tag_stats = {}
    for tag, count in tag_counts.items():
        percentage = (count / total_candidates) * 100
        tag_stats[tag] = {"count": count, "percentage": round(percentage, 2)}

    return tag_stats


def main():
    """Main verification function."""
    print("🔍 Verificación de Migración - TeamTailor")
    print("=" * 60)

    try:
        # Initialize tag manager
        tag_manager = CandidateTagManager()
        print("✅ Conectado a TeamTailor")

        # Get a sample of candidates for verification
        print("\n📥 Obteniendo muestra de candidatos...")
        all_candidates = []
        page = 1
        page_size = 25

        # Get first 100 candidates for verification
        while len(all_candidates) < 100:
            try:
                candidates_data = tag_manager.client.get_candidates(
                    {"page[size]": page_size, "page[number]": page}
                )

                candidates = candidates_data.get("data", [])
                if not candidates:
                    break

                all_candidates.extend(candidates)
                page += 1

            except Exception as e:
                print(f"❌ Error obteniendo página {page}: {e}")
                break

        if not all_candidates:
            print("❌ No se pudieron obtener candidatos")
            return

        print(f"✅ {len(all_candidates)} candidatos obtenidos para verificación")

        # Verify individual candidates
        print("\n🔍 Verificando candidatos individuales...")
        verification_results = []

        # Check first 10 candidates
        for i, candidate in enumerate(all_candidates[:10], 1):
            result = verify_candidate_tags(candidate)
            verification_results.append(result)

            status = "✅" if result["is_valid"] else "❌"
            print(f"   [{i}/10] {status} {result['name']}")
            print(f"        Tags: {', '.join(result['current_tags'])}")

            if result["missing_tags"]:
                print(f"        ❌ Faltan: {', '.join(result['missing_tags'])}")
            if result["extra_tags"]:
                print(f"        ✅ Extra: {', '.join(result['extra_tags'])}")

        # Get tag statistics
        print("\n📊 Estadísticas de Tags...")
        tag_stats = get_tag_statistics(all_candidates)

        print("\n🏷️ Distribución de Tags:")
        print("-" * 40)
        for tag, stats in sorted(tag_stats.items()):
            print(f"   {tag}: {stats['count']} ({stats['percentage']}%)")

        # Summary
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE VERIFICACIÓN")
        print("=" * 60)

        valid_candidates = sum(1 for r in verification_results if r["is_valid"])
        total_verified = len(verification_results)

        print(f"Candidatos verificados: {total_verified}")
        print(f"✅ Válidos: {valid_candidates}")
        print(f"❌ Con problemas: {total_verified - valid_candidates}")
        print(f"Tasa de éxito: {(valid_candidates/total_verified)*100:.1f}%")

        # Check for required tags
        required_tags = ["prospect", "imported-from-greenhouse"]
        for tag in required_tags:
            if tag in tag_stats:
                count = tag_stats[tag]["count"]
                percentage = tag_stats[tag]["percentage"]
                status = "✅" if percentage >= 95 else "⚠️"
                print(f"{status} {tag}: {count} candidatos ({percentage}%)")
            else:
                print(f"❌ {tag}: No encontrado")

        # Test search functionality
        print("\n🔍 Probando búsqueda por tags...")
        try:
            # Search for candidates with 'prospect' tag
            prospect_candidates = tag_manager.search_candidates_by_tags(
                ["prospect"], match_all=True
            )
            print(f"   ✅ Búsqueda 'prospect': {len(prospect_candidates)} candidatos")

            # Search for candidates with 'python' tag
            python_candidates = tag_manager.search_candidates_by_tags(
                ["python"], match_all=True
            )
            print(f"   ✅ Búsqueda 'python': {len(python_candidates)} candidatos")

        except Exception as e:
            print(f"   ❌ Error en búsqueda: {e}")

        print("\n🎉 ¡Verificación completada!")

        if valid_candidates == total_verified:
            print("✅ La migración fue exitosa")
        else:
            print("⚠️ Se encontraron algunos problemas")

    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")


if __name__ == "__main__":
    main()
