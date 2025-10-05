"""
Acadefy Progress Routes
Handles learning progress tracking and recommendations
"""

from flask import Blueprint, request, jsonify
from models import db, Session, Progress, Interaction
from services.recommendation_service import RecommendationService
import logging
from datetime import datetime, timedelta

progress_bp = Blueprint('progress', __name__)
logger = logging.getLogger(__name__)

@progress_bp.route('/progress', methods=['GET'])
def get_user_progress():
    """
    Retrieve learning progress for a user session
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Get all progress entries for the session
        progress_entries = Progress.query.filter_by(session_id=session_id).all()
        
        if not progress_entries:
            return jsonify({
                'session_id': session_id,
                'progress': [],
                'overall_stats': {
                    'total_subjects': 0,
                    'average_skill_level': 0,
                    'total_interactions': 0,
                    'overall_completion': 0
                }
            })
        
        # Format progress data
        progress_data = []
        total_skill = 0
        total_interactions = 0
        total_completion = 0
        
        for entry in progress_entries:
            progress_data.append({
                'id': entry.id,
                'subject': entry.subject,
                'topic': entry.topic,
                'skill_level': entry.skill_level,
                'completion_percentage': entry.completion_percentage,
                'interactions_count': entry.interactions_count,
                'accuracy_rate': entry.accuracy_rate,
                'last_interaction': entry.last_interaction.isoformat(),
                'created_at': entry.created_at.isoformat()
            })
            
            total_skill += entry.skill_level
            total_interactions += entry.interactions_count
            total_completion += entry.completion_percentage
        
        # Calculate overall statistics
        num_subjects = len(progress_entries)
        overall_stats = {
            'total_subjects': num_subjects,
            'average_skill_level': round(total_skill / num_subjects, 1),
            'total_interactions': total_interactions,
            'overall_completion': round(total_completion / num_subjects, 1)
        }
        
        return jsonify({
            'session_id': session_id,
            'progress': progress_data,
            'overall_stats': overall_stats
        })
        
    except Exception as e:
        logger.error(f'Error getting user progress: {str(e)}')
        return jsonify({'error': 'Failed to retrieve progress'}), 500

@progress_bp.route('/progress', methods=['POST'])
def update_progress():
    """
    Update learning progress for a specific subject/topic
    """
    try:
        data = request.get_json()
        
        required_fields = ['session_id', 'subject']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Session ID and subject are required'}), 400
        
        session_id = data['session_id']
        subject = data['subject']
        topic = data.get('topic', 'General')
        
        # Get or create progress entry
        progress = Progress.query.filter_by(
            session_id=session_id,
            subject=subject,
            topic=topic
        ).first()
        
        if not progress:
            progress = Progress(
                session_id=session_id,
                subject=subject,
                topic=topic
            )
            db.session.add(progress)
        
        # Update fields if provided
        if 'skill_level' in data:
            progress.skill_level = max(1, min(10, data['skill_level']))
        
        if 'completion_percentage' in data:
            progress.completion_percentage = max(0, min(100, data['completion_percentage']))
        
        if 'is_correct' in data:
            progress.update_progress(is_correct=data['is_correct'])
        else:
            progress.update_progress()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Progress updated successfully',
            'progress': {
                'subject': progress.subject,
                'topic': progress.topic,
                'skill_level': progress.skill_level,
                'completion_percentage': progress.completion_percentage,
                'accuracy_rate': progress.accuracy_rate
            }
        })
        
    except Exception as e:
        logger.error(f'Error updating progress: {str(e)}')
        return jsonify({'error': 'Failed to update progress'}), 500

@progress_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get personalized learning recommendations based on progress
    """
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Get user progress and interaction history
        progress_entries = Progress.query.filter_by(session_id=session_id).all()
        recent_interactions = Interaction.query.filter_by(session_id=session_id)\
                                             .order_by(Interaction.timestamp.desc())\
                                             .limit(10).all()
        
        # Generate recommendations
        recommendation_service = RecommendationService()
        recommendations = recommendation_service.generate_recommendations(
            progress_entries=progress_entries,
            recent_interactions=recent_interactions
        )
        
        return jsonify({
            'session_id': session_id,
            'recommendations': recommendations,
            'generated_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f'Error generating recommendations: {str(e)}')
        return jsonify({'error': 'Failed to generate recommendations'}), 500

@progress_bp.route('/analytics', methods=['GET'])
def get_learning_analytics():
    """
    Get detailed learning analytics and insights
    """
    try:
        session_id = request.args.get('session_id')
        days = int(request.args.get('days', 7))  # Default to last 7 days
        
        if not session_id:
            return jsonify({'error': 'Session ID is required'}), 400
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get interactions within date range
        interactions = Interaction.query.filter(
            Interaction.session_id == session_id,
            Interaction.timestamp >= start_date,
            Interaction.timestamp <= end_date
        ).all()
        
        # Calculate analytics
        total_interactions = len(interactions)
        avg_response_time = sum(i.response_time or 0 for i in interactions) / max(total_interactions, 1)
        
        # Daily interaction counts
        daily_counts = {}
        for interaction in interactions:
            date_key = interaction.timestamp.date().isoformat()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        # Subject distribution
        progress_entries = Progress.query.filter_by(session_id=session_id).all()
        subject_stats = {}
        
        for entry in progress_entries:
            subject_stats[entry.subject] = {
                'interactions': entry.interactions_count,
                'skill_level': entry.skill_level,
                'completion': entry.completion_percentage,
                'accuracy': entry.accuracy_rate
            }
        
        return jsonify({
            'session_id': session_id,
            'period': f'{days} days',
            'analytics': {
                'total_interactions': total_interactions,
                'average_response_time': round(avg_response_time, 2),
                'daily_interactions': daily_counts,
                'subject_statistics': subject_stats,
                'learning_streak': _calculate_learning_streak(interactions)
            }
        })
        
    except Exception as e:
        logger.error(f'Error generating analytics: {str(e)}')
        return jsonify({'error': 'Failed to generate analytics'}), 500

def _calculate_learning_streak(interactions):
    """
    Calculate consecutive days of learning activity
    """
    if not interactions:
        return 0
    
    # Get unique dates of interactions
    interaction_dates = set()
    for interaction in interactions:
        interaction_dates.add(interaction.timestamp.date())
    
    # Sort dates in descending order
    sorted_dates = sorted(interaction_dates, reverse=True)
    
    if not sorted_dates:
        return 0
    
    # Calculate streak from most recent date
    streak = 0
    current_date = datetime.utcnow().date()
    
    for date in sorted_dates:
        if date == current_date or (current_date - date).days == streak + 1:
            streak += 1
            current_date = date
        else:
            break
    
    return streak