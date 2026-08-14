from app.extensions import db
from app.models.base import BaseModel
from app.constants.complaint_status import ComplaintStatus

class Complaint(BaseModel):
    __tablename__ = "complaints"

    problem_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=False, default=ComplaintStatus.OPEN.value)
    severity = db.Column(db.String(50), nullable=False, default="MEDIUM")
    
    citizen_id = db.Column(db.String(36), db.ForeignKey("citizens.id"), nullable=False)
    department_id = db.Column(db.String(36), db.ForeignKey("departments.id"), nullable=True)
    ward_id = db.Column(db.String(36), db.ForeignKey("wards.id"), nullable=True)
    assigned_to = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)

    citizen = db.relationship("Citizen", back_populates="complaints")
    department = db.relationship("Department", back_populates="complaints")
    ward = db.relationship("Ward", back_populates="complaints")
    assigned_to_user = db.relationship("User", back_populates="managed_complaints")
    
    history = db.relationship("ComplaintHistory", back_populates="complaint", cascade="all, delete-orphan", order_by="ComplaintHistory.created_at.desc()")
    attachments = db.relationship("Attachment", back_populates="complaint", cascade="all, delete-orphan")


class ComplaintHistory(BaseModel):
    __tablename__ = "complaint_history"

    complaint_id = db.Column(db.String(36), db.ForeignKey("complaints.id"), nullable=False)
    status_changed_to = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    changed_by = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)

    complaint = db.relationship("Complaint", back_populates="history")
    user = db.relationship("User")


class Attachment(BaseModel):
    __tablename__ = "attachments"

    complaint_id = db.Column(db.String(36), db.ForeignKey("complaints.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=True)
    original_filename = db.Column(db.String(255), nullable=True)

    complaint = db.relationship("Complaint", back_populates="attachments")
