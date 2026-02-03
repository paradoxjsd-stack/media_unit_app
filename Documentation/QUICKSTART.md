<!-- Quick Start Checklist - Print or use as reference -->

# 🚀 QUICK START CHECKLIST

## Before You Start
- [ ] Python 3.8+ installed (`python --version`)
- [ ] pip updated (`python -m pip install --upgrade pip`)
- [ ] You're in the media_unit_app directory

## Installation (5 minutes)

### Step 1: Create Virtual Environment
```bash
python -m venv venv
```
- [ ] Folder `venv/` created

### Step 2: Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```
- [ ] You see `(venv)` in your terminal prompt

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] No errors in installation
- [ ] Flask, SQLAlchemy, etc. installed

### Step 4: Initialize Database
```bash
python init_db.py
```
- [ ] Output says "Database initialized successfully!"
- [ ] See credentials printed to console

### Step 5: Start Application
```bash
python run.py
```
- [ ] You see "Running on http://127.0.0.1:5000/"
- [ ] Application running without errors

## First Time Using

### Step 1: Open Browser
```
http://localhost:5000
```
- [ ] Homepage loads with subunits info
- [ ] Navigation bar visible

### Step 2: Login as Admin
1. Click "Admin Login" in navigation
2. Enter credentials from init_db.py output:
   - Username: `admin`
   - Password: `admin123`
3. Click "Login"
- [ ] Redirected to admin dashboard
- [ ] Dashboard shows statistics

### Step 3: Explore Features

#### View Dashboard
- [ ] See total applicants count
- [ ] See recent applications
- [ ] See status breakdown (Pending, Approved, etc.)

#### View Applicants
1. Click "View All Applicants" or go to `/admin/applicants`
- [ ] See list of 5 sample applicants
- [ ] Can filter by status

#### View Applicant Detail
1. Click "View" on any applicant
- [ ] See full profile
- [ ] See trial phases
- [ ] See portfolio files
- [ ] Can update status and scores

#### Upload Media
1. Click "Upload Media" button
2. Fill in form:
   - Title: "Test Photo"
   - Media Type: "Photo"
   - Click to upload any image
3. Click "Upload Media"
- [ ] File uploads successfully
- [ ] Redirected to media library

#### View Media Library
1. Click "Media Library" in main menu or go to `/media/`
- [ ] See uploaded media
- [ ] Can download files
- [ ] Can filter by type

### Step 4: Test Application Form
1. Click "Apply Now" button
2. Fill in form:
   - Full Name: "Test User"
   - Email: "test@example.com"
   - Phone: "555-1234"
   - Primary Interest: Select any subunit
   - Skills: Rate some skills (1-5)
3. Click "Submit Application"
- [ ] Form submits successfully
- [ ] See success page with reference ID
- [ ] New applicant appears in dashboard

## Troubleshooting Quick Fixes

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Problem: "Address already in use" error
**Solution**:
```bash
# Change port in run.py line: app.run(port=5001)
python run.py  # Now runs on 5001
```

### Problem: "Can't login with admin123"
**Solution**:
```bash
# Reinitialize database
python init_db.py
```

### Problem: "media_unit.db not found"
**Solution**:
```bash
python init_db.py
```

### Problem: Application won't start
**Solution**:
1. Make sure venv is activated (see `(venv)` in prompt)
2. Check Python version: `python --version` (need 3.8+)
3. Check all files exist: `ls app/models.py` (should show file)

## Next Steps

### Learn the Features
- [ ] Read [README.md](README.md) - Complete documentation
- [ ] Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - What's included

### Customize for Your Church
- [ ] Edit subunits in init_db.py
- [ ] Add your church name in templates
- [ ] Update logo/colors in base.html
- [ ] Customize announcements

### Deploy to Production
- [ ] Read [DEPLOYMENT.md](DEPLOYMENT.md)
- [ ] Choose platform (Heroku, DigitalOcean, etc.)
- [ ] Follow deployment guide

### Advanced Configuration
- [ ] Review [DATABASE.md](DATABASE.md) - Schema details
- [ ] Check [API.md](API.md) - API reference
- [ ] See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## Common Actions

### Add New Subunit
Edit `init_db.py`:
```python
subunits_data = [
    {
        'name': 'Your New Subunit',
        'description': 'Description...',
        'skills': ['Skill1', 'Skill2']
    }
]
```
Then run: `python init_db.py`

### Create Admin Account
1. Login as admin
2. Go to `/admin/manage-admins`
3. Click "Create Admin"
4. Fill in username, email, password
5. Click "Create Admin"

### Import Existing Data
See [DATABASE.md](DATABASE.md) for SQL import examples

### Enable Email Notifications
See [DEPLOYMENT.md](DEPLOYMENT.md) future enhancements section

## Important URLs to Remember

| URL | Purpose | Access |
|-----|---------|--------|
| http://localhost:5000 | Homepage | Public |
| http://localhost:5000/apply | Application form | Public |
| http://localhost:5000/media | Media library | Public |
| http://localhost:5000/auth/login | Admin login | Public |
| http://localhost:5000/admin/dashboard | Dashboard | Admin only |
| http://localhost:5000/admin/applicants | Applicants list | Admin only |
| http://localhost:5000/admin/reports | Reports | Admin only |

## File Organization

```
media_unit_app/
├── run.py              ← START HERE: python run.py
├── init_db.py          ← Setup database: python init_db.py
├── README.md           ← Full documentation
├── requirements.txt    ← Dependencies
├── config.py           ← Configuration
├── app/                ← Application code
│   ├── models.py       ← Database models
│   ├── routes.py       ← URL routes
│   └── templates/      ← HTML pages
└── uploads/            ← Uploaded files
```

## Key Concepts

**Subunits**: Team divisions (Display, Photography, Audio, etc.)
**Applicants**: People applying to join media unit
**Trial Phases**: 3-step process (Portfolio Review → Shadow Service → Practical Test)
**Admin Dashboard**: Central hub for managing applicants
**Media Library**: Storage for photos, audio, graphics

## Support

### Stuck?
1. Check error message - usually tells you what's wrong
2. Search [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
3. Check [README.md](README.md) for more details
4. Review code comments in app/models.py and app/routes.py

### Need to Reset?
```bash
# Deactivate and start fresh
deactivate
rm -rf venv media_unit.db
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python run.py
```

## ✅ Success Checklist

- [ ] Application running on http://localhost:5000
- [ ] Can access homepage
- [ ] Can login as admin
- [ ] Can view dashboard with sample data
- [ ] Can view applicants list
- [ ] Can submit application form
- [ ] Can upload media file
- [ ] Can see it in media library
- [ ] Can view reports
- [ ] Can create admin account

## 🎉 You're Done!

You have a fully functional Media Unit Management system!

Next: Customize it for your church and deploy to production.

Need help? See [README.md](README.md) or [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Questions?** Review the documentation files - they have detailed explanations!
