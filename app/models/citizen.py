from app.extensions import db
from app.models.base import BaseModel

class Citizen(BaseModel):
    __tablename__ = "citizens"

    voter_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=True)
    home_latitude = db.Column(db.Float, nullable=True)
    home_longitude = db.Column(db.Float, nullable=True)
    
    # user_id is nullable because a citizen can exist without a registered platform user account
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), unique=True, nullable=True)
    
    user = db.relationship("User", back_populates="citizen_profile")
    complaints = db.relationship("Complaint", back_populates="citizen", lazy="dynamic")
