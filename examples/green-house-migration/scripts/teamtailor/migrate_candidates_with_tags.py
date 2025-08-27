#!/usr/bin/env python3
"""
Migrate Candidates with Structured Tags

This script uses the structured CandidateTagManager to update existing candidates
with appropriate tags based on their data and profiles.

Usage:
    python scripts/teamtailor/migrate_candidates_with_tags.py --dry-run
    python scripts/teamtailor/migrate_candidates_with_tags.py --live
"""

import argparse
import logging
import os
import sys
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


class CandidateTagMigrator:
    """Migrate candidates with structured tags based on their data."""

    def __init__(self):
        """Initialize the migrator with tag manager."""
        self.tag_manager = CandidateTagManager()

        # Define tag mapping rules based on candidate data
        self.tag_rules = self._initialize_tag_rules()

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
        """
        Analyze candidate data and suggest appropriate tags.

        Args:
            candidate_data: Candidate data from TeamTailor

        Returns:
            List of suggested tags
        """
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

    def migrate_candidate(
        self, candidate_data: Dict[str, Any], dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Migrate a single candidate with appropriate tags.

        Args:
            candidate_data: Candidate data from TeamTailor
            dry_run: If True, don't make actual changes

        Returns:
            Migration result
        """
        candidate_id = candidate_data.get("id")
        candidate_name = self._get_candidate_name(candidate_data)

        logger.info(f"Processing candidate: {candidate_name} ({candidate_id})")

        # Analyze current tags
        current_tags = candidate_data.get("attributes", {}).get("tags", [])
        logger.info(f"Current tags: {', '.join(current_tags)}")

        # Analyze and suggest new tags
        suggested_tags = self.analyze_candidate_data(candidate_data)
        logger.info(f"Suggested tags: {', '.join(suggested_tags)}")

        # Find tags to add (not already present)
        tags_to_add = [tag for tag in suggested_tags if tag not in current_tags]

        if not tags_to_add:
            logger.info(f"No new tags to add for {candidate_name}")
            return {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "status": "no_changes",
                "current_tags": current_tags,
                "suggested_tags": suggested_tags,
                "tags_added": [],
            }

        logger.info(f"Tags to add: {', '.join(tags_to_add)}")

        if dry_run:
            logger.info(f"[DRY RUN] Would add tags to {candidate_name}")
            return {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "status": "dry_run",
                "current_tags": current_tags,
                "suggested_tags": suggested_tags,
                "tags_added": tags_to_add,
            }

        # Actually add tags
        result = self.tag_manager.add_tags_to_candidate(
            candidate_id, tags_to_add, validate=True
        )

        if result["success"]:
            logger.info(f"✅ Successfully updated {candidate_name}")
            return {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "status": "success",
                "current_tags": current_tags,
                "suggested_tags": suggested_tags,
                "tags_added": result["added_tags"],
            }
        else:
            logger.error(f"❌ Failed to update {candidate_name}: {result['error']}")
            return {
                "candidate_id": candidate_id,
                "candidate_name": candidate_name,
                "status": "error",
                "error": result["error"],
                "current_tags": current_tags,
                "suggested_tags": suggested_tags,
                "tags_added": [],
            }

    def migrate_all_candidates(
        self, limit: int = 100, dry_run: bool = True
    ) -> Dict[str, Any]:
        """
        Migrate all candidates with structured tags.

        Args:
            limit: Maximum number of candidates to process
            dry_run: If True, don't make actual changes

        Returns:
            Migration summary
        """
        logger.info(
            f"Starting migration of up to {limit} candidates (dry_run: {dry_run})"
        )

        # Get all candidates
        candidates = self.tag_manager.get_candidates_bulk(limit=limit)

        if not candidates:
            logger.warning("No candidates found")
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "no_changes": 0,
                "dry_run": 0,
                "errors": [],
            }

        logger.info(f"Found {len(candidates)} candidates to process")

        # Process each candidate
        results = []
        for candidate in candidates:
            result = self.migrate_candidate(candidate, dry_run)
            results.append(result)

        # Compile summary
        summary = {
            "total": len(results),
            "success": len([r for r in results if r["status"] == "success"]),
            "failed": len([r for r in results if r["status"] == "error"]),
            "no_changes": len([r for r in results if r["status"] == "no_changes"]),
            "dry_run": len([r for r in results if r["status"] == "dry_run"]),
            "errors": [r["error"] for r in results if r["status"] == "error"],
        }

        return summary

    def _get_candidate_name(self, candidate_data: Dict[str, Any]) -> str:
        """Extract candidate name from candidate data."""
        attributes = candidate_data.get("attributes", {})
        first_name = attributes.get("first-name", "")
        last_name = attributes.get("last-name", "")
        return f"{first_name} {last_name}".strip()


def main():
    """Main migration function."""
    parser = argparse.ArgumentParser(
        description="Migrate candidates with structured tags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Dry run - see what would be changed
    python migrate_candidates_with_tags.py --dry-run --limit 10

    # Live migration - actually make changes
    python migrate_candidates_with_tags.py --live --limit 50

    # Full migration
    python migrate_candidates_with_tags.py --live --limit 1000
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

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    else:
        print("🚀 LIVE MODE - Changes will be made to candidates")
        confirm = input("Are you sure you want to proceed? (y/N): ")
        if confirm.lower() != "y":
            print("Migration cancelled")
            return

    print(f"📊 Processing up to {args.limit} candidates...")
    print("=" * 60)

    try:
        # Initialize migrator
        migrator = CandidateTagMigrator()

        # Run migration
        summary = migrator.migrate_all_candidates(limit=args.limit, dry_run=dry_run)

        # Print summary
        print("\n" + "=" * 60)
        print("📊 MIGRATION SUMMARY")
        print("=" * 60)
        print(f"Total candidates processed: {summary['total']}")
        print(f"✅ Successful updates: {summary['success']}")
        print(f"❌ Failed updates: {summary['failed']}")
        print(f"⏭️ No changes needed: {summary['no_changes']}")
        print(f"🔍 Dry run operations: {summary['dry_run']}")

        if summary["errors"]:
            print(f"\n❌ Errors encountered:")
            for error in summary["errors"][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(summary["errors"]) > 5:
                print(f"   ... and {len(summary['errors']) - 5} more errors")

        print("\n🎉 Migration completed!")

        if dry_run:
            print("\n💡 To apply changes, run with --live flag")

    except Exception as e:
        logger.error(f"Migration failed: {e}")
        print(f"❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
