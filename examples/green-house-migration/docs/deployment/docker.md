# Docker Deployment Guide - Greenhouse to TeamTailor Migration

## Overview

This guide covers deploying the Greenhouse to TeamTailor migration service using
Docker and Docker Compose. The application acts as a bridge between Greenhouse
(data source) and TeamTailor (target system).

## Prerequisites

- Docker Engine 20.10+

- Docker Compose 2.0+

- At least 4GB RAM available (for full monitoring stack)

- TeamTailor API token

- Greenhouse API key

## Quick Start

1. Clone the repository

2. Copy `.env.example` to `.env` and configure your API keys:

   ```bash
   cp .env.example .env
   # Edit .env with your TT_TOKEN and GREENHOUSE_API_KEY
   ```

3. Run the application:

   ```bash
   docker-compose up --build
   ```

## Production Deployment

### Using Docker Compose

```bash
# Production build with monitoring
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# With custom environment file
docker-compose --env-file .env.production up -d

# With monitoring stack
docker-compose --profile monitoring up -d
```

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml greenhouse-teamtailor
```

## Configuration

### Environment Variables

| Variable             | Description             | Default                            | Required |
| -------------------- | ----------------------- | ---------------------------------- | -------- |
| `TT_TOKEN`           | TeamTailor API token    | -                                  | ✅       |
| `TT_BASE_URL`        | TeamTailor API base URL | `https://api.na.teamtailor.com/v1` | ✅       |
| `TT_API_VERSION`     | TeamTailor API version  | `20240904`                         | ✅       |
| `GREENHOUSE_API_KEY` | Greenhouse API key      | -                                  | ✅       |
| `GREENHOUSE_API_URL` | Greenhouse API URL      | `https://harvest.greenhouse.io/v1` | ✅       |
| `DEBUG`              | Debug mode              | `False`                            | ❌       |
| `LOG_LEVEL`          | Logging level           | `INFO`                             | ❌       |

### Volumes

- `./data:/app/data` - Persistent data storage

- `./logs:/app/logs` - Application logs

- `postgres_data:/var/lib/postgresql/data` - Database data

- `redis_data:/data` - Redis cache data

- `prometheus_data:/prometheus` - Prometheus metrics

- `grafana_data:/var/lib/grafana` - Grafana dashboards

## Services

### Core Services

- **app**: Main application with FastAPI

- **redis**: Caching for TeamTailor API responses

- **postgres**: Database for migration logs and metadata

### Monitoring Services

- **prometheus**: Metrics collection

- **grafana**: Dashboards and visualization

- **elasticsearch**: Log aggregation (optional)

- **kibana**: Log analysis (optional)

### Development Services

- **teamtailor-mock**: Mock TeamTailor API for testing

## Monitoring

### Health Checks

The application includes built-in health checks:

```bash
# Check application health
curl http://localhost:8000/health

# Check TeamTailor API health
curl http://localhost:8000/health/teamtailor

# Check Docker container health
docker-compose ps
```

### Metrics

Access Prometheus metrics:

```bash
# Application metrics
curl http://localhost:8000/metrics

# Prometheus UI
open http://localhost:9090
```

### Dashboards

Access Grafana dashboards:

```bash
# Grafana UI
open http://localhost:3000
# Default credentials: admin/admin
```

## TeamTailor Migration Workflow

### 1. Export Data from Greenhouse

```bash
# Export all entities
curl -X POST "http://localhost:8000/export/all"

# Export specific entities
curl -X POST "http://localhost:8000/export/candidates"
curl -X POST "http://localhost:8000/export/jobs"
curl -X POST "http://localhost:8000/export/applications"
```

### 2. Convert to TeamTailor Format

```bash
# Convert exported data to TeamTailor format
curl -X POST "http://localhost:8000/team_tailor_export"
```

### 3. Monitor Migration Progress

```bash
# Check migration logs
docker-compose logs -f app

# View metrics in Grafana
open http://localhost:3000
```

## Troubleshooting

### Common Issues

1. **TeamTailor API Connection Failed**

   ```bash
   # Check token validity
   curl -H "Authorization: Token token=YOUR_TOKEN" \
        https://api.na.teamtailor.com/v1/candidates

   # Check logs
   docker-compose logs app | grep -i teamtailor
   ```

2. **Greenhouse API Connection Failed**

   ```bash
   # Check API key format
   echo $GREENHOUSE_API_KEY | grep ":"

   # Check logs
   docker-compose logs app | grep -i greenhouse
   ```

3. **Rate Limiting Issues**

   ```bash
   # Check rate limit metrics
   curl http://localhost:8000/metrics | grep rate_limit

   # Adjust rate limiting in .env
   TT_RATE_LIMIT_DELAY=0.5
   ```

4. **Database Connection Issues**

   ```bash
   # Check database logs
   docker-compose logs postgres

   # Restart database
   docker-compose restart postgres
   ```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Set debug mode
export DEBUG=true
docker-compose up

# Or edit .env file
echo "DEBUG=true" >> .env
docker-compose up
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f redis

# View logs with timestamps
docker-compose logs -f --timestamps app
```

## Performance Tuning

### Memory Optimization

```bash
# Limit memory usage
docker-compose up -d --scale app=2
```

### Rate Limiting

```bash
# Adjust TeamTailor rate limiting
TT_RATE_LIMIT_DELAY=0.3  # 300ms between requests
TT_MAX_RETRIES=5
```

### Caching

```bash
# Enable Redis caching
REDIS_URL=redis://redis:6379/0
CACHE_ENABLED=true
```

## Security

### API Token Management

```bash
# Use Docker secrets (production)
echo "your_teamtailor_token" | docker secret create tt_token -

# Use environment variables (development)
export TT_TOKEN="your_token"
```

### Network Security

```bash
# Create custom network
docker network create greenhouse-network

# Use internal communication
docker-compose up --network greenhouse-network
```

## Backup and Recovery

### Data Backup

```bash
# Backup data directory
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/

# Backup database
docker-compose exec postgres pg_dump -U dev greenhouse_dev > backup.sql
```

### Recovery

```bash
# Restore data
tar -xzf backup_YYYYMMDD_HHMMSS.tar.gz

# Restore database
docker-compose exec -T postgres psql -U dev greenhouse_dev < backup.sql
```

## Scaling

### Horizontal Scaling

```bash
# Scale application instances
docker-compose up -d --scale app=3

# Use load balancer
docker-compose up -d nginx
```

### Vertical Scaling

```bash
# Increase memory limits
docker-compose up -d --memory=2g app
```

## Maintenance

### Regular Tasks

```bash
# Clean up old data
make cleanup-old-data

# Update dependencies
docker-compose build --no-cache

# Restart services
docker-compose restart
```

### Monitoring Maintenance

```bash
# Check disk usage
docker system df

# Clean up unused resources
docker system prune -f

# Update monitoring stack
docker-compose pull prometheus grafana
```
