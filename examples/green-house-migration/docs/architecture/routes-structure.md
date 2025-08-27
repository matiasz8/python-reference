# Routes Structure Documentation

## Overview

The `routes/` directory has been reorganized to provide better separation of
concerns and clearer organization. This document explains the new structure and
how to work with it.

## Directory Structure

```
routes/
├── api/                    # 🔌 Core API endpoints
│   ├── __init__.py
│   ├── candidates.py       # Candidate management endpoints
│   ├── applications.py     # Application management endpoints
│   ├── jobs.py            # Job management endpoints
│   ├── users.py           # User management endpoints
│   ├── metadata.py        # Metadata and configuration endpoints
│   ├── offers.py          # Offer management endpoints
│   ├── prospects.py       # Prospect management endpoints
│   ├── scheduled_interviews.py  # Interview scheduling endpoints
│   ├── scorecards.py      # Scorecard management endpoints
│   ├── stats.py           # Statistics and analytics endpoints
│   └── users_mapping.py   # User mapping utilities
├── import_/               # 📥 Data import operations
│   ├── __init__.py
│   ├── import_candidates.py
│   ├── import_applications.py
│   ├── import_jobs.py
│   ├── import_offers.py
│   ├── import_interviews.py
│   ├── import_comments.py
│   └── import_custom_fields.py
├── export/                # 📤 Data export operations
│   ├── __init__.py
│   ├── export.py          # General export functionality
│   └── export_team_tailor.py  # TeamTailor-specific exports
├── clients/               # 🔗 API clients
│   ├── __init__.py
│   ├── tt_client.py       # Basic TeamTailor client
│   └── tt_client_enhanced.py  # Enhanced TeamTailor client
└── __init__.py
```

## Module Purposes

### API Routes (`routes/api/`)

Core API endpoints that provide the main functionality of the application:

- **candidates.py**: Complete candidate CRUD operations

- **applications.py**: Application management and tracking

- **jobs.py**: Job posting and management

- **users.py**: User administration and role management

- **metadata.py**: System configuration and metadata

- **offers.py**: Offer creation and management

- **prospects.py**: Prospect tracking and management

- **scheduled_interviews.py**: Interview scheduling and management

- **scorecards.py**: Evaluation and scoring functionality

- **stats.py**: Analytics and reporting endpoints

- **users_mapping.py**: User mapping between systems

### Import Routes (`routes/import_/`)

Data import operations for migrating data from external sources:

- **import_candidates.py**: Import candidates from external systems

- **import_applications.py**: Import applications and related data

- **import_jobs.py**: Import job postings and requirements

- **import_offers.py**: Import offer data

- **import_interviews.py**: Import interview schedules and results

- **import_comments.py**: Import comments and notes

- **import_custom_fields.py**: Import custom field definitions

### Export Routes (`routes/export/`)

Data export functionality for reporting and data transfer:

- **export.py**: General export functionality (CSV, JSON, Excel)

- **export_team_tailor.py**: TeamTailor-specific export operations

### Client Routes (`routes/clients/`)

API client implementations for external service integration:

- **tt_client.py**: Basic TeamTailor API client

- **tt_client_enhanced.py**: Enhanced client with additional features

## Import Patterns

### From main.py

```python
from routes.api import (
    candidates,
    applications,
    jobs,
    users,
    metadata,
    offers,
    prospects,
    scheduled_interviews,
    scorecards,
    stats,
    users_mapping,
)
from routes.export import export, export_team_tailor
from routes.import_ import (
    import_applications,
    import_candidates,
    import_comments,
    import_custom_fields,
    import_interviews,
    import_jobs,
    import_offers,
)
```

### Within routes modules

```python
# For API routes
from routes.clients.tt_client import TTClient

# For import/export routes
from routes.clients.tt_client import TTClient
```

## Best Practices

1. **Keep API routes focused**: Each file should handle one main entity type

2. **Use consistent naming**: Follow the established naming conventions

3. **Import from clients**: Always import client classes from `routes.clients/`

4. **Maintain separation**: Don't mix import/export logic with core API logic

5. **Document endpoints**: Include proper docstrings for all endpoints

## Migration Notes

- All existing functionality has been preserved

- Import paths have been updated in `main.py`

- Client imports have been updated to use the new structure

- No breaking changes to the API endpoints themselves

## Future Considerations

- Consider adding middleware for common operations

- Implement shared utilities for common patterns

- Add validation schemas in a separate directory

- Consider versioning for API endpoints
