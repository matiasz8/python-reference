# Tag System Scripts

## 📁 Location

All scripts are located in `scripts/teamtailor/`

## 🚀 Main Scripts

### 1. `quick_start_tagging.py`

**Description**: Interactive script to get started with the tag system

```bash
pipenv run python scripts/teamtailor/quick_start_tagging.py
```

**Features**:

- Interactive menu with all options
- View available categories and tags
- System statistics
- Candidate search
- Tag application

### 2. `add_candidate_tags.py`

**Description**: Apply tags to individual candidates or in batch

```bash
# Individual candidate
pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags "python,react"

# By email
pipenv run python scripts/teamtailor/add_candidate_tags.py --email "candidate@example.com" --tags "fullstack"

# Batch with filters
pipenv run python scripts/teamtailor/add_candidate_tags.py --bulk --limit 50 --tags-filter "python"
```

**Options**:

- `--candidate-id`: Specific candidate ID
- `--email`: Candidate email
- `--tags`: Comma-separated list of tags
- `--bulk`: Batch mode
- `--limit`: Candidate limit
- `--tags-filter`: Filter by existing tags
- `--list-tags`: Only list available tags
- `--dry-run`: Simulate without applying changes

### 3. `fast_batch_migration.py`

**Description**: Fast and bulk migration of candidates with tags

```bash
pipenv run python scripts/teamtailor/fast_batch_migration.py --limit 100 --live
```

**Options**:

- `--limit`: Maximum number of candidates to process
- `--live`: Apply real changes (without --live is simulation)
- `--dry-run`: Only simulate (default)

## 🔧 Utility Scripts

### 4. `example_tag_usage.py`

**Description**: Usage examples for the tag system

```bash
pipenv run python scripts/teamtailor/example_tag_usage.py
```

**Features**:

- Demonstration of all functions
- Search examples
- Tag validation
- Statistics

### 5. `demo_tag_system.py`

**Description**: Demo of the system without real TeamTailor connection

```bash
pipenv run python scripts/teamtailor/demo_tag_system.py
```

**Features**:

- Test data
- No need for real token
- Ideal for development and testing

### 6. `add_common_tag_patterns.py`

**Description**: Apply predefined tag patterns

```bash
pipenv run python scripts/teamtailor/add_common_tag_patterns.py --pattern "fullstack-python"
```

**Available Patterns**:

- `fullstack-python`: Python + React/Vue + SQL
- `frontend-react`: React + TypeScript + CSS
- `backend-python`: Python + Django/Flask + PostgreSQL
- `devops`: Docker + Kubernetes + AWS
- `mobile`: React Native + iOS + Android

## 🔄 Migration Scripts

### 7. `migrate_candidates_with_tags.py`

**Description**: Complete migration with automatic data analysis

```bash
pipenv run python scripts/teamtailor/migrate_candidates_with_tags.py --dry-run
```

**Features**:

- Automatic skills analysis
- Technology detection
- Intelligent tag application
- Detailed reports

### 8. `retry_failed_migration.py`

**Description**: Retry migration for failed candidates

```bash
pipenv run python scripts/teamtailor/retry_failed_migration.py --failed-ids "123,456,789"
```

### 9. `verify_migration.py`

**Description**: Verify migration success

```bash
pipenv run python scripts/teamtailor/verify_migration.py
```

**Verifications**:

- Tags applied correctly
- Migration statistics
- Search tests
- Success report

## 🧪 Testing Scripts

### 10. `discover_endpoints.py`

**Description**: Discover available endpoints in TeamTailor

```bash
pipenv run python scripts/teamtailor/discover_endpoints.py
```

### 11. `teamtailor_endpoints.py`

**Description**: Test specific TeamTailor endpoints

```bash
pipenv run python scripts/teamtailor/teamtailor_endpoints.py
```

## 📊 Analysis Scripts

### 12. `analyze_user_access.py`

**Description**: Analyze user access in TeamTailor

```bash
pipenv run python scripts/teamtailor/analyze_user_access.py
```

### 13. `compare_users.py`

**Description**: Compare users between systems

```bash
pipenv run python scripts/teamtailor/compare_users.py
```

## 🎯 Recommended Workflow

1. **Start**: `quick_start_tagging.py`
2. **Test**: `demo_tag_system.py`
3. **Migration**: `fast_batch_migration.py --dry-run`
4. **Verification**: `verify_migration.py`
5. **Application**: `fast_batch_migration.py --live`
6. **Maintenance**: `add_candidate_tags.py`

## ⚠️ Considerations

- **Test Mode**: Use `TEAMTAILOR_TEST_MODE=true` for testing
- **Rate Limiting**: Scripts include automatic delays
- **Backup**: Always backup before bulk migrations
- **Logs**: Review logs for errors and warnings

## 🔗 Related Links

- [API Reference](api-reference.md)
- [Migration Guide](migration-guide.md)
- [Usage Examples](usage-examples.md)
