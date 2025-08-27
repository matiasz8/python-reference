# Step-by-Step Migration Guide: Greenhouse → TeamTailor

This guide will walk you through the complete process of migrating data
from Greenhouse to TeamTailor.

## 📋 Prerequisites

### 1. Environment Setup

```bash
# Configure environment variables
export TT_TOKEN="your_teamtailor_token"
export TT_BASE_URL="https://api.na.teamtailor.com/v1"
export TT_API_VERSION="20240904"

# Verify configuration
echo $TT_TOKEN
```

### 2. Verify Greenhouse Backup

```bash
# Verify export file exists
ls -la data/json/export_teamtailor.json

# Verify backup content
jq '.candidates | length' data/json/export_teamtailor.json
```

### 3. Install Dependencies

```bash
# Install project dependencies
pipenv install

# Verify jq is installed (for processing JSON)
which jq
```

---

## 🚀 Step 1: Start the Server

```bash
# Start FastAPI server
make run

# Or alternatively:
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verify the server is working:**

```bash
curl http://localhost:8000/
```

**Expected response:**

```json
{
  "message": "Welcome to the Greenhouse API Proxy!",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

---

## 🚀 Step 2: Verify TeamTailor Connection

```bash
# Test basic connection
curl -X GET "http://localhost:8000/candidates/" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

**If there are authentication errors:**

- Verify that `TT_TOKEN` is configured correctly
- Verify that the token has permissions in TeamTailor
- Verify that the API version is correct

---

## 🚀 Step 3: Create Prospect Pools

### 3.1 Create Engineering Pool

```bash
curl -X POST "http://localhost:8000/prospects/pools" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Engineering Prospects",
    "description": "Software engineering candidates from Greenhouse",
    "color": "#0076D7"
  }'
```

### 3.2 Create Design Pool

```bash
curl -X POST "http://localhost:8000/prospects/pools" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Design Prospects",
    "description": "UX/UI design candidates from Greenhouse",
    "color": "#FF6B35"
  }'
```

### 3.3 Create Product Pool

```bash
curl -X POST "http://localhost:8000/prospects/pools" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Prospects",
    "description": "Product management candidates from Greenhouse",
    "color": "#4CAF50"
  }'
```

### 3.4 Verify Created Pools

```bash
curl -X GET "http://localhost:8000/prospects/pools" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🚀 Step 4: Test Migration

### 4.1 Migrate Small Sample

```bash
# Migrate only 5 candidates for testing
curl -X POST "http://localhost:8000/candidates/migrate/greenhouse?limit=5" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

**Expected response:**

```json
{
  "created": 4,
  "failed": 1,
  "errors": [
    {
      "index": 2,
      "error": "Email already exists",
      "data": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
      }
    }
  ],
  "candidates": [...]
}
```

### 4.2 Verify Migrated Candidates

```bash
# List migrated candidates
curl -X GET "http://localhost:8000/candidates/?per_page=10" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

### 4.3 Review Errors (if any)

If there are errors, check:

- **Duplicate email**: The candidate already exists in TeamTailor
- **Missing data**: Required fields not present
- **Rate limiting**: Wait and retry

---

## 🚀 Step 5: Complete Migration

### 5.1 Migrate All Candidates

```bash
# Migrate all candidates (no limit)
curl -X POST "http://localhost:8000/candidates/migrate/greenhouse" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

**⚠️ Note:** This process can take time depending on the number of candidates.

### 5.2 Monitor Progress

```bash
# Check progress every 100 candidates
curl -X GET "http://localhost:8000/candidates/?per_page=1" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" | jq '.total'
```

---

## 🚀 Step 6: Organize into Prospect Pools

### 6.1 Migrate to Engineering Prospects

```bash
curl -X POST "http://localhost:8000/prospects/migrate/greenhouse?pool_name=Engineering%20Prospects&limit=100" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

### 6.2 Migrate to Design Prospects

```bash
curl -X POST "http://localhost:8000/prospects/migrate/greenhouse?pool_name=Design%20Prospects&limit=50" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

### 6.3 Migrate to Product Prospects

```bash
curl -X POST "http://localhost:8000/prospects/migrate/greenhouse?pool_name=Product%20Prospects&limit=30" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🚀 Step 7: Final Verification

### 7.1 Verify Totals

```bash
# Count total candidates
curl -X GET "http://localhost:8000/candidates/?per_page=1" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" | jq '.total'

# Verify prospect pools
curl -X GET "http://localhost:8000/prospects/pools" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" | jq '.pools[] | "\(.name): \(.candidate_count) candidates"'
```

### 7.2 Verify External IDs

```bash
# Search candidates with external IDs
curl -X GET "http://localhost:8000/candidates/?search=gh_cand" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" | jq '.candidates | length'
```

### 7.3 Verify Specific Data

```bash
# Search for specific candidate
curl -X GET "http://localhost:8000/candidates/?search=john" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"

# Verify tags
curl -X GET "http://localhost:8000/candidates/?tags=senior" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 🚀 Step 8: Using the Automated Script

### 8.1 Run Complete Script

```bash
# Run automated migration
./scripts/migrate_to_teamtailor.sh
```

### 8.2 Use Makefile

```bash
# Test migration
make migrate-test

# Complete migration
make migrate-full

# Verify migration
make verify-migration
```

---

## 🔍 Verification in TeamTailor Dashboard

### 1. Verify Candidates

- Go to TeamTailor Dashboard
- Navigate to "Candidates"
- Verify that candidates are present
- Verify that external IDs are correct

### 2. Verify Prospect Pools

- Go to "Prospect Pools"
- Verify that pools are created
- Verify that candidates are assigned correctly

### 3. Verify Data

- Review emails and phones
- Verify tags and custom fields
- Verify creation dates

---

## 🚨 Troubleshooting

### Error: "TT_TOKEN is not configured"

```bash
export TT_TOKEN="your_token_here"
```

### Error: "FastAPI server is not running"

```bash
make run
```

### Error: "Email already exists"

- Candidates already exist in TeamTailor
- Use `external_id` to identify duplicates
- Consider using PATCH instead of POST

### Error: "Rate limit exceeded"

- Wait a few minutes
- Reduce number of requests per minute
- Use the automatic retry of the client

### Error: "Invalid API version"

```bash
export TT_API_VERSION="20240904"
```

---

## 📊 Post-Migration

### 1. Clean Temporary Data

```bash
# Clean temporary files
rm -f /tmp/engineering_pool_id
rm -f /tmp/design_pool_id
rm -f /tmp/product_pool_id
```

### 2. Generate Migration Report

```bash
# Create migration report
curl -X GET "http://localhost:8000/candidates/?per_page=1" \
  -H "Authorization: Token token=$TT_TOKEN" \
  -H "Content-Type: application/json" > migration_report.json
```

### 3. Configure Workflows

- Configure stages in TeamTailor
- Configure email templates
- Configure scorecards
- Configure interviews

---

## ✅ Migration Checklist

- [ ] Environment variables configured
- [ ] FastAPI server running
- [ ] TeamTailor connection verified
- [ ] Prospect pools created
- [ ] Test migration successful
- [ ] Complete migration executed
- [ ] Candidates organized in pools
- [ ] External IDs verified
- [ ] Data verified in dashboard
- [ ] Migration report generated

---

## 🎉 Migration Completed

Once the migration is completed, you will have:

✅ **Candidates migrated** from Greenhouse to TeamTailor

✅ **Prospect pools organized** by categories

✅ **External IDs preserved** for reference

✅ **Complete data** including emails, phones, tags

✅ **Custom fields** migrated correctly

**Next steps:**

1. Configure workflows in TeamTailor
2. Import applications if necessary
3. Configure notifications
4. Train the team on the new system
