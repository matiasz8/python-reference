# TeamTailor Data Migration Guide

This guide explains how to migrate data from TeamTailor API in the correct order
to ensure all dependencies are met.

## 🚀 Quick Start

### Prerequisites

1. **Set your TeamTailor API token:**

   ```bash
   export TT_TOKEN=your_teamtailor_api_token_here
   ```

2. **Verify the token is set:**

   ```bash
   echo $TT_TOKEN
   ```

### Option 1: Run Complete Migration (Recommended)

```bash
cd scripts/teamtailor
python3 migrate_teamtailor.py
```

### Option 2: Run Step by Step

```bash
cd scripts/teamtailor
./run_teamtailor_migration.sh
```

## 📋 Migration Order

The migration must be executed in this specific order to ensure all dependencies
are met:

### Phase 1: Foundation Data (No Dependencies)

1. **Metadata** - Sources, reasons, degrees, etc.

2. **Custom Fields** - Custom fields for candidates, jobs, applications

3. **Departments** - Company departments

4. **Offices** - Company offices

### Phase 2: Core Entities

5. **Users** - System users (depends on departments, offices)

6. **Jobs** - Job postings (depends on departments, offices, users)

7. **Candidates** - Candidate profiles (no dependencies)

### Phase 3: Application Data

8. **Applications** - Job applications (depends on candidates, jobs, users)

9. **Offers** - Job offers (depends on applications)

10. **Scorecards** - Evaluation scorecards (depends on applications)

11. **Scheduled Interviews** - Interview scheduling (depends on applications)

### Phase 4: Additional Data

12. **Demographics** - Demographic data (no dependencies)

## 🔧 Manual Migration Steps

If you prefer to run migrations manually, here are the commands for each step:

### Step 1: Metadata

```bash
# Test the connection
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/metadata/sources
```

### Step 2: Custom Fields

```bash
# Get custom fields for candidates
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/custom_fields/candidates
```

### Step 3: Departments

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/departments
```

### Step 4: Offices

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/offices
```

### Step 5: Users

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/users
```

### Step 6: Jobs

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/jobs
```

### Step 7: Candidates

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/candidates
```

### Step 8: Applications

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/applications
```

### Step 9: Offers

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/offers
```

### Step 10: Scorecards

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/scorecards
```

### Step 11: Scheduled Interviews

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/scheduled_interviews
```

### Step 12: Demographics

```bash
curl -H "Authorization: Token token=$TT_TOKEN" \
     -H "X-Api-Version: 20240904" \
     -H "Content-Type: application/vnd.api+json" \
     https://api.na.teamtailor.com/v1/demographics/question_sets
```

## 📁 Output Structure

After migration, your data will be organized as follows:

```
data/
├── json/
│   ├── candidates.json
│   ├── applications.json
│   ├── jobs.json
│   ├── users.json
│   ├── offers.json
│   ├── scorecards.json
│   ├── scheduled_interviews.json
│   ├── departments.json
│   ├── offices.json
│   ├── metadata/
│   │   ├── sources.json
│   │   ├── close_reasons.json
│   │   ├── rejection_reasons.json
│   │   ├── degrees.json
│   │   ├── disciplines.json
│   │   ├── schools.json
│   │   ├── offices.json
│   │   ├── departments.json
│   │   ├── eeoc.json
│   │   ├── user_roles.json
│   │   ├── email_templates.json
│   │   └── prospect_pools.json
│   ├── custom_fields/
│   │   ├── candidates.json
│   │   ├── jobs.json
│   │   └── applications.json
│   └── demographics/
│       ├── question_sets.json
│       ├── questions.json
│       ├── answer_options.json
│       └── answers.json
```

## ⚠️ Important Notes

### Rate Limiting

- TeamTailor API has rate limits

- The migration script includes automatic retry logic

- If you encounter rate limit errors, wait a few minutes and retry

### Dependencies

- **Applications** depend on **Candidates**, **Jobs**, and **Users**

- **Offers** depend on **Applications**

- **Scorecards** depend on **Applications**

- **Scheduled Interviews** depend on **Applications**

- **Users** depend on **Departments** and **Offices**

- **Jobs** depend on **Departments**, **Offices**, and **Users**

### Error Handling

- The migration script will continue even if some endpoints fail

- Check the console output for any error messages

- Failed endpoints will be logged with details

### Data Validation

- After migration, verify that all expected files are created

- Check file sizes to ensure data was downloaded completely

- Validate JSON structure for any malformed data

## 🔍 Troubleshooting

### Common Issues

1. **Authentication Error (401)**

   - Verify your TT_TOKEN is correct
   - Check if the token has expired
   - Ensure the token has the necessary permissions

2. **Rate Limit Error (429)**

   - Wait a few minutes before retrying
   - The script includes automatic retry logic
   - Consider running during off-peak hours

3. **Network Error**

   - Check your internet connection
   - Verify you can reach `https://api.na.teamtailor.com`
   - Try running the migration again

4. **Permission Error**

   - Ensure your token has access to all endpoints
   - Contact your TeamTailor administrator if needed

### Debug Mode

To run with more verbose output:

```bash
# Set debug environment variable
export DEBUG=1

# Run migration
cd scripts/teamtailor
python3 migrate_teamtailor.py
```

## 📊 Migration Monitoring

The migration script provides real-time feedback:

- ✅ Success indicators for each step

- ❌ Error messages with details

- 📊 Progress counters

- ⏱️ Timing information

- 📈 Summary statistics

## 🎯 Next Steps

After successful migration:

1. **Verify Data Integrity**

   - Check all JSON files are valid
   - Verify file sizes are reasonable
   - Test data access

2. **Data Processing**

   - Use the exported data for analysis
   - Import into other systems
   - Create reports and dashboards

3. **Automation**

   - Set up scheduled migrations
   - Implement incremental updates
   - Monitor for changes

## 📞 Support

If you encounter issues:

1. Check this guide for common solutions

2. Review the console output for error details

3. Verify your API token and permissions

4. Contact your TeamTailor administrator if needed

## 📚 Related Documentation

- [TeamTailor API Endpoints](./TEAMTAILOR_API_ENDPOINTS.md)

  - Complete API reference

- [Scripts Documentation](./scripts/teamtailor/README.md)

  - Detailed script usage

- [Project Status](./NORMALIZATION_SUMMARY.md) - Current migration status

---

**Last updated:** December 2024
**API Version:** 20240904
**Base URL:** `https://api.na.teamtailor.com/v1`
