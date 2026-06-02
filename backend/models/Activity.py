from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    DynamicField
)
from datetime import datetime


class Activity(Document):
    """
    Activity Log Model
    """

    ACTIVITY_TYPES = [
        "user_registered",
        "house_added",
        "user_searched",
        "furniture_selected",
        "nearby_viewed"
    ]

    type = StringField(
        required=True,
        choices=ACTIVITY_TYPES
    )

    description = StringField(
        required=True
    )

    icon = StringField(
        required=True
    )

    user_id = StringField()

    metadata = DynamicField()

    timestamp = DateTimeField(
        default=datetime.utcnow
    )

    meta = {
        "collection": "activities",
        "indexes": [
            "timestamp",
            "type",
            "user_id"
        ]
    }

    def to_dict(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "description": self.description,
            "icon": self.icon,
            "userId": self.user_id,
            "metadata": self.metadata if self.metadata else {},
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }