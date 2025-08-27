.PHONY: help install dev test lint format clean run docker-build docker-run setup-dev db-migrate db-rollback docs-serve docs-build benchmark security-scan quality-report backup-data cleanup-old-data check-env generate-mock-data docker-clean docker-logs health-check dev-setup teamtailor-test teamtailor-migrate teamtailor-export

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  clean       - Clean up cache and temporary files"
	@echo "  run         - Run the development server"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"
	@echo ""
	@echo "TeamTailor specific commands:"
	@echo "  teamtailor-test    - Test TeamTailor API connection"
	@echo "  teamtailor-migrate - Run TeamTailor migration scripts"
	@echo "  teamtailor-export  - Export data to TeamTailor format"
	@echo ""
	@echo "Development utilities:"
	@echo "  setup-dev   - Complete development setup"
	@echo "  check-env   - Check environment variables"
	@echo "  health-check - Check application health"

# Install dependencies
install:
	pipenv install

# Install development dependencies
dev:
	pipenv install --dev
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg

# Run tests
test:
	pipenv run pytest tests/ -v --cov=greenhouse --cov=routes --cov-report=term-missing

# Run linting
lint:
	pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	pipenv run black --check --diff .
	pipenv run isort --check-only --diff .
	pipenv run mypy . --ignore-missing-imports

# Format code
format:
	pipenv run black .
	pipenv run isort .

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf build/
	rm -rf dist/

# Run development server
run:
	pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Migration commands
migrate-test:
	@echo "🧪 Ejecutando migración de prueba..."
	./scripts/migrate_to_teamtailor.sh

migrate-full:
	@echo "🚀 Ejecutando migración completa..."
	@read -p "¿Estás seguro de que quieres migrar TODOS los datos? (y/N): " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		./scripts/migrate_to_teamtailor.sh; \
	else \
		echo "Migración cancelada"; \
	fi

verify-migration:
	@echo "🔍 Verificando migración..."
	@curl -s -X GET "http://localhost:8000/candidates/?per_page=1" \
		-H "Authorization: Token token=$$TT_TOKEN" \
		-H "Content-Type: application/json" | jq '.total'

# Build Docker image
docker-build:
	docker-compose build

# Run with Docker
docker-run:
	docker-compose up --build

# Run pre-commit hooks
pre-commit:
	pipenv run pre-commit run --all-files

# Security check
security:
	pipenv run bandit -r . -f json -o bandit-report.json

# Type checking
type-check:
	pipenv run mypy . --ignore-missing-imports --show-error-codes

# TeamTailor specific commands
teamtailor-test:
	@echo "Testing TeamTailor connection..."
	pipenv run python -c "from teamtailor.api.client import TeamTailorClient; client = TeamTailorClient(); print('✅ TeamTailor connection successful')"

teamtailor-stats:
	@echo "Getting TeamTailor user statistics..."
	pipenv run python -c "from teamtailor.management.user_manager import UserManager; manager = UserManager(); stats = manager.get_user_statistics(); print('📊 User Statistics:', stats)"

teamtailor-export:
	@echo "Exporting TeamTailor user data..."
	pipenv run python -c "from teamtailor.management.user_manager import UserManager; manager = UserManager(); filepath = manager.export_users_report('json'); print(f'📄 Exported to: {filepath}')"

teamtailor-users:
	@echo "Getting all TeamTailor users..."
	pipenv run python -c "from teamtailor.management.user_manager import UserManager; manager = UserManager(); users = manager.get_all_users(); print(f'👥 Found {len(users)} users')"

teamtailor-create-user:
	@echo "Creating test user in TeamTailor..."
	pipenv run python -c "from teamtailor.management.user_manager import UserManager; manager = UserManager(); print('⚠️  Use the UserManager.create_user() method with proper data')"

# Legacy Greenhouse commands
legacy-greenhouse-test:
	@echo "Testing legacy Greenhouse connection..."
	pipenv run python -c "from legacy.greenhouse.client import gh_get; result = gh_get('candidates'); print('✅ Legacy Greenhouse connection successful')"

legacy-greenhouse-export:
	@echo "Exporting legacy Greenhouse data..."
	pipenv run python -c "from legacy.greenhouse.batch.candidates import CandidatesProcessor; processor = CandidatesProcessor(); print('📄 Legacy data export available')"

# Analytics and Reporting commands
analytics-dashboard:
	@echo "Getting TeamTailor analytics dashboard data..."
	pipenv run python -c "from teamtailor.analytics.reporting import TeamTailorAnalytics; analytics = TeamTailorAnalytics(); data = analytics.get_dashboard_data(); print('📊 Dashboard data:', data)"

analytics-report:
	@echo "Generating comprehensive analytics report..."
	pipenv run python -c "from teamtailor.analytics.reporting import TeamTailorAnalytics; analytics = TeamTailorAnalytics(); filepath = analytics.generate_custom_report('comprehensive', {'days': 30}); print(f'📄 Report generated: {filepath}')"

analytics-pipeline:
	@echo "Getting recruitment pipeline metrics..."
	pipenv run python -c "from teamtailor.analytics.reporting import TeamTailorAnalytics; analytics = TeamTailorAnalytics(); metrics = analytics.get_recruitment_pipeline_metrics(30); print('📈 Pipeline metrics:', metrics)"

# Notification commands
notifications-test:
	@echo "Testing notification system..."
	pipenv run python -c "from teamtailor.notifications.notification_manager import NotificationManager; manager = NotificationManager(); print('🔔 Notification system ready')"

notifications-config:
	@echo "Opening notification configuration..."
	@echo "Edit config/notifications/notification_config.json to configure notifications"

# Development utilities
setup-dev: install dev
	@echo "Development environment setup complete!"

# Database operations (for future use)
db-migrate:
	pipenv run alembic upgrade head

db-rollback:
	pipenv run alembic downgrade -1

# Documentation
docs-serve:
	cd docs && jekyll serve --livereload

docs-build:
	cd docs && jekyll build

# Performance testing
benchmark:
	pipenv run locust -f tests/load_test.py

# Security scanning
security-scan:
	pipenv run bandit -r . -f json -o bandit-report.json
	pipenv run safety check

# Snyk security scanning
snyk-install:
	@echo "Installing Snyk CLI..."
	npm install -g snyk

snyk-auth:
	@echo "Authenticating with Snyk..."
	snyk auth

snyk-test:
	@echo "Running Snyk security test..."
	snyk test --severity-threshold=high

snyk-monitor:
	@echo "Monitoring dependencies with Snyk..."
	snyk monitor

snyk-code-test:
	@echo "Running Snyk code security test..."
	snyk code test

snyk-container-test:
	@echo "Running Snyk container security test..."
	snyk container test greenhouse-api-proxy

snyk-full-scan: snyk-test snyk-code-test snyk-container-test
	@echo "Full Snyk security scan completed"

# Generate security report
security-report: security-scan snyk-full-scan
	@echo "Generating comprehensive security report..."
	@echo "Security scan completed. Check reports:"
	@echo "- Bandit: bandit-report.json"
	@echo "- Snyk: snyk-results.json"

# Comprehensive security analysis
security-analysis:
	@echo "Running comprehensive security analysis..."
	pipenv run python scripts/security/security_analysis.py

# Code quality report
quality-report:
	pipenv run radon cc . -a
	pipenv run radon mi . -a
	pipenv run radon hal . -a

# Backup and cleanup
backup-data:
	@echo "Creating backup of data directory..."
	tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz data/

cleanup-old-data:
	@echo "Cleaning up old data files..."
	find data/ -name "*.json" -mtime +30 -delete
	find data/ -name "*.csv" -mtime +30 -delete

# Development helpers
check-env:
	@echo "Checking environment variables..."
	@test -n "$(TT_TOKEN)" || (echo "TT_TOKEN not set" && exit 1)
	@test -n "$(GREENHOUSE_API_KEY)" || (echo "GREENHOUSE_API_KEY not set" && exit 1)
	@echo "Environment variables OK"

generate-mock-data:
	pipenv run python scripts/development/generate_mock_data.py

# Docker helpers
docker-clean:
	docker system prune -f
	docker volume prune -f

docker-logs:
	docker-compose logs -f app

# Monitoring
health-check:
	curl -f http://localhost:8000/health || echo "Health check failed"

# Full development setup
dev-setup: setup-dev check-env
	@echo "Full development setup complete!"
