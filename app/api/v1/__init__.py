from flask import Blueprint
from .health import health_bp
from .auth import auth_bp
from .users import users_bp
from .roles import roles_bp
from .citizens import citizens_bp
from .complaints import complaints_bp
from .analytics import analytics_bp
from .gis import gis_bp
from .reports import reports_bp
from .ai import ai_bp
from .system import system_bp

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api_v1_bp.register_blueprint(health_bp)
api_v1_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_v1_bp.register_blueprint(users_bp, url_prefix="/users")
api_v1_bp.register_blueprint(roles_bp, url_prefix="/roles")
api_v1_bp.register_blueprint(citizens_bp, url_prefix="/citizens")
api_v1_bp.register_blueprint(complaints_bp, url_prefix="/complaints")
api_v1_bp.register_blueprint(analytics_bp, url_prefix="/analytics")
api_v1_bp.register_blueprint(gis_bp, url_prefix="/gis")
api_v1_bp.register_blueprint(reports_bp, url_prefix="/reports")
api_v1_bp.register_blueprint(ai_bp, url_prefix="/ai")
api_v1_bp.register_blueprint(system_bp, url_prefix="/system")
