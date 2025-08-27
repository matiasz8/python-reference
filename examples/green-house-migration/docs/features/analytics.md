# TeamTailor Analytics & Reporting

## Overview

The TeamTailor Analytics system provides comprehensive insights into your
recruitment operations, user activity, and system performance.

## Features

### 📊 **Recruitment Pipeline Analytics**

- **Application tracking** by status and job

- **Conversion rates** through the pipeline

- **Time-to-hire** metrics

- **Source effectiveness** analysis

### 👥 **User Activity Analytics**

- **User engagement** metrics

- **Activity patterns** and trends

- **Role-based** analytics

- **Performance** tracking

### ⚡ **System Performance Metrics**

- **API response times**

- **Rate limiting** statistics

- **Error rates** and monitoring

- **Data processing** metrics

## Usage

### Command Line Interface

```bash
# Get dashboard data
make analytics-dashboard

# Generate comprehensive report
make analytics-report

# Get pipeline metrics
make analytics-pipeline
```

### Python API

```python
from teamtailor.analytics.reporting import TeamTailorAnalytics

# Initialize analytics
analytics = TeamTailorAnalytics()

# Get recruitment pipeline metrics
pipeline_metrics = analytics.get_recruitment_pipeline_metrics(days=30)

# Get user activity analytics
user_analytics = analytics.get_user_activity_analytics(days=30)

# Generate custom report
report_path = analytics.generate_custom_report('comprehensive', {'days': 30})

# Export to Excel
excel_path = analytics.export_to_excel(data, 'report_name')
```

## Report Types

### 1. **Recruitment Pipeline Report**

- Applications by status

- Top performing jobs

- Conversion rates

- Time-to-hire analysis

### 2. **User Activity Report**

- User engagement scores

- Activity patterns

- Growth metrics

- Performance indicators

### 3. **Performance Report**

- System health metrics

- API performance

- Error rates

- Processing statistics

### 4. **Comprehensive Report**

- All metrics combined

- Executive summary

- Trend analysis

- Recommendations

## Configuration

### Environment Variables

```env
# Analytics Configuration
ANALYTICS_ENABLED=True
ANALYTICS_RETENTION_DAYS=90
ANALYTICS_EXPORT_FORMAT=json
```

### Data Storage

Reports are stored in `data/teamtailor/analytics/` with the following structure:

```
data/teamtailor/analytics/
├── recruitment_pipeline_report_20241201_143022.json
├── user_activity_report_20241201_143022.json
├── performance_report_20241201_143022.json
├── comprehensive_report_20241201_143022.json
└── excel_exports/
    └── report_name.xlsx
```

## Integration

### Prometheus Metrics

The analytics system integrates with Prometheus for real-time monitoring:

```python
# Custom metrics
RECRUITMENT_PIPELINE_METRICS = Gauge(
    'teamtailor_recruitment_pipeline_total',
    'Total applications in pipeline'
)

USER_ENGAGEMENT_SCORE = Gauge(
    'teamtailor_user_engagement_score',
    'User engagement score percentage'
)
```

### Grafana Dashboards

Pre-configured Grafana dashboards are available for:

- **Recruitment Pipeline Overview**

- **User Activity Dashboard**

- **System Performance Monitor**

- **Custom Analytics Dashboard**

## Best Practices

### 1. **Regular Reporting**

- Schedule daily/weekly reports

- Monitor key metrics

- Set up alerts for anomalies

### 2. **Data Retention**

- Configure appropriate retention periods

- Archive old reports

- Maintain data privacy

### 3. **Performance Optimization**

- Use caching for frequently accessed data

- Optimize database queries

- Monitor system resources

### 4. **Security**

- Secure access to analytics data

- Audit report access

- Encrypt sensitive information

## Troubleshooting

### Common Issues

1. **No data in reports**

   - Check TeamTailor API connection
   - Verify date ranges
   - Check permissions

2. **Slow report generation**

   - Optimize queries
   - Use caching
   - Check system resources

3. **Export failures**

   - Verify file permissions
   - Check disk space
   - Validate export format

### Debug Commands

```bash
# Test analytics connection
make analytics-dashboard

# Check report generation
make analytics-report

# Verify data access
make teamtailor-test
```

## Future Enhancements

### Planned Features

- **Real-time dashboards** with WebSocket updates

- **Predictive analytics** for hiring trends

- **Advanced visualizations** with interactive charts

- **Custom metric definitions** for business-specific KPIs

- **Automated insights** and recommendations
