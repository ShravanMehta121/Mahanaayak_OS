from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.middleware.auth import admin_required
from app.utils.responses import success_response, error_response

users_bp = Blueprint("users", __name__)

def _serialize_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "role": user.role.name if user.role else None,
        "assigned_ward_id": user.assigned_ward_id,
        "assigned_department_id": user.assigned_department_id,
        "is_active": user.is_active,
        "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }

@users_bp.route("", methods=["GET"])
@jwt_required()
@admin_required()
def get_all_users():
    """Get all users (Admin only)."""
    users = UserService.get_users()
    return success_response([_serialize_user(u) for u in users])

@users_bp.route("/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """Get user by ID."""
    current_user_id = get_jwt_identity()
    # A user can view their own profile, or admins can view any profile
    # For now, let's allow any authenticated user to view profiles.
    user = UserService.get_user_by_id(user_id)
    if not user:
        return error_response("User not found", 404)
    return success_response(_serialize_user(user))

@users_bp.route("", methods=["POST"])
@jwt_required()
@admin_required()
def create_user():
    """Create a new user (Admin only)."""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user, error = UserService.create_user(data, current_user_id)
    if error:
        return error_response(error, 400)
    return success_response(_serialize_user(user), "User created successfully", 201)

@users_bp.route("/<user_id>", methods=["PUT"])
@jwt_required()
@admin_required()
def update_user(user_id):
    """Update a user (Admin only)."""
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user, error = UserService.update_user(user_id, data, current_user_id)
    if error:
        return error_response(error, 400)
    return success_response(_serialize_user(user), "User updated successfully")

@users_bp.route("/<user_id>", methods=["DELETE"])
@jwt_required()
@admin_required()
def delete_user(user_id):
    """Delete a user (Admin only)."""
    current_user_id = get_jwt_identity()
    success, error = UserService.delete_user(user_id, current_user_id)
    if error:
        return error_response(error, 400)
    return success_response(message="User deleted successfully")
