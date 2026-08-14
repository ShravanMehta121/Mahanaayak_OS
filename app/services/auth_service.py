from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti
from app.extensions import db
from app.models.user import User
from app.models.token_blocklist import TokenBlocklist
from app.services.activity_logger import ActivityLogger

class AuthService:
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            return None, "Invalid username or password"
        if not user.is_active:
            return None, "User account is disabled"
        
        # Update last login
        user.last_login_at = datetime.now(timezone.utc)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=user.id, additional_claims={"role": user.role.name})
        refresh_token = create_refresh_token(identity=user.id)
        
        ActivityLogger.log("LOGIN", "User logged in successfully", user.id)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role.name
            }
        }, None

    @staticmethod
    def logout(jti):
        now = datetime.now(timezone.utc)
        db.session.add(TokenBlocklist(jti=jti, created_at=now))
        db.session.commit()
        # Activity log will be done in the route since user ID is accessible there

    @staticmethod
    def refresh(identity, role_name):
        access_token = create_access_token(identity=identity, additional_claims={"role": role_name})
        return access_token

    @staticmethod
    def change_password(user_id, old_password, new_password):
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        if not check_password_hash(user.password_hash, old_password):
            return False, "Incorrect old password"
        
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        ActivityLogger.log("PASSWORD_CHANGED", "User changed their password", user_id)
        return True, "Password updated successfully"
