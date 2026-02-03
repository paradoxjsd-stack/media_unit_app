"""
SQLAlchemy database models for Media Unit Management
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()


class User(db.Model):
    """User model for admin accounts"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='admin')  # 'admin', 'moderator'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'


class ApplicantAccount(db.Model):
    """Applicant login account"""
    __tablename__ = 'applicant_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    applicant = db.relationship('Applicant', backref='account', uselist=False)
    
    def __repr__(self):
        return f'<ApplicantAccount {self.applicant_id}>'


class Subunit(db.Model):
    """Subunit categories"""
    __tablename__ = 'subunits'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    skills = db.Column(db.JSON)  # List of required skills
    
    applicants = db.relationship('Applicant', backref='subunit', lazy=True)
    media = db.relationship('Media', backref='subunit', lazy=True)
    
    def __repr__(self):
        return f'<Subunit {self.name}>'


class Applicant(db.Model):
    """Membership applicant"""
    __tablename__ = 'applicants'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    occupation = db.Column(db.String(150))
    social_media = db.Column(db.JSON)  # {facebook: url, instagram: url, etc}
    professional_background = db.Column(db.Text)
    availability = db.Column(db.Text)  # Availability description
    primary_interest = db.Column(db.String(100))
    profile_picture = db.Column(db.String(255))  # Path to profile picture
    
    status = db.Column(db.String(50), default='pending')  # 'pending', 'approved', 'rejected', 'completed'
    assigned_subunit_id = db.Column(db.Integer, db.ForeignKey('subunits.id'))
    assigned_role = db.Column(db.String(100))  # Minor role if not full member
    assigned_mentor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('SkillAssessment', backref='applicant', lazy=True, cascade='all, delete-orphan')
    trial_phases = db.relationship('TrialPhase', backref='applicant', lazy=True, cascade='all, delete-orphan')
    portfolio_files = db.relationship('Portfolio', backref='applicant', lazy=True, cascade='all, delete-orphan')
    pictures = db.relationship('ApplicantPicture', backref='applicant', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Applicant {self.full_name}>'


class SkillAssessment(db.Model):
    """Skill assessment for applicants (1-5 scale)"""
    __tablename__ = 'skill_assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 scale
    self_assessed = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<SkillAssessment {self.skill_name}: {self.rating}/5>'


class TrialPhase(db.Model):
    """Track trial phases for applicants"""
    __tablename__ = 'trial_phases'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    phase_type = db.Column(db.String(50), nullable=False)  # 'portfolio_review', 'shadow_service', 'practical_test'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'pass', 'fail'
    score = db.Column(db.Integer)  # Score if applicable
    notes = db.Column(db.Text)
    completed_date = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrialPhase {self.phase_type}: {self.status}>'


class Portfolio(db.Model):
    """Portfolio files uploaded by applicants"""
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20))  # 'image', 'audio', 'document', 'video'
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    description = db.Column(db.Text)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Portfolio {self.filename}>'


class ApplicantPicture(db.Model):
    """Pictures uploaded by applicants for profile and portfolio"""
    __tablename__ = 'applicant_pictures'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    picture_type = db.Column(db.String(50), default='portfolio')  # 'profile', 'portfolio', 'work_sample'
    description = db.Column(db.Text)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ApplicantPicture {self.filename}>'


class Media(db.Model):
    """Media library for organized storage"""
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    media_type = db.Column(db.String(20), nullable=False)  # 'photo', 'audio', 'graphics', 'video'
    subunit_id = db.Column(db.Integer, db.ForeignKey('subunits.id'))
    event_name = db.Column(db.String(200))
    event_date = db.Column(db.Date)
    
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    thumbnail_path = db.Column(db.String(255))  # Path to thumbnail preview
    
    uploaded_by = db.Column(db.String(120))  # Username/email of uploader
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Media {self.title}>'


class Event(db.Model):
    """Events like rehearsals and services"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50))  # 'rehearsal', 'service', 'training'
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Event {self.title}>'


class Announcement(db.Model):
    """Announcements for unit members"""
    __tablename__ = 'announcements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(120))
    priority = db.Column(db.String(20), default='normal')  # 'low', 'normal', 'high'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Announcement {self.title}>'


class RosterTemplate(db.Model):
    """Duty roster templates configured by admin"""
    __tablename__ = 'roster_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # e.g., "Sunday Service", "Mid-week"
    description = db.Column(db.Text)
    
    # Schedule parameters
    days_of_week = db.Column(db.JSON)  # [0=Monday, 1=Tuesday, ..., 6=Sunday]
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)  # None = ongoing
    
    # Time parameters
    start_time = db.Column(db.String(5))  # HH:MM format
    end_time = db.Column(db.String(5))    # HH:MM format
    
    # Roster parameters
    subunits = db.Column(db.JSON)  # List of subunit IDs
    roles = db.Column(db.JSON)  # List of roles to assign
    members_per_slot = db.Column(db.Integer, default=1)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rosters = db.relationship('DutyRoster', backref='template', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<RosterTemplate {self.name}>'


class DutyRoster(db.Model):
    """Generated duty roster entries"""
    __tablename__ = 'duty_rosters'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('roster_templates.id'), nullable=False)
    
    # Schedule details
    duty_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(5))  # HH:MM
    end_time = db.Column(db.String(5))    # HH:MM
    
    # Assignment
    assigned_to = db.Column(db.String(120))  # Applicant name or member ID
    subunit = db.Column(db.String(100))  # Assigned subunit
    role = db.Column(db.String(100))  # Assigned role (e.g., "Audio Operator", "Camera")
    
    # Status tracking
    status = db.Column(db.String(50), default='assigned')  # assigned, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    
    # Confirmation
    confirmed_by = db.Column(db.String(120))  # Member who confirmed
    confirmed_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DutyRoster {self.assigned_to} - {self.duty_date}>'
