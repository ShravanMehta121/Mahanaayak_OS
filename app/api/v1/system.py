import time
import platform
import sys
from flask import Blueprint
from app.utils.responses import success_response
from app.extensions import db

system_bp = Blueprint("system", __name__)
startup_time = time.time()

@system_bp.route("/info", methods=["GET"])
def system_info():
    uptime = time.time() - startup_time
    
    db_status = "Connected"
    try:
        db.session.execute("SELECT 1")
    except Exception:
        db_status = "Disconnected"

    return success_response({
        "version": "1.0.0",
        "build_date": "2026-08-07",
        "environment": "production",
        "database": db_status,
        "python_version": sys.version.split(" ")[0],
        "os": platform.system(),
        "uptime_seconds": round(uptime, 2)
    })
