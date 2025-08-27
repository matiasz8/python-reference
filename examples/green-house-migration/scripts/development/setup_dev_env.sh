#!/bin/bash

echo "🚀 Setting up development environment for Greenhouse to TeamTailor migration..."

# Check if Python 3.9+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is installed"
else
    echo "❌ Python 3.9+ is required. Current version: $python_version"
    exit 1
fi

# Install pipenv if not installed
if ! command -v pipenv &> /dev/null; then
    echo "📦 Installing pipenv..."
    pip3 install pipenv
fi

# Install dependencies
echo "📦 Installing project dependencies..."
pipenv install --dev

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pipenv run pre-commit install
pipenv run pre-commit install --hook-type commit-msg

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys:"
    echo "   - TT_TOKEN (TeamTailor API token)"
    echo "   - GREENHOUSE_API_KEY (Greenhouse API key)"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data/{json,csv,logs}
mkdir -p logs
mkdir -p tests/{unit,integration,fixtures,utils}
mkdir -p monitoring/{grafana/{dashboards,datasources},prometheus}
mkdir -p security
mkdir -p cache
mkdir -p database
mkdir -p docs/{deployment,development,architecture}

# Create monitoring configuration files
echo "📊 Setting up monitoring configuration..."
cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"
  # - "second_rules.yml"

scrape_configs:
  - job_name: 'greenhouse-api-proxy'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'teamtailor-api'
    static_configs:
      - targets: ['teamtailor-mock:1080']
    scrape_interval: 10s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

# Create TeamTailor mock configuration
cat > monitoring/teamtailor-mock-config.json << 'EOF'
[
  {
    "httpRequest": {
      "method": "GET",
      "path": "/v1/candidates"
    },
    "httpResponse": {
      "statusCode": 200,
      "headers": {
        "Content-Type": ["application/vnd.api+json"]
      },
      "body": {
        "data": [
          {
            "id": "1",
            "type": "candidates",
            "attributes": {
              "first-name": "John",
              "last-name": "Doe",
              "email": "john.doe@example.com"
            }
          }
        ]
      }
    }
  }
]
EOF

# Create database initialization script
cat > database/init.sql << 'EOF'
-- Database initialization for Greenhouse to TeamTailor migration

CREATE TABLE IF NOT EXISTS migration_logs (
    id SERIAL PRIMARY KEY,
    operation VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    external_id VARCHAR(255),
    teamtailor_id VARCHAR(255),
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS api_calls (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_migration_logs_operation ON migration_logs(operation);
CREATE INDEX idx_migration_logs_entity_type ON migration_logs(entity_type);
CREATE INDEX idx_migration_logs_status ON migration_logs(status);
CREATE INDEX idx_api_calls_endpoint ON api_calls(endpoint);
CREATE INDEX idx_api_calls_created_at ON api_calls(created_at);
EOF

# Create Grafana datasource configuration
mkdir -p monitoring/grafana/datasources
cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

# Create Grafana dashboard configuration
mkdir -p monitoring/grafana/dashboards
cat > monitoring/grafana/dashboards/dashboard.yml << 'EOF'
apiVersion: 1

providers:
  - name: 'TeamTailor Migration'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
EOF

echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Edit .env file with your API keys:"
echo "      - TT_TOKEN (TeamTailor API token)"
echo "      - GREENHOUSE_API_KEY (Greenhouse API key)"
echo ""
echo "   2. Test TeamTailor connection:"
echo "      make teamtailor-test"
echo ""
echo "   3. Start development server:"
echo "      make run"
echo ""
echo "   4. Start with Docker (includes monitoring):"
echo "      docker-compose up --build"
echo ""
echo "   5. Access services:"
echo "      - API Documentation: http://localhost:8000/docs"
echo "      - Grafana: http://localhost:3000 (admin/admin)"
echo "      - Prometheus: http://localhost:9090"
echo "      - TeamTailor Mock: http://localhost:1080"
echo ""
echo "   6. Run TeamTailor migration:"
echo "      make teamtailor-migrate"
