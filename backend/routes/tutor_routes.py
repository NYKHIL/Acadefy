"""
Acadefy AI Tutor Routes
Handles AI conversation endpoints and context management
"""

from flask import Blueprint, request, jsonify
from models import db, Session, Interaction, Progress
from services.ai_service import AIService
import uuid
import time
import logging

tutor_bp = Blueprint('tutor', __name__)
logger = logging.getLogger(__name__)

@tutor_bp.route('/tutor', methods=['POST'])
def chat_with_tutor():
    """
    Main AI tutor endpoint for processing user messages and generating responses
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get or create session
        session = Session.query.filter_by(session_id=session_id).first()
        if not session:
            session = Session(session_id=session_id)
            db.session.add(session)
            db.session.commit()
        
        # Get conversation context
        context = session.get_context()
        
        # Initialize AI service
        ai_service = AIService()
        
        # Generate AI response with timing
        start_time = time.time()
        ai_response = ai_service.generate_response(
            user_message=user_message,
            context=context,
            session_id=session_id
        )
        response_time = time.time() - start_time
        
        # Update session context
        updated_context = ai_service.update_context(context, user_message, ai_response)
        session.set_context(updated_context)
        
        # Save interaction
        interaction = Interaction(
            session_id=session_id,
            user_message=user_message,
            ai_response=ai_response,
            response_time=response_time
        )
        
        db.session.add(interaction)
        db.session.commit()
        
        # Extract learning insights and update progress
        _update_learning_progress(session_id, user_message, ai_response)
        
        return jsonify({
            'response': ai_response,
            'session_id': session_id,
            'response_time': round(response_time, 2),
            'context_updated': True
        })
        
    except Exception as e:
        logger.error(f'Error in chat_with_tutor: {str(e)}')
        return jsonify({'error': 'Failed to process message'}), 500

@tutor_bp.route('/tutor/context/<session_id>', methods=['GET'])
def get_session_context(session_id):
    """
    Retrieve conversation context for a specific session
    """
    try:
        session = Session.query.filter_by(session_id=session_id).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        context = session.get_context()
        
        return jsonify({
            'session_id': session_id,
            'context': context,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'is_active': session.is_active
        })
        
    except Exception as e:
        logger.error(f'Error getting session context: {str(e)}')
        return jsonify({'error': 'Failed to retrieve context'}), 500

@tutor_bp.route('/tutor/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """
    Retrieve chat history for a specific session
    """
    try:
        interactions = Interaction.query.filter_by(session_id=session_id)\
                                      .order_by(Interaction.timestamp.desc())\
                                      .limit(50).all()
        
        history = []
        for interaction in reversed(interactions):  # Show oldest first
            history.append({
                'id': interaction.id,
                'user_message': interaction.user_message,
                'ai_response': interaction.ai_response,
                'timestamp': interaction.timestamp.isoformat(),
                'response_time': interaction.response_time
            })
        
        return jsonify({
            'session_id': session_id,
            'history': history,
            'total_interactions': len(history)
        })
        
    except Exception as e:
        logger.error(f'Error getting chat history: {str(e)}')
        return jsonify({'error': 'Failed to retrieve history'}), 500

def _update_learning_progress(session_id, user_message, ai_response):
    """
    Analyze conversation and update learning progress
    """
    try:
        # Simple keyword-based subject detection
        subjects = {
            'math': ['math', 'algebra', 'calculus', 'geometry', 'arithmetic', 'equation'],
            'science': ['science', 'physics', 'chemistry', 'biology', 'experiment'],
            'english': ['english', 'grammar', 'writing', 'literature', 'essay'],
            'history': ['history', 'historical', 'war', 'ancient', 'civilization'],
            'programming': ['code', 'programming', 'python', 'javascript', 'algorithm']
        }
        
        detected_subject = 'general'
        user_lower = user_message.lower()
        
        for subject, keywords in subjects.items():
            if any(keyword in user_lower for keyword in keywords):
                detected_subject = subject
                break
        
        # Get or create progress entry
        progress = Progress.query.filter_by(
            session_id=session_id,
            subject=detected_subject
        ).first()
        
        if not progress:
            progress = Progress(
                session_id=session_id,
                subject=detected_subject,
                topic='General Discussion'
            )
            db.session.add(progress)
        
        # Update interaction count
        progress.update_progress(increment_interaction=True)
        
        # Simple completion estimation based on interaction count
        progress.completion_percentage = min(progress.interactions_count * 2, 100)
        
        db.session.commit()
        
    except Exception as e:
        logger.error(f'Error updating learning progress: {str(e)}')