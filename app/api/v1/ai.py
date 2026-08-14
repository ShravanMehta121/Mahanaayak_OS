from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ai.ai_service import AIService
from app.utils.responses import success_response, error_response

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/executive-summary", methods=["POST"])
@jwt_required()
def executive_summary():
    data = request.get_json() or {}
    timeframe = data.get("timeframe", "this week")
    
    result = AIService.process_ai_request(
        prompt_type="executive_summary",
        template_name="executive_summary",
        template_kwargs={"timeframe": timeframe},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/complaint-summary", methods=["POST"])
@jwt_required()
def complaint_summary():
    data = request.get_json() or {}
    description = data.get("description", "")
    
    if not description:
        return error_response("Missing description", 400)
        
    result = AIService.process_ai_request(
        prompt_type="complaint_summary",
        template_name="complaint_summary",
        template_kwargs={"description": description},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/campaign-planner", methods=["POST"])
@jwt_required()
def campaign_planner():
    data = request.get_json() or {}
    context = data.get("context", "General planning")
    
    result = AIService.process_ai_request(
        prompt_type="campaign_planner",
        template_name="campaign_planner",
        template_kwargs={"context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/manifesto", methods=["POST"])
@jwt_required()
def manifesto():
    data = request.get_json() or {}
    context = data.get("context", "Upcoming elections")
    
    result = AIService.process_ai_request(
        prompt_type="manifesto",
        template_name="manifesto_generator",
        template_kwargs={"context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/speech", methods=["POST"])
@jwt_required()
def speech():
    data = request.get_json() or {}
    speech_type = data.get("type", "Public Speech")
    topic = data.get("topic", "General updates")
    
    result = AIService.process_ai_request(
        prompt_type="speech",
        template_name="speech_generator",
        template_kwargs={"type": speech_type, "topic": topic},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/resource-allocation", methods=["POST"])
@jwt_required()
def resource_allocation():
    data = request.get_json() or {}
    context = data.get("context", "City wide resources")
    
    result = AIService.process_ai_request(
        prompt_type="resource_allocation",
        template_name="resource_allocator",
        template_kwargs={"context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/ward-health", methods=["GET"])
@jwt_required()
def ward_health():
    ward_name = request.args.get("ward_name", "All")
    context = request.args.get("context", "General")
    
    result = AIService.process_ai_request(
        prompt_type="ward_health",
        template_name="ward_health",
        template_kwargs={"ward_name": ward_name, "context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/constituency-health", methods=["GET"])
@jwt_required()
def constituency_health():
    context = request.args.get("context", "General")
    
    result = AIService.process_ai_request(
        prompt_type="constituency_health",
        template_name="constituency_health",
        template_kwargs={"context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/priority", methods=["GET"])
@jwt_required()
def priority():
    context = request.args.get("context", "General visit planning")
    
    result = AIService.process_ai_request(
        prompt_type="priority_engine",
        template_name="priority_engine",
        template_kwargs={"context": context},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)

@ai_bp.route("/sentiment", methods=["POST"])
@jwt_required()
def sentiment():
    data = request.get_json() or {}
    text = data.get("text", "")
    
    if not text:
        return error_response("Missing text", 400)
        
    result = AIService.process_ai_request(
        prompt_type="sentiment",
        template_name="sentiment_analysis",
        template_kwargs={"text": text},
        current_user_id=get_jwt_identity()
    )
    return success_response(result)
