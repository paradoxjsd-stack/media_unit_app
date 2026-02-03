# Database Schema Documentation

## Overview
The Media Unit Management system uses SQLAlchemy ORM with support for SQLite (development) and PostgreSQL (production).

## Entity Relationship Diagram

```
Users (Admins)
    ├── Applicants (1-to-many, as mentor)
    └── Media (1-to-many, as uploader)

Applicants
    ├── SkillAssessments (1-to-many)
    ├── TrialPhases (1-to-many)
    ├── Portfolio (1-to-many)
    └── Subunits (many-to-1)

Subunits
    ├── Applicants (1-to-many)
    └── Media (1-to-many)

Events
    └── (standalone for scheduling)

Announcements
    └── (standalone for communications)

Media
    ├── Subunits (many-to-1)
    └── Events (through description)
```

## Tables

### users
Admin and moderator accounts.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| username | String(80) | UNIQUE, NOT NULL | Login username |
| password | String(255) | NOT NULL | Hashed password |
| email | String(120) | UNIQUE, NOT NULL | Contact email |
| role | String(20) | DEFAULT 'admin' | 'admin' or 'moderator' |
| created_at | DateTime | DEFAULT now | Account creation timestamp |

### subunits
Team divisions (Display, Photography, Audio, etc.)

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| name | String(100) | UNIQUE, NOT NULL | Subunit name |
| description | Text | | Purpose and responsibilities |
| skills | JSON | | Array of required skills |

### applicants
Membership applications.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| full_name | String(120) | NOT NULL | Applicant's full name |
| email | String(120) | NOT NULL | Contact email |
| phone | String(20) | | Phone number |
| social_media | JSON | | {facebook, instagram, etc} |
| professional_background | Text | | Experience description |
| availability | Text | | When applicant can serve |
| primary_interest | String(100) | | Preferred subunit |
| status | String(50) | DEFAULT 'pending' | pending/approved/completed/rejected |
| assigned_subunit_id | Integer | FK → subunits.id | Assigned team |
| assigned_role | String(100) | | Minor role if applicable |
| assigned_mentor_id | Integer | FK → users.id | Assigned mentor |
| created_at | DateTime | DEFAULT now | Application submission time |
| updated_at | DateTime | DEFAULT now | Last updated time |

### skill_assessments
Proficiency ratings for applicants.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| applicant_id | Integer | FK → applicants.id | Which applicant |
| skill_name | String(100) | NOT NULL | Skill being rated |
| rating | Integer | 1-5 scale | Proficiency level |
| self_assessed | Boolean | DEFAULT TRUE | Self or admin assessed |

### trial_phases
Track application processing phases.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| applicant_id | Integer | FK → applicants.id | Which applicant |
| phase_type | String(50) | NOT NULL | portfolio_review/shadow_service/practical_test |
| status | String(20) | DEFAULT 'pending' | pending/completed/pass/fail |
| score | Integer | | Points earned (0-100) |
| notes | Text | | Admin notes |
| completed_date | DateTime | | When phase completed |
| created_at | DateTime | DEFAULT now | Creation timestamp |
| updated_at | DateTime | DEFAULT now | Last update timestamp |

### portfolios
Files uploaded by applicants.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| applicant_id | Integer | FK → applicants.id | Which applicant |
| filename | String(255) | NOT NULL | Original filename |
| file_type | String(20) | | image/audio/document/video |
| file_path | String(255) | NOT NULL | Server storage path |
| file_size | Integer | | Bytes |
| description | Text | | Portfolio item description |
| uploaded_at | DateTime | DEFAULT now | Upload timestamp |

### media
Media library files.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| title | String(255) | NOT NULL | Display title |
| description | Text | | Details about media |
| media_type | String(20) | NOT NULL | photo/audio/graphics/video |
| subunit_id | Integer | FK → subunits.id | Associated team |
| event_name | String(200) | | Related event name |
| event_date | Date | | Event date |
| filename | String(255) | NOT NULL | Stored filename |
| file_path | String(255) | NOT NULL | Server path |
| file_size | Integer | | Bytes |
| thumbnail_path | String(255) | | Preview image path |
| uploaded_by | String(120) | | Username of uploader |
| uploaded_at | DateTime | DEFAULT now | Upload timestamp |

### events
Calendar events and services.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| title | String(200) | NOT NULL | Event name |
| description | Text | | Event details |
| event_type | String(50) | | rehearsal/service/training |
| start_date | DateTime | NOT NULL | Start time |
| end_date | DateTime | | End time |
| location | String(255) | | Physical location |
| created_at | DateTime | DEFAULT now | Creation timestamp |

### announcements
Communications for team members.

| Column | Type | Constraints | Description |
|--------|------|-----------|-------------|
| id | Integer | PRIMARY KEY | Unique identifier |
| title | String(200) | NOT NULL | Headline |
| content | Text | NOT NULL | Full announcement text |
| author | String(120) | | Who posted it |
| priority | String(20) | DEFAULT 'normal' | low/normal/high |
| created_at | DateTime | DEFAULT now | Posted timestamp |
| expires_at | DateTime | | When to hide announcement |

## Indexes

For optimal query performance:

```sql
-- Recommended indexes
CREATE INDEX idx_applicants_status ON applicants(status);
CREATE INDEX idx_applicants_email ON applicants(email);
CREATE INDEX idx_applicants_subunit ON applicants(assigned_subunit_id);
CREATE INDEX idx_trial_phases_applicant ON trial_phases(applicant_id);
CREATE INDEX idx_media_type ON media(media_type);
CREATE INDEX idx_media_subunit ON media(subunit_id);
```

## Relationships

### One-to-Many
- Users → Applicants (mentor relationship)
- Users → Media (uploaded_by)
- Subunits → Applicants
- Subunits → Media
- Applicants → SkillAssessments
- Applicants → TrialPhases
- Applicants → Portfolio

### Many-to-One
- Applicants → Subunits (assigned_subunit)
- Applicants → Users (assigned_mentor)
- Media → Subunits
- SkillAssessment → Applicants
- TrialPhase → Applicants
- Portfolio → Applicants

## Sample Queries

### Get all approved applicants
```sql
SELECT * FROM applicants WHERE status = 'approved';
```

### Get applicants with skills >= 4
```sql
SELECT DISTINCT a.* FROM applicants a
JOIN skill_assessments s ON a.id = s.applicant_id
WHERE s.rating >= 4;
```

### Get applicants by trial phase status
```sql
SELECT DISTINCT a.*, tp.phase_type, tp.status
FROM applicants a
JOIN trial_phases tp ON a.id = tp.applicant_id
WHERE tp.phase_type = 'practical_test' AND tp.status = 'pass';
```

### Get media by subunit
```sql
SELECT m.* FROM media m
JOIN subunits s ON m.subunit_id = s.id
WHERE s.name = 'Photography & Post-Processing';
```

### Get applicant statistics
```sql
SELECT status, COUNT(*) as count FROM applicants GROUP BY status;
```

## Backup & Recovery

### Export to CSV
```python
import csv
from app.models import Applicant

applicants = Applicant.query.all()
with open('applicants.csv', 'w') as f:
    writer = csv.writer(f)
    for app in applicants:
        writer.writerow([app.id, app.full_name, app.email, app.status])
```

### Database Dump (PostgreSQL)
```bash
pg_dump media_unit > media_unit_backup.sql
```

### Database Restore
```bash
psql media_unit < media_unit_backup.sql
```

## Data Validation

### Constraints Enforced
- Email format validation
- File type restrictions
- Skill rating (1-5 only)
- Status enumerations
- Phase type restrictions
- Unique usernames and emails

### Application-Level Checks
```python
# See app/routes.py and app/utils.py for:
- File size limits (50MB)
- Allowed file extensions
- Required field validation
- Email format verification
```

---

For detailed implementation, see `app/models.py`.
