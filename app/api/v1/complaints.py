from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.complaint_service import ComplaintService
from app.services.csv_import_service import CsvImportService
from app.utils.responses import success_response, error_response

complaints_bp = Blueprint("complaints", __name__)

def _serialize_complaint(c):
    return {
        "id": c.id,
        "problem_id": c.problem_id,
        "title": c.title,
        "description": c.description,
        "address": c.address,
        "status": c.status,
        "severity": c.severity,
        "citizen_id": c.citizen_id,
        "department_id": c.department_id,
        "ward_id": c.ward_id,
        "assigned_to": c.assigned_to,
        "created_at": c.created_at.isoformat(),
        "attachments": [{"file_path": a.file_path, "original_filename": a.original_filename} for a in c.attachments]
    }

@complaints_bp.route("", methods=["POST"])
@jwt_required()
def create_complaint():
    # Handle multipart form data
    data = request.form.to_dict()
    files = request.files.getlist("attachments")
    
    if not data.get("title") or not data.get("description") or not data.get("voter_id"):
        return error_response("Missing required fields", 400)
        
    complaint, err = ComplaintService.create_complaint(data, files, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(_serialize_complaint(complaint), "Complaint created", 201)

@complaints_bp.route("", methods=["GET"])
@jwt_required()
def get_complaints():
    complaints = ComplaintService.get_complaints()
    return success_response([_serialize_complaint(c) for c in complaints])

@complaints_bp.route("/<complaint_id>", methods=["GET"])
@jwt_required()
def get_complaint(complaint_id):
    complaint = ComplaintService.get_complaint_by_id(complaint_id)
    if not complaint:
        return error_response("Complaint not found", 404)
    return success_response(_serialize_complaint(complaint))

@complaints_bp.route("/<complaint_id>", methods=["PUT"])
@jwt_required()
def update_complaint(complaint_id):
    data = request.get_json()
    complaint, err = ComplaintService.update_complaint(complaint_id, data, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(_serialize_complaint(complaint), "Complaint updated")

@complaints_bp.route("/<complaint_id>", methods=["DELETE"])
@jwt_required()
def delete_complaint(complaint_id):
    success, err = ComplaintService.delete_complaint(complaint_id, get_jwt_identity())
    if err:
        return error_response(err, 400)
    return success_response(message="Complaint deleted")

@complaints_bp.route("/import", methods=["POST"])
@jwt_required()
def import_csv():
    if 'file' not in request.files:
        return error_response("No file uploaded", 400)
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return error_response("File must be a CSV", 400)
        
    result, err = CsvImportService.import_complaints(file, get_jwt_identity())
    if err:
        return error_response(message="Import failed", errors=err, status_code=400)
    return success_response(result, "CSV imported successfully")

@complaints_bp.route("/check-duplicate", methods=["POST"])
@jwt_required()
def check_duplicate():
    data = request.get_json()
    voter_id = data.get("voter_id")
    department_id = data.get("department_id")
    address = data.get("address")
    description = data.get("description")
    
    score = ComplaintService.check_duplicate(voter_id, department_id, address, description)
    return success_response({"duplicate_score": score})
