from app.extensions import db
from app.models.base import BaseModel

class Department(BaseModel):
    __tablename__ = "departments"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    complaints = db.relationship("Complaint", back_populates="department", lazy="dynamic")

class Ward(BaseModel):
    __tablename__ = "wards"

    name = db.Column(db.String(100), unique=True, nullable=False)
    pincode = db.Column(db.String(10), nullable=True)

    complaints = db.relationship("Complaint", back_populates="ward", lazy="dynamic")
