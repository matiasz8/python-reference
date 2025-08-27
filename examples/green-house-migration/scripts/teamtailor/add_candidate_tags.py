#!/usr/bin/env python3
"""
Add Tags to TeamTailor Candidates

This script allows you to add specific tags to candidates in TeamTailor
to categorize them by technologies, skills, or other criteria.

Usage:
    python scripts/teamtailor/add_candidate_tags.py --help
    python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags "full-stack,python,react"
    python scripts/teamtailor/add_candidate_tags.py --email "john@example.com" --tags "senior,backend"
    python scripts/teamtailor/add_candidate_tags.py --bulk --tags "prospect,imported" --limit 10
"""

import argparse
import logging
import os
import sys
from typing import Any, Dict, List, Optional

import requests

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from teamtailor.api.client import TeamTailorClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CandidateTagManager:
    """Manage tags for TeamTailor candidates."""

    def __init__(self):
        """Initialize the tag manager."""
        self.client = TeamTailorClient()
        self.base_url = os.getenv("TT_BASE_URL", "https://api.na.teamtailor.com/v1")
        self.token = os.getenv("TT_TOKEN")

        if not self.token:
            raise ValueError("TT_TOKEN environment variable is required")

        self.headers = {
            "Authorization": f"Token token={self.token}",
            "X-Api-Version": "20240904",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

    def get_candidate_by_id(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """Get candidate by ID."""
        try:
            response = self.client.get_candidate(candidate_id)
            return response.get("data")
        except Exception as e:
            logger.error(f"Error getting candidate {candidate_id}: {e}")
            return None

    def get_candidate_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get candidate by email."""
        try:
            params = {"filter[search]": email}
            response = self.client.get_candidates(params=params)
            candidates = response.get("data", [])

            for candidate in candidates:
                candidate_email = candidate.get("attributes", {}).get("email")
                if candidate_email == email:
                    return candidate

            return None
        except Exception as e:
            logger.error(f"Error getting candidate by email {email}: {e}")
            return None

    def get_candidates_bulk(
        self, limit: int = 100, tags_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get multiple candidates with optional tag filtering."""
        try:
            params = {"page[size]": limit}
            if tags_filter:
                params["filter[tags]"] = tags_filter

            response = self.client.get_candidates(params=params)
            return response.get("data", [])
        except Exception as e:
            logger.error(f"Error getting candidates bulk: {e}")
            return []

    def add_tags_to_candidate(self, candidate_id: str, new_tags: List[str]) -> bool:
        """Add tags to a specific candidate."""
        try:
            # Get current candidate data
            candidate = self.get_candidate_by_id(candidate_id)
            if not candidate:
                logger.error(f"Candidate {candidate_id} not found")
                return False

            # Get current tags
            current_tags = candidate.get("attributes", {}).get("tags", [])

            # Add new tags (avoid duplicates)
            updated_tags = list(set(current_tags + new_tags))

            # Prepare update payload
            update_data = {
                "data": {
                    "id": candidate_id,
                    "type": "candidates",
                    "attributes": {"tags": updated_tags},
                }
            }

            # Update candidate
            response = requests.patch(
                f"{self.base_url}/candidates/{candidate_id}",
                headers=self.headers,
                json=update_data,
                timeout=30,
            )

            if response.status_code == 200:
                logger.info(f"✅ Successfully updated candidate {candidate_id}")
                logger.info(f"   Tags: {', '.join(updated_tags)}")
                return True
            else:
                logger.error(
                    f"❌ Failed to update candidate {candidate_id}: {response.status_code}"
                )
                if response.text:
                    logger.error(f"   Error: {response.text[:200]}...")
                return False

        except Exception as e:
            logger.error(f"❌ Error updating candidate {candidate_id}: {e}")
            return False

    def add_tags_by_email(self, email: str, tags: List[str]) -> bool:
        """Add tags to candidate by email."""
        candidate = self.get_candidate_by_email(email)
        if not candidate:
            logger.error(f"Candidate with email {email} not found")
            return False

        candidate_id = candidate.get("id")
        return self.add_tags_to_candidate(candidate_id, tags)

    def add_tags_bulk(
        self, tags: List[str], limit: int = 100, tags_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add tags to multiple candidates."""
        candidates = self.get_candidates_bulk(limit, tags_filter)

        if not candidates:
            logger.warning("No candidates found")
            return {"success": 0, "failed": 0, "total": 0}

        logger.info(f"Found {len(candidates)} candidates to update")

        success_count = 0
        failed_count = 0

        for candidate in candidates:
            candidate_id = candidate.get("id")
            candidate_name = f"{candidate.get('attributes', {}).get('first-name', '')} {candidate.get('attributes', {}).get('last-name', '')}".strip()

            logger.info(f"Processing: {candidate_name} ({candidate_id})")

            if self.add_tags_to_candidate(candidate_id, tags):
                success_count += 1
            else:
                failed_count += 1

        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(candidates),
        }

    def list_available_tags(self) -> List[str]:
        """List all available tags in the system."""
        try:
            # Get a sample of candidates to extract tags
            candidates = self.get_candidates_bulk(limit=100)

            all_tags = set()
            for candidate in candidates:
                tags = candidate.get("attributes", {}).get("tags", [])
                all_tags.update(tags)

            return sorted(list(all_tags))
        except Exception as e:
            logger.error(f"Error listing tags: {e}")
            return []


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Add tags to TeamTailor candidates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add tags to specific candidate by ID
  python add_candidate_tags.py --candidate-id 123 --tags "full-stack,python,react"

  # Add tags to candidate by email
  python add_candidate_tags.py --email "john@example.com" --tags "senior,backend"

  # Add tags to multiple candidates (bulk)
  python add_candidate_tags.py --bulk --tags "prospect,imported" --limit 50

  # List all available tags
  python add_candidate_tags.py --list-tags

Common Tags:
  - Technology: python, javascript, react, nodejs, java, c#, php, ruby, go, rust
  - Level: junior, mid, senior, lead, principal
  - Type: full-stack, frontend, backend, devops, qa, designer
  - Status: prospect, sourced, imported-from-greenhouse, active, passive
  - Location: remote, onsite, hybrid, usa, europe, latam
        """,
    )

    # Add arguments
    parser.add_argument("--candidate-id", type=str, help="Candidate ID to update")
    parser.add_argument("--email", type=str, help="Candidate email to update")
    parser.add_argument(
        "--tags", type=str, required=True, help="Comma-separated list of tags to add"
    )
    parser.add_argument(
        "--bulk", action="store_true", help="Update multiple candidates"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Limit number of candidates for bulk operations (default: 100)",
    )
    parser.add_argument(
        "--tags-filter",
        type=str,
        help="Filter candidates by existing tags (for bulk operations)",
    )
    parser.add_argument(
        "--list-tags", action="store_true", help="List all available tags in the system"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.candidate_id, args.email, args.bulk, args.list_tags]):
        parser.error(
            "Must specify one of: --candidate-id, --email, --bulk, or --list-tags"
        )

    if args.list_tags:
        # List available tags
        manager = CandidateTagManager()
        tags = manager.list_available_tags()
        print("\n📋 Available Tags:")
        print("=" * 50)
        for tag in tags:
            print(f"  • {tag}")
        print(f"\nTotal: {len(tags)} tags")
        return

    # Parse tags
    new_tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if not new_tags:
        print("❌ No valid tags provided")
        return

    print(f"🎯 Tags to add: {', '.join(new_tags)}")

    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        return

    # Initialize manager
    try:
        manager = CandidateTagManager()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return

    # Execute based on mode
    if args.candidate_id:
        # Update specific candidate by ID
        print(f"👤 Updating candidate {args.candidate_id}...")
        success = manager.add_tags_to_candidate(args.candidate_id, new_tags)
        if success:
            print("✅ Success!")
        else:
            print("❌ Failed!")
            sys.exit(1)

    elif args.email:
        # Update candidate by email
        print(f"📧 Updating candidate with email {args.email}...")
        success = manager.add_tags_by_email(args.email, new_tags)
        if success:
            print("✅ Success!")
        else:
            print("❌ Failed!")
            sys.exit(1)

    elif args.bulk:
        # Bulk update
        print(f"🚀 Bulk updating candidates...")
        print(f"   Limit: {args.limit}")
        if args.tags_filter:
            print(f"   Filter: {args.tags_filter}")

        result = manager.add_tags_bulk(new_tags, args.limit, args.tags_filter)

        print(f"\n📊 Results:")
        print(f"   ✅ Success: {result['success']}")
        print(f"   ❌ Failed: {result['failed']}")
        print(f"   📈 Total: {result['total']}")


if __name__ == "__main__":
    main()
