from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from app.services.auth_service import AuthService
from app.services.activity_logger import ActivityLogger
from app.utils.responses import success_response, error_response

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login and get tokens."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return error_response("Username and password are required")
        
    result, error = AuthService.login(username, password)
    if error:
        return error_response(error, 401)
        
    response = jsonify({
        "status": "success",
        "message": "Logged in successfully",
        "data": {"user": result["user"]}
    })
    set_access_cookies(response, result["access_token"])
    set_refresh_cookies(response, result["refresh_token"])
    
    return response, 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout current user (blacklist token)."""
    jti = get_jwt()["jti"]
    user_id = get_jwt_identity()
    AuthService.logout(jti)
    ActivityLogger.log("LOGOUT", "User logged out", user_id)
    
    response = jsonify({"status": "success", "message": "Logged out successfully"})
    unset_jwt_cookies(response)
    
    return response, 200

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    identity = get_jwt_identity()
    # In a real app, you might want to re-fetch the user to get the latest role
    # but for simplicity we can assume the claims are passed via refresh token, 
    # or just fetch the user.
    from app.models.user import User
    user = User.query.get(identity)
    if not user:
        return error_response("User not found", 404)
        
    new_token = AuthService.refresh(identity, user.role.name)
    response = jsonify({"status": "success", "message": "Token refreshed"})
    set_access_cookies(response, new_token)
    return response, 200

@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    """Change current user's password."""
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    
    if not old_password or not new_password:
        return error_response("Old and new passwords are required")
        
    user_id = get_jwt_identity()
    success, message = AuthService.change_password(user_id, old_password, new_password)
    
    if not success:
        return error_response(message, 400)
        
    return success_response(message=message)
