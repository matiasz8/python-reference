# Single stage Dockerfile for Greenhouse API Proxy
FROM python:3.12.7-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8000

# Install system dependencies
RUN apk add --no-cache-dir \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    curl \
    git

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Create non-root user
RUN addgroup -g 1000 appuser && adduser -D -s /bin/sh -u 1000 -G appuser appuser

# Set work directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --system

# Copy application code
COPY . .

# Create data directory and set permissions
RUN mkdir -p data/json data/csv data/logs && chown -R appuser:appuser data

# Change ownership to appuser
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
