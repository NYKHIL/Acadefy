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
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'documents/uploads'

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
from routes.document_routes import document_bp

# Register blueprints
app.register_blueprint(tutor_bp, url_prefix='/api')
app.register_blueprint(progress_bp, url_prefix='/api')
app.register_blueprint(document_bp, url_prefix='/api')

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

@app.route('/api/upload-direct', methods=['POST'])
def upload_direct():
    """Direct upload route for testing"""
    try:
        from services.document_service import DocumentService
        doc_service = DocumentService()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        title = request.form.get('title', file.filename)
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        result = doc_service.add_document_from_file(file, title)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-upload')
def test_upload():
    """Test upload page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Test File Upload</title></head>
    <body>
        <h1>Test File Upload</h1>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" id="fileInput" name="file" accept=".pdf,.docx,.pptx,.txt"><br><br>
            <input type="text" id="titleInput" name="title" placeholder="Title (optional)"><br><br>
            <button type="submit">Upload</button>
        </form>
        <div id="result"></div>
        <script>
            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const fileInput = document.getElementById('fileInput');
                const titleInput = document.getElementById('titleInput');
                const resultDiv = document.getElementById('result');
                
                if (!fileInput.files[0]) {
                    resultDiv.innerHTML = 'Please select a file';
                    return;
                }
                
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('title', titleInput.value || fileInput.files[0].name);
                
                try {
                    resultDiv.innerHTML = 'Uploading...';
                    const response = await fetch('/api/documents/upload', {
                        method: 'POST',
                        body: formData
                    });
                    const result = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
                    } else {
                        resultDiv.innerHTML = '<pre>Error: ' + JSON.stringify(result, null, 2) + '</pre>';
                    }
                } catch (error) {
                    resultDiv.innerHTML = 'Error: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    '''

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

@app.route('/routes')
def list_routes():
    """List all available routes"""
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'rule': str(rule)
        })
    return jsonify({'routes': routes})

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