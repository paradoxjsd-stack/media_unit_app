"""
Initialize database with sample dummy data for testing
"""
from app import create_app
from app.models import db, User, Subunit, Applicant, SkillAssessment, TrialPhase, Event, Announcement
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app('development')

def initialize_database():
    """Create all tables and add sample data"""
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        # Create admin users
        print("Creating admin users...")
        admin = User(
            username='admin',
            email='admin@church.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        mod = User(
            username='moderator',
            email='moderator@church.com',
            password=generate_password_hash('mod123'),
            role='moderator'
        )
        db.session.add_all([admin, mod])
        db.session.flush()
        
        # Create subunits
        print("Creating subunits...")
        subunits_data = [
            {
                'name': 'Display Team',
                'description': 'Manage live displays and visual presentations',
                'skills': ['PowerPoint', 'ProPresenter', 'Video', 'Graphics', 'Leadership', 'Team Management']
            },
            {
                'name': 'Photography & Post-Processing',
                'description': 'Capture and edit photos from events',
                'skills': ['Photography', 'Photoshop', 'Lightroom', 'Composition', 'Leadership', 'Team Management']
            },
            {
                'name': 'Audio - Live Mix & Stage',
                'description': 'Manage live audio mixing',
                'skills': ['Mixing Console', 'Audio Equipment', 'Sound Design', 'Leadership', 'Team Management']
            },
            {
                'name': 'Audio Recording & Archiving',
                'description': 'Record and archive audio files',
                'skills': ['Recording Equipment', 'Audio Editing', 'File Management', 'Leadership', 'Team Management']
            },
            {
                'name': 'Graphics Design',
                'description': 'Create graphics and designs',
                'skills': ['Design Litatracy', 'Design Software', 'Illustration', 'Leadership', 'Team Management']
            },
            {
                'name': 'Content & Publicity',
                'description': 'Develop content strategy, social media, and publicity',
                'skills': ['Social Media', 'Content Writing', 'Marketing', 'Photography', 'Content Creation', 'Leadership', 'Team Management']
            }
        ]
        
        subunits = []
        for su_data in subunits_data:
            su = Subunit(
                name=su_data['name'],
                description=su_data['description'],
                skills=su_data['skills']
            )
            subunits.append(su)
            db.session.add(su)
        
        db.session.flush()
        
        # Create sample applicants
        print("Creating sample applicants...")
        applicants_data = [
            {
                'full_name': 'John Smith',
                'email': 'john@example.com',
                'phone': '555-0101',
                'professional_background': 'IT professional with 5 years experience',
                'availability': 'Sundays and Wednesday evenings',
                'primary_interest': 'Display Team',
                'status': 'approved',
                'skills': [('PowerPoint', 4), ('Technical Skills', 5), ('Leadership', 3), ('Content Creation', 3)]
            },
            {
                'full_name': 'Sarah Johnson',
                'email': 'sarah@example.com',
                'phone': '555-0102',
                'professional_background': 'Professional photographer',
                'availability': 'Weekends',
                'primary_interest': 'Photography & Post-Processing',
                'status': 'approved',
                'skills': [('Photography', 5), ('Photoshop', 4), ('Lightroom', 5), ('Content Creation', 4), ('Leadership', 3)]
            },
            {
                'full_name': 'Mike Davis',
                'email': 'mike@example.com',
                'phone': '555-0103',
                'professional_background': 'Audio engineer',
                'availability': 'Sundays',
                'primary_interest': 'Audio - Live Mix & Stage',
                'status': 'pending',
                'skills': [('Mixing Console', 4), ('Audio Equipment', 5), ('Leadership', 2), ('Content Creation', 2)]
            },
            {
                'full_name': 'Emily Chen',
                'email': 'emily@example.com',
                'phone': '555-0104',
                'professional_background': 'Graphic designer',
                'availability': 'Flexible',
                'primary_interest': 'Graphics Design',
                'status': 'approved',
                'skills': [('Adobe Creative Suite', 5), ('Design Software', 5), ('Content Creation', 5), ('Leadership', 4)]
            },
            {
                'full_name': 'James Wilson',
                'email': 'james@example.com',
                'phone': '555-0105',
                'professional_background': 'Music producer',
                'availability': 'Saturdays and Sundays',
                'primary_interest': 'Audio Recording & Archiving',
                'status': 'completed',
                'skills': [('Recording Equipment', 4), ('Audio Editing', 4), ('Content Creation', 3), ('Leadership', 3)]
            },
            {
                'full_name': 'Rachel Martinez',
                'email': 'rachel@example.com',
                'phone': '555-0106',
                'professional_background': 'Marketing specialist with social media expertise',
                'availability': 'Flexible',
                'primary_interest': 'Content & Publicity',
                'status': 'approved',
                'skills': [('Content Creation', 5), ('Social Media', 5), ('Marketing', 5), ('Leadership', 4), ('Publicity', 4)]
            }
        ]
        
        for app_data in applicants_data:
            applicant = Applicant(
                full_name=app_data['full_name'],
                email=app_data['email'],
                phone=app_data['phone'],
                professional_background=app_data['professional_background'],
                availability=app_data['availability'],
                primary_interest=app_data['primary_interest'],
                status=app_data['status'],
                social_media={'facebook': '', 'instagram': ''}
            )
            
            # Add skills
            for skill_name, rating in app_data['skills']:
                skill = SkillAssessment(
                    skill_name=skill_name,
                    rating=rating,
                    self_assessed=True
                )
                applicant.skills.append(skill)
            
            # Add trial phases
            for phase in ['portfolio_review', 'shadow_service', 'practical_test']:
                trial = TrialPhase(
                    phase_type=phase,
                    status='completed' if app_data['status'] == 'completed' else ('pass' if app_data['status'] == 'approved' else 'pending'),
                    score=85 if app_data['status'] in ['approved', 'completed'] else None,
                    completed_date=datetime.utcnow() if app_data['status'] in ['approved', 'completed'] else None
                )
                applicant.trial_phases.append(trial)
            
            # Assign mentor
            if app_data['status'] in ['approved', 'completed']:
                applicant.assigned_mentor_id = admin.id
            
            db.session.add(applicant)
        
        # Create sample events
        print("Creating sample events...")
        events = [
            Event(
                title='Sunday Service',
                event_type='service',
                start_date=datetime.utcnow() + timedelta(days=1),
                location='Main Sanctuary'
            ),
            Event(
                title='Equipment Training',
                event_type='training',
                start_date=datetime.utcnow() + timedelta(days=7),
                location='Media Room'
            ),
            Event(
                title='Mid-week Rehearsal',
                event_type='rehearsal',
                start_date=datetime.utcnow() + timedelta(days=2),
                location='Fellowship Hall'
            )
        ]
        db.session.add_all(events)
        
        # Create sample announcements
        print("Creating sample announcements...")
        announcements = [
            Announcement(
                title='Welcome to Media Unit!',
                content='We are excited to have new members join our team. Please review the application process and contact us with any questions.',
                author='admin',
                priority='high'
            ),
            Announcement(
                title='New Equipment Available',
                content='We have just received new audio mixing equipment. Training sessions will start next week.',
                author='admin',
                priority='normal'
            ),
            Announcement(
                title='Thank You',
                content='Thank you all for your hard work last Sunday. The service was amazing!',
                author='admin',
                priority='low'
            )
        ]
        db.session.add_all(announcements)
        
        # Commit all changes
        print("Committing changes to database...")
        db.session.commit()
        
        print("\n✅ Database initialized successfully!")
        print("\nLogin credentials:")
        print("  Admin - Username: admin, Password: admin123")
        print("  Moderator - Username: moderator, Password: mod123")
        print("\nSample applicants created:")
        for app_data in applicants_data:
            print(f"  - {app_data['full_name']} ({app_data['email']})")

if __name__ == '__main__':
    initialize_database()
