"""
Acadefy AI Service
Handles LLM integration and context-aware response generation
"""

import requests
import os
import json
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class AIService:
    """
    AI service for generating context-aware tutoring responses
    """
    
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY', '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')
        self.model = os.getenv('LLM_MODEL', 'moonshotai/kimi-k2:free')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Tutoring system prompt
        self.system_prompt = """You are Acadefy, an intelligent AI tutor designed to provide personalized, adaptive learning support. Your role is to:

1. Provide clear, educational explanations tailored to the student's level
2. Ask probing questions to assess understanding
3. Offer encouragement and positive reinforcement
4. Break down complex topics into manageable steps
5. Adapt your teaching style based on the student's responses and progress
6. Suggest practice exercises and learning resources when appropriate

Guidelines:
- Be patient, encouraging, and supportive
- Use examples and analogies to clarify concepts
- Check for understanding before moving to new topics
- Provide hints rather than direct answers when possible
- Celebrate progress and learning milestones
- Keep responses concise but comprehensive
- Always maintain a friendly, professional tutoring tone"""

    def generate_response(self, user_message: str, context: Dict[str, Any], session_id: str) -> str:
        """
        Generate AI response with context awareness
        """
        try:
            # Build conversation history from context
            messages = self._build_message_history(context, user_message)
            
            # Prepare API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 0.9
            }
            
            # Make API request
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                logger.info(f"AI response generated successfully for session {session_id}")
                return ai_response
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return self._get_fallback_response(user_message)
                
        except requests.exceptions.Timeout:
            logger.error("API request timed out")
            return "I apologize, but I'm experiencing some delays. Could you please repeat your question?"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return self._get_fallback_response(user_message)
            
        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {str(e)}")
            return "I encountered an unexpected issue. Let me try to help you with that question again."

    def _build_message_history(self, context: Dict[str, Any], current_message: str) -> List[Dict[str, str]]:
        """
        Build message history for API request including system prompt and context
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context-based personalization
        if context:
            context_summary = self._summarize_context(context)
            if context_summary:
                messages.append({
                    "role": "system", 
                    "content": f"Context from previous interactions: {context_summary}"
                })
        
        # Add recent conversation history if available
        conversation_history = context.get('recent_messages', [])
        for msg in conversation_history[-6:]:  # Last 6 messages for context
            messages.append(msg)
        
        # Add current user message
        messages.append({"role": "user", "content": current_message})
        
        return messages

    def _summarize_context(self, context: Dict[str, Any]) -> str:
        """
        Create a summary of the conversation context
        """
        summary_parts = []
        
        if context.get('current_subject'):
            summary_parts.append(f"Currently studying: {context['current_subject']}")
        
        if context.get('skill_level'):
            summary_parts.append(f"Skill level: {context['skill_level']}/10")
        
        if context.get('learning_goals'):
            summary_parts.append(f"Learning goals: {', '.join(context['learning_goals'])}")
        
        if context.get('difficulty_areas'):
            summary_parts.append(f"Areas needing help: {', '.join(context['difficulty_areas'])}")
        
        return ". ".join(summary_parts) if summary_parts else ""

    def update_context(self, current_context: Dict[str, Any], user_message: str, ai_response: str) -> Dict[str, Any]:
        """
        Update conversation context with new interaction
        """
        updated_context = current_context.copy()
        
        # Initialize context structure if empty
        if not updated_context:
            updated_context = {
                'recent_messages': [],
                'current_subject': None,
                'skill_level': 5,
                'learning_goals': [],
                'difficulty_areas': [],
                'interaction_count': 0
            }
        
        # Add new messages to history
        recent_messages = updated_context.get('recent_messages', [])
        recent_messages.extend([
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": ai_response}
        ])
        
        # Keep only recent messages (last 10)
        updated_context['recent_messages'] = recent_messages[-10:]
        
        # Update interaction count
        updated_context['interaction_count'] = updated_context.get('interaction_count', 0) + 1
        
        # Extract subject from user message
        detected_subject = self._detect_subject(user_message)
        if detected_subject:
            updated_context['current_subject'] = detected_subject
        
        # Extract learning goals and difficulties
        self._extract_learning_insights(user_message, ai_response, updated_context)
        
        return updated_context

    def _detect_subject(self, message: str) -> str:
        """
        Detect the subject being discussed
        """
        subjects = {
            'mathematics': ['math', 'algebra', 'calculus', 'geometry', 'arithmetic', 'equation', 'formula'],
            'science': ['science', 'physics', 'chemistry', 'biology', 'experiment', 'hypothesis'],
            'english': ['english', 'grammar', 'writing', 'literature', 'essay', 'reading'],
            'history': ['history', 'historical', 'war', 'ancient', 'civilization', 'timeline'],
            'programming': ['code', 'programming', 'python', 'javascript', 'algorithm', 'function']
        }
        
        message_lower = message.lower()
        for subject, keywords in subjects.items():
            if any(keyword in message_lower for keyword in keywords):
                return subject
        
        return None

    def _extract_learning_insights(self, user_message: str, ai_response: str, context: Dict[str, Any]):
        """
        Extract learning insights from the conversation
        """
        user_lower = user_message.lower()
        
        # Detect difficulty indicators
        difficulty_phrases = ['confused', 'don\'t understand', 'difficult', 'hard', 'stuck', 'help']
        if any(phrase in user_lower for phrase in difficulty_phrases):
            subject = context.get('current_subject', 'general')
            difficulty_areas = context.get('difficulty_areas', [])
            if subject not in difficulty_areas:
                difficulty_areas.append(subject)
                context['difficulty_areas'] = difficulty_areas[-5:]  # Keep last 5
        
        # Detect learning goals
        goal_phrases = ['want to learn', 'need to understand', 'studying for', 'preparing for']
        for phrase in goal_phrases:
            if phrase in user_lower:
                # Extract potential goal (simple heuristic)
                words_after = user_lower.split(phrase, 1)
                if len(words_after) > 1:
                    potential_goal = words_after[1].strip()[:50]  # First 50 chars
                    learning_goals = context.get('learning_goals', [])
                    if potential_goal not in learning_goals:
                        learning_goals.append(potential_goal)
                        context['learning_goals'] = learning_goals[-3:]  # Keep last 3

    def _get_fallback_response(self, user_message: str) -> str:
        """
        Generate a fallback response when AI service is unavailable
        """
        fallback_responses = [
            "I'm here to help you learn! Could you tell me more about what you're studying?",
            "That's an interesting question! Let me help you work through this step by step.",
            "I'd be happy to assist you with your learning. What specific topic would you like to explore?",
            "Great question! Let's break this down together. What part would you like to focus on first?",
            "I'm here to support your learning journey. Could you provide a bit more context about what you need help with?"
        ]
        
        # Simple keyword-based response selection
        user_lower = user_message.lower()
        if any(word in user_lower for word in ['math', 'calculate', 'solve']):
            return "I'd love to help you with math! Could you share the specific problem or concept you're working on?"
        elif any(word in user_lower for word in ['write', 'essay', 'grammar']):
            return "Writing is a great skill to develop! What type of writing are you working on, and how can I assist you?"
        elif any(word in user_lower for word in ['science', 'experiment', 'theory']):
            return "Science is fascinating! What scientific concept or topic would you like to explore together?"
        
        return fallback_responses[hash(user_message) % len(fallback_responses)]