# 📱 Media Unit Management Website

A comprehensive, full-featured web application for managing church/organization media unit memberships, applications, skills assessment, trial tracking, and media library management.

**Version 1.0** | Built with Flask, SQLAlchemy, and Tailwind CSS

## ✨ Features

### Core Features
- **Membership Application Form**: Collect applicant information, skills, availability, and portfolio uploads
- **Skills Assessment**: Track proficiency levels (1-5 scale) for subunit-specific skills
- **Trial Tracking**: Monitor three phases (Portfolio Review, Shadow Service, Practical Test)
- **Media Library**: Organized storage and management of photos, audio, graphics by event and subunit
- **Admin Dashboard**: Complete applicant management, trial phase tracking, and reporting
- **Authentication**: Secure admin login with session management

### 🆕 Duty Roster Management
- **Roster Templates**: Create reusable templates with configurable parameters (days, times, roles, members)
- **Automatic Generation**: System auto-generates duty assignments for entire date ranges
- **Admin Control**: Configure days of week, time slots, roles, member counts, and subunit selection
- **Roster Management**: View, filter, edit, and export duty assignments
- **Member Confirmation**: Members can confirm their assigned duties
- **Status Tracking**: Track rosters from assigned → confirmed → completed/cancelled

📖 **Documentation**: See [ROSTER_QUICKSTART.md](ROSTER_QUICKSTART.md) and [ROSTER_GUIDE.md](ROSTER_GUIDE.md)

### Subunits
1. Display Team
2. Photography & Post-Processing
3. Audio (Live Mix & Stage)
4. Audio Recording & Archiving
5. Graphics Design

## Tech Stack

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **File Storage**: Local server (extensible to AWS S3)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### 1. Clone or Download the Project

```bash
cd media_unit_app
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python init_db.py
```

This will:
- Create the SQLite database
- Set up all tables
- Add sample admin users and applicants for testing
- Create sample events and announcements

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### 5. Run the Application

```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## Project Structure

```
media_unit_app/
├── app/
│   ├── templates/          # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/           # Login pages
│   │   ├── applicant/      # Application forms
│   │   ├── admin/          # Admin dashboard
│   │   └── media/          # Media library pages
│   ├── static/             # CSS, JavaScript, images
│   │   ├── css/
│   │   └── js/
│   ├── __init__.py         # App factory
│   ├── models.py           # Database models
│   ├── routes.py           # All route handlers
│   └── utils.py            # Helper functions
├── uploads/                # User-uploaded files
│   ├── portfolio/          # Applicant portfolio files
│   └── media/              # Media library files
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── init_db.py              # Database initialization
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Database Schema

### Users
- Admin accounts for system management
- Roles: admin, moderator

### Applicants
- Full name, contact info, professional background
- Primary interest in subunits
- Current status (pending, approved, completed, rejected)
- Assigned subunit and mentor

### Trial Phases
- Three phases tracked per applicant
- Status: pending, completed, pass, fail
- Score and notes for each phase

### Skills
- Self-assessed skills (1-5 scale)
- Linked to applicants

### Portfolio
- Uploaded files from applicants
- File type detection and storage

### Media Library
- Organized by type (photo, audio, graphics, video)
- Associated with events and subunits
- Admin-controlled uploads

### Events
- Rehearsals, services, training sessions
- Calendar scheduling

## 🚀 Quick Start (30 seconds)

```bash
# 1. Enter project directory
cd media_unit_app

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database with sample data
python init_db.py

# 5. Run application
python run.py
```

🎉 **Open your browser**: http://localhost:5000

**Login Credentials** (from sample data):
- **Admin**: username `admin` / password `admin123`
- **Moderator**: username `moderator` / password `mod123`

---

## 📖 Usage Guide

### For Applicants
1. **Visit homepage** and click "Apply Now"
2. **Fill in personal information**
   - Full name, email, phone
   - Social media links (optional)
   - Professional background
   - Availability
3. **Select primary interest** from 5 subunits
4. **Rate your skills** on 1-5 scale (automatically adjusted per subunit)
5. **Upload portfolio samples** (photos, audio, PDFs, etc.)
6. **Submit application** - immediately saved to database
7. **Receive confirmation** with reference ID

### For Admins
1. **Login** with credentials
2. **Dashboard View** 
   - See all applicant statistics
   - View recent applications
   - Quick status breakdown
3. **Manage Applicants**
   - View all applications with filtering
   - See detailed applicant profiles
   - Review portfolio files
   - Track trial phase progress
4. **Update Trial Phases**
   - Portfolio Review status
   - Shadow Service completion
   - Practical Test scores
   - Add notes and feedback
5. **Assign Roles**
   - Assign to subunits
   - Assign mentors
   - Set minor roles
   - Auto-assignment on pass
6. **Generate Reports**
   - Ready for team
   - Needs training
   - Assigned roles
   - Summary statistics
7. **Media Library**
   - Upload media files
   - Organize by event/subunit
   - Download files
   - Delete old media
8. **Manage Admin Accounts**
   - Create new admins
   - View all administrators

### Application Workflow
```
1. Applicant submits form
        ↓
2. Portfolio Review Phase (Admin reviews files)
        ↓
3. Shadow Service Phase (Applicant observes team)
        ↓
4. Practical Test Phase (Applicant demonstrates skills)
        ↓
5. Auto-Assignment (on pass: minor role or full subunit)
```

---

## 📊 Example Application Scenarios

### Scenario 1: Photography Applicant
1. John applies with photography portfolio (10 images)
2. Admin reviews Portfolio Review: PASS
3. John attends Shadow Service: COMPLETED
4. John takes practical photo session test: PASS (Score: 92)
5. **Result**: Auto-assigned as "Photographer" in Photography & Post-Processing subunit

### Scenario 2: Audio Team Applicant
1. Sarah applies for Live Mix role with audio samples
2. Admin rates Portfolio Review: FAIL (needs improvement)
3. Admin provides feedback via notes
4. Sarah resubmits portfolio
5. Admin updates Portfolio Review: PASS
6. Sarah shadows 2 services and takes practical test
7. **Result**: Assigned as "Junior Audio Operator" with mentor

---

## 🏗️ Application Architecture

```
media_unit_app/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (9 tables)
│   ├── routes.py                # All 25+ route handlers
│   ├── api.py                   # API endpoints
│   ├── utils.py                 # Helper functions
│   ├── templates/               # HTML templates (14 pages)
│   │   ├── base.html            # Layout template
│   │   ├── index.html           # Homepage
│   │   ├── about.html           # About page
│   │   ├── auth/
│   │   │   └── login.html       # Admin login
│   │   ├── applicant/
│   │   │   ├── form.html        # Application form
│   │   │   └── success.html     # Success page
│   │   ├── admin/
│   │   │   ├── dashboard.html   # Admin dashboard
│   │   │   ├── applicants.html  # Applicants list
│   │   │   ├── applicant_detail.html  # Detail view
│   │   │   ├── reports.html     # Report generator
│   │   │   └── manage_admins.html     # Admin management
│   │   └── media/
│   │       ├── library.html     # Media library
│   │       └── upload.html      # Media upload
│   └── static/                  # CSS, JavaScript
│       ├── css/
│       └── js/
├── uploads/                     # User-uploaded files
│   ├── portfolio/               # Applicant portfolios
│   └── media/                   # Media library files
├── config.py                    # Configuration
├── run.py                       # Entry point
├── init_db.py                   # Database initialization
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # This file
├── DEPLOYMENT.md                # Deployment guide
└── DATABASE.md                  # Database schema
```

---

## 🗄️ Database Overview

**9 Tables** - Fully normalized relational schema:

- **users** - Admin accounts
- **subunits** - 5 team divisions
- **applicants** - Membership applications
- **skill_assessments** - 1-5 proficiency ratings
- **trial_phases** - 3-phase progress tracking
- **portfolios** - Applicant file uploads
- **media** - Media library
- **events** - Calendar events
- **announcements** - Team communications

See `DATABASE.md` for full schema details

---

## 🔐 Authentication & Authorization

### Session Management
- Secure login with password hashing (Werkzeug)
- Session-based authentication
- Admin-only protected routes
- Automatic timeout after 1 hour inactivity

### Role-Based Access
- **Admin**: Full system access
- **Moderator**: Read-only dashboard access
- **Public**: Apply form, media library, public pages

---

## 📁 File Upload System

### Supported File Types
- **Images**: JPG, JPEG, PNG, GIF
- **Audio**: MP3, WAV, M4A
- **Documents**: PDF, DOC, DOCX
- **Archives**: ZIP

### Upload Limits
- Maximum file size: 50MB
- Stored in: `/uploads/portfolio` or `/uploads/media`
- Secure filename handling
- File type validation

---

## 🎨 UI/UX Features

### Responsive Design
- Mobile-first approach
- Works on phones, tablets, desktops
- Tailwind CSS framework
- Modern color scheme

### User Experience
- Form validation on client & server
- Real-time feedback messages
- Drag-and-drop file uploads
- Pagination for large lists
- Filtering & sorting

### Admin Features
- Dashboard statistics
- Quick action cards
- Detailed reports
- Inline form editing
- Status color coding

## Customization

### Adding New Subunits
Edit `init_db.py`:
```python
subunits_data = [
    {
        'name': 'New Subunit Name',
        'description': 'Description',
        'skills': ['Skill1', 'Skill2']
    }
]
```

### Adjusting File Upload Limits
Edit `config.py`:
```python
MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
```

### Changing Database
For PostgreSQL in production:
```python
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/media_unit'
```

## Deployment

### Heroku
```bash
heroku create media-unit-app
git push heroku main
heroku run python init_db.py
```

### DigitalOcean/Render
1. Create PostgreSQL database
2. Set environment variables:
   - `FLASK_ENV=production`
   - `DATABASE_URL=postgresql://...`
   - `SECRET_KEY=your-secret-key`
3. Deploy using your platform's CLI or GitHub integration

## API Endpoints

### Public
- `GET /` - Homepage
- `GET /apply` - Application form
- `POST /apply/submit` - Submit application
- `GET /media` - Media library
- `GET /media/{id}/download` - Download media file

### Admin (Protected)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/applicants` - View all applicants
- `GET /admin/applicant/{id}` - Detailed applicant view
- `POST /admin/applicant/{id}/update` - Update applicant
- `POST /admin/applicant/{id}/trial/{phase_id}/update` - Update trial phase
- `GET /admin/reports` - Generate reports
- `POST /media/upload` - Upload media
- `POST /media/{id}/delete` - Delete media

## Support & Troubleshooting

### Database Already Exists
Delete `media_unit.db` and run `python init_db.py` again

### Port Already in Use
Change port in `run.py`: `app.run(port=5001)`

### File Upload Issues
- Check `uploads/` folder permissions
- Verify `MAX_CONTENT_LENGTH` in config.py
- Check allowed file extensions in `app/utils.py`

## Future Enhancements

- Email notifications for applicants
- Calendar integration with Google Calendar
- Social media CMS module
- AWS S3 file storage
- Advanced reporting with charts
- Mobile app
- Two-factor authentication
- Automated mentor assignment based on skills

## License

MIT License - Feel free to use and modify as needed.

## Contact

For issues or questions, contact the development team.
