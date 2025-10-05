"""
Acadefy - AI Tutor Platform
Main Flask application entry point
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
           template_folder='../frontend/templates',
           static_folder='../frontend/static')

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///acadefy.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)

# Import and initialize database
from models import db
db.init_app(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import models and routes after db initialization
from models import Session, Progress, Interaction
from routes.tutor_routes import tutor_bp
from routes.progress_routes import progress_bp

# Register blueprints
app.register_blueprint(tutor_bp, url_prefix='/api')
app.register_blueprint(progress_bp, url_prefix='/api')

# Frontend routes
@app.route('/')
def landing():
    """Landing page route"""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page route"""
    return render_template('dashboard.html')

@app.route('/tutor')
def tutor_chat():
    """AI tutor chat page route"""
    return render_template('tutor.html')

@app.route('/profile')
def profile():
    """User profile page route"""
    return render_template('profile.html')

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal server error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'acadefy-api'})

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info('Database tables created successfully')
    
    print("🎓 Acadefy AI Tutor Platform")
    print("🌐 Server starting at: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 40)
    
    # Run the application
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    try:
        app.run(host='0.0.0.0', port=5000, debug=debug_mode, use_reloader=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check the logs above for details")