# Troubleshooting Guide

## Common Issues & Solutions

### Installation & Setup

#### Issue: `pip install` fails
**Symptoms**: Error messages about missing dependencies

**Solutions**:
1. Upgrade pip first:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Use specific Python version:
   ```bash
   python3 -m venv venv
   python3 -m pip install -r requirements.txt
   ```

3. Clear pip cache:
   ```bash
   pip install --upgrade pip
   pip cache purge
   pip install -r requirements.txt
   ```

---

#### Issue: `python init_db.py` fails
**Symptoms**: Database creation error, file permissions

**Solutions**:
1. Check if database exists:
   ```bash
   ls -la *.db  # Unix/Mac
   dir *.db     # Windows
   ```

2. Delete old database:
   ```bash
   rm media_unit.db  # Unix/Mac
   del media_unit.db  # Windows
   ```

3. Run init script again:
   ```bash
   python init_db.py
   ```

4. Check folder permissions:
   ```bash
   chmod 755 media_unit_app/  # Unix/Mac
   ```

---

#### Issue: Virtual environment not activating
**Symptoms**: Still using system Python

**Solutions**:
```bash
# Windows
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate

# Verify
which python  # Should show path to venv/bin/python
```

---

### Running the Application

#### Issue: Port 5000 already in use
**Symptoms**: `Address already in use` error

**Solutions**:
1. Check what's using port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   
   # macOS/Linux
   lsof -i :5000
   ```

2. Kill the process or use different port:
   ```python
   # In run.py
   app.run(port=5001)  # Use 5001 instead
   ```

3. Or find and terminate the process:
   ```bash
   # Windows
   taskkill /PID <PID> /F
   
   # macOS/Linux
   kill -9 <PID>
   ```

---

#### Issue: Application won't start - ModuleNotFoundError
**Symptoms**: `No module named 'flask'` or similar

**Solutions**:
1. Verify virtual environment is active:
   ```bash
   which python  # Check if it's in venv
   ```

2. Reinstall dependencies:
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. Check requirements.txt exists:
   ```bash
   cat requirements.txt
   ```

---

#### Issue: SQLAlchemy connection error
**Symptoms**: `operational error` when accessing database

**Solutions**:
1. Check database file exists:
   ```bash
   ls -la media_unit.db
   ```

2. Reinitialize database:
   ```bash
   python init_db.py
   ```

3. Check DATABASE_URL in config.py:
   ```python
   SQLALCHEMY_DATABASE_URI = 'sqlite:///media_unit.db'
   ```

---

### Login & Authentication

#### Issue: Can't login - "Invalid credentials"
**Symptoms**: Login fails with correct password

**Solutions**:
1. Verify admin exists in database:
   ```python
   # Check init_db.py was run
   python init_db.py  # Reinitialize
   ```

2. Check credentials:
   - Default admin: `admin` / `admin123`
   - Default moderator: `moderator` / `mod123`

3. Reset admin password:
   ```python
   from app import create_app
   from app.models import db, User
   from werkzeug.security import generate_password_hash
   
   app = create_app()
   with app.app_context():
       user = User.query.filter_by(username='admin').first()
       if user:
           user.password = generate_password_hash('newpassword')
           db.session.commit()
   ```

---

#### Issue: Session keeps expiring
**Symptoms**: Logged out after 1 hour

**Solutions**:
1. This is normal behavior - change in config.py if needed:
   ```python
   PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
   ```

2. Enable "Remember Me" (advanced):
   ```python
   session.permanent = True
   ```

---

### File Uploads

#### Issue: File upload fails silently
**Symptoms**: File doesn't save, no error message

**Solutions**:
1. Check upload folder permissions:
   ```bash
   chmod -R 755 uploads/
   ```

2. Check file extension allowed:
   - See `app/utils.py`
   - Add to ALLOWED_EXTENSIONS if needed

3. Check file size:
   - Max: 50MB
   - Increase in `config.py`: `MAX_CONTENT_LENGTH`

4. Check folder exists:
   ```bash
   mkdir -p uploads/portfolio
   mkdir -p uploads/media
   ```

---

#### Issue: "File type not allowed"
**Symptoms**: Can't upload certain file types

**Solutions**:
1. Add extension to allowed list in `app/utils.py`:
   ```python
   ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav', 'm4a', 'zip', 'mov'}
   ```

2. Restart application:
   ```bash
   # Stop: Ctrl+C
   # Start: python run.py
   ```

---

### Database Issues

#### Issue: "Database locked" error
**Symptoms**: Can't update database, tables are locked

**Solutions**:
1. Stop application (Ctrl+C)
2. Restart application
3. Check no other processes have database:
   ```bash
   # Unix/Mac
   lsof media_unit.db
   ```

4. For production (PostgreSQL):
   - Check connection pool settings
   - Increase max connections

---

#### Issue: Data disappeared after restart
**Symptoms**: Sample data gone, need to reinitialize

**Solutions**:
1. Run init script again (clears and recreates):
   ```bash
   python init_db.py
   ```

2. Or backup before reinitializing:
   ```bash
   cp media_unit.db media_unit.db.backup
   python init_db.py
   ```

---

### Frontend Issues

#### Issue: Styling looks broken - no Tailwind CSS
**Symptoms**: No colors, wrong layout

**Solutions**:
1. Clear browser cache:
   - Ctrl+Shift+Delete → Clear cached images/files

2. Hard refresh:
   - Ctrl+Shift+R (or Cmd+Shift+R on Mac)

3. Check template is correct:
   - View page source
   - Look for Tailwind CDN link

---

#### Issue: File upload drag-and-drop not working
**Symptoms**: Can only use file picker

**Solutions**:
1. Check browser supports drag-and-drop
2. Check JavaScript console for errors:
   - F12 → Console tab
   - Look for JavaScript errors

3. Try different browser

---

#### Issue: Form validation not working
**Symptoms**: Can submit form with blank fields

**Solutions**:
1. Check HTML has `required` attribute
2. Check JavaScript running without errors
3. Enable client-side validation in browser

---

### Admin Dashboard

#### Issue: Dashboard shows no data
**Symptoms**: Statistics are 0, no applicants

**Solutions**:
1. Run init_db.py to populate sample data:
   ```bash
   python init_db.py
   ```

2. Submit real application:
   - Go to /apply/
   - Fill and submit form
   - Check dashboard updates

---

#### Issue: Trial phases not updating
**Symptoms**: Changes don't save in trial phase

**Solutions**:
1. Check logged in as admin
2. Verify JavaScript not showing errors (F12)
3. Check browser network tab for failed requests

4. Manually check database:
   ```python
   from app import create_app
   from app.models import db, TrialPhase
   
   app = create_app()
   with app.app_context():
       phases = TrialPhase.query.all()
       for phase in phases:
           print(f"{phase.phase_type}: {phase.status}")
   ```

---

### Media Library

#### Issue: Can't see uploaded media
**Symptoms**: Media library is empty or missing files

**Solutions**:
1. Check files were uploaded:
   ```bash
   ls -la uploads/media/
   ```

2. Check database has records:
   ```python
   from app import create_app
   from app.models import db, Media
   
   app = create_app()
   with app.app_context():
       media = Media.query.all()
       print(f"Total media: {len(media)}")
   ```

3. Check file permissions:
   ```bash
   chmod -R 755 uploads/
   ```

---

#### Issue: Download broken - 404 error
**Symptoms**: Can't download uploaded media

**Solutions**:
1. Check file still exists:
   ```bash
   ls -la uploads/media/filename
   ```

2. Verify file path in database:
   ```python
   from app import create_app
   from app.models import db, Media
   
   app = create_app()
   with app.app_context():
       media = Media.query.get(1)
       print(media.file_path)  # Check path is correct
   ```

3. Check web server has read permission

---

### Performance Issues

#### Issue: Application running slowly
**Symptoms**: Pages load slow, forms unresponsive

**Solutions**:
1. Check for database N+1 queries:
   ```python
   # Use eager loading
   applicants = Applicant.query.options(
       db.joinedload(Applicant.skills)
   ).all()
   ```

2. Add database indexes:
   ```bash
   python  # Start Python shell
   >>> from app import create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.session.execute("CREATE INDEX idx_applicants_status ON applicants(status)")
   ```

3. Reduce page size:
   - Lower pagination (20 instead of 50)
   - Limit query results

4. Enable caching:
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

---

### Deployment Issues

See `DEPLOYMENT.md` for:
- Heroku deployment errors
- DigitalOcean setup issues
- PostgreSQL connection problems
- Static file serving issues

---

### Getting Help

1. **Check logs**:
   ```bash
   # Flask development
   tail -f flask.log
   
   # Production
   tail -f /var/log/media-unit/err.log
   ```

2. **Enable debug mode**:
   ```python
   # In run.py
   app.run(debug=True)  # Shows detailed error pages
   ```

3. **Check Python version**:
   ```bash
   python --version  # Should be 3.8+
   ```

4. **Verify all files exist**:
   ```bash
   ls -la app/templates/
   ls -la app/models.py
   ls -la config.py
   ```

5. **Check for typos** in imports or file names

---

## Still Having Issues?

1. Read error message carefully - often explains the problem
2. Check browser console (F12) for JavaScript errors
3. Check Flask console output for Python errors
4. Review the full stack trace
5. Google the error message
6. Check GitHub issues if using external library
7. Ask for help with full error message and steps to reproduce

---

## Quick Reset

If everything is broken, start fresh:

```bash
# 1. Deactivate venv
deactivate

# 2. Remove venv
rm -rf venv  # or rmdir /s venv on Windows

# 3. Delete database
rm media_unit.db  # or del media_unit.db on Windows

# 4. Create fresh venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 5. Reinstall
pip install -r requirements.txt

# 6. Reinitialize
python init_db.py

# 7. Run
python run.py
```

---

## Performance Benchmarks

Expected performance on development machine:
- Application startup: < 2 seconds
- Page load: 100-500ms
- Form submission: 500ms-1s
- Database query: < 100ms

If slower, check:
- CPU usage
- Disk I/O
- Network latency
- Database size
