from flask import Flask, jsonify
from app.core.config import config_by_name
from app.core.logger import configure_logging
from app.core.exceptions import register_error_handlers
from app.extensions import db, migrate, jwt, cors
from app.api.v1 import api_v1_bp
from app.models.token_blocklist import TokenBlocklist
from app.core.seeder import seed_data
from app.frontend import frontend_bp

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Configure logging
    configure_logging(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register blueprints
    app.register_blueprint(api_v1_bp)
    app.register_blueprint(frontend_bp)

    # Register global error handlers
    register_error_handlers(app)
    
    # Configure JWT token blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token is not None

    # Register CLI Commands
    app.cli.add_command(seed_data)

    # Removed the basic index route so frontend_bp handles /

    return app
