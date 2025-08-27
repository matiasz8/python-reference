#!/usr/bin/env python3
"""
Add Common Tag Patterns to Candidates

This script adds common tag patterns to candidates based on their profiles
and technologies. It uses the structured tag manager for consistency.

Usage:
    python scripts/teamtailor/add_common_tag_patterns.py --pattern fullstack-python
    python scripts/teamtailor/add_common_tag_patterns.py --pattern frontend-react --live
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


class CommonTagPatterns:
    """Common tag patterns for different roles and technologies."""

    def __init__(self):
        """Initialize with tag manager."""
        self.tag_manager = CandidateTagManager()
        self.patterns = self._initialize_patterns()

    def _initialize_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize common tag patterns."""
        return {
            "fullstack-python": {
                "name": "Full Stack Python Developer",
                "description": "Python developers with frontend skills",
                "tags": ["full-stack", "python", "senior", "remote"],
                "search_tags": ["python"],
                "category": TagCategory.TYPE,
            },
            "fullstack-javascript": {
                "name": "Full Stack JavaScript Developer",
                "description": "JavaScript developers with full-stack skills",
                "tags": ["full-stack", "javascript", "nodejs", "senior", "remote"],
                "search_tags": ["javascript", "nodejs"],
                "category": TagCategory.TYPE,
            },
            "frontend-react": {
                "name": "Frontend React Developer",
                "description": "React specialists",
                "tags": [
                    "frontend",
                    "react",
                    "javascript",
                    "typescript",
                    "senior",
                    "remote",
                ],
                "search_tags": ["react"],
                "category": TagCategory.TYPE,
            },
            "backend-python": {
                "name": "Backend Python Developer",
                "description": "Python backend specialists",
                "tags": ["backend", "python", "django", "flask", "senior", "remote"],
                "search_tags": ["python", "django", "flask"],
                "category": TagCategory.TYPE,
            },
            "backend-java": {
                "name": "Backend Java Developer",
                "description": "Java backend specialists",
                "tags": ["backend", "java", "spring", "senior", "remote"],
                "search_tags": ["java", "spring"],
                "category": TagCategory.TYPE,
            },
            "devops": {
                "name": "DevOps Engineer",
                "description": "DevOps and infrastructure specialists",
                "tags": ["devops", "docker", "kubernetes", "aws", "senior", "remote"],
                "search_tags": ["devops", "docker", "kubernetes"],
                "category": TagCategory.TYPE,
            },
            "data-scientist": {
                "name": "Data Scientist",
                "description": "Data science and ML specialists",
                "tags": ["data-scientist", "python", "ml-engineer", "senior", "remote"],
                "search_tags": ["data-scientist", "ml-engineer"],
                "category": TagCategory.TYPE,
            },
            "senior-developers": {
                "name": "Senior Developers",
                "description": "All senior level developers",
                "tags": ["senior", "prospect"],
                "search_tags": ["senior"],
                "category": TagCategory.LEVEL,
            },
            "remote-developers": {
                "name": "Remote Developers",
                "description": "All remote developers",
                "tags": ["remote", "prospect"],
                "search_tags": ["remote"],
                "category": TagCategory.LOCATION,
            },
            "latam-developers": {
                "name": "LATAM Developers",
                "description": "Developers from Latin America",
                "tags": ["latam", "prospect"],
                "search_tags": ["argentina", "mexico", "colombia", "brazil", "chile"],
                "category": TagCategory.LOCATION,
            },
        }

    def get_available_patterns(self) -> List[str]:
        """Get list of available patterns."""
        return list(self.patterns.keys())

    def get_pattern_info(self, pattern_name: str) -> Dict[str, Any]:
        """Get information about a specific pattern."""
        return self.patterns.get(pattern_name, {})

    def apply_pattern(
        self, pattern_name: str, dry_run: bool = True, limit: int = 100
    ) -> Dict[str, Any]:
        """
        Apply a tag pattern to candidates.

        Args:
            pattern_name: Name of the pattern to apply
            dry_run: If True, don't make actual changes
            limit: Maximum number of candidates to process

        Returns:
            Application result
        """
        pattern = self.patterns.get(pattern_name)
        if not pattern:
            return {"success": False, "error": f"Pattern '{pattern_name}' not found"}

        logger.info(f"Applying pattern: {pattern['name']}")
        logger.info(f"Description: {pattern['description']}")
        logger.info(f"Tags to add: {', '.join(pattern['tags'])}")

        # Search for candidates with the pattern's search tags
        search_tags = pattern["search_tags"]
        candidates = self.tag_manager.search_candidates_by_tags(
            tags=search_tags, limit=limit, match_all=False  # Any of the search tags
        )

        if not candidates:
            logger.warning(f"No candidates found with tags: {', '.join(search_tags)}")
            return {
                "success": True,
                "pattern": pattern_name,
                "candidates_found": 0,
                "candidates_updated": 0,
                "errors": [],
            }

        logger.info(f"Found {len(candidates)} candidates to update")

        # Apply tags to each candidate
        updated_count = 0
        errors = []

        for candidate in candidates:
            candidate_id = candidate["candidate_id"]
            candidate_name = candidate["candidate_name"]

            logger.info(f"Processing: {candidate_name}")

            if dry_run:
                logger.info(f"[DRY RUN] Would add tags to {candidate_name}")
                updated_count += 1
            else:
                result = self.tag_manager.add_tags_to_candidate(
                    candidate_id, pattern["tags"], validate=True
                )

                if result["success"]:
                    logger.info(f"✅ Updated {candidate_name}")
                    updated_count += 1
                else:
                    error_msg = f"Failed to update {candidate_name}: {result['error']}"
                    logger.error(error_msg)
                    errors.append(error_msg)

        return {
            "success": True,
            "pattern": pattern_name,
            "candidates_found": len(candidates),
            "candidates_updated": updated_count,
            "errors": errors,
        }


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Add common tag patterns to candidates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Patterns:
    fullstack-python     - Full Stack Python developers
    fullstack-javascript - Full Stack JavaScript developers
    frontend-react       - Frontend React developers
    backend-python       - Backend Python developers
    backend-java         - Backend Java developers
    devops               - DevOps engineers
    data-scientist       - Data scientists
    senior-developers    - All senior developers
    remote-developers    - All remote developers
    latam-developers     - LATAM developers

Examples:
    # List available patterns
    python add_common_tag_patterns.py --list-patterns

    # Dry run - see what would be changed
    python add_common_tag_patterns.py --pattern frontend-react --dry-run

    # Apply pattern to candidates
    python add_common_tag_patterns.py --pattern fullstack-python --live
        """,
    )

    parser.add_argument("--pattern", type=str, help="Pattern to apply")

    parser.add_argument(
        "--list-patterns", action="store_true", help="List all available patterns"
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

    # Initialize patterns
    patterns = CommonTagPatterns()

    # List patterns if requested
    if args.list_patterns:
        print("📋 Available Tag Patterns:")
        print("=" * 50)

        for pattern_name in patterns.get_available_patterns():
            pattern_info = patterns.get_pattern_info(pattern_name)
            print(f"\n🎯 {pattern_info['name']}")
            print(f"   Description: {pattern_info['description']}")
            print(f"   Tags: {', '.join(pattern_info['tags'])}")
            print(f"   Search: {', '.join(pattern_info['search_tags'])}")

        return

    # Validate pattern argument
    if not args.pattern:
        parser.error("Must specify --pattern or --list-patterns")

    # Check if pattern exists
    if args.pattern not in patterns.get_available_patterns():
        print(f"❌ Pattern '{args.pattern}' not found")
        print("Use --list-patterns to see available patterns")
        return

    # Determine if this is a dry run
    dry_run = not args.live

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
    else:
        print("🚀 LIVE MODE - Changes will be made to candidates")
        confirm = input("Are you sure you want to proceed? (y/N): ")
        if confirm.lower() != "y":
            print("Operation cancelled")
            return

    print(f"📊 Processing up to {args.limit} candidates...")
    print("=" * 60)

    try:
        # Apply pattern
        result = patterns.apply_pattern(
            pattern_name=args.pattern, dry_run=dry_run, limit=args.limit
        )

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            return

        # Print results
        print("\n" + "=" * 60)
        print("📊 PATTERN APPLICATION SUMMARY")
        print("=" * 60)
        print(f"Pattern: {result['pattern']}")
        print(f"Candidates found: {result['candidates_found']}")
        print(f"Candidates updated: {result['candidates_updated']}")

        if result["errors"]:
            print(f"\n❌ Errors encountered:")
            for error in result["errors"][:5]:  # Show first 5 errors
                print(f"   • {error}")
            if len(result["errors"]) > 5:
                print(f"   ... and {len(result['errors']) - 5} more errors")

        print("\n🎉 Pattern application completed!")

        if dry_run:
            print("\n💡 To apply changes, run with --live flag")

    except Exception as e:
        logger.error(f"Pattern application failed: {e}")
        print(f"❌ Pattern application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
