"""
Additional API endpoints and helper routes
"""
from flask import Blueprint, jsonify
from app.models import db, Applicant, Media, Subunit

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/members-count')
def members_count():
    """Get count of approved members"""
    count = Applicant.query.filter_by(status='approved').count()
    return jsonify({'count': count})


@api_bp.route('/media-count')
def media_count():
    """Get count of media files by type"""
    counts = {}
    for media_type in ['photo', 'audio', 'graphics', 'video']:
        count = Media.query.filter_by(media_type=media_type).count()
        counts[media_type] = count
    
    return jsonify(counts)


@api_bp.route('/subunits')
def get_subunits():
    """Get all subunits as JSON"""
    subunits = Subunit.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'skills': s.skills or []
    } for s in subunits])


@api_bp.route('/applicant-stats')
def applicant_stats():
    """Get applicant statistics"""
    return jsonify({
        'total': Applicant.query.count(),
        'pending': Applicant.query.filter_by(status='pending').count(),
        'approved': Applicant.query.filter_by(status='approved').count(),
        'completed': Applicant.query.filter_by(status='completed').count(),
        'rejected': Applicant.query.filter_by(status='rejected').count(),
    })
