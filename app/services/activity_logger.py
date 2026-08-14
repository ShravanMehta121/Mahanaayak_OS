from flask import request
from app.extensions import db
from app.models.notification import ActivityLog

class ActivityLogger:
    @staticmethod
    def log(action: str, details: str = None, user_id: str = None):
        """
        Logs an activity in the database.
        """
        ip_address = request.remote_addr if request else None
        
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log_entry)
        db.session.commit()
