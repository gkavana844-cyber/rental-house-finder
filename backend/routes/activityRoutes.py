from flask import Blueprint, request, jsonify
from services.activityService import ActivityService

activity_routes = Blueprint('activities', __name__, url_prefix='/api/activities')

@activity_routes.route('/recent', methods=['GET'])
def get_recent_activities():
    """Get recent activities - endpoint for dashboard"""
    try:
        limit = request.args.get('limit', 5, type=int)
        activities = ActivityService.get_recent_activities(limit)
        return jsonify({
            'success': True,
            'data': activities
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@activity_routes.route('/type/<activity_type>', methods=['GET'])
def get_by_type(activity_type):
    """Get activities by type"""
    try:
        limit = request.args.get('limit', 10, type=int)
        activities = ActivityService.get_activities_by_type(activity_type, limit)
        return jsonify({
            'success': True,
            'data': activities
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@activity_routes.route('/log', methods=['POST'])
def log_activity():
    """Log a new activity"""
    try:
        data = request.get_json()
        
        activity = ActivityService.log_activity(
            activity_type=data.get('type'),
            description=data.get('description'),
            user_id=data.get('user_id'),
            metadata=data.get('metadata')
        )
        
        return jsonify({
            'success': True,
            'data': activity
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@activity_routes.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        stats = ActivityService.get_dashboard_stats()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@activity_routes.route('/clear-old', methods=['DELETE'])
def clear_old_activities():
    """Delete activities older than 30 days"""
    try:
        days = request.args.get('days', 30, type=int)
        ActivityService.clear_old_activities(days)
        return jsonify({
            'success': True,
            'message': f'Cleared activities older than {days} days'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500