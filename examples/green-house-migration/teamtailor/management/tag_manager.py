"""
TeamTailor Candidate Tag Manager

A comprehensive Python-based solution for managing candidate tags in TeamTailor.
This module provides a structured approach to categorizing candidates with
predefined tag categories and reusable methods.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from teamtailor.api.client import TeamTailorClient

logger = logging.getLogger(__name__)


class TagCategory(Enum):
    """Predefined tag categories for consistent categorization."""

    # Technology tags
    TECHNOLOGY = "technology"
    FRAMEWORK = "framework"
    LANGUAGE = "language"
    DATABASE = "database"
    TOOL = "tool"

    # Professional tags
    LEVEL = "level"
    TYPE = "type"
    STATUS = "status"
    LOCATION = "location"
    EXPERIENCE = "experience"

    # Custom tags
    CUSTOM = "custom"


@dataclass
class TagDefinition:
    """Definition of a tag with metadata."""

    name: str
    category: TagCategory
    description: str
    aliases: Optional[List[str]] = None
    color: Optional[str] = None
    priority: int = 1


class CandidateTagManager:
    """
    Comprehensive tag manager for TeamTailor candidates.

    This class provides a structured approach to managing candidate tags
    with predefined categories, validation, and bulk operations.
    """

    def __init__(self):
        """Initialize the tag manager with TeamTailor client and tag definitions."""
        self.client = TeamTailorClient()
        self.tag_definitions = self._initialize_tag_definitions()

    def _initialize_tag_definitions(self) -> Dict[str, TagDefinition]:
        """Initialize predefined tag definitions."""
        definitions = {}

        # Technology Languages
        languages = [
            ("python", "Python programming language"),
            ("javascript", "JavaScript programming language"),
            ("typescript", "TypeScript programming language"),
            ("java", "Java programming language"),
            ("csharp", "C# programming language"),
            ("php", "PHP programming language"),
            ("ruby", "Ruby programming language"),
            ("go", "Go programming language"),
            ("rust", "Rust programming language"),
            ("swift", "Swift programming language"),
            ("kotlin", "Kotlin programming language"),
            ("scala", "Scala programming language"),
        ]

        for name, description in languages:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.LANGUAGE, description=description
            )

        # Frameworks and Libraries
        frameworks = [
            ("react", "React.js framework"),
            ("vue", "Vue.js framework"),
            ("angular", "Angular framework"),
            ("django", "Django web framework"),
            ("flask", "Flask web framework"),
            ("express", "Express.js framework"),
            ("spring", "Spring framework"),
            ("laravel", "Laravel framework"),
            ("rails", "Ruby on Rails"),
            ("dotnet", ".NET framework"),
            ("nodejs", "Node.js runtime"),
            ("nextjs", "Next.js framework"),
            ("nuxt", "Nuxt.js framework"),
        ]

        for name, description in frameworks:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.FRAMEWORK, description=description
            )

        # Databases
        databases = [
            ("postgresql", "PostgreSQL database"),
            ("mysql", "MySQL database"),
            ("mongodb", "MongoDB database"),
            ("redis", "Redis database"),
            ("elasticsearch", "Elasticsearch"),
            ("dynamodb", "AWS DynamoDB"),
            ("sqlite", "SQLite database"),
        ]

        for name, description in databases:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.DATABASE, description=description
            )

        # Tools and Platforms
        tools = [
            ("docker", "Docker containerization"),
            ("kubernetes", "Kubernetes orchestration"),
            ("aws", "Amazon Web Services"),
            ("azure", "Microsoft Azure"),
            ("gcp", "Google Cloud Platform"),
            ("git", "Git version control"),
            ("jenkins", "Jenkins CI/CD"),
            ("github", "GitHub platform"),
            ("gitlab", "GitLab platform"),
        ]

        for name, description in tools:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.TOOL, description=description
            )

        # Professional Levels
        levels = [
            ("junior", "Junior level (0-2 years)"),
            ("mid", "Mid-level (2-5 years)"),
            ("senior", "Senior level (5-8 years)"),
            ("lead", "Team lead"),
            ("principal", "Principal engineer"),
            ("architect", "Software architect"),
        ]

        for name, description in levels:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.LEVEL, description=description
            )

        # Professional Types
        types = [
            ("full-stack", "Full-stack developer"),
            ("frontend", "Frontend developer"),
            ("backend", "Backend developer"),
            ("devops", "DevOps engineer"),
            ("qa", "Quality Assurance engineer"),
            ("designer", "UI/UX designer"),
            ("data-scientist", "Data scientist"),
            ("ml-engineer", "Machine learning engineer"),
            ("mobile", "Mobile developer"),
            ("ios", "iOS developer"),
            ("android", "Android developer"),
        ]

        for name, description in types:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.TYPE, description=description
            )

        # Status tags
        statuses = [
            ("prospect", "Prospect candidate"),
            ("sourced", "Sourced candidate"),
            ("imported-from-greenhouse", "Imported from Greenhouse"),
            ("active", "Active candidate"),
            ("passive", "Passive candidate"),
            ("available", "Available for opportunities"),
            ("not-available", "Not available"),
        ]

        for name, description in statuses:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.STATUS, description=description
            )

        # Location tags
        locations = [
            ("remote", "Remote work"),
            ("onsite", "On-site work"),
            ("hybrid", "Hybrid work"),
            ("usa", "United States"),
            ("europe", "Europe"),
            ("latam", "Latin America"),
            ("canada", "Canada"),
            ("uk", "United Kingdom"),
            ("germany", "Germany"),
            ("spain", "Spain"),
            ("argentina", "Argentina"),
            ("mexico", "Mexico"),
        ]

        for name, description in locations:
            definitions[name] = TagDefinition(
                name=name, category=TagCategory.LOCATION, description=description
            )

        return definitions

    def get_tag_definition(self, tag_name: str) -> Optional[TagDefinition]:
        """Get tag definition by name."""
        return self.tag_definitions.get(tag_name.lower())

    def get_tags_by_category(self, category: TagCategory) -> List[str]:
        """Get all tags in a specific category."""
        return [
            tag_name
            for tag_name, definition in self.tag_definitions.items()
            if definition.category == category
        ]

    def validate_tags(self, tags: List[str]) -> Dict[str, List[str]]:
        """
        Validate tags and categorize them.

        Returns:
            Dict with 'valid', 'invalid', and 'suggestions' lists
        """
        valid_tags = []
        invalid_tags = []
        suggestions = []

        for tag in tags:
            tag_lower = tag.lower()
            if tag_lower in self.tag_definitions:
                valid_tags.append(tag_lower)
            else:
                invalid_tags.append(tag)
                # Find similar tags
                similar = self._find_similar_tags(tag_lower)
                if similar:
                    suggestions.extend(similar)

        return {
            "valid": valid_tags,
            "invalid": invalid_tags,
            "suggestions": list(set(suggestions)),
        }

    def _find_similar_tags(self, tag: str) -> List[str]:
        """Find similar tags for suggestions."""
        similar = []
        for defined_tag in self.tag_definitions.keys():
            if tag in defined_tag or defined_tag in tag:
                similar.append(defined_tag)
        return similar[:3]  # Return top 3 suggestions

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
        self,
        limit: int = 100,
        tags_filter: Optional[str] = None,
        category_filter: Optional[TagCategory] = None,
    ) -> List[Dict[str, Any]]:
        """Get multiple candidates with optional filtering."""
        try:
            params = {"page[size]": limit}
            if tags_filter:
                params["filter[tags]"] = tags_filter

            response = self.client.get_candidates(params=params)
            candidates = response.get("data", [])

            # Filter by category if specified
            if category_filter:
                category_tags = set(self.get_tags_by_category(category_filter))
                filtered_candidates = []

                for candidate in candidates:
                    candidate_tags = set(
                        candidate.get("attributes", {}).get("tags", [])
                    )
                    if candidate_tags.intersection(category_tags):
                        filtered_candidates.append(candidate)

                return filtered_candidates

            return candidates
        except Exception as e:
            logger.error(f"Error getting candidates bulk: {e}")
            return []

    def add_tags_to_candidate(
        self, candidate_id: str, new_tags: List[str], validate: bool = True
    ) -> Dict[str, Any]:
        """
        Add tags to a specific candidate.

        Args:
            candidate_id: TeamTailor candidate ID
            new_tags: List of tags to add
            validate: Whether to validate tags before adding

        Returns:
            Dict with operation results
        """
        try:
            # Validate tags if requested
            if validate:
                validation = self.validate_tags(new_tags)
                if validation["invalid"]:
                    return {
                        "success": False,
                        "error": f"Invalid tags: {', '.join(validation['invalid'])}",
                        "suggestions": validation["suggestions"],
                    }
                new_tags = validation["valid"]

            # Get current candidate data
            candidate = self.get_candidate_by_id(candidate_id)
            if not candidate:
                return {
                    "success": False,
                    "error": f"Candidate {candidate_id} not found",
                }

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
            self.client.update_candidate(candidate_id, update_data)

            return {
                "success": True,
                "candidate_id": candidate_id,
                "added_tags": new_tags,
                "total_tags": len(updated_tags),
                "all_tags": updated_tags,
            }

        except Exception as e:
            logger.error(f"Error updating candidate {candidate_id}: {e}")
            return {"success": False, "error": str(e)}

    def add_tags_by_email(
        self, email: str, tags: List[str], validate: bool = True
    ) -> Dict[str, Any]:
        """Add tags to candidate by email."""
        candidate = self.get_candidate_by_email(email)
        if not candidate:
            return {
                "success": False,
                "error": f"Candidate with email {email} not found",
            }

        candidate_id = candidate.get("id")
        return self.add_tags_to_candidate(candidate_id, tags, validate)

    def add_tags_bulk(
        self,
        tags: List[str],
        limit: int = 100,
        tags_filter: Optional[str] = None,
        category_filter: Optional[TagCategory] = None,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """Add tags to multiple candidates."""
        candidates = self.get_candidates_bulk(limit, tags_filter, category_filter)

        if not candidates:
            return {
                "success": 0,
                "failed": 0,
                "total": 0,
                "errors": ["No candidates found"],
            }

        logger.info(f"Found {len(candidates)} candidates to update")

        success_count = 0
        failed_count = 0
        errors = []

        for candidate in candidates:
            candidate_id = candidate.get("id")
            candidate_name = _get_candidate_name(candidate)

            logger.info(f"Processing: {candidate_name} ({candidate_id})")

            result = self.add_tags_to_candidate(candidate_id, tags, validate)

            if result["success"]:
                success_count += 1
            else:
                failed_count += 1
                errors.append(f"{candidate_name}: {result['error']}")

        return {
            "success": success_count,
            "failed": failed_count,
            "total": len(candidates),
            "errors": errors,
        }

    def remove_tags_from_candidate(
        self, candidate_id: str, tags_to_remove: List[str]
    ) -> Dict[str, Any]:
        """Remove specific tags from a candidate."""
        try:
            candidate = self.get_candidate_by_id(candidate_id)
            if not candidate:
                return {
                    "success": False,
                    "error": f"Candidate {candidate_id} not found",
                }

            current_tags = candidate.get("attributes", {}).get("tags", [])
            updated_tags = [tag for tag in current_tags if tag not in tags_to_remove]

            # Prepare update payload
            update_data = {
                "data": {
                    "id": candidate_id,
                    "type": "candidates",
                    "attributes": {"tags": updated_tags},
                }
            }

            # Update candidate
            self.client.update_candidate(candidate_id, update_data)

            removed_count = len(current_tags) - len(updated_tags)

            return {
                "success": True,
                "candidate_id": candidate_id,
                "removed_tags": tags_to_remove,
                "remaining_tags": updated_tags,
                "removed_count": removed_count,
            }

        except Exception as e:
            logger.error(f"Error removing tags from candidate {candidate_id}: {e}")
            return {"success": False, "error": str(e)}

    def search_candidates_by_tags(
        self, tags: List[str], limit: int = 50, match_all: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Search candidates by tags.

        Args:
            tags: List of tags to search for
            limit: Maximum number of candidates to return
            match_all: If True, candidates must have ALL tags; if False, ANY tag

        Returns:
            List of candidate data with tag information
        """
        try:
            # Search for candidates with any of the specified tags
            params = {"page[size]": limit, "filter[tags]": ",".join(tags)}

            response = self.client.get_candidates(params=params)
            candidates = response.get("data", [])

            results = []
            for candidate in candidates:
                candidate_tags = candidate.get("attributes", {}).get("tags", [])

                # Filter based on match_all parameter
                if match_all:
                    # Must have ALL tags
                    if all(tag in candidate_tags for tag in tags):
                        results.append(self._format_candidate_result(candidate))
                else:
                    # Must have ANY tag
                    if any(tag in candidate_tags for tag in tags):
                        results.append(self._format_candidate_result(candidate))

            return results

        except Exception as e:
            logger.error(f"Error searching candidates by tags: {e}")
            return []

    def _format_candidate_result(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Format candidate data for search results."""
        attributes = candidate.get("attributes", {})
        return {
            "candidate_id": candidate.get("id"),
            "candidate_name": _get_candidate_name(candidate),
            "email": attributes.get("email"),
            "tags": attributes.get("tags", []),
            "total_tags": len(attributes.get("tags", [])),
            "created_at": attributes.get("created-at"),
            "updated_at": attributes.get("updated-at"),
        }

    def get_tag_statistics(self) -> Dict[str, Any]:
        """Get statistics about tag usage."""
        try:
            candidates = self.get_candidates_bulk(limit=1000)

            tag_counts = {}
            category_counts = {}

            for candidate in candidates:
                tags = candidate.get("attributes", {}).get("tags", [])

                for tag in tags:
                    # Count tag usage
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1

                    # Count by category
                    definition = self.get_tag_definition(tag)
                    if definition:
                        category = definition.category.value
                        category_counts[category] = category_counts.get(category, 0) + 1

            return {
                "total_candidates": len(candidates),
                "total_unique_tags": len(tag_counts),
                "tag_counts": dict(
                    sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
                ),
                "category_counts": category_counts,
            }

        except Exception as e:
            logger.error(f"Error getting tag statistics: {e}")
            return {}

    def list_available_tags(self) -> List[str]:
        """Get list of all available tags."""
        return list(self.tag_definitions.keys())


def _get_candidate_name(candidate_data: Dict[str, Any]) -> str:
    """Extract candidate name from candidate data."""
    attributes = candidate_data.get("attributes", {})
    first_name = attributes.get("first-name", "")
    last_name = attributes.get("last-name", "")
    return f"{first_name} {last_name}".strip()
