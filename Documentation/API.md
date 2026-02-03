# API Documentation

## REST API Reference

Base URL: `http://localhost:5000` (development)

### Authentication

Most admin endpoints require a valid session. Login at `/auth/login`.

---

## Public Endpoints

### Home
```
GET /
```
Returns homepage with announcements.

### Apply Form
```
GET /apply/
```
Display membership application form.

### Submit Application
```
POST /apply/submit
Content-Type: multipart/form-data

Form Data:
- full_name (required)
- email (required)
- phone (optional)
- facebook (optional)
- instagram (optional)
- professional_background (optional)
- availability (optional)
- primary_interest (required)
- skill_* (1-5 scale)
- portfolio_* (files)
```

**Response:**
```json
{
    "success": true,
    "message": "Application submitted successfully!",
    "applicant_id": 5
}
```

### View Application Success
```
GET /apply/success/<applicant_id>
```
Show success page with reference ID.

### Media Library
```
GET /media/
Query Parameters:
- type: photo|audio|graphics|video
- subunit: <subunit_id>
- page: <page_number>
```
List media files with filtering.

### Download Media
```
GET /media/<media_id>/download
```
Download a media file.

### About Page
```
GET /about
```
Information about media unit.

---

## Authentication Endpoints

### Login
```
GET /auth/login
```
Display login form.

```
POST /auth/login
Form Data:
- username
- password
```

**Response (on success):**
Redirect to `/admin/dashboard`

**Response (on failure):**
Render login page with error message

### Logout
```
GET /auth/logout
```
Clear session and return to homepage.

---

## Admin Endpoints (Protected)

### Dashboard
```
GET /admin/dashboard
```
Admin dashboard with statistics.

**Response includes:**
- total_applicants
- pending_applications
- approved_members
- recent_applicants (last 10)
- status_summary (counts by status)

### List All Applicants
```
GET /admin/applicants
Query Parameters:
- status: pending|approved|completed|rejected
- page: <page_number>
```

### View Applicant Detail
```
GET /admin/applicant/<applicant_id>
```
Full applicant profile with all data.

### Update Applicant
```
POST /admin/applicant/<applicant_id>/update
Form Data:
- status
- assigned_role
- assigned_mentor_id
- assigned_subunit_id
```

**Response:**
```json
{
    "success": true,
    "message": "Applicant updated"
}
```

### Update Trial Phase
```
POST /admin/applicant/<applicant_id>/trial/<phase_id>/update
Form Data:
- status: pending|completed|pass|fail
- score: <0-100>
- notes: <feedback>
```

**Response:**
```json
{
    "success": true,
    "message": "Trial phase updated"
}
```

### Generate Reports
```
GET /admin/reports
Query Parameters:
- type: summary|ready_for_team|needs_training|assigned_roles
```

### Manage Admins
```
GET /admin/manage-admins
```
List all admin accounts.

### Create Admin
```
POST /admin/admin/create
Form Data:
- username (required)
- email (required)
- password (required)
```

**Response:**
```json
{
    "success": true,
    "message": "Admin created successfully"
}
```

---

## Media Library Endpoints (Admin)

### View Media Library
```
GET /media/
Query Parameters:
- type: photo|audio|graphics|video
- subunit: <subunit_id>
- page: <page_number>
```

### Upload Media (Form)
```
GET /media/upload
```
Display upload form.

### Upload Media (Submit)
```
POST /media/upload
Content-Type: multipart/form-data

Form Data:
- title (required)
- description (optional)
- media_type (required): photo|audio|graphics|video
- subunit_id (optional)
- event_name (optional)
- event_date (optional)
- media_file (required)
```

**Response:**
```json
{
    "success": true,
    "message": "Media uploaded successfully"
}
```

### Delete Media
```
POST /media/<media_id>/delete
```

**Response:**
```json
{
    "success": true,
    "message": "Media deleted"
}
```

---

## API Endpoints (JSON)

### Get Members Count
```
GET /api/members-count
```

**Response:**
```json
{
    "count": 5
}
```

### Get Subunits
```
GET /api/subunits
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Display Team",
        "description": "Manage live displays...",
        "skills": ["PowerPoint", "Video", ...]
    },
    ...
]
```

### Get Media Count by Type
```
GET /api/media-count
```

**Response:**
```json
{
    "photo": 15,
    "audio": 8,
    "graphics": 12,
    "video": 3
}
```

### Get Applicant Statistics
```
GET /api/applicant-stats
```

**Response:**
```json
{
    "total": 50,
    "pending": 10,
    "approved": 25,
    "completed": 10,
    "rejected": 5
}
```

### Health Check
```
GET /health
```

**Response:**
```json
{
    "status": "healthy"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "error": "Missing required fields"
}
```

### 403 Forbidden
```
Admin-only endpoints without permission
```

### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Database error message"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 302 | Redirect |
| 400 | Bad Request |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## Rate Limiting

None currently implemented. For production, add:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/submit')
@limiter.limit("10 per minute")
def submit():
    pass
```

---

## CORS

No CORS enabled by default (same-origin only).

To enable cross-origin requests:

```python
from flask_cors import CORS
CORS(app)
```

---

## Pagination

List endpoints support pagination:

```
GET /admin/applicants?page=2
```

**Response includes:**
- items
- total
- pages
- has_prev
- has_next
- prev_num
- next_num

---

## Example cURL Requests

### Submit Application
```bash
curl -X POST http://localhost:5000/apply/submit \
  -F "full_name=John Smith" \
  -F "email=john@example.com" \
  -F "primary_interest=Display Team" \
  -F "portfolio_1=@photo.jpg"
```

### Login
```bash
curl -X POST http://localhost:5000/auth/login \
  -d "username=admin" \
  -d "password=admin123" \
  -c cookies.txt
```

### Get Statistics
```bash
curl http://localhost:5000/api/applicant-stats
```

### Upload Media
```bash
curl -X POST http://localhost:5000/media/upload \
  -b cookies.txt \
  -F "title=Sunday Service" \
  -F "media_type=photo" \
  -F "media_file=@image.jpg"
```

---

## Webhooks (Future)

Plan to add email notifications:
- Application submitted
- Trial phase updated
- Status changed
- Admin created

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-03 | Initial release |

---

For more information, see README.md and DATABASE.md
