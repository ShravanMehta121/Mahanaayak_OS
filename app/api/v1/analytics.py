from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analytics_service import AnalyticsService
from app.core.cache import Cache
from app.middleware.auth import admin_required
from app.utils.responses import success_response

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/admin-dashboard", methods=["GET"])
@jwt_required()
@admin_required()
def admin_dashboard():
    cache_key = "analytics:admin_dashboard"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_admin_dashboard()
    Cache.set(cache_key, data, timeout=300) # Cache for 5 minutes
    return success_response(data)

@analytics_bp.route("/team-dashboard", methods=["GET"])
@jwt_required()
def team_dashboard():
    user_id = get_jwt_identity()
    cache_key = f"analytics:team_dashboard:{user_id}"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_team_dashboard(user_id)
    Cache.set(cache_key, data, timeout=300)
    return success_response(data)

@analytics_bp.route("/charts", methods=["GET"])
@jwt_required()
def charts():
    cache_key = "analytics:charts"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_charts()
    Cache.set(cache_key, data, timeout=300)
    return success_response(data)

@analytics_bp.route("/department", methods=["GET"])
@jwt_required()
def department_analytics():
    cache_key = "analytics:department"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_department_analytics()
    Cache.set(cache_key, data, timeout=300)
    return success_response(data)

@analytics_bp.route("/ward", methods=["GET"])
@jwt_required()
def ward_analytics():
    cache_key = "analytics:ward"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_ward_analytics()
    Cache.set(cache_key, data, timeout=300)
    return success_response(data)

@analytics_bp.route("/member", methods=["GET"])
@jwt_required()
@admin_required()
def member_performance():
    cache_key = "analytics:member"
    cached_data = Cache.get(cache_key)
    if cached_data:
        return success_response(cached_data)
        
    data = AnalyticsService.get_member_performance()
    Cache.set(cache_key, data, timeout=300)
    return success_response(data)
