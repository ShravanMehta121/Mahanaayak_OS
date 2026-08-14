from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.constants.roles import UserRole
from app.utils.responses import error_response

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") != required_role:
                return error_response("Access forbidden: insufficient permissions", 403)
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def admin_required():
    return role_required(UserRole.ADMIN)

def member_required():
    return role_required(UserRole.TEAM_MEMBER)
