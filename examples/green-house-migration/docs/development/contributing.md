# Contributing Guide - Greenhouse to TeamTailor Migration

## Getting Started

1. Fork the repository

2. Clone your fork

3. Set up the development environment

4. Create a feature branch

5. Make your changes

6. Run tests and linting

7. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/green-house.git
cd green-house

# Set up development environment
make setup-dev

# Create feature branch
git checkout -b feature/your-feature-name
```

## TeamTailor Development Workflow

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env

# Required variables:
# TT_TOKEN=your_teamtailor_token
# GREENHOUSE_API_KEY=your_greenhouse_key
```

### 2. Test TeamTailor Connection

```bash
# Test API connection
make teamtailor-test

# Test specific endpoints
python scripts/teamtailor/test_connection.py
```

### 3. Development Workflow

```bash
# Start development server
make run

# Run tests
make test

# Run TeamTailor-specific tests
pytest tests/ -m teamtailor

# Run migration tests
pytest tests/ -m migration
```

## Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting

- **isort**: Import sorting

- **Flake8**: Linting

- **mypy**: Type checking

Run all checks:

```bash
make lint
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test categories
pytest tests/ -m unit
pytest tests/ -m integration
pytest tests/ -m teamtailor
pytest tests/ -m migration

# Run with coverage
pytest --cov=greenhouse --cov=routes --cov-report=html
```

### Writing Tests

- Place tests in the `tests/` directory

- Use descriptive test names

- Include both unit and integration tests

- Use fixtures for common test data

### TeamTailor Test Examples

```python
@pytest.mark.teamtailor
def test_teamtailor_candidate_creation():
    """Test creating a candidate in TeamTailor."""
    # Test implementation

@pytest.mark.migration
def test_greenhouse_to_teamtailor_migration():
    """Test data migration from Greenhouse to TeamTailor."""
    # Test implementation
```

## TeamTailor API Development

### Adding New Endpoints

1. Update `routes/tt_client_enhanced.py`

2. Add corresponding tests

3. Update documentation

### Example Endpoint Addition

```python
def create_candidate(self, candidate_data: dict) -> dict:
    """Create a new candidate in TeamTailor."""
    return self.post("/candidates", json_data=candidate_data)
```

### Rate Limiting

Always respect TeamTailor's rate limits:

```python
import time

# Add delay between requests
time.sleep(0.2)  # 200ms delay
```

## Migration Development

### Adding New Entity Types

1. Create migration script in `scripts/teamtailor/`

2. Add export functionality in `routes/export_team_tailor.py`

3. Add corresponding tests

### Example Migration Script

```python
def migrate_candidates():
    """Migrate candidates from Greenhouse to TeamTailor."""
    # Implementation
```

## Pull Request Process

1. Ensure all tests pass

2. Update documentation if needed

3. Follow the commit message format

4. Request review from maintainers

## Commit Message Format

We use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:

- `feat(teamtailor): add candidate creation endpoint`

- `fix(migration): resolve rate limiting issue`

- `docs(api): update TeamTailor API documentation`

## TeamTailor-Specific Guidelines

### API Versioning

- Always specify the API version in headers

- Test with multiple API versions when possible

- Document breaking changes

### Error Handling

```python
try:
    response = self.client.post("/candidates", json=data)
    return response.json()
except requests.exceptions.RequestException as e:
    logger.error(f"TeamTailor API error: {e}")
    raise
```

### Data Validation

```python
from pydantic import BaseModel

class TeamTailorCandidate(BaseModel):
    first_name: str
    last_name: str
    email: str
```

### Testing with Mock Data

```python
@pytest.fixture
def mock_teamtailor_response():
    return {
        "data": {
            "id": "123",
            "type": "candidates",
            "attributes": {
                "first-name": "John",
                "last-name": "Doe"
            }
        }
    }
```

## Documentation

### API Documentation

- Update `docs/api/TEAMTAILOR_API_ENDPOINTS.md`

- Include request/response examples

- Document rate limits and error codes

### Migration Documentation

- Update migration guides in `docs/guides/`

- Include step-by-step instructions

- Document common issues and solutions

## Performance Considerations

### Rate Limiting

- Implement exponential backoff

- Use bulk operations when possible

- Cache frequently accessed data

### Memory Usage

- Process data in batches

- Use generators for large datasets

- Monitor memory usage during migrations

## Security

### API Token Management

- Never commit API tokens to version control

- Use environment variables

- Rotate tokens regularly

### Data Privacy

- Anonymize test data

- Follow GDPR compliance

- Implement data retention policies

## Monitoring and Logging

### Metrics

- Add Prometheus metrics for new features

- Monitor API call success rates

- Track migration progress

### Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Starting TeamTailor migration")
logger.error("Migration failed", exc_info=True)
```

## Questions?

Open an issue or reach out to the maintainers. For TeamTailor-specific
questions, refer to the [TeamTailor API documentation](https://developer.teamtailor.com/).
