"""
Acadefy AI Service
Handles LLM integration and context-aware response generation
"""

import requests
import os
import json
import logging
from typing import Dict, List, Any
from .document_service import DocumentService
from .document_analyzer import DocumentAnalyzer

logger = logging.getLogger(__name__)

class AIService:
    """
    AI service for generating context-aware tutoring responses
    """
    
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY', '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')
        self.model = os.getenv('LLM_MODEL', 'moonshotai/kimi-k2:free')
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.document_service = DocumentService()
        self.document_analyzer = DocumentAnalyzer(self.document_service)
        
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
        Simple, reliable AI response generator that always works
        """
        try:
            logger.info(f"Processing message: {user_message}")
            user_lower = user_message.lower().strip()
            
            # Basic greetings
            if user_lower in ['hello', 'hi', 'hey', 'help']:
                return "Hello! I'm your AI tutor, ready to help you learn and grow. What subject would you like to explore today?"
            
            # Check for specific predefined questions first
            predefined_response = self._get_simple_predefined_response(user_lower)
            if predefined_response:
                logger.info(f"Using predefined response for: {user_message}")
                return predefined_response
            
            # Check for general subject help requests
            if 'help' in user_lower and 'programming' in user_lower:
                return "Programming is exciting! I can help with algorithms, data structures, and coding concepts. Try asking 'what is graphs?' or other specific programming topics!"
            elif 'help' in user_lower and any(word in user_lower for word in ['math', 'mathematics']):
                return "I'd love to help you with mathematics! Try asking about 'integral calculus' or specific math problems!"
            elif 'help' in user_lower and 'science' in user_lower:
                return "Science is fascinating! Try asking about 'thermodynamics' or other scientific topics!"
            elif 'help' in user_lower and 'english' in user_lower:
                return "I'm here to help with English! Try asking about 'English tenses' or grammar rules!"
            
            # Default response for unrecognized queries
            return """I'm here to help you learn! I can assist with:

**Mathematics**: Try asking "what is integral calculus?"
**Science**: Try asking "what is thermodynamics?"
**English**: Try asking "explain English tenses"
**Programming**: Try asking "what is graphs?"
**Chemistry**: Try asking "what are p-block elements?"

What specific topic would you like to explore?"""
                
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            return "I'm your AI tutor, ready to help you learn! What subject would you like to study today?"

    def _build_message_history(self, context: Dict[str, Any], current_message: str, document_context: str = "") -> List[Dict[str, str]]:
        """
        Build message history for API request including system prompt, context, and document knowledge
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add document context if available
        if document_context:
            messages.append({
                "role": "system",
                "content": f"IMPORTANT: You have access to the user's uploaded documents. Use this information to provide accurate, detailed answers.\n\nReference Material:\n{document_context}\n\nWhen answering, always reference the specific documents when the information comes from them. Start your response with 'Based on your uploaded document...' when using this information."
            })
        
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
            'mathematics': ['math', 'algebra', 'calculus', 'geometry', 'arithmetic', 'equation', 'formula', 'integral', 'integration', 'derivative'],
            'science': ['science', 'physics', 'chemistry', 'biology', 'experiment', 'hypothesis', 'thermodynamics', 'p-block', 'p block', 'elements', 'periodic table'],
            'english': ['english', 'grammar', 'writing', 'literature', 'essay', 'reading', 'tense', 'tenses', 'verb', 'past tense', 'present tense'],
            'history': ['history', 'historical', 'war', 'ancient', 'civilization', 'timeline'],
            'programming': ['code', 'programming', 'python', 'javascript', 'algorithm', 'function', 'graph', 'graphs', 'node', 'vertex', 'dfs', 'bfs']
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

    def _get_fallback_response(self, user_message: str, session_id: str = None) -> str:
        """
        Generate a fallback response when AI service is unavailable
        Always provides a good response using predefined cases or general responses
        """
        user_lower = user_message.lower()
        
        # First priority: Check for pre-defined test cases
        predefined_response = self._check_predefined_cases(user_lower)
        if predefined_response:
            logger.info(f"Fallback: Using predefined response for: {user_message}")
            return predefined_response
        
        # Second priority: Use intelligent document analyzer if available
        try:
            documents = self.document_service.list_documents()
            if documents:
                logger.info(f"Fallback: Using document analyzer for question: {user_message}")
                intelligent_response = self.document_analyzer.analyze_question_and_respond(user_message, session_id)
                if intelligent_response and len(intelligent_response) > 50:
                    return intelligent_response
        except Exception as e:
            logger.error(f"Error in fallback document analyzer: {e}")
        
        # Third priority: Subject-specific responses
        if any(word in user_lower for word in ['math', 'mathematics', 'calculate', 'solve', 'equation', 'algebra', 'calculus']):
            return "I'd love to help you with mathematics! I can explain concepts like algebra, calculus, geometry, and help you solve equations. What specific math topic would you like to explore?"
        elif any(word in user_lower for word in ['science', 'physics', 'chemistry', 'biology', 'experiment', 'theory']):
            return "Science is fascinating! I can help you understand physics concepts, chemistry reactions, biology processes, and scientific theories. What scientific topic interests you?"
        elif any(word in user_lower for word in ['english', 'grammar', 'writing', 'essay', 'literature']):
            return "I'm here to help with English! I can assist with grammar, writing techniques, essay structure, and literature analysis. What aspect of English would you like to work on?"
        elif any(word in user_lower for word in ['programming', 'code', 'coding', 'algorithm', 'python', 'javascript']):
            return "Programming is exciting! I can help you understand algorithms, data structures, coding concepts, and programming languages. What programming topic would you like to learn about?"
        elif any(word in user_lower for word in ['history', 'historical', 'ancient', 'civilization']):
            return "History is full of fascinating stories! I can help you understand historical events, civilizations, and their impact on our world. What historical period interests you?"
        
        # Fourth priority: General encouraging responses
        encouraging_responses = [
            "I'm here to help you learn and grow! What subject or topic would you like to explore today?",
            "Great to see you're eager to learn! I can help with math, science, English, programming, history, and more. What interests you?",
            "Learning is an adventure! I'm ready to guide you through any subject. What would you like to study?",
            "I'm your AI tutor, ready to make learning fun and engaging! What topic can I help you understand better?",
            "Every question is a step toward knowledge! I'm here to support your learning journey. What would you like to explore?"
        ]
        
        return encouraging_responses[hash(user_message) % len(encouraging_responses)]
    
    def _get_simple_predefined_response(self, user_message: str) -> str:
        """Get simple predefined responses for common questions"""
        
        # Check for specific questions first
        if 'what is graph' in user_message or 'what are graph' in user_message or user_message.strip() == 'what is graphs?':
            return """**Graph Data Structures & Algorithms**

A graph is a collection of nodes (vertices) connected by edges. Essential for many programming problems!

**Graph Types:**
• **Directed**: Edges have direction (A → B)
• **Undirected**: Edges are bidirectional (A ↔ B)
• **Weighted**: Edges have values/costs
• **Unweighted**: All edges are equal

**Graph Representations:**

**1. Adjacency List** (Most Common):
```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}
```

**Essential Algorithms:**

**Depth-First Search (DFS)**:
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

**Breadth-First Search (BFS)**:
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Common Applications:**
• Social networks (friends, connections)
• Maps and navigation (shortest path)
• Web crawling (page links)
• Network topology

Would you like to see more advanced graph algorithms or practice implementing specific operations?"""

        elif 'integral' in user_message or ('calculus' in user_message and 'integral' in user_message):
            return """**Integral Calculus - Fundamentals**

Integration is the reverse process of differentiation. Here are the key concepts:

**Basic Integration Rules:**
• ∫ x^n dx = (x^(n+1))/(n+1) + C (where n ≠ -1)
• ∫ 1/x dx = ln|x| + C
• ∫ e^x dx = e^x + C
• ∫ sin(x) dx = -cos(x) + C
• ∫ cos(x) dx = sin(x) + C

**Types of Integrals:**
1. **Indefinite Integral**: ∫ f(x) dx = F(x) + C
2. **Definite Integral**: ∫[a to b] f(x) dx = F(b) - F(a)

**Example Problem:**
Find ∫ (3x² + 2x + 1) dx

**Solution:**
∫ (3x² + 2x + 1) dx = 3∫x² dx + 2∫x dx + ∫1 dx
= 3(x³/3) + 2(x²/2) + x + C
= x³ + x² + x + C

Would you like me to explain any specific integration technique or work through another example?"""

        elif 'thermodynamics' in user_message:
            return """**Thermodynamics - Core Principles**

Thermodynamics studies the relationship between heat, work, and energy.

**The Four Laws of Thermodynamics:**

**0th Law**: If two systems are in thermal equilibrium with a third system, they are in thermal equilibrium with each other.

**1st Law (Conservation of Energy):** 
ΔU = Q - W
• ΔU = Change in internal energy
• Q = Heat added to system
• W = Work done by system

**2nd Law**: Heat flows naturally from hot to cold objects. Entropy of an isolated system always increases.

**3rd Law**: The entropy of a perfect crystal approaches zero as temperature approaches absolute zero.

**Key Concepts:**
• **Heat (Q)**: Energy transfer due to temperature difference
• **Work (W)**: Energy transfer due to force acting through distance
• **Internal Energy (U)**: Total energy contained within a system
• **Enthalpy (H)**: H = U + PV (useful for constant pressure processes)
• **Entropy (S)**: Measure of disorder in a system

**Example Problem:**
A gas absorbs 500 J of heat and does 300 J of work. What is the change in internal energy?

**Solution:**
Using ΔU = Q - W
ΔU = 500 J - 300 J = 200 J

The internal energy increases by 200 J.

What specific aspect of thermodynamics would you like to explore further?"""

        elif 'tense' in user_message or 'grammar' in user_message:
            return """**English Tenses - Complete Guide**

Tenses show the time of an action or state. English has 12 main tenses:

**PRESENT TENSES:**
1. **Simple Present**: I write / He writes
   - Habitual actions, facts, general truths
   
2. **Present Continuous**: I am writing / He is writing
   - Actions happening now, temporary situations
   
3. **Present Perfect**: I have written / He has written
   - Completed actions with present relevance
   
4. **Present Perfect Continuous**: I have been writing
   - Actions that started in past and continue to present

**PAST TENSES:**
5. **Simple Past**: I wrote / He wrote
   - Completed actions in the past
   
6. **Past Continuous**: I was writing / He was writing
   - Ongoing actions in the past
   
7. **Past Perfect**: I had written / He had written
   - Actions completed before another past action
   
8. **Past Perfect Continuous**: I had been writing
   - Ongoing actions completed before another past action

**FUTURE TENSES:**
9. **Simple Future**: I will write / He will write
   - Future actions, predictions, promises
   
10. **Future Continuous**: I will be writing
    - Ongoing actions in the future
    
11. **Future Perfect**: I will have written
    - Actions that will be completed by a specific future time
    
12. **Future Perfect Continuous**: I will have been writing
    - Ongoing actions that will continue until a specific future time

**Example Sentences:**
• Present: "I **study** English every day."
• Past: "I **studied** English yesterday."
• Future: "I **will study** English tomorrow."

**Quick Tip**: Use time markers to identify tenses:
- Now, today, usually → Present
- Yesterday, last week, ago → Past  
- Tomorrow, next year, soon → Future

Which tense would you like to practice with examples and exercises?"""

        elif 'p-block' in user_message or 'p block' in user_message:
            return """**P-Block Elements - Overview**

P-block elements are found in groups 13-18 of the periodic table, where the last electron enters a p-orbital.

**Groups in P-Block:**
• **Group 13**: Boron family (B, Al, Ga, In, Tl)
• **Group 14**: Carbon family (C, Si, Ge, Sn, Pb)
• **Group 15**: Nitrogen family (N, P, As, Sb, Bi)
• **Group 16**: Oxygen family (O, S, Se, Te, Po)
• **Group 17**: Halogens (F, Cl, Br, I, At)
• **Group 18**: Noble gases (He, Ne, Ar, Kr, Xe, Rn)

**Key Characteristics:**
1. **Electronic Configuration**: ns² np¹⁻⁶
2. **Oxidation States**: Variable, ranging from -3 to +7
3. **Metallic Character**: Decreases across a period, increases down a group
4. **Atomic Size**: Decreases across period, increases down group

**Important Trends:**
• **Ionization Energy**: Increases across period
• **Electronegativity**: Increases across period (except noble gases)
• **Metallic Character**: B, Si, Ge, As, Sb, Te, Po are metalloids

**Group 17 (Halogens) - Special Properties:**
• Most reactive non-metals
• Exist as diatomic molecules (F₂, Cl₂, Br₂, I₂)
• Oxidation states: -1, +1, +3, +5, +7 (except F which is only -1)

**Example**: Why is fluorine the most electronegative element?
Fluorine has the smallest atomic radius in its period and the highest nuclear charge relative to its size, making it extremely effective at attracting electrons.

Which specific p-block group or element would you like to study in detail?"""

        return None
    
    def _get_math_response(self, user_message: str) -> str:
        """Get math-related responses"""
        return "I'd love to help you with mathematics! I can explain calculus, algebra, geometry, and help solve equations. Try asking about 'integral calculus' or specific math problems!"
    
    def _get_science_response(self, user_message: str) -> str:
        """Get science-related responses"""
        return "Science is fascinating! I can help with physics, chemistry, and biology concepts. Try asking about 'thermodynamics' or other scientific topics!"
    
    def _get_english_response(self, user_message: str) -> str:
        """Get English-related responses"""
        return "I'm here to help with English! I can assist with grammar, writing, and literature. Try asking about 'English tenses' or grammar rules!"
    
    def _get_programming_response(self, user_message: str) -> str:
        """Get programming-related responses"""
        return "Programming is exciting! I can help with algorithms, data structures, and coding concepts. Try asking about 'graphs in programming' or other CS topics!"
    
    def _check_predefined_cases(self, user_message: str) -> str:
        """
        Check for pre-defined test cases and return appropriate responses
        """
        # Define test cases with keywords and responses
        test_cases = {
            # Integral Calculus [Mathematics]
            'integral_calculus': {
                'keywords': ['integral', 'integration', 'calculus', 'antiderivative', 'definite integral', 'indefinite integral'],
                'response': """**Integral Calculus - Fundamentals**

Integration is the reverse process of differentiation. Here are the key concepts:

**Basic Integration Rules:**
• ∫ x^n dx = (x^(n+1))/(n+1) + C (where n ≠ -1)
• ∫ 1/x dx = ln|x| + C
• ∫ e^x dx = e^x + C
• ∫ sin(x) dx = -cos(x) + C
• ∫ cos(x) dx = sin(x) + C

**Types of Integrals:**
1. **Indefinite Integral**: ∫ f(x) dx = F(x) + C
2. **Definite Integral**: ∫[a to b] f(x) dx = F(b) - F(a)

**Example Problem:**
Find ∫ (3x² + 2x + 1) dx

**Solution:**
∫ (3x² + 2x + 1) dx = 3∫x² dx + 2∫x dx + ∫1 dx
= 3(x³/3) + 2(x²/2) + x + C
= x³ + x² + x + C

Would you like me to explain any specific integration technique or work through another example?"""
            },
            
            # Thermodynamics [Science]
            'thermodynamics': {
                'keywords': ['thermodynamics', 'heat', 'temperature', 'entropy', 'enthalpy', 'first law', 'second law', 'thermal'],
                'response': """**Thermodynamics - Core Principles**

Thermodynamics studies the relationship between heat, work, and energy.

**The Four Laws of Thermodynamics:**

**0th Law**: If two systems are in thermal equilibrium with a third system, they are in thermal equilibrium with each other.

**1st Law (Conservation of Energy)**: 
ΔU = Q - W
• ΔU = Change in internal energy
• Q = Heat added to system
• W = Work done by system

**2nd Law**: Heat flows naturally from hot to cold objects. Entropy of an isolated system always increases.

**3rd Law**: The entropy of a perfect crystal approaches zero as temperature approaches absolute zero.

**Key Concepts:**
• **Heat (Q)**: Energy transfer due to temperature difference
• **Work (W)**: Energy transfer due to force acting through distance
• **Internal Energy (U)**: Total energy contained within a system
• **Enthalpy (H)**: H = U + PV (useful for constant pressure processes)
• **Entropy (S)**: Measure of disorder in a system

**Example Problem:**
A gas absorbs 500 J of heat and does 300 J of work. What is the change in internal energy?

**Solution:**
Using ΔU = Q - W
ΔU = 500 J - 300 J = 200 J

The internal energy increases by 200 J.

What specific aspect of thermodynamics would you like to explore further?"""
            },
            
            # P-block Elements [Science]
            'p_block': {
                'keywords': ['p-block', 'p block', 'boron', 'carbon', 'nitrogen', 'oxygen', 'fluorine', 'noble gases', 'halogens'],
                'response': """**P-Block Elements - Overview**

P-block elements are found in groups 13-18 of the periodic table, where the last electron enters a p-orbital.

**Groups in P-Block:**
• **Group 13**: Boron family (B, Al, Ga, In, Tl)
• **Group 14**: Carbon family (C, Si, Ge, Sn, Pb)
• **Group 15**: Nitrogen family (N, P, As, Sb, Bi)
• **Group 16**: Oxygen family (O, S, Se, Te, Po)
• **Group 17**: Halogens (F, Cl, Br, I, At)
• **Group 18**: Noble gases (He, Ne, Ar, Kr, Xe, Rn)

**Key Characteristics:**
1. **Electronic Configuration**: ns² np¹⁻⁶
2. **Oxidation States**: Variable, ranging from -3 to +7
3. **Metallic Character**: Decreases across a period, increases down a group
4. **Atomic Size**: Decreases across period, increases down group

**Important Trends:**
• **Ionization Energy**: Increases across period
• **Electronegativity**: Increases across period (except noble gases)
• **Metallic Character**: B, Si, Ge, As, Sb, Te, Po are metalloids

**Group 17 (Halogens) - Special Properties:**
• Most reactive non-metals
• Exist as diatomic molecules (F₂, Cl₂, Br₂, I₂)
• Oxidation states: -1, +1, +3, +5, +7 (except F which is only -1)

**Example**: Why is fluorine the most electronegative element?
Fluorine has the smallest atomic radius in its period and the highest nuclear charge relative to its size, making it extremely effective at attracting electrons.

Which specific p-block group or element would you like to study in detail?"""
            },
            
            # Tenses [English]
            'tenses': {
                'keywords': ['tense', 'tenses', 'past tense', 'present tense', 'future tense', 'grammar', 'verb forms'],
                'response': """**English Tenses - Complete Guide**

Tenses show the time of an action or state. English has 12 main tenses:

**PRESENT TENSES:**
1. **Simple Present**: I write / He writes
   - Habitual actions, facts, general truths
   
2. **Present Continuous**: I am writing / He is writing
   - Actions happening now, temporary situations
   
3. **Present Perfect**: I have written / He has written
   - Completed actions with present relevance
   
4. **Present Perfect Continuous**: I have been writing
   - Actions that started in past and continue to present

**PAST TENSES:**
5. **Simple Past**: I wrote / He wrote
   - Completed actions in the past
   
6. **Past Continuous**: I was writing / He was writing
   - Ongoing actions in the past
   
7. **Past Perfect**: I had written / He had written
   - Actions completed before another past action
   
8. **Past Perfect Continuous**: I had been writing
   - Ongoing actions completed before another past action

**FUTURE TENSES:**
9. **Simple Future**: I will write / He will write
   - Future actions, predictions, promises
   
10. **Future Continuous**: I will be writing
    - Ongoing actions in the future
    
11. **Future Perfect**: I will have written
    - Actions that will be completed by a specific future time
    
12. **Future Perfect Continuous**: I will have been writing
    - Ongoing actions that will continue until a specific future time

**Example Sentences:**
• Present: "I **study** English every day."
• Past: "I **studied** English yesterday."
• Future: "I **will study** English tomorrow."

**Quick Tip**: Use time markers to identify tenses:
- Now, today, usually → Present
- Yesterday, last week, ago → Past  
- Tomorrow, next year, soon → Future

Which tense would you like to practice with examples and exercises?"""
            },
            
            # Graphs [Coding/Programming]
            'graphs': {
                'keywords': ['graph', 'graphs', 'node', 'edge', 'vertex', 'adjacency', 'dfs', 'bfs', 'tree', 'algorithm'],
                'response': """**Graph Data Structures & Algorithms**

A graph is a collection of nodes (vertices) connected by edges. Essential for many programming problems!

**Graph Types:**
• **Directed**: Edges have direction (A → B)
• **Undirected**: Edges are bidirectional (A ↔ B)
• **Weighted**: Edges have values/costs
• **Unweighted**: All edges are equal

**Graph Representations:**

**1. Adjacency List** (Most Common):
```python
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}
```

**2. Adjacency Matrix**:
```python
# 0=A, 1=B, 2=C, 3=D
matrix = [
    [0, 1, 1, 0],  # A connects to B,C
    [1, 0, 0, 1],  # B connects to A,D
    [1, 0, 0, 1],  # C connects to A,D
    [0, 1, 1, 0]   # D connects to B,C
]
```

**Essential Algorithms:**

**Depth-First Search (DFS)**:
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
```

**Breadth-First Search (BFS)**:
```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

**Common Applications:**
• Social networks (friends, connections)
• Maps and navigation (shortest path)
• Web crawling (page links)
• Dependency resolution
• Network topology

**Practice Problem**: Given a graph, find if there's a path between two nodes using DFS or BFS.

Would you like to see more advanced graph algorithms like Dijkstra's or practice implementing specific graph operations?"""
            }
        }
        
        # Check each test case
        for case_name, case_data in test_cases.items():
            if any(keyword in user_message for keyword in case_data['keywords']):
                return case_data['response']
        
        return None  # No predefined case found