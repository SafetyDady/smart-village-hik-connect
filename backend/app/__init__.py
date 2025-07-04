"""
Smart Village HIK Connect - Flask Application Factory
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name=None):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    
    # Database configuration
    database_uri = os.getenv('DATABASE_URI', 'sqlite:///smart_village.db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Initialize extensions with app
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, origins=['*'])  # Allow all origins for development
    
    # Register blueprints
    from app.routes.camera import camera_bp
    from app.routes.vehicle import vehicle_bp
    from app.routes.gate import gate_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(camera_bp, url_prefix='/api/camera')
    app.register_blueprint(vehicle_bp, url_prefix='/api/vehicle')
    app.register_blueprint(gate_bp, url_prefix='/api/gate')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {
            'status': 'healthy',
            'service': 'Smart Village HIK Connect Backend',
            'version': '1.0.0'
        }
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
    
    return app

