"""
Acadefy Recommendation Service
Generates personalized learning recommendations based on user progress and interactions
"""

import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RecommendationService:
    """
    Service for generating personalized learning recommendations
    """
    
    def __init__(self):
        # Learning resource database
        self.learning_resources = {
            'mathematics': {
                'beginner': [
                    {'title': 'Basic Arithmetic Review', 'type': 'practice', 'difficulty': 1},
                    {'title': 'Introduction to Algebra', 'type': 'lesson', 'difficulty': 2},
                    {'title': 'Fraction Fundamentals', 'type': 'practice', 'difficulty': 2}
                ],
                'intermediate': [
                    {'title': 'Linear Equations Mastery', 'type': 'practice', 'difficulty': 4},
                    {'title': 'Quadratic Functions', 'type': 'lesson', 'difficulty': 5},
                    {'title': 'Geometry Proofs', 'type': 'challenge', 'difficulty': 6}
                ],
                'advanced': [
                    {'title': 'Calculus Derivatives', 'type': 'lesson', 'difficulty': 8},
                    {'title': 'Advanced Statistics', 'type': 'practice', 'difficulty': 9},
                    {'title': 'Mathematical Modeling', 'type': 'project', 'difficulty': 10}
                ]
            },
            'science': {
                'beginner': [
                    {'title': 'Scientific Method Basics', 'type': 'lesson', 'difficulty': 1},
                    {'title': 'Simple Experiments', 'type': 'practice', 'difficulty': 2},
                    {'title': 'States of Matter', 'type': 'lesson', 'difficulty': 2}
                ],
                'intermediate': [
                    {'title': 'Chemical Reactions', 'type': 'practice', 'difficulty': 5},
                    {'title': 'Physics Motion Laws', 'type': 'lesson', 'difficulty': 6},
                    {'title': 'Biology Cell Structure', 'type': 'study', 'difficulty': 4}
                ],
                'advanced': [
                    {'title': 'Organic Chemistry', 'type': 'lesson', 'difficulty': 8},
                    {'title': 'Quantum Physics Intro', 'type': 'challenge', 'difficulty': 9},
                    {'title': 'Molecular Biology', 'type': 'project', 'difficulty': 8}
                ]
            },
            'english': {
                'beginner': [
                    {'title': 'Grammar Fundamentals', 'type': 'practice', 'difficulty': 1},
                    {'title': 'Vocabulary Building', 'type': 'study', 'difficulty': 2},
                    {'title': 'Simple Essay Structure', 'type': 'lesson', 'difficulty': 3}
                ],
                'intermediate': [
                    {'title': 'Advanced Grammar', 'type': 'practice', 'difficulty': 5},
                    {'title': 'Literary Analysis', 'type': 'lesson', 'difficulty': 6},
                    {'title': 'Creative Writing', 'type': 'practice', 'difficulty': 4}
                ],
                'advanced': [
                    {'title': 'Academic Writing', 'type': 'lesson', 'difficulty': 8},
                    {'title': 'Critical Thinking Essays', 'type': 'challenge', 'difficulty': 9},
                    {'title': 'Research Papers', 'type': 'project', 'difficulty': 10}
                ]
            },
            'programming': {
                'beginner': [
                    {'title': 'Programming Basics', 'type': 'lesson', 'difficulty': 1},
                    {'title': 'Variables and Data Types', 'type': 'practice', 'difficulty': 2},
                    {'title': 'Simple Loops', 'type': 'practice', 'difficulty': 3}
                ],
                'intermediate': [
                    {'title': 'Functions and Methods', 'type': 'lesson', 'difficulty': 5},
                    {'title': 'Object-Oriented Programming', 'type': 'lesson', 'difficulty': 6},
                    {'title': 'Data Structures', 'type': 'practice', 'difficulty': 7}
                ],
                'advanced': [
                    {'title': 'Algorithm Design', 'type': 'challenge', 'difficulty': 8},
                    {'title': 'System Architecture', 'type': 'lesson', 'difficulty': 9},
                    {'title': 'Full-Stack Project', 'type': 'project', 'difficulty': 10}
                ]
            }
        }

    def generate_recommendations(self, progress_entries: List, recent_interactions: List) -> List[Dict[str, Any]]:
        """
        Generate personalized learning recommendations
        """
        try:
            recommendations = []
            
            # Analyze current progress
            progress_analysis = self._analyze_progress(progress_entries)
            interaction_analysis = self._analyze_interactions(recent_interactions)
            
            # Generate different types of recommendations
            recommendations.extend(self._get_skill_improvement_recommendations(progress_analysis))
            recommendations.extend(self._get_subject_expansion_recommendations(progress_analysis))
            recommendations.extend(self._get_review_recommendations(progress_analysis))
            recommendations.extend(self._get_challenge_recommendations(progress_analysis))
            
            # Add interaction-based recommendations
            if interaction_analysis['struggling_topics']:
                recommendations.extend(self._get_support_recommendations(interaction_analysis))
            
            # Sort by priority and limit results
            recommendations = sorted(recommendations, key=lambda x: x['priority'], reverse=True)
            return recommendations[:8]  # Return top 8 recommendations
            
        except Exception as e:
            logger.error(f'Error generating recommendations: {str(e)}')
            return self._get_default_recommendations()

    def _analyze_progress(self, progress_entries: List) -> Dict[str, Any]:
        """
        Analyze user progress patterns
        """
        if not progress_entries:
            return {
                'subjects': {},
                'average_skill': 1,
                'total_interactions': 0,
                'strengths': [],
                'weaknesses': []
            }
        
        subjects = {}
        total_skill = 0
        total_interactions = 0
        
        for entry in progress_entries:
            subjects[entry.subject] = {
                'skill_level': entry.skill_level,
                'completion': entry.completion_percentage,
                'interactions': entry.interactions_count,
                'accuracy': entry.accuracy_rate,
                'last_activity': entry.last_interaction
            }
            total_skill += entry.skill_level
            total_interactions += entry.interactions_count
        
        average_skill = total_skill / len(progress_entries)
        
        # Identify strengths and weaknesses
        strengths = [subject for subject, data in subjects.items() 
                    if data['skill_level'] >= average_skill and data['accuracy'] >= 70]
        weaknesses = [subject for subject, data in subjects.items() 
                     if data['skill_level'] < average_skill or data['accuracy'] < 60]
        
        return {
            'subjects': subjects,
            'average_skill': average_skill,
            'total_interactions': total_interactions,
            'strengths': strengths,
            'weaknesses': weaknesses
        }

    def _analyze_interactions(self, recent_interactions: List) -> Dict[str, Any]:
        """
        Analyze recent interaction patterns
        """
        if not recent_interactions:
            return {'struggling_topics': [], 'engagement_level': 'low', 'recent_subjects': []}
        
        # Simple analysis based on message content
        struggling_indicators = ['confused', 'don\'t understand', 'difficult', 'help', 'stuck']
        struggling_count = 0
        recent_subjects = set()
        
        for interaction in recent_interactions:
            user_message = interaction.user_message.lower()
            
            # Check for struggling indicators
            if any(indicator in user_message for indicator in struggling_indicators):
                struggling_count += 1
            
            # Extract subjects mentioned
            for subject in self.learning_resources.keys():
                if subject in user_message or any(keyword in user_message 
                    for keyword in self._get_subject_keywords(subject)):
                    recent_subjects.add(subject)
        
        engagement_level = 'high' if len(recent_interactions) >= 5 else 'medium' if len(recent_interactions) >= 2 else 'low'
        struggling_topics = list(recent_subjects) if struggling_count >= 2 else []
        
        return {
            'struggling_topics': struggling_topics,
            'engagement_level': engagement_level,
            'recent_subjects': list(recent_subjects)
        }

    def _get_skill_improvement_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations for skill improvement
        """
        recommendations = []
        
        for subject, data in analysis['subjects'].items():
            skill_level = data['skill_level']
            accuracy = data['accuracy']
            
            # Recommend practice if accuracy is low
            if accuracy < 70:
                level_category = self._get_level_category(skill_level)
                resources = self.learning_resources.get(subject, {}).get(level_category, [])
                
                for resource in resources[:2]:  # Top 2 resources
                    if resource['type'] == 'practice':
                        recommendations.append({
                            'id': f"skill_improve_{subject}_{resource['title'].replace(' ', '_').lower()}",
                            'type': 'skill_improvement',
                            'title': f"Improve {subject.title()}: {resource['title']}",
                            'description': f"Practice exercises to strengthen your {subject} skills",
                            'subject': subject,
                            'difficulty': resource['difficulty'],
                            'estimated_time': '15-30 minutes',
                            'priority': 8,
                            'resource': resource
                        })
        
        return recommendations

    def _get_subject_expansion_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations for exploring new subjects
        """
        recommendations = []
        current_subjects = set(analysis['subjects'].keys())
        all_subjects = set(self.learning_resources.keys())
        new_subjects = all_subjects - current_subjects
        
        for subject in list(new_subjects)[:2]:  # Recommend up to 2 new subjects
            beginner_resources = self.learning_resources[subject]['beginner']
            
            for resource in beginner_resources[:1]:  # One resource per new subject
                recommendations.append({
                    'id': f"expand_{subject}_{resource['title'].replace(' ', '_').lower()}",
                    'type': 'subject_expansion',
                    'title': f"Explore {subject.title()}: {resource['title']}",
                    'description': f"Start learning {subject} with this beginner-friendly introduction",
                    'subject': subject,
                    'difficulty': resource['difficulty'],
                    'estimated_time': '20-40 minutes',
                    'priority': 6,
                    'resource': resource
                })
        
        return recommendations

    def _get_review_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations for reviewing previous topics
        """
        recommendations = []
        
        for subject, data in analysis['subjects'].items():
            # Recommend review if last activity was more than 3 days ago
            if data['last_activity']:
                days_since = (datetime.utcnow() - data['last_activity']).days
                if days_since >= 3:
                    level_category = self._get_level_category(data['skill_level'])
                    resources = self.learning_resources.get(subject, {}).get(level_category, [])
                    
                    if resources:
                        resource = resources[0]  # First resource for review
                        recommendations.append({
                            'id': f"review_{subject}_{resource['title'].replace(' ', '_').lower()}",
                            'type': 'review',
                            'title': f"Review {subject.title()}: {resource['title']}",
                            'description': f"Refresh your knowledge in {subject} - it's been {days_since} days since your last session",
                            'subject': subject,
                            'difficulty': resource['difficulty'],
                            'estimated_time': '10-20 minutes',
                            'priority': 7,
                            'resource': resource
                        })
        
        return recommendations

    def _get_challenge_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate challenging recommendations for advanced learners
        """
        recommendations = []
        
        for subject in analysis['strengths']:
            data = analysis['subjects'][subject]
            if data['skill_level'] >= 7:  # High skill level
                advanced_resources = self.learning_resources.get(subject, {}).get('advanced', [])
                
                for resource in advanced_resources[:1]:  # One challenge per strong subject
                    if resource['type'] in ['challenge', 'project']:
                        recommendations.append({
                            'id': f"challenge_{subject}_{resource['title'].replace(' ', '_').lower()}",
                            'type': 'challenge',
                            'title': f"Challenge: {resource['title']}",
                            'description': f"Take on an advanced {subject} challenge to push your skills further",
                            'subject': subject,
                            'difficulty': resource['difficulty'],
                            'estimated_time': '45-90 minutes',
                            'priority': 5,
                            'resource': resource
                        })
        
        return recommendations

    def _get_support_recommendations(self, interaction_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate support recommendations for struggling topics
        """
        recommendations = []
        
        for subject in interaction_analysis['struggling_topics']:
            beginner_resources = self.learning_resources.get(subject, {}).get('beginner', [])
            
            for resource in beginner_resources[:1]:  # One support resource per struggling topic
                recommendations.append({
                    'id': f"support_{subject}_{resource['title'].replace(' ', '_').lower()}",
                    'type': 'support',
                    'title': f"Get Help with {subject.title()}: {resource['title']}",
                    'description': f"Build a stronger foundation in {subject} with guided practice",
                    'subject': subject,
                    'difficulty': resource['difficulty'],
                    'estimated_time': '25-45 minutes',
                    'priority': 9,
                    'resource': resource
                })
        
        return recommendations

    def _get_level_category(self, skill_level: int) -> str:
        """
        Convert skill level to category
        """
        if skill_level <= 3:
            return 'beginner'
        elif skill_level <= 7:
            return 'intermediate'
        else:
            return 'advanced'

    def _get_subject_keywords(self, subject: str) -> List[str]:
        """
        Get keywords associated with a subject
        """
        keywords = {
            'mathematics': ['math', 'algebra', 'calculus', 'geometry', 'arithmetic'],
            'science': ['physics', 'chemistry', 'biology', 'experiment'],
            'english': ['grammar', 'writing', 'literature', 'essay'],
            'programming': ['code', 'python', 'javascript', 'algorithm'],
            'history': ['historical', 'ancient', 'civilization']
        }
        return keywords.get(subject, [])

    def _get_default_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get default recommendations when analysis fails
        """
        return [
            {
                'id': 'default_math_basics',
                'type': 'getting_started',
                'title': 'Start with Math Basics',
                'description': 'Begin your learning journey with fundamental mathematics',
                'subject': 'mathematics',
                'difficulty': 1,
                'estimated_time': '20-30 minutes',
                'priority': 7,
                'resource': {'title': 'Basic Arithmetic Review', 'type': 'practice', 'difficulty': 1}
            },
            {
                'id': 'default_science_intro',
                'type': 'getting_started',
                'title': 'Introduction to Science',
                'description': 'Explore the scientific method and basic concepts',
                'subject': 'science',
                'difficulty': 1,
                'estimated_time': '15-25 minutes',
                'priority': 6,
                'resource': {'title': 'Scientific Method Basics', 'type': 'lesson', 'difficulty': 1}
            }
        ]