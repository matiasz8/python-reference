# Candidate Tag System

## 📋 General Description

The tag system allows categorizing candidates in TeamTailor with specific
labels (e.g., "Full Stack", "React", "Python") as a replacement for
"Prospect Pools" that are not available in TeamTailor.

## 🏗️ Architecture

### Main Components

1. **`teamtailor/management/tag_manager.py`**

- Central tag management system

2. **`routes/api/candidate_tags.py`** - API endpoints for tag management
3. **Migration scripts** - Tools for applying tags in bulk

### Tag Structure

```python
class TagCategory(Enum):
    LANGUAGES = "languages"
    FRAMEWORKS = "frameworks"
    ROLES = "roles"
    SKILLS = "skills"
    EXPERIENCE = "experience"
    LOCATION = "location"
    SENIORITY = "seniority"
```

## 🚀 Quick Start

### 1. View Available Tags

```bash
pipenv run python scripts/teamtailor/quick_start_tagging.py
```

### 2. Apply Tags to a Candidate

```bash
pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags "python,react,fullstack"
```

### 3. Bulk Migration

```bash
pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live
```

## 📚 Detailed Documentation

- [Migration Guide](migration-guide.md)
- [API Reference](api-reference.md)
- [Available Scripts](scripts-overview.md)
- [Usage Examples](usage-examples.md)

## 🔧 Configuration

### Required Environment Variables

```bash
TT_TOKEN=your_teamtailor_token
TT_BASE_URL=https://api.teamtailor.com
TT_API_VERSION=v1
```

### Test Mode

```bash
TEAMTAILOR_TEST_MODE=true
```

## 📊 Statistics

- **Predefined Tags**: 50+ tags organized in 7 categories
- **Processed Candidates**: ~3,656 unique candidates
- **Available Scripts**: 10+ management tools

## 🎯 Use Cases

1. **Automatic Categorization**: Tags based on skills and experience
2. **Advanced Search**: Filtering by specific technologies
3. **Market Analysis**: Statistics by technologies
4. **Talent Management**: Candidate identification by role

## 🔗 Related Links

- [Dual Dashboard](../dashboard/README.md)
- [TeamTailor API](../../api/TEAMTAILOR_API_ENDPOINTS.md)
- [Migration Guides](../../guides/migration/README.md)
