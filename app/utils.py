"""
Utility functions for the application
"""
import os
from werkzeug.utils import secure_filename
from functools import wraps
from flask import session, redirect, url_for, abort
from app.models import User


ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'mp3', 'wav', 'm4a', 'zip'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_save_file(file, upload_folder):
    """Securely save uploaded file and return file path"""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    # Add timestamp to prevent filename collisions
    import time
    filename = f"{int(time.time())}_{filename}"
    
    filepath = os.path.join(upload_folder, filename)
    os.makedirs(upload_folder, exist_ok=True)
    file.save(filepath)
    
    return filepath


def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def get_file_type(filename):
    """Determine file type from extension"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if ext in {'jpg', 'jpeg', 'png', 'gif'}:
        return 'image'
    elif ext in {'mp3', 'wav', 'm4a'}:
        return 'audio'
    elif ext in {'pdf', 'doc', 'docx'}:
        return 'document'
    elif ext == 'zip':
        return 'archive'
    
    return 'unknown'
