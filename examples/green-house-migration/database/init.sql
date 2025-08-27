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
