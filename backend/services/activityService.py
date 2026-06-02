from models.Activity import Activity
from datetime import datetime, timedelta

class ActivityService:
    """Service for managing activity logs"""
    
    ACTIVITY_ICONS = {
        'user_registered': '👤',
        'house_added': '🏠',
        'user_searched': '🔍',
        'furniture_selected': '🛋️',
        'nearby_viewed': '📍'
    }
    
    @staticmethod
    def log_activity(activity_type, description, user_id=None, metadata=None):
        """Log a new activity"""
        try:
            if activity_type not in Activity.ACTIVITY_TYPES:
                raise ValueError(f"Invalid activity type: {activity_type}")
            
            activity = Activity(
                type=activity_type,
                description=description,
                icon=ActivityService.ACTIVITY_ICONS.get(activity_type, '📌'),
                user_id=user_id,
                metadata=metadata,
                timestamp=datetime.utcnow()
            )
            activity.save()
            return activity.to_dict()
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            raise
    
    @staticmethod
    def get_recent_activities(limit=5):
        """Get recent activities"""
        try:
            activities = Activity.objects.order_by('-timestamp').limit(limit)
            return [activity.to_dict() for activity in activities]
        except Exception as e:
            print(f"Error fetching activities: {str(e)}")
            raise
    
    @staticmethod
    def get_activities_by_type(activity_type, limit=10):
        """Get activities filtered by type"""
        try:
            activities = Activity.objects(type=activity_type).order_by('-timestamp').limit(limit)
            return [activity.to_dict() for activity in activities]
        except Exception as e:
            print(f"Error fetching activities by type: {str(e)}")
            raise
    
    @staticmethod
    def get_dashboard_stats():
        """Get dashboard statistics"""
        try:
            total_activities = Activity.objects.count()
            
            # Count by type
            activities_by_type = {}
            for activity_type in Activity.ACTIVITY_TYPES:
                count = Activity.objects(type=activity_type).count()
                activities_by_type[activity_type] = count
            
            # Activities in last 24 hours
            last_24_hours = datetime.utcnow() - timedelta(hours=24)
            last_24_count = Activity.objects(timestamp__gte=last_24_hours).count()
            
            return {
                'total_activities': total_activities,
                'activities_by_type': activities_by_type,
                'last_24_hours': last_24_count
            }
        except Exception as e:
            print(f"Error fetching stats: {str(e)}")
            raise
    
    @staticmethod
    def clear_old_activities(days=30):
        """Delete activities older than specified days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            Activity.objects(timestamp__lt=cutoff_date).delete()
            return True
        except Exception as e:
            print(f"Error clearing old activities: {str(e)}")
            raise