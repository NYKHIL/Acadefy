"""
Acadefy Database Models
Defines the data structure for sessions, progress tracking, and user interactions
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# db will be imported and initialized in app.py
db = SQLAlchemy()

class Session(db.Model):
    """
    User session model for tracking chat sessions and context
    """
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.String(100), nullable=True)  # Optional user identification
    context_data = db.Column(db.Text, nullable=True)  # JSON string of conversation context
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationship with progress
    progress_entries = db.relationship('Progress', backref='session', lazy=True)
    
    def __repr__(self):
        return f'<Session {self.session_id}>'
    
    def get_context(self):
        """Parse and return context data as dictionary"""
        if self.context_data:
            try:
                return json.loads(self.context_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def set_context(self, context_dict):
        """Set context data from dictionary"""
        self.context_data = json.dumps(context_dict)
        self.updated_at = datetime.utcnow()

class Progress(db.Model):
    """
    Learning progress model for tracking user advancement and achievements
    """
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('sessions.session_id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)  # e.g., "Mathematics", "Science"
    topic = db.Column(db.String(200), nullable=False)    # e.g., "Algebra", "Physics"
    skill_level = db.Column(db.Integer, default=1)       # 1-10 proficiency scale
    completion_percentage = db.Column(db.Float, default=0.0)  # 0.0-100.0
    interactions_count = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
    last_interaction = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Progress {self.subject}:{self.topic} - {self.skill_level}>'
    
    @property
    def accuracy_rate(self):
        """Calculate accuracy percentage"""
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100
    
    def update_progress(self, is_correct=None, increment_interaction=True):
        """Update progress metrics"""
        if increment_interaction:
            self.interactions_count += 1
        
        if is_correct is not None:
            self.total_questions += 1
            if is_correct:
                self.correct_answers += 1
        
        self.last_interaction = datetime.utcnow()
        
        # Auto-adjust skill level based on accuracy
        if self.total_questions >= 5:  # Minimum questions for skill assessment
            accuracy = self.accuracy_rate
            if accuracy >= 80 and self.skill_level < 10:
                self.skill_level += 1
            elif accuracy < 50 and self.skill_level > 1:
                self.skill_level -= 1

class Interaction(db.Model):
    """
    Individual chat interactions for maintaining conversation history
    """
    __tablename__ = 'interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('sessions.session_id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    response_time = db.Column(db.Float, nullable=True)  # Response time in seconds
    feedback_rating = db.Column(db.Integer, nullable=True)  # 1-5 rating
    
    def __repr__(self):
        return f'<Interaction {self.id} - {self.timestamp}>'