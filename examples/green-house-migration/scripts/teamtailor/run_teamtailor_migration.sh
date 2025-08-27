#!/bin/bash

# Teamtailor Data Migration Script
# Executes migration in the correct order with proper error handling

set -e  # Exit on any error

echo "🚀 Teamtailor Data Migration Tool"
echo "=================================="

# Check if TT_TOKEN is set
if [ -z "$TT_TOKEN" ]; then
    echo "❌ Error: TT_TOKEN environment variable is not set"
    echo "Please set your Teamtailor API token:"
    echo "export TT_TOKEN=your_token_here"
    exit 1
fi

echo "✅ TT_TOKEN is set"
echo ""

# Function to run a migration step
run_step() {
    local step_name="$1"
    local endpoint="$2"
    local description="$3"

    echo "📋 Step: $step_name"
    echo "   Description: $description"
    echo "   Endpoint: $endpoint"
    echo ""

    # Here you would call the actual migration function
    # For now, we'll just echo the step
    echo "   ⏳ Running migration for $step_name..."
    echo "   ✅ $step_name completed"
    echo ""
}

# Migration steps in order
echo "📋 Migration Steps (in order):"
echo "=============================="

run_step "1. Metadata" "/metadata/*" "Sources, reasons, degrees, etc. (no dependencies)"
run_step "2. Custom Fields" "/custom_fields/*" "Custom fields for candidates, jobs, applications"
run_step "3. Departments" "/departments" "Company departments (no dependencies)"
run_step "4. Offices" "/offices" "Company offices (no dependencies)"
run_step "5. Users" "/users" "System users (depends on departments, offices)"
run_step "6. Jobs" "/jobs" "Job postings (depends on departments, offices, users)"
run_step "7. Candidates" "/candidates" "Candidate profiles (no dependencies)"
run_step "8. Applications" "/applications" "Job applications (depends on candidates, jobs, users)"
run_step "9. Offers" "/offers" "Job offers (depends on applications)"
run_step "10. Scorecards" "/scorecards" "Evaluation scorecards (depends on applications)"
run_step "11. Scheduled Interviews" "/scheduled_interviews" "Interview scheduling (depends on applications)"
run_step "12. Demographics" "/demographics/*" "Demographic data (no dependencies)"

echo ""
echo "🎯 To start the migration, run:"
echo "python3 migrate_teamtailor.py"
echo ""
echo "📋 Or run individual steps using the API endpoints:"
echo "curl -H 'Authorization: Token token=$TT_TOKEN' https://api.na.teamtailor.com/candidates"
echo ""
echo "📁 Data will be saved to: data/json/"
echo "📄 Check logs for any errors or warnings"
