from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.gis_service import GisService
from app.utils.responses import success_response

gis_bp = Blueprint("gis", __name__)

@gis_bp.route("/complaints", methods=["GET"])
@jwt_required()
def get_complaints():
    ward_id = request.args.get('ward_id')
    department_id = request.args.get('department_id')
    severity = request.args.get('severity')
    status = request.args.get('status')
    
    data = GisService.get_complaints_gis(ward_id, department_id, severity, status)
    return success_response(data)

@gis_bp.route("/heatmap", methods=["GET"])
@jwt_required()
def get_heatmap():
    data = GisService.get_heatmap_data()
    return success_response(data)
