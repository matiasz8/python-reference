# TeamTailor API - All GET Endpoints

**Base URL:** `https://api.na.teamtailor.com/v1`

## 📋 Table of Contents

- [TeamTailor API - All GET Endpoints](#teamtailor-api-all-get-endpoints)
  - [📋 Table of Contents](#table-of-contents)
  - [🔧 Configuration](#configuration)
    - [Required Headers](#required-headers)

## 🔧 Configuration

### Required Headers

```python
headers = {
    "Authorization": f"Token token={TT_TOKEN}",
    "X-Api-Version": "20240904",
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
}
```

### Environment Variables

```bash
TT_BASE_URL=https://api.na.teamtailor.com/v1
TT_API_VERSION=20240904
TT_TOKEN=your_token_here
```

## 📚 Endpoints by Category

### 👤 **Candidates**

| Endpoint                         | Method | Description                |
| -------------------------------- | ------ | -------------------------- |
| `/candidates`                    | GET    | List all candidates        |
| `/candidates/{id}`               | GET    | Get candidate by ID        |
| `/candidates/{id}/activity_feed` | GET    | Candidate activity history |

**Examples:**

```bash
# Get all candidates
GET https://api.na.teamtailor.com/v1/candidates

# Get specific candidate
GET https://api.na.teamtailor.com/v1/candidates/123

# Get candidate activity
GET https://api.na.teamtailor.com/v1/candidates/123/activity_feed
```

### 🎓 **Applications**

| Endpoint                                  | Method | Description                |
| ----------------------------------------- | ------ | -------------------------- |
| `/applications`                           | GET    | List all applications      |
| `/applications/{id}`                      | GET    | Get application by ID      |
| `/applications/{id}/demographics/answers` | GET    | View demographic responses |
| `/applications/{id}/scorecards`           | GET    | Associated scorecards      |
| `/applications/{id}/scheduled_interviews` | GET    | Scheduled interviews       |
| `/applications/{id}/offer`                | GET    | Associated job offer       |
| `/applications/{id}/offers`               | GET    | All offers for application |
| `/applications/{id}/offers/current_offer` | GET    | Current offer details      |

**Examples:**

```bash
# Get all applications
GET https://api.na.teamtailor.com/v1/applications

# Get specific application
GET https://api.na.teamtailor.com/v1/applications/456

# Get demographic responses
GET https://api.na.teamtailor.com/v1/applications/456/demographics/answers
```

### 💼 **Jobs**

| Endpoint                        | Method | Description         |
| ------------------------------- | ------ | ------------------- |
| `/jobs`                         | GET    | List all jobs       |
| `/jobs/{id}`                    | GET    | Get job by ID       |
| `/jobs/job_posts`               | GET    | List all job posts  |
| `/jobs/{job_id}/job_posts`      | GET    | Job posts by job    |
| `/jobs/job_posts/{id}`          | GET    | Get job post by ID  |
| `/jobs/{job_id}/approval_flows` | GET    | Job approval flows  |
| `/jobs/approval_flows/{id}`     | GET    | Approval flow by ID |
| `/jobs/{job_id}/openings`       | GET    | Job openings        |
| `/jobs/{job_id}/stages`         | GET    | Job stages          |

**Examples:**

```bash
# Get all jobs
GET https://api.na.teamtailor.com/v1/jobs

# Get specific job
GET https://api.na.teamtailor.com/v1/jobs/789

# Get job posts
GET https://api.na.teamtailor.com/v1/jobs/job_posts
```

### 💰 **Offers**

| Endpoint             | Method | Description                 |
| -------------------- | ------ | --------------------------- |
| `/offers`            | GET    | List all offers (paginated) |
| `/offers/{offer_id}` | GET    | Get offer by ID             |

**Examples:**

```bash
# Get all offers
GET https://api.na.teamtailor.com/v1/offers

# Get specific offer
GET https://api.na.teamtailor.com/v1/offers/101
```

### 👨‍💼 **Users**

| Endpoint                        | Method | Description          |
| ------------------------------- | ------ | -------------------- |
| `/users`                        | GET    | List all users       |
| `/users/{id}`                   | GET    | Get user by ID       |
| `/users/user_roles`             | GET    | List user roles      |
| `/users/{id}/permissions/jobs`  | GET    | User job permissions |
| `/users/{id}/pending_approvals` | GET    | Pending approvals    |

**Examples:**

```bash
# Get all users
GET https://api.na.teamtailor.com/v1/users

# Get specific user
GET https://api.na.teamtailor.com/v1/users/202

# Get user roles
GET https://api.na.teamtailor.com/v1/users/user_roles
```

### 📊 **Demographics**

| Endpoint                                      | Method | Description          |
| --------------------------------------------- | ------ | -------------------- |
| `/demographics/question_sets`                 | GET    | Question sets        |
| `/demographics/question_sets/{id}`            | GET    | Question set details |
| `/demographics/questions`                     | GET    | List all questions   |
| `/demographics/question_sets/{id}/questions`  | GET    | Questions by set     |
| `/demographics/questions/{id}`                | GET    | Question details     |
| `/demographics/answer_options`                | GET    | All answer options   |
| `/demographics/questions/{id}/answer_options` | GET    | Options by question  |
| `/demographics/answer_options/{id}`           | GET    | Option details       |
| `/demographics/answers`                       | GET    | All answers          |
| `/demographics/answers/{id}`                  | GET    | Answer details       |

**Examples:**

```bash
# Get question sets
GET https://api.na.teamtailor.com/v1/demographics/question_sets

# Get specific questions
GET https://api.na.teamtailor.com/v1/demographics/questions
```

### 📃 **Metadata**

| Endpoint                      | Method | Description                |
| ----------------------------- | ------ | -------------------------- |
| `/metadata/close_reasons`     | GET    | Close reasons              |
| `/metadata/rejection_reasons` | GET    | Rejection reasons          |
| `/metadata/sources`           | GET    | Candidate sources          |
| `/metadata/degrees`           | GET    | Degrees or titles          |
| `/metadata/disciplines`       | GET    | Disciplines or specialties |
| `/metadata/schools`           | GET    | Schools or universities    |
| `/metadata/offices`           | GET    | Offices                    |
| `/metadata/departments`       | GET    | Departments                |
| `/metadata/eeoc`              | GET    | EEOC data                  |
| `/metadata/user_roles`        | GET    | User roles                 |
| `/metadata/email_templates`   | GET    | Email templates            |
| `/metadata/prospect_pools`    | GET    | Prospect pools             |

**Examples:**

```bash
# Get candidate sources
GET https://api.na.teamtailor.com/v1/metadata/sources

# Get close reasons
GET https://api.na.teamtailor.com/v1/metadata/close_reasons
```

### 🔧 **Custom Fields**

| Endpoint                                  | Method | Description           |
| ----------------------------------------- | ------ | --------------------- |
| `/custom_fields/{type}`                   | GET    | Custom fields by type |
| `/custom_field/{id}`                      | GET    | Custom field by ID    |
| `/custom_field/{id}/custom_field_options` | GET    | Field options         |

**Available types:** `candidates`, `jobs`, `applications`

**Examples:**

```bash
# Get custom fields for candidates
GET https://api.na.teamtailor.com/v1/custom_fields/candidates

# Get specific custom field
GET https://api.na.teamtailor.com/v1/custom_field/303
```

### 📋 **Scorecards**

| Endpoint      | Method | Description          |
| ------------- | ------ | -------------------- |
| `/scorecards` | GET    | List all evaluations |

**Example:**

```bash
# Get all evaluations
GET https://api.na.teamtailor.com/v1/scorecards
```

### 📅 **Scheduled Interviews**

| Endpoint                | Method | Description                   |
| ----------------------- | ------ | ----------------------------- |
| `/scheduled_interviews` | GET    | List all scheduled interviews |

**Example:**

```bash
# Get all scheduled interviews
GET https://api.na.teamtailor.com/v1/scheduled_interviews
```

### 🏢 **Departments**

| Endpoint            | Method | Description          |
| ------------------- | ------ | -------------------- |
| `/departments`      | GET    | List all departments |
| `/departments/{id}` | GET    | Get department by ID |

**Examples:**

```bash
# Get all departments
GET https://api.na.teamtailor.com/v1/departments

# Get specific department
GET https://api.na.teamtailor.com/v1/departments/404
```

### 🏢 **Offices**

| Endpoint        | Method | Description      |
| --------------- | ------ | ---------------- |
| `/offices`      | GET    | List all offices |
| `/offices/{id}` | GET    | Get office by ID |

**Examples:**

```bash
# Get all offices
GET https://api.na.teamtailor.com/v1/offices

# Get specific office
GET https://api.na.teamtailor.com/v1/offices/505
```

### 🏷️ **Tags**

| Endpoint           | Method | Description    |
| ------------------ | ------ | -------------- |
| `/candidates/tags` | GET    | Candidate tags |

**Example:**

```bash
# Get candidate tags
GET https://api.na.teamtailor.com/v1/candidates/tags
```

## 💡 Usage Examples

### Using the Basic Client

```python
import requests

# Configuration
TT_BASE_URL = "https://api.na.teamtailor.com/v1"
TT_TOKEN = "your_token_here"

headers = {
    "Authorization": f"Token token={TT_TOKEN}",
    "X-Api-Version": "20240904",
    "Content-Type": "application/vnd.api+json",
    "Accept": "application/vnd.api+json",
}

# Get all candidates
response = requests.get(f"{TT_BASE_URL}/candidates", headers=headers)
candidates = response.json()

# Get specific application
app_id = 123
response = requests.get(f"{TT_BASE_URL}/applications/{app_id}", headers=headers)
application = response.json()
```

### Using the Enhanced Client

```python
from routes.tt_client_enhanced import create_tt_client

# Create client
client = create_tt_client()

# Get all candidates
candidates = client.get_candidates()
print(f"Found {len(candidates.get('data', []))} candidates")

# Get specific candidate
candidate = client.get_candidate(123)

# Get applications
applications = client.get_applications()

# Get metadata
sources = client.get_metadata_sources()

# Get custom fields
custom_fields = client.get_custom_fields("candidates")
```

## 🔄 Enhanced Client

The project includes an enhanced client (`routes/tt_client_enhanced.py`) that
provides:

- ✅ All GET endpoints organized by category

- ✅ Automatic header and authentication handling

- ✅ Automatic retry on errors

- ✅ Integrated rate limiting

- ✅ Specific methods for each endpoint

- ✅ Complete documentation

### Enhanced Client Features

1. **Error Handling**: Automatic retry for error codes 429, 500, 502, 503, 504

2. **Rate Limiting**: Automatic configuration to respect API limits

3. **Typing**: Full support for type hints

4. **Documentation**: Detailed docstrings for each method

5. **Flexibility**: Optional parameters for filters and pagination

### Installation and Usage

```python
# Import the client
from routes.tt_client_enhanced import create_tt_client

# Create instance
client = create_tt_client()

# Use specific methods
candidates = client.get_candidates()
applications = client.get_applications()
jobs = client.get_jobs()
```

## 📝 Important Notes

1. **Pagination**: Most endpoints support pagination with parameters like `page`
   and `per_page`

2. **Filters**: Many endpoints support filters by date, status, etc.

3. **Include relationships**: You can use the `include` parameter to get related
   data

4. **Rate Limiting**: Respect the API rate limiting limits

5. **Authentication**: All endpoints require token authentication

## 🔗 Related Files

- `routes/tt_client.py` - Basic TeamTailor client

- `routes/tt_client_enhanced.py` - Enhanced client with all endpoints

- `scripts/teamtailor/teamtailor_endpoints.py` - Definition of all endpoints

- `TEAMTAILOR_API_ENDPOINTS.md` - This documentation

---

**Last updated:** December 2024
**API Version:** 20240904
**Base URL:** `https://api.na.teamtailor.com/v1`
