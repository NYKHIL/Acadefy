"""
Acadefy Document Routes
Handles document upload, management, and knowledge base operations
"""

from flask import Blueprint, request, jsonify
from services.document_service import DocumentService
import logging

document_bp = Blueprint('documents', __name__)
logger = logging.getLogger(__name__)

# Initialize document service
try:
    doc_service = DocumentService()
    logger.info("Document service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize document service: {e}")
    doc_service = None

@document_bp.route('/documents', methods=['GET'])
def list_documents():
    """
    List all documents in the knowledge base
    """
    try:
        documents = doc_service.list_documents()
        return jsonify({
            'success': True,
            'documents': documents,
            'total_count': len(documents)
        })
    except Exception as e:
        logger.error(f'Error listing documents: {str(e)}')
        return jsonify({'error': 'Failed to list documents'}), 500

@document_bp.route('/documents/add-url', methods=['POST'])
def add_document_from_url():
    """
    Add a document from URL
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        url = data['url']
        title = data.get('title', '')
        
        result = doc_service.add_document_from_url(url, title)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f'Error adding document from URL: {str(e)}')
        return jsonify({'error': 'Failed to add document'}), 500

@document_bp.route('/documents/add-text', methods=['POST'])
def add_document_from_text():
    """
    Add a document from direct text input
    """
    try:
        data = request.get_json()
        
        required_fields = ['content', 'title']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Content and title are required'}), 400
        
        content = data['content']
        title = data['title']
        source = data.get('source', 'manual_input')
        
        result = doc_service.add_document_from_text(content, title, source)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f'Error adding text document: {str(e)}')
        return jsonify({'error': 'Failed to add document'}), 500

@document_bp.route('/documents/<doc_id>', methods=['DELETE'])
def remove_document(doc_id):
    """
    Remove a document from the knowledge base
    """
    try:
        success = doc_service.remove_document(doc_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Document removed successfully'
            })
        else:
            return jsonify({'error': 'Document not found'}), 404
            
    except Exception as e:
        logger.error(f'Error removing document: {str(e)}')
        return jsonify({'error': 'Failed to remove document'}), 500

@document_bp.route('/documents/search', methods=['POST'])
def search_documents():
    """
    Search through documents for relevant content
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        max_results = data.get('max_results', 3)
        
        results = doc_service.search_documents(query, max_results)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results,
            'results_count': len(results)
        })
        
    except Exception as e:
        logger.error(f'Error searching documents: {str(e)}')
        return jsonify({'error': 'Failed to search documents'}), 500

@document_bp.route('/documents/context', methods=['POST'])
def get_document_context():
    """
    Get relevant document context for a query (used by AI service)
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Query is required'}), 400
        
        query = data['query']
        context = doc_service.get_document_context(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'context': context,
            'has_context': bool(context.strip())
        })
        
    except Exception as e:
        logger.error(f'Error getting document context: {str(e)}')
        return jsonify({'error': 'Failed to get context'}), 500

@document_bp.route('/documents/upload-test', methods=['GET'])
def test_upload_endpoint():
    """Test if upload endpoint is accessible"""
    return jsonify({'message': 'Upload endpoint is accessible', 'methods': ['POST']})

@document_bp.route('/documents/upload-new', methods=['POST'])
def upload_document_file_new():
    """
    Upload a document file (PDF, DOCX, PPTX, TXT) - New implementation
    """
    return jsonify({'message': 'New upload endpoint working!', 'success': True})

@document_bp.route('/documents/upload', methods=['POST'])
def upload_document_file():
    """
    Upload a document file (PDF, DOCX, PPTX, TXT)
    """
    try:
        logger.info(f"Upload request received. Files: {list(request.files.keys())}")
        logger.info(f"Form data: {dict(request.form)}")
        
        # Check if file is present
        if 'file' not in request.files:
            logger.error("No 'file' key in request.files")
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        title = request.form.get('title', '')
        
        logger.info(f"File received: {file.filename}, Title: {title}")
        
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        # Use title from form or filename
        if not title:
            title = file.filename
        
        logger.info(f"Processing file: {file.filename} with title: {title}")
        
        if doc_service is None:
            return jsonify({'error': 'Document service not available'}), 500
            
        result = doc_service.add_document_from_file(file, title)
        
        logger.info(f"Upload result: {result}")
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f'Error uploading document: {str(e)}', exc_info=True)
        return jsonify({'error': f'Failed to upload document: {str(e)}'}), 500