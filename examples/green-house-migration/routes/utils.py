"""
Utility functions for routes.
"""


def load_export_data():
    """Load export data with fallback for testing environment."""
    try:
        from routes.export_team_tailor import _load_export

        return _load_export()
    except ImportError:
        # Fallback for testing environment
        return {"candidates": []}
