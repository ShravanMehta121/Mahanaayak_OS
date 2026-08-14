from app.extensions import db
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    
    role_id = db.Column(db.String(36), db.ForeignKey("roles.id"), nullable=False)
    assigned_ward_id = db.Column(db.String(36), db.ForeignKey("wards.id"), nullable=True)
    assigned_department_id = db.Column(db.String(36), db.ForeignKey("departments.id"), nullable=True)
    
    role = db.relationship("Role", back_populates="users")
    assigned_ward = db.relationship("Ward")
    assigned_department = db.relationship("Department")
    
    # Relationships for citizens / complaints
    citizen_profile = db.relationship("Citizen", back_populates="user", uselist=False)
    managed_complaints = db.relationship("Complaint", back_populates="assigned_to_user")
    
    activity_logs = db.relationship("ActivityLog", back_populates="user", lazy="dynamic")
