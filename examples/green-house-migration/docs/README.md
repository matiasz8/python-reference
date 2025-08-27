# 📚 Project Documentation

## 🎯 General Description

This project is a candidate management system that integrates data from
Greenhouse and TeamTailor, providing interactive dashboards and a tag system
for advanced categorization.

> 📚 **See [Complete Documentation Index](./DOCUMENTATION_INDEX.md) for a comprehensive view of all organized documentation.**

## 📁 Documentation Structure

### 🚀 Main Features

#### [Tag System](./features/tag-system/README.md)

- **Description**: Candidate categorization system with structured tags
- **Components**: TagManager, API endpoints, migration scripts
- **Use Cases**: Automatic categorization, advanced search, market analysis

#### [Dashboard System](./features/dashboard/README.md)

- **Description**: Web interfaces for data visualization
- **Dashboards**: Main, Dual (local + TeamTailor), Test page
- **Features**: Advanced filters, interactive charts, real-time data

### 📖 Guides and Tutorials

#### [Migration Guides](./guides/migration/README.md)

- **Data Migration**: Process of data transfer between systems
- **User Migration**: User and role management
- **Verification**: Post-migration validation tools

#### [Development Guides](./development/README.md)

- **Configuration**: Development environment setup
- **Contribution**: Guides for contributing to the project
- **Testing**: Testing strategies and tools

### 🔧 Scripts and Tools

#### [TeamTailor Scripts](./scripts/teamtailor/README.md)

- **Tag Management**: Scripts for applying and managing tags
- **Migration**: Bulk migration tools
- **Analysis**: Analysis and reporting scripts

#### [Dashboard Scripts](./scripts/dashboard/README.md)

- **Diagnostics**: Troubleshooting tools
- **Testing**: Validation and testing scripts
- **Maintenance**: Cleanup and backup tools

### 📡 APIs and Endpoints

#### [TeamTailor API](./api/TEAMTAILOR_API_ENDPOINTS.md)

- **Endpoints**: Complete API documentation
- **Authentication**: Token configuration and access
- **Rate Limiting**: Limits and best practices

#### [Candidates API](./api/CANDIDATES_PROSPECTS_API.md)

- **Candidate Management**: CRUD operations
- **Search**: Advanced filters and queries
- **Prospects**: Prospect management

### 🏗️ Architecture

#### [Routes Structure](./architecture/routes-structure.md)

- **Organization**: File and directory structure
- **Routers**: Endpoint configuration
- **Middleware**: CORS and authentication configuration

### 🔒 Security

#### [Security Guide](./security/security-guide.md)

- **Configuration**: Environment variables and secrets
- **Audit**: Security analysis tools
- **Best Practices**: Security recommendations

### 📊 Analysis and Reports

#### [Data Analysis](./analysis/DUPLICATES_ANALYSIS.md)

- **Duplicate Detection**: Duplicate data analysis
- **Normalization**: Data cleaning process
- **Reports**: Quality report generation

#### [Project Reports](./reports/README.md)

- **Project Status**: Status and progress reports
- **Improvements**: Summaries of implemented improvements
- **Security**: Security audit reports
- **Development**: Development and configuration guides

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone and configure
git clone <repository>
cd green-house
./setup-dev.sh

# Configure environment variables
cp .env.example .env
# Edit .env with your credentials
```

### 2. Run the Project

```bash
# Development mode
./scripts/start_server.sh

# Or directly
pipenv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access Dashboards

- **Main Dashboard**: <http://localhost:8000/dashboard/>
- **Dual Dashboard**: <http://localhost:8000/dashboard/dual>
- **Test Page**: <http://localhost:8000/dashboard/test>

### 4. Tag System

```bash
# View available tags
pipenv run python scripts/teamtailor/quick_start_tagging.py

# Apply tags
pipenv run python scripts/teamtailor/add_candidate_tags.py --candidate-id 123 --tags "python,react"
```

## 📋 Project Status

### ✅ Completed

- [x] Structured tag system
- [x] Dual dashboard (local + TeamTailor)
- [x] Complete API endpoints
- [x] Migration scripts
- [x] Organized documentation
- [x] Diagnostic tools

### 🔄 In Progress

- [ ] Performance optimization
- [ ] Automated tests
- [ ] Advanced monitoring

### 📋 Pending

- [ ] Data export
- [ ] Real-time notifications
- [ ] Advanced charts
- [ ] Offline mode

## 🔗 Useful Links

### External Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TeamTailor API](https://developer.teamtailor.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)

### Project Tools

- [GitHub Pages](https://pages.github.com/)
- [Pre-commit Hooks](https://pre-commit.com/)
- [Bandit Security](https://bandit.readthedocs.io/)

## 📞 Support

### Common Issues

1. **Dashboard not loading**: Use test page at `/dashboard/test`
2. **API errors**: Check environment variables
3. **Migration issues**: Review logs in `logs/`

### Diagnostic Tools

- **Quick Diagnosis**: `scripts/diagnose_dashboard.py`
- **Browser Test**: `scripts/test_dashboard_browser.py`
- **Data Validation**: `scripts/dashboard/data_validation.py`

## 📝 Contribution

To contribute to the project:

1. Review [Development Guides](./development/README.md)
2. Follow [Contribution Guide](./development/contributing.md)
3. Use pre-commit hooks: `pre-commit install`

## 📄 License

This project is under MIT license. See LICENSE file for more details.
