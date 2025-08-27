#!/usr/bin/env python3
"""
Batch Tag Migration with Progress Tracking

This script migrates candidates with structured tags in batches of 10
with detailed progress tracking and visual feedback.

Usage:
    python scripts/teamtailor/batch_tag_migration.py --dry-run
    python scripts/teamtailor/batch_tag_migration.py --live --batch-size 10
"""

import argparse
import logging
import os
import sys
import time
from typing import Any, Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from teamtailor.management.tag_manager import CandidateTagManager, TagCategory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class BatchTagMigrator:
    """Migrate candidates with structured tags in batches."""

    def __init__(self, batch_size: int = 10):
        """Initialize the batch migrator."""
        self.tag_manager = CandidateTagManager()
        self.batch_size = batch_size
        self.tag_rules = self._initialize_tag_rules()

        # Progress tracking
        self.total_processed = 0
        self.total_success = 0
        self.total_failed = 0
        self.total_no_changes = 0
        self.batch_results = []

    def _initialize_tag_rules(self) -> Dict[str, List[str]]:
        """Initialize rules for automatic tag assignment."""
        return {
            # Default tags for all candidates
            "default": ["prospect", "imported-from-greenhouse"],
            # Tags based on common patterns in candidate data
            "patterns": {
                "python": ["python", "django", "flask", "fastapi"],
                "javascript": ["javascript", "js", "react", "vue", "angular", "node"],
                "java": ["java", "spring", "hibernate"],
                "fullstack": ["full-stack", "fullstack", "full stack"],
                "frontend": ["frontend", "front-end", "front end", "ui", "ux"],
                "backend": ["backend", "back-end", "back end", "api"],
                "senior": ["senior", "lead", "principal", "architect"],
                "remote": ["remote", "remoto", "home office"],
                "latam": ["argentina", "mexico", "colombia", "brazil", "chile"],
            },
        }

    def analyze_candidate_data(self, candidate_data: Dict[str, Any]) -> List[str]:
        """Analyze candidate data and suggest appropriate tags."""
        suggested_tags = []
        attributes = candidate_data.get("attributes", {})

        # Get candidate information
        pitch = attributes.get("pitch", "").lower()
        custom_fields = attributes.get("custom-fields", {})

        # Add default tags
        suggested_tags.extend(self.tag_rules["default"])

        # Analyze pitch and custom fields for patterns
        text_to_analyze = (
            f"{pitch} {' '.join(str(v) for v in custom_fields.values())}".lower()
        )

        # Apply pattern matching
        for tag, patterns in self.tag_rules["patterns"].items():
            for pattern in patterns:
                if pattern in text_to_analyze:
                    suggested_tags.append(tag)
                    break

        # Remove duplicates and validate
        unique_tags = list(set(suggested_tags))
        validation = self.tag_manager.validate_tags(unique_tags)

        return validation["valid"]

    def process_batch(
        self, candidates: List[Dict[str, Any]], batch_num: int, dry_run: bool = True
    ) -> Dict[str, Any]:
        """Process a batch of candidates."""
        print(f"\n🔄 Procesando lote {batch_num} ({len(candidates)} candidatos)")
        print("=" * 60)

        batch_success = 0
        batch_failed = 0
        batch_no_changes = 0
        batch_errors = []

        for i, candidate in enumerate(candidates, 1):
            candidate_id = candidate.get("id")
            candidate_name = self._get_candidate_name(candidate)

            # Progress indicator
            progress = f"[{i}/{len(candidates)}]"
            print(f"{progress} Procesando: {candidate_name}")

            # Analyze current tags
            current_tags = candidate.get("attributes", {}).get("tags", [])
            print(
                f"   Tags actuales: {', '.join(current_tags) if current_tags else 'Ninguno'}"
            )

            # Analyze and suggest new tags
            suggested_tags = self.analyze_candidate_data(candidate_data)
            print(f"   Tags sugeridos: {', '.join(suggested_tags)}")

            # Find tags to add (not already present)
            tags_to_add = [tag for tag in suggested_tags if tag not in current_tags]

            if not tags_to_add:
                print(f"   ⏭️ Sin cambios necesarios")
                batch_no_changes += 1
                self.total_no_changes += 1
                continue

            print(f"   Tags a agregar: {', '.join(tags_to_add)}")

            if dry_run:
                print(f"   🔍 [DRY RUN] Se agregarían tags a {candidate_name}")
                batch_success += 1
                self.total_success += 1
            else:
                # Actually add tags
                result = self.tag_manager.add_tags_to_candidate(
                    candidate_id, tags_to_add, validate=True
                )

                if result["success"]:
                    print(f"   ✅ Actualizado exitosamente")
                    print(f"      Tags agregados: {', '.join(result['added_tags'])}")
                    print(f"      Total de tags: {result['total_tags']}")
                    batch_success += 1
                    self.total_success += 1
                else:
                    error_msg = f"Error: {result['error']}"
                    print(f"   ❌ {error_msg}")
                    batch_failed += 1
                    self.total_failed += 1
                    batch_errors.append(f"{candidate_name}: {result['error']}")

            # Small delay to avoid rate limiting
            if not dry_run:
                time.sleep(0.5)

        # Batch summary
        print(f"\n📊 Resumen del lote {batch_num}:")
        print(f"   ✅ Exitosos: {batch_success}")
        print(f"   ❌ Fallidos: {batch_failed}")
        print(f"   ⏭️ Sin cambios: {batch_no_changes}")

        if batch_errors:
            print(f"   Errores en este lote:")
            for error in batch_errors[:3]:  # Show first 3 errors
                print(f"      • {error}")
            if len(batch_errors) > 3:
                print(f"      ... y {len(batch_errors) - 3} más")

        return {
            "batch_num": batch_num,
            "total_candidates": len(candidates),
            "success": batch_success,
            "failed": batch_failed,
            "no_changes": batch_no_changes,
            "errors": batch_errors,
        }

    def migrate_in_batches(
        self, total_limit: int = 100, dry_run: bool = True
    ) -> Dict[str, Any]:
        """Migrate candidates in batches with progress tracking."""
        print(f"🚀 Iniciando migración en lotes de {self.batch_size}")
        print(f"📊 Total de candidatos a procesar: {total_limit}")
        print(f"🔍 Modo: {'DRY RUN' if dry_run else 'LIVE'}")
        print("=" * 80)

        # Get all candidates
        all_candidates = self.tag_manager.get_candidates_bulk(limit=total_limit)

        if not all_candidates:
            print("❌ No se encontraron candidatos")
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "no_changes": 0,
                "batches": 0,
                "errors": [],
            }

        print(f"✅ Encontrados {len(all_candidates)} candidatos para procesar")

        # Process in batches
        batch_num = 1
        for i in range(0, len(all_candidates), self.batch_size):
            batch_candidates = all_candidates[i : i + self.batch_size]

            # Process batch
            batch_result = self.process_batch(batch_candidates, batch_num, dry_run)
            self.batch_results.append(batch_result)

            # Update totals
            self.total_processed += len(batch_candidates)

            # Progress update
            print(
                f"\n📈 Progreso general: {self.total_processed}/{len(all_candidates)} candidatos procesados"
            )
            print(f"   ✅ Total exitosos: {self.total_success}")
            print(f"   ❌ Total fallidos: {self.total_failed}")
            print(f"   ⏭️ Total sin cambios: {self.total_no_changes}")

            batch_num += 1

            # Pause between batches
            if not dry_run and i + self.batch_size < len(all_candidates):
                print(f"\n⏳ Pausa de 2 segundos entre lotes...")
                time.sleep(2)

        return self._compile_final_summary()

    def _compile_final_summary(self) -> Dict[str, Any]:
        """Compile final migration summary."""
        all_errors = []
        for batch_result in self.batch_results:
            all_errors.extend(batch_result["errors"])

        return {
            "total": self.total_processed,
            "success": self.total_success,
            "failed": self.total_failed,
            "no_changes": self.total_no_changes,
            "batches": len(self.batch_results),
            "batch_size": self.batch_size,
            "errors": all_errors,
        }

    def _get_candidate_name(self, candidate_data: Dict[str, Any]) -> str:
        """Extract candidate name from candidate data."""
        attributes = candidate_data.get("attributes", {})
        first_name = attributes.get("first-name", "")
        last_name = attributes.get("last-name", "")
        return f"{first_name} {last_name}".strip()


def print_banner():
    """Print the script banner."""
    print("🎯 Batch Tag Migration System")
    print("=" * 60)
    print("Migración de candidatos con tags estructurados en lotes")
    print("Progreso visual detallado y control de errores")
    print()


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(
        description="Migrate candidates with structured tags in batches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run with default batch size (10)
    python batch_tag_migration.py --dry-run --limit 50

    # Live migration with custom batch size
    python batch_tag_migration.py --live --batch-size 5 --limit 100

    # Full migration with progress tracking
    python batch_tag_migration.py --live --batch-size 10 --limit 1000
        """,
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would be changed without making changes (default)",
    )

    parser.add_argument(
        "--live", action="store_true", help="Actually make changes to candidates"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of candidates to process per batch (default: 10)",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of candidates to process (default: 100)",
    )

    parser.add_argument("--verbose", action="store_true", help="Show detailed logging")

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine if this is a dry run
    dry_run = not args.live

    print_banner()

    if dry_run:
        print("🔍 MODO DRY RUN - No se harán cambios reales")
    else:
        print("🚀 MODO LIVE - Se harán cambios reales en los candidatos")
        confirm = input("¿Estás seguro de que quieres proceder? (y/N): ")
        if confirm.lower() != "y":
            print("Migración cancelada")
            return

    print(f"📊 Configuración:")
    print(f"   Tamaño de lote: {args.batch_size}")
    print(f"   Límite total: {args.limit}")
    print(f"   Modo: {'DRY RUN' if dry_run else 'LIVE'}")
    print()

    try:
        # Initialize migrator
        migrator = BatchTagMigrator(batch_size=args.batch_size)

        # Run migration
        summary = migrator.migrate_in_batches(total_limit=args.limit, dry_run=dry_run)

        # Print final summary
        print("\n" + "=" * 80)
        print("📊 RESUMEN FINAL DE LA MIGRACIÓN")
        print("=" * 80)
        print(f"Total de candidatos procesados: {summary['total']}")
        print(f"✅ Actualizaciones exitosas: {summary['success']}")
        print(f"❌ Actualizaciones fallidas: {summary['failed']}")
        print(f"⏭️ Sin cambios necesarios: {summary['no_changes']}")
        print(f"📦 Lotes procesados: {summary['batches']}")
        print(f"📏 Tamaño de lote: {summary['batch_size']}")

        if summary["errors"]:
            print(f"\n❌ Errores encontrados:")
            for error in summary["errors"][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(summary["errors"]) > 5:
                print(f"   ... y {len(summary['errors']) - 5} más errores")

        print("\n🎉 ¡Migración completada!")

        if dry_run:
            print("\n💡 Para aplicar cambios reales, ejecuta con --live")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        print(f"❌ La migración falló: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
