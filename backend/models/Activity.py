from mongoengine import Document, StringField, DateTimeField, ReferenceField, DynamicField
from datetime import datetime

class Activity(Document):
    """Activity log model for tracking user actions"""
    
    ACTIVITY_TYPES = [
        'user_registered',
        'house_added',
        'user_searched',
        'furniture_selected',
        'nearby_viewed'
    ]
    
    type = StringField(choices=ACTIVITY_TYPES, required=True)
    description = StringField(required=True)
    icon = StringField(required=True)
    user_id = StringField()  # Store as string or Reference if you have User model
    metadata = DynamicField()
    timestamp = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'activities',
        'indexes': [
            'timestamp',
            'type',
            'user_id'
        ]
    }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'type': self.type,
            'description': self.description,
            'icon': self.icon,
            'userId': self.user_id,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }