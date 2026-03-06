from flask import Flask
from flask_cors import CORS
from config import get_config
from api.routes import api_bp
from flask_swagger_ui import get_swaggerui_blueprint
import logging

def create_app():
    """Flask app start"""
    app = Flask(__name__)
    
    # Configuration
    config = get_config()
    app.config.from_object(config)
    
    # CORS
    CORS(app)
    
    # Logging
    logging.basicConfig(level=config.LOG_LEVEL)
    
    # Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/openapi.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': 'AI Bug & Error Root Cause Analyzer'}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    
    return app

    