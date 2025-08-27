# Dashboard System

## 📋 General Description

The dashboard system provides web interfaces to visualize and analyze
candidate data from multiple sources (local database and TeamTailor).

## 🏗️ Architecture

### Main Components

1. **`routes/dashboard.py`** - Main dashboard routes
2. **`routes/api/teamtailor_dashboard.py`** - API endpoints for dual data
3. **`dashboard/index.html`** - Main dashboard
4. **`dashboard/dual_dashboard.html`** - Dual dashboard (local + TeamTailor)
5. **`dashboard/test.html`** - Testing and diagnostics page

### JavaScript Files

- **`dashboard/static/dashboard.js`** - Main dashboard logic
- **`dashboard/static/dual_dashboard.js`** - Dual dashboard logic

## 🚀 Available Dashboards

### 1. Main Dashboard

**URL**: `http://localhost:8000/dashboard/`
**Description**: Original dashboard with TeamTailor data
**Features**:

- General statistics
- Candidate list
- Basic filters
- Distribution charts

### 2. Dual Dashboard

**URL**: `http://localhost:8000/dashboard/dual`
**Description**: Dashboard with two data sources
**Features**:

- Local Tab: Local database data
- TeamTailor Tab: Real-time data
- Comparison Tab: Comparative analysis
- Advanced tag filters
- Real-time search

### 3. Test Page

**URL**: `http://localhost:8000/dashboard/test`
**Description**: Diagnostic tool
**Functionalities**:

- Connectivity test
- Endpoint verification
- Problem diagnosis
- Data validation

## 📊 API Endpoints

### Local Endpoints

- `GET /api/teamtailor/local/stats` - Local data statistics
- `GET /api/teamtailor/local/candidates` - Local candidate list

### TeamTailor Endpoints

- `GET /api/teamtailor/stats` - TeamTailor statistics
- `GET /api/teamtailor/candidates` - TeamTailor candidate list
- `GET /api/teamtailor/test` - Connectivity test
- `GET /api/teamtailor/tags` - Available tags

### Search Endpoints

- `GET /api/teamtailor/search` - Advanced search
- `GET /candidate-tags/search` - Tag-based search

## 🎨 UI Features

### Bootstrap 5

- Responsive design
- Modern components
- Consistent themes

### Advanced Filters

- Text search
- Tag filtering
- Category filtering
- Customizable sorting

### Data Visualization

- Chart.js charts
- Real-time statistics
- Status indicators
- Progress bars

## 🔧 Configuration

### Environment Variables

```bash
# TeamTailor
TT_TOKEN=your_token
TT_BASE_URL=https://api.teamtailor.com
TT_API_VERSION=v1

# Test mode
TEAMTAILOR_TEST_MODE=true
```

### Data Files

- **Local**: `data/json/candidates.json`
- **Logs**: `logs/dashboard.log`
- **Config**: `config/notifications/notification_config.json`

## 🚨 Troubleshooting

### Common Issues

1. **Dashboard not loading data**

   - Check connectivity: `http://localhost:8000/dashboard/test`
   - Review browser console (F12)
   - Verify endpoints: `http://localhost:8000/api/teamtailor/test`

2. **Filters not working**

   - Hard refresh (Ctrl+F5)
   - Check JavaScript in console
   - Verify data in Network tab

3. **Duplicate data**
   - Check local data source
   - Review endpoint configuration
   - Validate JSON files

### Diagnostic Tools

1. **Diagnostic Script**

   ```bash
   pipenv run python scripts/diagnose_dashboard.py
   ```

2. **Test Page**

   ```bash
   http://localhost:8000/dashboard/test
   ```

3. **Server Logs**

   ```bash
   tail -f logs/dashboard.log
   ```

## 📈 Metrics and Statistics

### Current Data

- **Local Candidates**: ~3,656 unique
- **TeamTailor Candidates**: ~25 (paginated)
- **Available Tags**: 50+ categorized
- **Categories**: 7 main types

### Performance

- **Load Time**: < 3 seconds
- **Auto-refresh**: 10 minutes
- **Rate Limiting**: 1 second between requests
- **Cache**: In-memory data

## 🔗 Related Links

- [Tag System](../tag-system/README.md)
- [TeamTailor API](../../api/TEAMTAILOR_API_ENDPOINTS.md)
- [Development Guides](../../development/README.md)
- [Dashboard Scripts](../../scripts/dashboard/README.md)

## 📝 Development Notes

### File Structure

```
dashboard/
├── index.html              # Main dashboard
├── dual_dashboard.html     # Dual dashboard
├── test.html              # Test page
└── static/
    ├── dashboard.js       # Main dashboard JS
    └── dual_dashboard.js  # Dual dashboard JS
```

### Conventions

- **HTML**: Bootstrap 5, responsive design
- **JavaScript**: ES6+, async/await, error handling
- **CSS**: Bootstrap classes, custom styles
- **API**: RESTful, JSON responses

### Upcoming Improvements

- [ ] Data export
- [ ] Advanced charts
- [ ] Real-time notifications
- [ ] Offline mode
- [ ] Dashboard customization
