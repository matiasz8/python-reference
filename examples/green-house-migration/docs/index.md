# 🏠 TeamTailor Management System

Welcome to the **TeamTailor Management System** documentation! This project
provides a comprehensive FastAPI application for managing and optimizing your
TeamTailor ATS operations with advanced analytics, user management, and legacy
data handling.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd green-house

# Install dependencies
pipenv install

# Set up environment variables
export TT_TOKEN="your_teamtailor_token"
export TT_BASE_URL="https://api.na.teamtailor.com/v1"

# Test connection
python3 scripts/teamtailor/test_connection.py
```

## 📚 Documentation Sections

### 🔗 [API Documentation](api/)

- **TeamTailor API Endpoints**
  - Complete reference of all available GET endpoints
- Base URL: `https://api.na.teamtailor.com/v1`
- Authentication and configuration details

### 📖 [Guides](guides/)

- **Migration Guide** - Step-by-step data migration process
- **Normalization Summary** - Project organization and improvements
- Best practices and troubleshooting

### 🛠️ [Scripts Documentation](scripts/)

- **TeamTailor Scripts** - Complete reference of all available scripts
- Usage examples and configuration
- Script categories and purposes

## 🏗️ Project Structure

```
green-house/
├── docs/                    # 📚 Documentation
│   ├── api/                # 🔗 API documentation
│   ├── guides/             # 📖 User guides
│   └── scripts/            # 🛠️ Scripts documentation
├── routes/                 # 🛣️ API routes
│   ├── api/                # 🔌 Core API endpoints
│   ├── import_/            # 📥 Data import operations
│   ├── export/             # 📤 Data export operations
│   └── clients/            # 🔗 API clients
├── teamtailor/             # 🎯 TeamTailor core modules
│   ├── api/                # 🔌 API client
│   ├── analytics/          # 📊 Analytics & reporting
│   ├── management/         # 👥 User management
│   ├── notifications/      # 🔔 Notifications
│   └── integrations/       # 🔗 Integrations
├── scripts/                # 🐍 Utility scripts
│   └── teamtailor/         # TeamTailor integration scripts
├── legacy/                 # 🌱 Legacy Greenhouse code
├── monitoring/             # 📈 Monitoring & health checks
├── config/                 # ⚙️ Configuration files
└── tests/                  # 🧪 Test files
```

## 🔧 Key Features

- ✅ **Complete TeamTailor API Integration**
  - All endpoints with enhanced functionality
- ✅ **Advanced User Management**
  - Create, update, assign roles, and manage permissions
- ✅ **Analytics & Reporting**
  - Comprehensive data insights and performance metrics
- ✅ **Legacy Data Handling** - Historical Greenhouse data management
- ✅ **Security & Monitoring** - Enterprise-grade security with health checks
- ✅ **Modern FastAPI Architecture** - High-performance, scalable API

## 📊 Current Status

- **Migration Progress**: 83.1% (59/71 users migrated)
- **API Endpoints**: All GET endpoints documented
- **Scripts Available**: 21 organized scripts
- **Documentation**: Complete and up-to-date

## 🆘 Getting Help

1. **Check the [Guides](guides/)** for step-by-step instructions
2. **Review [API Documentation](api/)** for technical details
3. **Explore [Scripts](scripts/)** for available tools
4. **Run status check**: `python3 scripts/check_project_status.py`

## 🔗 Quick Links

- [TeamTailor API Reference](api/TEAMTAILOR_API_ENDPOINTS.md)
- [Migration Guide](guides/MIGRATION_GUIDE.md)
- [Scripts Documentation](scripts/README.md)
- [Project Status](guides/NORMALIZATION_SUMMARY.md)

---

**Last updated**: December 2024
**API Version**: 20240904
**Base URL**: `https://api.na.teamtailor.com/v1`
