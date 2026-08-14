from app.extensions import db
from app.models.base import BaseModel

class AIHistory(BaseModel):
    __tablename__ = "ai_history"

    prompt_type = db.Column(db.String(100), nullable=False, index=True)
    input_data = db.Column(db.Text, nullable=True)
    output_data = db.Column(db.Text, nullable=False)
    
    generated_by = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)

    user = db.relationship("User")
