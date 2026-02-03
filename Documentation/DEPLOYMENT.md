# Deployment Guide - Media Unit Management Website

This guide covers deploying the Media Unit Management application to various hosting platforms.

## Pre-Deployment Checklist

- [ ] Test application locally
- [ ] Run database initialization with sample data
- [ ] Verify all file uploads work
- [ ] Test admin dashboard and reporting
- [ ] Update `SECRET_KEY` in production
- [ ] Configure proper logging
- [ ] Set up SSL/HTTPS
- [ ] Back up database regularly

## Deployment Options

### Option 1: Heroku (Easiest for beginners)

#### Prerequisites
- Heroku CLI installed
- Git installed
- GitHub account (optional but recommended)

#### Steps

1. **Create Heroku app**
```bash
heroku create media-unit-app
```

2. **Create Procfile** in root directory:
```
web: gunicorn run:app
```

3. **Create runtime.txt**:
```
python-3.11.0
```

4. **Update requirements.txt with Gunicorn**:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

5. **Set environment variables**:
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-random-secret-key-here
```

6. **Deploy**:
```bash
git push heroku main
```

7. **Initialize database**:
```bash
heroku run python init_db.py
```

8. **View logs**:
```bash
heroku logs --tail
```

**Access**: https://media-unit-app.herokuapp.com

---

### Option 2: DigitalOcean (VPS)

#### Prerequisites
- DigitalOcean account
- Ubuntu 20.04 or 22.04 droplet (2GB RAM minimum)
- SSH access

#### Setup Steps

1. **Connect to droplet and update system**:
```bash
ssh root@your_droplet_ip
apt update && apt upgrade -y
```

2. **Install dependencies**:
```bash
apt install python3-pip python3-venv postgresql postgresql-contrib nginx supervisor -y
```

3. **Create application directory**:
```bash
mkdir -p /var/www/media-unit-app
cd /var/www/media-unit-app
```

4. **Clone/upload application**:
```bash
# Upload files or git clone
git clone your-repo-url .
```

5. **Create virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

6. **Create PostgreSQL database**:
```bash
sudo -u postgres psql
CREATE DATABASE media_unit;
CREATE USER media_user WITH PASSWORD 'secure_password';
ALTER ROLE media_user SET client_encoding TO 'utf8';
GRANT ALL PRIVILEGES ON DATABASE media_unit TO media_user;
\q
```

7. **Update application configuration**:
Create `.env` file:
```
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
DATABASE_URL=postgresql://media_user:secure_password@localhost/media_unit
```

8. **Initialize database**:
```bash
python init_db.py
```

9. **Configure Gunicorn** - Create `/etc/supervisor/conf.d/media-unit.conf`:
```ini
[program:media-unit]
directory=/var/www/media-unit-app
command=/var/www/media-unit-app/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 run:app
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/media-unit/err.log
stdout_logfile=/var/log/media-unit/out.log
```

10. **Create logs directory**:
```bash
mkdir -p /var/log/media-unit
chown www-data:www-data /var/log/media-unit
```

11. **Configure Nginx** - Create `/etc/nginx/sites-available/media-unit`:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /var/www/media-unit-app/app/static;
    }

    location /uploads {
        alias /var/www/media-unit-app/uploads;
    }
}
```

12. **Enable Nginx site**:
```bash
ln -s /etc/nginx/sites-available/media-unit /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

13. **Start application**:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start media-unit
```

14. **Set up SSL with Let's Encrypt**:
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your_domain.com
```

---

### Option 3: Render

#### Steps

1. **Connect GitHub repository** to Render

2. **Create render.yaml** in root:
```yaml
services:
  - type: web
    name: media-unit
    env: python311
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true

  - type: pserv
    name: media-unit-db
    plan: free
    ipAllowList: []
    maxConnections: 1
```

3. **Deploy via Render dashboard**:
   - Connect GitHub account
   - Select repository
   - Render will auto-deploy on push

---

### Option 4: AWS (EC2 + RDS)

#### Architecture
- EC2 instance for application
- RDS PostgreSQL for database
- S3 for media storage

#### Basic Setup

1. **Launch EC2 Instance**:
   - Ubuntu 22.04 AMI
   - t3.micro or larger
   - Configure security groups for HTTP/HTTPS

2. **Install & Configure** (similar to DigitalOcean above)

3. **Create RDS PostgreSQL**:
   - Multi-AZ for production
   - Automated backups enabled
   - Security group allows port 5432 from EC2

4. **Configure S3 bucket** for media uploads:
```python
# In config.py
import boto3
S3_BUCKET = 'media-unit-uploads'
S3_REGION = 'us-east-1'
```

---

## Database Migration to PostgreSQL

### From SQLite to PostgreSQL

1. **Install PostgreSQL driver**:
```bash
pip install psycopg2-binary
```

2. **Backup SQLite**:
```bash
cp media_unit.db media_unit.db.backup
```

3. **Create PostgreSQL database** (as shown above)

4. **Export data** (Python script):
```python
from app import create_app
from app.models import db
from flask_sqlalchemy import SQLAlchemy

# Connect to SQLite
app = create_app('development')

# Backup data
backup_data = {
    'users': db.session.query(User).all(),
    'applicants': db.session.query(Applicant).all(),
    # ... export all tables
}

# Connect to PostgreSQL and import
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'
# ... restore data
```

---

## Monitoring & Maintenance

### Logging
```python
# In run.py
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

### Backups
```bash
# PostgreSQL backup
pg_dump media_unit > backup.sql

# Restore
psql media_unit < backup.sql

# Automated daily backup (cron)
0 2 * * * pg_dump media_unit > /backups/media_unit_$(date +\%Y\%m\%d).sql
```

### Health Check
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200
```

---

## Performance Optimization

### Enable Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@app.route('/media')
@cache.cached(timeout=300)
def media_library():
    # ...
```

### Database Indexing
```python
# In models.py
class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    status = db.Column(db.String(50), index=True)
    email = db.Column(db.String(120), index=True)
```

---

## Troubleshooting

### Application won't start
```bash
# Check logs
tail -f /var/log/media-unit/err.log

# Test database connection
python -c "from app import create_app; app = create_app()"
```

### Database connection errors
```bash
# Test PostgreSQL connection
psql postgresql://user:password@host/database

# Check DATABASE_URL format
# postgresql://user:password@localhost/dbname
```

### Static files not serving
- Ensure `STATIC_FOLDER` is set correctly
- Run `python -m flask collect-static` if using WhiteNoise

### Email not sending
- Configure SMTP settings
- Test with development email (Gmail, SendGrid, etc.)

---

## Security Hardening

1. **Enable HTTPS only**:
```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
PREFERRED_URL_SCHEME = 'https'
```

2. **Update dependencies regularly**:
```bash
pip install --upgrade -r requirements.txt
```

3. **Set strong SECRET_KEY**:
```python
import secrets
secrets.token_hex(32)
```

4. **Configure CORS** (if needed):
```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "example.com"}})
```

5. **Rate limiting**:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    pass
```

---

## Scaling Considerations

- Use CDN for static assets
- Implement caching layer (Redis)
- Database read replicas for large deployments
- Load balancing across multiple app instances
- Consider microservices for media processing

---

For questions or issues, refer to the main README.md or contact the development team.
