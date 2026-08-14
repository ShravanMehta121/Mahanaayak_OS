from app.extensions import db
from app.models.base import BaseModel

class TokenBlocklist(BaseModel):
    __tablename__ = "token_blocklist"

    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
