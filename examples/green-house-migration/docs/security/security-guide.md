# Security Guide - Greenhouse to TeamTailor Migration

## Overview

This guide covers security best practices and tools for the Greenhouse to
TeamTailor migration project. We use multiple security tools to ensure the
safety of our application and data.

## Security Tools

### 1. Snyk - Vulnerability Management

Snyk is our primary security tool for:

- **Dependency vulnerability scanning**

- **Code security analysis**

- **Container security scanning**

- **Infrastructure as Code security**

#### Installation

```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate with Snyk
snyk auth
```

#### Usage

```bash
# Test dependencies for vulnerabilities
snyk test

# Test code for security issues
snyk code test

# Test Docker containers
snyk container test <image-name>

# Monitor dependencies
snyk monitor

# Full security scan
make snyk-full-scan
```

### 2. Bandit - Python Security Linting

Bandit scans Python code for common security issues:

```bash
# Run Bandit analysis
pipenv run bandit -r . -f json -o bandit-report.json

# Run with specific configuration
pipenv run bandit -r . -c .bandit
```

### 3. Safety - Dependency Vulnerability Check

Safety checks Python dependencies against known vulnerabilities:

```bash
# Check dependencies
pipenv run safety check

# Check with JSON output
pipenv run safety check --json --output safety-report.json
```

## Security Workflow

### Daily Development

1. **Pre-commit checks**: Security tools run automatically

2. **Manual testing**: Run security scans before commits

3. **CI/CD integration**: Automated security checks in pipeline

### Weekly Security Review

1. **Dependency updates**: Review and update vulnerable dependencies

2. **Security reports**: Review generated security reports

3. **Policy updates**: Update security policies as needed

### Monthly Security Audit

1. **Comprehensive scan**: Run full security analysis

2. **Penetration testing**: Manual security testing

3. **Policy review**: Review and update security policies

## TeamTailor-Specific Security

### API Token Security

```python
# ✅ Good: Use environment variables
token = os.getenv("TT_TOKEN")

# ❌ Bad: Hardcode tokens
token = "your_token_here"
```

### Rate Limiting

```python
# ✅ Good: Implement proper rate limiting
import time

def make_api_call():
    response = requests.get(url, headers=headers)
    time.sleep(0.2) # 200ms delay
    return response
```

### Error Handling

```python
# ✅ Good: Proper error handling
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"API call failed: {e}")
    raise
```

## Security Configuration

### Environment Variables

```bash
# Required security variables
TT_TOKEN=your_teamtailor_token
GREENHOUSE_API_KEY=your_greenhouse_key
SECRET_KEY=your_secret_key_minimum_32_chars

# Optional security variables
DEBUG=False
LOG_LEVEL=INFO
```

### File Permissions

```bash
# Set secure permissions for sensitive files
chmod 600 .env
chmod 600 *.pem
chmod 600 *.key
```

### Docker Security

```dockerfile
# Use non-root user
USER app

# Copy only necessary files
COPY --chown=app:app app/ /app/

# Use specific base image versions
FROM python:3.11-slim
```

## Vulnerability Management

### Severity Levels

- **High**: Fix immediately, block deployment

- **Medium**: Fix within 1 week

- **Low**: Fix within 1 month

### False Positives

To ignore false positives, update `.snyk`:

```yaml
ignore:
  "SNYK-PYTHON-REQUESTS-1061915":
    - "tests/fixtures/*":
        reason: "Test data only, not used in production"
        expires: 2024-12-31T00:00:00.000Z
```

## Security Monitoring

### Prometheus Metrics

Monitor security-related metrics:

```python
# Security metrics
SECURITY_SCAN_FAILURES = Counter(
    'security_scan_failures_total',
    'Total security scan failures'
)

API_SECURITY_VIOLATIONS = Counter(
    'api_security_violations_total',
    'Total API security violations'
)
```

### Grafana Dashboards

Create security dashboards to monitor:

- Failed security scans

- API security violations

- Dependency vulnerabilities

- Rate limiting violations

## Incident Response

### Security Incident Process

1. **Detection**: Automated tools detect security issues

2. **Assessment**: Evaluate severity and impact

3. **Containment**: Isolate affected systems

4. **Eradication**: Remove security threats

5. **Recovery**: Restore normal operations

6. **Lessons Learned**: Update security policies

### Contact Information

- **Security Team**: `security@company.com`

- **Emergency**: +1-XXX-XXX-XXXX

- **Snyk Support**: `https://support.snyk.io`

## Compliance

### GDPR Compliance

- **Data Minimization**: Only collect necessary data

- **Consent Management**: Proper consent handling

- **Data Portability**: Export capabilities

- **Right to be Forgotten**: Data deletion capabilities

### SOC 2 Compliance

- **Access Control**: Proper authentication and authorization

- **Change Management**: Document all changes

- **Security Monitoring**: Continuous security monitoring

- **Incident Response**: Documented incident response procedures

## Best Practices

### Code Security

1. **Input Validation**: Validate all inputs

2. **Output Encoding**: Encode outputs to prevent XSS

3. **Authentication**: Implement proper authentication

4. **Authorization**: Implement proper authorization

5. **Session Management**: Secure session handling

### API Security

1. **Rate Limiting**: Implement proper rate limiting

2. **Authentication**: Use secure authentication methods

3. **Authorization**: Implement proper authorization

4. **Input Validation**: Validate all API inputs

5. **Error Handling**: Don't expose sensitive information in errors

### Data Security

1. **Encryption**: Encrypt sensitive data at rest and in transit

2. **Access Control**: Implement proper access controls

3. **Audit Logging**: Log all access to sensitive data

4. **Data Classification**: Classify data by sensitivity

5. **Data Retention**: Implement proper data retention policies

## Tools and Commands

### Quick Security Check

```bash
# Run all security tools
make security-analysis

# Run specific tools
make snyk-test
make snyk-code-test
pipenv run bandit -r .
pipenv run safety check
```

### Security Report Generation

```bash
# Generate comprehensive security report
make security-report

# View security reports
ls -la security-reports/
cat security-reports/security-summary-*.json
```

### Continuous Monitoring

```bash
# Set up Snyk monitoring
snyk monitor

# Check for new vulnerabilities
snyk test --severity-threshold=high
```

## Resources

- [Snyk Documentation](https://docs.snyk.io/)

- [Bandit Documentation](https://bandit.readthedocs.io/)

- [Safety Documentation](https://pyup.io/safety/)

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

- [TeamTailor Security](https://developer.teamtailor.com/security)
