from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import io
from app.services.report_service import ReportService
from app.utils.responses import error_response

reports_bp = Blueprint("reports", __name__)

def generate_report_response(title, data, headers, fmt, user_id):
    if fmt == 'csv':
        file_data = ReportService.generate_csv(data, headers, user_id)
        mimetype = 'text/csv'
        ext = 'csv'
    elif fmt == 'excel':
        file_data = ReportService.generate_excel(data, headers, user_id)
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ext = 'xlsx'
    elif fmt == 'pdf':
        file_data = ReportService.generate_pdf(data, headers, title, user_id)
        mimetype = 'application/pdf'
        ext = 'pdf'
    else:
        return error_response("Invalid format. Use csv, excel, or pdf.", 400)
        
    return send_file(
        io.BytesIO(file_data),
        mimetype=mimetype,
        as_attachment=True,
        download_name=f"{title}.{ext}"
    )

# Mocked data generation functions for the reports
def get_mock_data():
    return [["Row 1 Data A", "Row 1 Data B"], ["Row 2 Data A", "Row 2 Data B"]]

@reports_bp.route("/daily", methods=["GET"])
@jwt_required()
def daily_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Daily_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())

@reports_bp.route("/weekly", methods=["GET"])
@jwt_required()
def weekly_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Weekly_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())

@reports_bp.route("/monthly", methods=["GET"])
@jwt_required()
def monthly_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Monthly_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())

@reports_bp.route("/department", methods=["GET"])
@jwt_required()
def department_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Department_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())

@reports_bp.route("/ward", methods=["GET"])
@jwt_required()
def ward_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Ward_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())

@reports_bp.route("/member", methods=["GET"])
@jwt_required()
def member_report():
    fmt = request.args.get('format', 'csv').lower()
    return generate_report_response("Member_Report", get_mock_data(), ["Col A", "Col B"], fmt, get_jwt_identity())
