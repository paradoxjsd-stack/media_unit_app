"""
Flask routes/blueprints for the application
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_file, abort
from app.models import db, Applicant, User, Subunit, SkillAssessment, TrialPhase, Portfolio, ApplicantPicture, Media, Event, Announcement, RosterTemplate, DutyRoster, ApplicantAccount
from app.utils import login_required, admin_required, allowed_file, secure_save_file, get_file_type
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import datetime, timedelta, date, time

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
applicant_bp = Blueprint('applicant', __name__, url_prefix='/apply')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
media_bp = Blueprint('media', __name__, url_prefix='/media')
roster_bp = Blueprint('roster', __name__, url_prefix='/roster')


# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Home page"""
    announcements = Announcement.query.filter(
        (Announcement.expires_at == None) | (Announcement.expires_at > datetime.utcnow())
    ).order_by(Announcement.created_at.desc()).limit(5).all()
    
    return render_template('index.html', announcements=announcements)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/api/members-count')
def members_count():
    """API: Get count of approved members"""
    count = Applicant.query.filter_by(status='approved').count()
    return jsonify({'count': count})


# ==================== AUTH ROUTES ====================

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('auth/login.html', error='Invalid credentials')
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('main.index'))


@auth_bp.route('/applicant-login', methods=['GET', 'POST'])
def applicant_login():
    """Applicant login to personal dashboard"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        applicant = Applicant.query.filter_by(email=email).first()
        
        if applicant and applicant.account:
            if check_password_hash(applicant.account.password, password) and applicant.account.is_active:
                session['applicant_id'] = applicant.id
                session['applicant_email'] = applicant.email
                session['applicant_name'] = applicant.full_name
                applicant.account.last_login = datetime.utcnow()
                db.session.commit()
                return redirect(url_for('applicant.applicant_dashboard'))
            else:
                return render_template('applicant/login.html', error='Invalid credentials or account disabled')
        else:
            return render_template('applicant/login.html', error='Email not found or no account created yet')
    
    return render_template('applicant/login.html')


@auth_bp.route('/applicant-logout')
def applicant_logout():
    """Applicant logout"""
    session.pop('applicant_id', None)
    session.pop('applicant_email', None)
    session.pop('applicant_name', None)
    return redirect(url_for('main.index'))


# ==================== APPLICANT ROUTES ====================

@applicant_bp.route('/')
def application_form():
    """Display application form"""
    subunits = Subunit.query.all()
    return render_template('applicant/form.html', subunits=subunits)


@applicant_bp.route('/submit', methods=['POST'])
def submit_application():
    """Process application submission"""
    try:
        # Get form data
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        date_of_birth_str = request.form.get('date_of_birth', '').strip()
        occupation = request.form.get('occupation', '').strip()
        facebook = request.form.get('facebook', '').strip()
        instagram = request.form.get('instagram', '').strip()
        professional_background = request.form.get('professional_background', '').strip()
        availability = request.form.get('availability', '').strip()
        primary_interest = request.form.get('primary_interest', '').strip()
        password = request.form.get('password', '').strip()
        
        # Validate required fields
        if not all([full_name, email, primary_interest, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if email already exists
        existing = Applicant.query.filter_by(email=email).first()
        if existing:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Parse date of birth
        date_of_birth = None
        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Create applicant
        applicant = Applicant(
            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            occupation=occupation,
            social_media={'facebook': facebook, 'instagram': instagram},
            professional_background=professional_background,
            availability=availability,
            primary_interest=primary_interest,
            status='pending'
        )
        
        # Process skill assessments
        for key, value in request.form.items():
            if key.startswith('skill_'):
                skill_name = key.replace('skill_', '')
                try:
                    rating = int(value)
                    if 1 <= rating <= 5:
                        skill = SkillAssessment(
                            skill_name=skill_name,
                            rating=rating,
                            self_assessed=True
                        )
                        applicant.skills.append(skill)
                except (ValueError, AttributeError):
                    pass
        
        db.session.add(applicant)
        db.session.flush()  # Get applicant ID
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'pictures')
                filepath = secure_save_file(file, upload_folder)
                
                if filepath:
                    applicant.profile_picture = filepath
                    # Also save to ApplicantPicture table
                    picture = ApplicantPicture(
                        applicant_id=applicant.id,
                        filename=file.filename,
                        file_path=filepath,
                        file_size=os.path.getsize(filepath),
                        picture_type='profile',
                        description='Profile picture'
                    )
                    db.session.add(picture)
        
        # Handle portfolio pictures upload
        if 'portfolio_pictures' in request.files:
            files = request.files.getlist('portfolio_pictures')
            for file in files:
                if file and allowed_file(file.filename):
                    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'pictures')
                    filepath = secure_save_file(file, upload_folder)
                    
                    if filepath:
                        picture = ApplicantPicture(
                            applicant_id=applicant.id,
                            filename=file.filename,
                            file_path=filepath,
                            file_size=os.path.getsize(filepath),
                            picture_type='portfolio',
                            description='Portfolio work sample'
                        )
                        db.session.add(picture)
        
        # Handle portfolio file uploads
        for file_key in request.files:
            if file_key.startswith('portfolio_'):
                file = request.files[file_key]
                if file and allowed_file(file.filename):
                    upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'portfolio')
                    filepath = secure_save_file(file, upload_folder)
                    
                    if filepath:
                        portfolio = Portfolio(
                            applicant_id=applicant.id,
                            filename=file.filename,
                            file_type=get_file_type(file.filename),
                            file_path=filepath,
                            file_size=os.path.getsize(filepath),
                            description=request.form.get(f'portfolio_desc_{file_key}', '')
                        )
                        db.session.add(portfolio)
        
        # Initialize trial phases
        for phase in ['portfolio_review', 'shadow_service', 'practical_test']:
            trial = TrialPhase(
                applicant_id=applicant.id,
                phase_type=phase,
                status='pending'
            )
            db.session.add(trial)
        
        # Create applicant account for login
        account = ApplicantAccount(
            applicant_id=applicant.id,
            password=generate_password_hash(password),
            is_active=True
        )
        db.session.add(account)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Application submitted successfully!',
            'applicant_id': applicant.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@applicant_bp.route('/success/<int:applicant_id>')
def application_success(applicant_id):
    """Show success page"""
    applicant = Applicant.query.get_or_404(applicant_id)
    return render_template('applicant/success.html', applicant=applicant)


def applicant_required(f):
    """Decorator to require applicant login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'applicant_id' not in session:
            return redirect(url_for('auth.applicant_login'))
        return f(*args, **kwargs)
    return decorated_function


@applicant_bp.route('/dashboard')
@applicant_required
def applicant_dashboard():
    """Applicant personal dashboard"""
    applicant_id = session.get('applicant_id')
    applicant = Applicant.query.get_or_404(applicant_id)
    
    # Suggested features based on status
    suggested_features = []
    
    if applicant.status == 'pending':
        suggested_features = [
            {'icon': '📋', 'title': 'Update Skills', 'description': 'Add or update your skill assessments', 'link': url_for('applicant.update_profile')},
            {'icon': '📸', 'title': 'Add Pictures', 'description': 'Upload profile and portfolio pictures', 'link': url_for('applicant.update_profile')},
            {'icon': '📚', 'title': 'View Guidelines', 'description': 'Learn about our selection process', 'link': '#'},
        ]
    elif applicant.status == 'approved':
        suggested_features = [
            {'icon': '👥', 'title': 'Meet Your Mentor', 'description': 'Connect with your assigned mentor', 'link': '#'},
            {'icon': '📅', 'title': 'Schedule Training', 'description': 'Book your orientation and training', 'link': '#'},
            {'icon': '🎬', 'title': 'View Media Resources', 'description': 'Access team resources and guides', 'link': url_for('media.library')},
        ]
    elif applicant.status == 'completed':
        suggested_features = [
            {'icon': '📊', 'title': 'View Roster', 'description': 'Check your duty assignments', 'link': url_for('roster.view_rosters')},
            {'icon': '🎓', 'title': 'Training Materials', 'description': 'Access ongoing training resources', 'link': url_for('media.library')},
            {'icon': '💬', 'title': 'Contact Your Team', 'description': 'Reach out to team leaders', 'link': '#'},
        ]
    
    return render_template('applicant/dashboard.html', 
                         applicant=applicant, 
                         suggested_features=suggested_features)


@applicant_bp.route('/update-profile', methods=['GET', 'POST'])
@applicant_required
def update_profile():
    """Update applicant profile"""
    applicant_id = session.get('applicant_id')
    applicant = Applicant.query.get_or_404(applicant_id)
    subunits = Subunit.query.all()
    
    if request.method == 'POST':
        # Update basic info
        applicant.occupation = request.form.get('occupation', applicant.occupation)
        applicant.availability = request.form.get('availability', applicant.availability)
        applicant.professional_background = request.form.get('professional_background', applicant.professional_background)
        
        # Update skills
        for key, value in request.form.items():
            if key.startswith('skill_'):
                skill_name = key.replace('skill_', '')
                try:
                    rating = int(value)
                    if 1 <= rating <= 5:
                        skill = SkillAssessment.query.filter_by(
                            applicant_id=applicant_id,
                            skill_name=skill_name
                        ).first()
                        
                        if skill:
                            skill.rating = rating
                        else:
                            skill = SkillAssessment(
                                skill_name=skill_name,
                                rating=rating,
                                self_assessed=True
                            )
                            applicant.skills.append(skill)
                except (ValueError, AttributeError):
                    pass
        
        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'pictures')
                filepath = secure_save_file(file, upload_folder)
                
                if filepath:
                    applicant.profile_picture = filepath
        
        db.session.commit()
        return redirect(url_for('applicant.applicant_dashboard'))
    
    return render_template('applicant/update_profile.html', applicant=applicant, subunits=subunits)


# ==================== ADMIN ROUTES ====================

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_applicants = Applicant.query.count()
    pending_applications = Applicant.query.filter_by(status='pending').count()
    approved_members = Applicant.query.filter_by(status='approved').count()
    
    # Get recent applicants
    recent_applicants = Applicant.query.order_by(Applicant.created_at.desc()).limit(10).all()
    
    # Get summary by status
    status_summary = {
        'pending': Applicant.query.filter_by(status='pending').count(),
        'approved': Applicant.query.filter_by(status='approved').count(),
        'rejected': Applicant.query.filter_by(status='rejected').count(),
        'completed': Applicant.query.filter_by(status='completed').count(),
    }
    
    return render_template('admin/dashboard.html',
                         total_applicants=total_applicants,
                         pending_applications=pending_applications,
                         approved_members=approved_members,
                         recent_applicants=recent_applicants,
                         status_summary=status_summary)


@admin_bp.route('/applicants')
@admin_required
def applicants_list():
    """List all applicants"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)
    
    query = Applicant.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    applicants = query.order_by(Applicant.created_at.desc()).paginate(page=page, per_page=20)
    
    return render_template('admin/applicants.html', applicants=applicants, status_filter=status_filter)


@admin_bp.route('/applicant/<int:applicant_id>')
@admin_required
def view_applicant(applicant_id):
    """View detailed applicant profile"""
    applicant = Applicant.query.get_or_404(applicant_id)
    subunits = Subunit.query.all()
    users = User.query.all()
    
    return render_template('admin/applicant_detail.html',
                         applicant=applicant,
                         subunits=subunits,
                         users=users)


@admin_bp.route('/applicant/<int:applicant_id>/update', methods=['POST'])
@admin_required
def update_applicant(applicant_id):
    """Update applicant information"""
    applicant = Applicant.query.get_or_404(applicant_id)
    
    try:
        applicant.status = request.form.get('status', applicant.status)
        applicant.assigned_role = request.form.get('assigned_role', applicant.assigned_role)
        
        mentor_id = request.form.get('assigned_mentor_id')
        if mentor_id:
            applicant.assigned_mentor_id = int(mentor_id)
        
        subunit_id = request.form.get('assigned_subunit_id')
        if subunit_id:
            applicant.assigned_subunit_id = int(subunit_id)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Applicant updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/applicant/<int:applicant_id>/trial/<phase_id>/update', methods=['POST'])
@admin_required
def update_trial_phase(applicant_id, phase_id):
    """Update trial phase"""
    trial = TrialPhase.query.get_or_404(phase_id)
    
    if trial.applicant_id != applicant_id:
        abort(403)
    
    try:
        trial.status = request.form.get('status', trial.status)
        trial.score = request.form.get('score')
        trial.notes = request.form.get('notes', '')
        
        if trial.status in ['pass', 'completed']:
            trial.completed_date = datetime.utcnow()
        
        # Auto-assign minor role if practical test passed
        if trial.phase_type == 'practical_test' and trial.status == 'pass':
            applicant = trial.applicant
            if not applicant.assigned_role:
                applicant.assigned_role = f"Minor - {applicant.primary_interest}"
                applicant.status = 'completed'
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Trial phase updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/reports')
@admin_required
def reports():
    """Generate reports"""
    report_type = request.args.get('type', 'summary')
    
    if report_type == 'ready_for_team':
        applicants = Applicant.query.filter(
            Applicant.status == 'approved',
            TrialPhase.phase_type == 'practical_test',
            TrialPhase.status == 'pass'
        ).join(TrialPhase).all()
    
    elif report_type == 'needs_training':
        # Find applicants with low skill scores and pending practical test
        applicants = Applicant.query.filter(
            TrialPhase.phase_type == 'practical_test',
            TrialPhase.status == 'pending'
        ).join(TrialPhase).all()
    
    elif report_type == 'assigned_roles':
        applicants = Applicant.query.filter(
            Applicant.assigned_role != None
        ).all()
    
    else:  # summary
        applicants = Applicant.query.all()
    
    return render_template('admin/reports.html', applicants=applicants, report_type=report_type)


@admin_bp.route('/manage-admins')
@admin_required
def manage_admins():
    """Manage admin users"""
    admins = User.query.all()
    return render_template('admin/manage_admins.html', admins=admins)


@admin_bp.route('/admin/create', methods=['POST'])
@admin_required
def create_admin():
    """Create new admin user"""
    try:
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not all([username, email, password]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role='admin'
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Admin created successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== MEDIA LIBRARY ROUTES ====================

@media_bp.route('/')
def library():
    """Media library view"""
    media_type = request.args.get('type', '')
    subunit_id = request.args.get('subunit', '', type=int)
    page = request.args.get('page', 1, type=int)
    
    query = Media.query
    
    if media_type:
        query = query.filter_by(media_type=media_type)
    
    if subunit_id:
        query = query.filter_by(subunit_id=subunit_id)
    
    media_items = query.order_by(Media.uploaded_at.desc()).paginate(page=page, per_page=20)
    subunits = Subunit.query.all()
    
    return render_template('media/library.html',
                         media_items=media_items,
                         subunits=subunits,
                         selected_type=media_type,
                         selected_subunit=subunit_id)


@media_bp.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload_media():
    """Upload media file"""
    if request.method == 'GET':
        subunits = Subunit.query.all()
        return render_template('media/upload.html', subunits=subunits)
    
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        media_type = request.form.get('media_type', '').strip()
        subunit_id = request.form.get('subunit_id', type=int)
        event_name = request.form.get('event_name', '').strip()
        event_date_str = request.form.get('event_date', '')
        
        file = request.files.get('media_file')
        
        if not all([title, media_type, file]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        upload_folder = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'media')
        filepath = secure_save_file(file, upload_folder)
        
        if not filepath:
            return jsonify({'error': 'Failed to save file'}), 500
        
        event_date = None
        if event_date_str:
            try:
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        media = Media(
            title=title,
            description=description,
            media_type=media_type,
            subunit_id=subunit_id if subunit_id else None,
            event_name=event_name,
            event_date=event_date,
            filename=file.filename,
            file_path=filepath,
            file_size=os.path.getsize(filepath),
            uploaded_by=session.get('username', 'unknown')
        )
        
        db.session.add(media)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Media uploaded successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@media_bp.route('/<int:media_id>/download')
def download_media(media_id):
    """Download media file"""
    media = Media.query.get_or_404(media_id)
    
    try:
        return send_file(media.file_path, as_attachment=True, download_name=media.filename)
    except:
        abort(404)


@media_bp.route('/<int:media_id>/delete', methods=['POST'])
@admin_required
def delete_media(media_id):
    """Delete media file"""
    media = Media.query.get_or_404(media_id)
    
    try:
        if os.path.exists(media.file_path):
            os.remove(media.file_path)
        
        db.session.delete(media)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Media deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== DUTY ROSTER ROUTES ====================

@roster_bp.route('/')
@admin_required
def roster_dashboard():
    """Duty roster dashboard"""
    templates = RosterTemplate.query.all()
    rosters = DutyRoster.query.order_by(DutyRoster.duty_date.desc()).limit(20).all()
    
    return render_template('roster/dashboard.html',
                         templates=templates,
                         rosters=rosters)


@roster_bp.route('/templates')
@admin_required
def roster_templates():
    """List all roster templates"""
    page = request.args.get('page', 1, type=int)
    templates = RosterTemplate.query.paginate(page=page, per_page=10)
    
    return render_template('roster/templates.html', templates=templates)


@roster_bp.route('/template/create', methods=['GET', 'POST'])
@admin_required
def create_template():
    """Create new roster template"""
    if request.method == 'GET':
        subunits = Subunit.query.all()
        return render_template('roster/template_form.html', subunits=subunits, template=None)
    
    try:
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        days = request.form.getlist('days')  # Array of selected days
        start_date_str = request.form.get('start_date', '')
        end_date_str = request.form.get('end_date', '')
        start_time = request.form.get('start_time', '')
        end_time = request.form.get('end_time', '')
        subunit_ids = request.form.getlist('subunits')
        roles = request.form.get('roles', '').split(',')
        members_per_slot = int(request.form.get('members_per_slot', 1))
        
        if not name or not days:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse dates
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else date.today()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        # Convert day strings to integers
        days_int = [int(d) for d in days]
        
        template = RosterTemplate(
            name=name,
            description=description,
            days_of_week=days_int,
            start_date=start_date,
            end_date=end_date,
            start_time=start_time,
            end_time=end_time,
            subunits=[int(s) for s in subunit_ids if s],
            roles=[r.strip() for r in roles if r.strip()],
            members_per_slot=members_per_slot
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify({'success': True, 'template_id': template.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/template/<int:template_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_template(template_id):
    """Edit roster template"""
    template = RosterTemplate.query.get_or_404(template_id)
    
    if request.method == 'GET':
        subunits = Subunit.query.all()
        return render_template('roster/template_form.html', 
                             subunits=subunits, 
                             template=template)
    
    try:
        template.name = request.form.get('name', template.name).strip()
        template.description = request.form.get('description', '').strip()
        
        days = request.form.getlist('days')
        template.days_of_week = [int(d) for d in days]
        
        start_date_str = request.form.get('start_date', '')
        if start_date_str:
            template.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        
        end_date_str = request.form.get('end_date', '')
        template.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        template.start_time = request.form.get('start_time', '')
        template.end_time = request.form.get('end_time', '')
        
        subunit_ids = request.form.getlist('subunits')
        template.subunits = [int(s) for s in subunit_ids if s]
        
        roles = request.form.get('roles', '').split(',')
        template.roles = [r.strip() for r in roles if r.strip()]
        
        template.members_per_slot = int(request.form.get('members_per_slot', 1))
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Template updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/template/<int:template_id>/delete', methods=['POST'])
@admin_required
def delete_template(template_id):
    """Delete roster template"""
    template = RosterTemplate.query.get_or_404(template_id)
    
    try:
        db.session.delete(template)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Template deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/generate/<int:template_id>', methods=['GET', 'POST'])
@admin_required
def generate_roster(template_id):
    """Generate duty roster from template"""
    template = RosterTemplate.query.get_or_404(template_id)
    
    if request.method == 'GET':
        return render_template('roster/generate.html', template=template)
    
    try:
        # Get parameters from form
        start_date_str = request.form.get('start_date', '')
        end_date_str = request.form.get('end_date', '')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else template.start_date
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else template.end_date
        
        # Get eligible members from subunits
        # Convert subunit IDs from JSON (which might be strings) to integers
        subunit_ids = [int(s) if isinstance(s, str) else s for s in template.subunits] if template.subunits else []
        
        eligible_members = Applicant.query.filter(
            Applicant.status.in_(['approved', 'completed']),
            Applicant.assigned_subunit_id.in_(subunit_ids) if subunit_ids else False
        ).all()
        
        if not eligible_members:
            return jsonify({'error': 'No eligible members found for selected subunits'}), 400
        
        # Generate rosters for each day in range
        current_date = start_date
        roster_count = 0
        member_index = 0
        
        while current_date <= (end_date or start_date + timedelta(days=365)):
            # Check if this day of week should have a roster
            if current_date.weekday() in template.days_of_week:
                # Create roster entries for each role
                for role in template.roles:
                    for slot in range(template.members_per_slot):
                        # Round-robin member assignment
                        member = eligible_members[member_index % len(eligible_members)]
                        member_index += 1
                        
                        subunit = Subunit.query.get(member.assigned_subunit_id)
                        subunit_name = subunit.name if subunit else 'Unknown'
                        
                        roster = DutyRoster(
                            template_id=template.id,
                            duty_date=current_date,
                            start_time=template.start_time,
                            end_time=template.end_time,
                            assigned_to=member.full_name,
                            subunit=subunit_name,
                            role=role,
                            status='assigned'
                        )
                        db.session.add(roster)
                        roster_count += 1
            
            current_date += timedelta(days=1)
            
            # Prevent infinite loop for ongoing rosters
            if not end_date and (current_date - start_date).days > 365:
                break
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{roster_count} roster entries generated',
            'count': roster_count
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/view')
def view_rosters():
    """View duty rosters (public/member access)"""
    page = request.args.get('page', 1, type=int)
    date_filter = request.args.get('date', '')
    subunit_filter = request.args.get('subunit', '')
    
    query = DutyRoster.query
    
    if date_filter:
        filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
        query = query.filter(DutyRoster.duty_date >= filter_date)
    else:
        # Default to upcoming rosters
        query = query.filter(DutyRoster.duty_date >= date.today())
    
    if subunit_filter:
        query = query.filter_by(subunit=subunit_filter)
    
    rosters = query.order_by(DutyRoster.duty_date, DutyRoster.start_time).paginate(page=page, per_page=20)
    subunits = Subunit.query.all()
    
    return render_template('roster/view.html',
                         rosters=rosters,
                         subunits=subunits,
                         date_filter=date_filter,
                         subunit_filter=subunit_filter)


@roster_bp.route('/<int:roster_id>/confirm', methods=['POST'])
def confirm_roster(roster_id):
    """Member confirms their duty"""
    roster = DutyRoster.query.get_or_404(roster_id)
    
    try:
        roster.status = 'confirmed'
        roster.confirmed_by = request.form.get('confirmed_by', 'member')
        roster.confirmed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Duty confirmed'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/<int:roster_id>/update', methods=['POST'])
@admin_required
def update_roster(roster_id):
    """Update duty roster status"""
    roster = DutyRoster.query.get_or_404(roster_id)
    
    try:
        roster.status = request.form.get('status', roster.status)
        roster.notes = request.form.get('notes', '')
        
        if request.form.get('assigned_to'):
            roster.assigned_to = request.form.get('assigned_to')
        
        if request.form.get('role'):
            roster.role = request.form.get('role')
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Roster updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/<int:roster_id>/delete', methods=['POST'])
@admin_required
def delete_roster(roster_id):
    """Delete duty roster entry"""
    roster = DutyRoster.query.get_or_404(roster_id)
    
    try:
        db.session.delete(roster)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Roster deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@roster_bp.route('/export/<int:template_id>')
@admin_required
def export_roster(template_id):
    """Export roster to CSV"""
    import csv
    from io import StringIO
    
    template = RosterTemplate.query.get_or_404(template_id)
    rosters = DutyRoster.query.filter_by(template_id=template_id).order_by(
        DutyRoster.duty_date,
        DutyRoster.start_time
    ).all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Time', 'Member', 'Subunit', 'Role', 'Status'])
    
    for roster in rosters:
        time_range = f"{roster.start_time}-{roster.end_time}" if roster.start_time else "TBA"
        writer.writerow([
            roster.duty_date.strftime('%Y-%m-%d'),
            time_range,
            roster.assigned_to,
            roster.subunit,
            roster.role,
            roster.status
        ])
    
    output.seek(0)
    return send_file(
        StringIO(output.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'roster_{template.name}.csv'
    )
