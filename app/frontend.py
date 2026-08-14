import os
from flask import Blueprint, send_from_directory, current_app

# Define the absolute path to the frontend folder
FRONTEND_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frontend')

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_index():
    return send_from_directory(FRONTEND_FOLDER, 'login.html')

@frontend_bp.route('/<path:path>')
def serve_root_files(path):
    if os.path.exists(os.path.join(FRONTEND_FOLDER, path)):
        return send_from_directory(FRONTEND_FOLDER, path)
    return "Not Found", 404

@frontend_bp.route('/admin/<path:path>')
def serve_admin_pages(path):
    admin_folder = os.path.join(FRONTEND_FOLDER, 'admin')
    if os.path.exists(os.path.join(admin_folder, path)):
        return send_from_directory(admin_folder, path)
    return "Not Found", 404

@frontend_bp.route('/member/<path:path>')
def serve_member_pages(path):
    member_folder = os.path.join(FRONTEND_FOLDER, 'user')
    if os.path.exists(os.path.join(member_folder, path)):
        return send_from_directory(member_folder, path)
    return "Not Found", 404
