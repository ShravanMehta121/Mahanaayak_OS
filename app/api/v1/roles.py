from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.models.role import Role
from app.utils.responses import success_response

roles_bp = Blueprint("roles", __name__)

@roles_bp.route("", methods=["GET"])
@jwt_required()
def get_roles():
    """Get all roles."""
    roles = Role.query.all()
    return success_response([{"id": r.id, "name": r.name, "description": r.description} for r in roles])
