from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.citizen_service import CitizenService
from app.utils.responses import success_response, error_response

citizens_bp = Blueprint("citizens", __name__)

def _serialize_citizen(c):
    return {
        "id": c.id,
        "voter_id": c.voter_id,
        "first_name": c.first_name,
        "last_name": c.last_name,
        "phone_number": c.phone_number,
        "address": c.address,
        "user_id": c.user_id,
        "created_at": c.created_at.isoformat(),
        "is_deleted": c.is_deleted
    }

@citizens_bp.route("", methods=["POST"])
@jwt_required()
def create_citizen():
    data = request.get_json()
    if not data.get("voter_id") or not data.get("first_name") or not data.get("last_name") or not data.get("phone_number"):
        return error_response("Missing required fields", 400)
        
    citizen, err = CitizenService.create_citizen(data, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(_serialize_citizen(citizen), "Citizen created", 201)

@citizens_bp.route("", methods=["GET"])
@jwt_required()
def get_citizens():
    voter_id = request.args.get('voter_id')
    name = request.args.get('name')
    phone = request.args.get('phone')
    
    citizens = CitizenService.get_citizens(voter_id, name, phone)
    return success_response([_serialize_citizen(c) for c in citizens])

@citizens_bp.route("/<citizen_id>", methods=["GET"])
@jwt_required()
def get_citizen(citizen_id):
    citizen = CitizenService.get_citizen_by_id(citizen_id)
    if not citizen:
        return error_response("Citizen not found", 404)
    return success_response(_serialize_citizen(citizen))

@citizens_bp.route("/<citizen_id>", methods=["PUT"])
@jwt_required()
def update_citizen(citizen_id):
    data = request.get_json()
    citizen, err = CitizenService.update_citizen(citizen_id, data, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(_serialize_citizen(citizen), "Citizen updated")

@citizens_bp.route("/<citizen_id>", methods=["DELETE"])
@jwt_required()
def delete_citizen(citizen_id):
    success, err = CitizenService.delete_citizen(citizen_id, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(message="Citizen deleted")

@citizens_bp.route("/voter/<voter_id>/history", methods=["GET"])
@jwt_required()
def get_citizen_history(voter_id):
    history, err = CitizenService.get_citizen_history(voter_id)
    if err:
        return error_response(err, 404)
    return success_response(history)
