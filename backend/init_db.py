"""
Acadefy Database Initialization
Creates database tables and sets up initial data
"""

import os
import sys
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Session, Progress, Interaction

def init_database():
    """
    Initialize the database with tables and sample data
    """
    print("Initializing Acadefy database...")
    
    with app.app_context():
        try:
            # Drop all tables (for development)
            db.drop_all()
            print("Dropped existing tables")
            
            # Create all tables
            db.create_all()
            print("Created database tables successfully")
            
            # Create sample data for demonstration
            create_sample_data()
            
            print("Database initialization completed successfully!")
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            return False
    
    return True

def create_sample_data():
    """
    Create sample data for demonstration purposes
    """
    try:
        # Create a sample session
        sample_session = Session(
            session_id="demo_session_001",
            user_id="demo_user",
            context_data='{"current_subject": "mathematics", "skill_level": 5, "learning_goals": ["algebra mastery"], "interaction_count": 3}'
        )
        db.session.add(sample_session)
        
        # Create sample progress entries
        math_progress = Progress(
            session_id="demo_session_001",
            subject="mathematics",
            topic="Algebra Basics",
            skill_level=5,
            completion_percentage=65.0,
            interactions_count=8,
            correct_answers=6,
            total_questions=8
        )
        
        science_progress = Progress(
            session_id="demo_session_001",
            subject="science",
            topic="Physics Fundamentals",
            skill_level=3,
            completion_percentage=30.0,
            interactions_count=4,
            correct_answers=2,
            total_questions=4
        )
        
        db.session.add(math_progress)
        db.session.add(science_progress)
        
        # Create sample interactions
        interactions = [
            Interaction(
                session_id="demo_session_001",
                user_message="Can you help me understand linear equations?",
                ai_response="I'd be happy to help you with linear equations! A linear equation is an equation that makes a straight line when graphed. The general form is y = mx + b, where m is the slope and b is the y-intercept. Would you like me to walk through an example?",
                response_time=1.2
            ),
            Interaction(
                session_id="demo_session_001",
                user_message="Yes, please show me an example",
                ai_response="Great! Let's look at the equation y = 2x + 3. Here, the slope (m) is 2, which means for every 1 unit we move right on the x-axis, we move up 2 units on the y-axis. The y-intercept (b) is 3, so the line crosses the y-axis at point (0, 3). Try plotting a few points: when x = 0, y = 3; when x = 1, y = 5; when x = 2, y = 7. Do you see the pattern?",
                response_time=1.8
            ),
            Interaction(
                session_id="demo_session_001",
                user_message="I think I understand! Can we try a physics problem now?",
                ai_response="Absolutely! I'm glad you're feeling confident with linear equations. Let's switch to physics. What area of physics interests you? We could explore motion, forces, energy, or waves. What would you like to start with?",
                response_time=1.1
            )
        ]
        
        for interaction in interactions:
            db.session.add(interaction)
        
        # Commit all changes
        db.session.commit()
        print("Sample data created successfully")
        
    except Exception as e:
        print(f"Error creating sample data: {str(e)}")
        db.session.rollback()

if __name__ == "__main__":
    if init_database():
        print("\n✅ Database setup complete!")
        print("You can now run the application with: python app.py")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)