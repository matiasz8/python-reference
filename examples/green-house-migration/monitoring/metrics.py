"""Prometheus metrics for the Greenhouse to TeamTailor migration."""

from prometheus_client import Counter, Gauge, Histogram, generate_latest

# Request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

# Greenhouse API metrics
GREENHOUSE_API_CALLS_TOTAL = Counter(
    "greenhouse_api_calls_total",
    "Total Greenhouse API calls",
    ["endpoint", "status"],
)

GREENHOUSE_API_CALL_DURATION = Histogram(
    "greenhouse_api_call_duration_seconds",
    "Greenhouse API call duration in seconds",
    ["endpoint"],
)

# TeamTailor API metrics
TEAMTAILOR_API_CALLS_TOTAL = Counter(
    "teamtailor_api_calls_total",
    "Total TeamTailor API calls",
    ["endpoint", "method", "status"],
)

TEAMTAILOR_API_CALL_DURATION = Histogram(
    "teamtailor_api_call_duration_seconds",
    "TeamTailor API call duration in seconds",
    ["endpoint", "method"],
)

# Migration metrics
MIGRATION_OPERATIONS_TOTAL = Counter(
    "migration_operations_total",
    "Total migration operations",
    ["entity_type", "operation", "status"],
)

MIGRATION_DURATION = Histogram(
    "migration_duration_seconds",
    "Migration operation duration in seconds",
    ["entity_type", "operation"],
)

# Export metrics
EXPORT_OPERATIONS_TOTAL = Counter(
    "export_operations_total",
    "Total export operations",
    ["entity_type", "status"],
)

EXPORT_DURATION = Histogram(
    "export_duration_seconds",
    "Export operation duration in seconds",
    ["entity_type"],
)

# Data metrics
DATA_SIZE_BYTES = Gauge(
    "data_size_bytes",
    "Size of exported data in bytes",
    ["entity_type", "format"],
)

RECORDS_PROCESSED = Counter(
    "records_processed_total",
    "Total records processed",
    ["entity_type", "operation"],
)

# TeamTailor specific metrics
TEAMTAILOR_ENTITIES_CREATED = Counter(
    "teamtailorentities_created_total",
    "Total entities created in TeamTailor",
    ["entity_type", "status"],
)

TEAMTAILOR_ENTITIES_UPDATED = Counter(
    "teamtailorentities_updated_total",
    "Total entities updated in TeamTailor",
    ["entity_type", "status"],
)

TEAMTAILOR_RATE_LIMIT_HITS = Counter(
    "teamtailor_rate_limit_hits_total",
    "Total TeamTailor rate limit hits",
    ["endpoint"],
)

TEAMTAILOR_API_ERRORS = Counter(
    "teamtailor_apierrors_total",
    "Total TeamTailor API errors",
    ["endpoint", "error_type"],
)

# Cache metrics
CACHE_HITS = Counter("cache_hits_total", "Total cache hits", ["cache_type"])

CACHE_MISSES = Counter("cache_misses_total", "Total cache misses", ["cache_type"])

CACHE_SIZE = Gauge("cache_size_items", "Number of items in cache", ["cache_type"])


def get_metrics() -> str:
    """Get Prometheus metrics."""
    return generate_latest()


def record_request(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics."""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, _status=status).inc()
    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)


def record_greenhouse_api_call(endpoint: str, status: str, duration: float):
    """Record Greenhouse API call metrics."""
    GREENHOUSE_API_CALLS_TOTAL.labels(endpoint=endpoint, _status=status).inc()
    GREENHOUSE_API_CALL_DURATION.labels(endpoint=endpoint).observe(duration)


def record_teamtailor_api_call(
    endpoint: str, method: str, status: str, duration: float
):
    """Record TeamTailor API call metrics."""
    TEAMTAILOR_API_CALLS_TOTAL.labels(
        endpoint=endpoint, method=method, _status=status
    ).inc()
    TEAMTAILOR_API_CALL_DURATION.labels(endpoint=endpoint, method=method).observe(
        duration
    )


def record_migration(
    entity_type: str,
    operation: str,
    status: str,
    duration: float,
    records: int,
):
    """Record migration operation metrics."""
    MIGRATION_OPERATIONS_TOTAL.labels(
        entity_type=entity_type, operation=operation, _status=status
    ).inc()
    MIGRATION_DURATION.labels(entity_type=entity_type, operation=operation).observe(
        duration
    )
    RECORDS_PROCESSED.labels(entity_type=entity_type, operation=operation).inc(records)


def recordexport(entity_type: str, status: str, duration: float, records: int):
    """Record export operation metrics."""
    EXPORT_OPERATIONS_TOTAL.labels(entity_type=entity_type, _status=status).inc()
    EXPORT_DURATION.labels(entity_type=entity_type).observe(duration)
    RECORDS_PROCESSED.labels(entity_type=entity_type, operation="export").inc(records)


def record_data_size(entity_type: str, format_type: str, size_bytes: int):
    """Record data size metrics."""
    DATA_SIZE_BYTES.labels(entity_type=entity_type, format=format_type).set(size_bytes)


def record_teamtailorentity_created(entity_type: str, status: str):
    """Record TeamTailor entity creation."""
    TEAMTAILOR_ENTITIES_CREATED.labels(entity_type=entity_type, _status=status).inc()


def record_teamtailorentity_updated(entity_type: str, status: str):
    """Record TeamTailor entity update."""
    TEAMTAILOR_ENTITIES_UPDATED.labels(entity_type=entity_type, _status=status).inc()


def record_teamtailor_rate_limit(endpoint: str):
    """Record TeamTailor rate limit hit."""
    TEAMTAILOR_RATE_LIMIT_HITS.labels(endpoint=endpoint).inc()


def record_teamtailorerror(endpoint: str, error_type: str):
    """Record TeamTailor API error."""
    TEAMTAILOR_API_ERRORS.labels(endpoint=endpoint, error_type=error_type).inc()


def record_cache_hit(cache_type: str):
    """Record cache hit."""
    CACHE_HITS.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type: str):
    """Record cache miss."""
    CACHE_MISSES.labels(cache_type=cache_type).inc()


def record_cache_size(cache_type: str, size: int):
    """Record cache size."""
    CACHE_SIZE.labels(cache_type=cache_type).set(size)
