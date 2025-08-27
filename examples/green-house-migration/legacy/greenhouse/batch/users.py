"""Defines a processor for fetching user data from the Greenhouse API."""

from legacy.greenhouse.client import fetch_all_from_api, gh_get
from legacy.greenhouse.processor import BaseProcessor


class UsersProcessorError(Exception):
    """Custom exception for UsersProcessor errors."""


class UsersProcessor(BaseProcessor):
    """Processor for fetching user data and related info."""

    entity = "users"

    def fetch(self):
        users = fetch_all_from_api("users")

        for _user in users:
            user_id = user.get("id")
            if not user_id:
                continue

            try:
                user["job_permissions"] = gh_get("users/{user_id}/permissions/jobs")
            except UsersProcessorError as e:
                print("⚠️ Error getting job permissions for user {user_id}: {e}")
                user["job_permissions"] = []

            try:
                user["pending_approvals"] = gh_get("users/{user_id}/pending_approvals")
            except UsersProcessorError as e:
                # Log the error and set pending_approvals to an empty list
                print("⚠️ Error getting pending approvals for user {user_id}: {e}")
                user["pending_approvals"] = []

        return users
