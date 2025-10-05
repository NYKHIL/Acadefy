"""
Acadefy Document Analyzer
Intelligent document analysis and question answering system
"""

import re
import logging
from typing import Dict, List, Any, Optional
from collections import Counter
import json

logger = logging.getLogger(__name__)

class DocumentAnalyzer:
    """
    ChatGPT-like document analyzer that provides natural, conversational responses
    with deep understanding and contextual awareness
    """
    
    def __init__(self, document_service):
        self.document_service = document_service
        self.analysis_cache = {}
        self.document_context = {}
        self.conversation_memory = {}
        
    def analyze_question_and_respond(self, question: str, session_id: str = None) -> str:
        """
        Analyze a question and provide an intelligent, understanding-based response
        """
        try:
            # Get all available documents
            documents = self.document_service.list_documents()
            
            if not documents:
                return "I don't have any uploaded documents to reference. Please upload some documents first, and I'll be happy to help answer questions about them!"
            
            logger.info(f"Analyzing question: '{question}' with {len(documents)} available documents")
            
            # Build comprehensive knowledge base from documents
            knowledge_base = self._build_knowledge_base(documents)
            
            # Analyze the question to understand what's being asked
            question_intent = self._understand_question_intent(question)
            logger.info(f"Question intent: {question_intent}")
            
            # Generate intelligent, conceptual response
            response = self._generate_conceptual_response(question, question_intent, knowledge_base)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in document analysis: {str(e)}")
            return "I encountered an error while analyzing your documents. Please try rephrasing your question."
    
    def _build_knowledge_base(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build a comprehensive knowledge base from uploaded documents
        """
        knowledge = {
            'concepts': {},
            'processes': {},
            'definitions': {},
            'relationships': {},
            'facts': {},
            'examples': {},
            'equations': {},
            'applications': {}
        }
        
        for doc in documents:
            doc_data = self.document_service.knowledge_base.get(doc['id'])
            if not doc_data:
                continue
                
            content = doc_data['content']
            
            # Extract different types of knowledge
            self._extract_definitions(content, knowledge['definitions'])
            self._extract_processes(content, knowledge['processes'])
            self._extract_concepts(content, knowledge['concepts'])
            self._extract_relationships(content, knowledge['relationships'])
            self._extract_facts(content, knowledge['facts'])
            self._extract_equations(content, knowledge['equations'])
            self._extract_applications(content, knowledge['applications'])
        
        return knowledge
    
    def _extract_definitions(self, content: str, definitions: Dict[str, str]):
        """Extract definitions from content"""
        # Look for definition patterns
        definition_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an|the)\s+([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+are\s+([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+means\s+([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+refers\s+to\s+([^.!?]+[.!?])'
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                term = match[0].strip()
                definition = match[1].strip()
                if len(term) > 2 and len(definition) > 10:
                    definitions[term.lower()] = definition
    
    def _extract_processes(self, content: str, processes: Dict[str, List[str]]):
        """Extract process descriptions and steps"""
        # Look for numbered steps or process descriptions
        step_patterns = [
            r'(\d+)\.\s+([^.!?]+[.!?])',
            r'(First|Second|Third|Fourth|Fifth|Next|Then|Finally)[,:]?\s+([^.!?]+[.!?])',
            r'(Stage\s+\d+|Step\s+\d+)[:\s]+([^.!?]+[.!?])'
        ]
        
        current_process = None
        
        # Look for process indicators
        process_indicators = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:process|occurs|happens|involves)', content, re.IGNORECASE)
        
        for indicator in process_indicators:
            process_name = indicator.strip().lower()
            if process_name not in processes:
                processes[process_name] = []
        
        # Extract steps
        for pattern in step_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                step_indicator = match[0]
                step_description = match[1].strip()
                
                # Try to associate with a process
                for process_name in processes:
                    if process_name in content.lower():
                        processes[process_name].append(f"{step_indicator}: {step_description}")
                        break
    
    def _extract_concepts(self, content: str, concepts: Dict[str, str]):
        """Extract key concepts and their descriptions"""
        # Look for concept explanations
        concept_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[:\-]\s*([^.!?]+[.!?])',
            r'The\s+([a-z]+(?:\s+[a-z]+)*)\s+([^.!?]+[.!?])'
        ]
        
        for pattern in concept_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                concept = match[0].strip().lower()
                description = match[1].strip()
                if len(concept) > 2 and len(description) > 15:
                    concepts[concept] = description
    
    def _extract_relationships(self, content: str, relationships: Dict[str, List[str]]):
        """Extract relationships between concepts"""
        # Look for relationship indicators
        relationship_patterns = [
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:causes?|leads?\s+to|results?\s+in)\s+([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:requires?|needs?|depends?\s+on)\s+([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+(?:produces?|creates?|generates?)\s+([^.!?]+[.!?])'
        ]
        
        for pattern in relationship_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                source = match[0].strip().lower()
                target = match[1].strip()
                if source not in relationships:
                    relationships[source] = []
                relationships[source].append(target)
    
    def _extract_facts(self, content: str, facts: Dict[str, List[str]]):
        """Extract factual statements"""
        # Look for factual statements
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20:
                # Check if it's a factual statement
                if any(indicator in sentence.lower() for indicator in [
                    'is essential', 'is important', 'produces', 'contains', 'occurs in', 'found in'
                ]):
                    # Extract the main subject
                    words = sentence.split()
                    if len(words) > 3:
                        subject = ' '.join(words[:3]).lower()
                        if subject not in facts:
                            facts[subject] = []
                        facts[subject].append(sentence)
    
    def _extract_equations(self, content: str, equations: Dict[str, str]):
        """Extract mathematical equations, formulas, and visual elements"""
        # Enhanced equation patterns
        equation_patterns = [
            # Standard equations with symbols
            r'([^.!?\n]*(?:\+|\-|\=|\→|\←|×|÷|\*|\/)[^.!?\n]*)',
            # Chemical equations
            r'([A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*\s*→\s*[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*)',
            # Mathematical formulas
            r'([A-Za-z]+\s*=\s*[^.!?\n]+)',
            # Ratios and proportions
            r'(\d+:\d+(?::\d+)*)',
            # Percentages and measurements
            r'(\d+(?:\.\d+)?%|\d+(?:\.\d+)?\s*[a-zA-Z]+)',
        ]
        
        # Look for equation context
        equation_contexts = [
            r'(?:equation|formula|expression)[:\s]*([^.!?\n]+)',
            r'(?:overall|general|main)\s+(?:equation|formula)[:\s]*([^.!?\n]+)',
            r'(?:the|this)\s+(?:equation|formula)\s+(?:is|for)[:\s]*([^.!?\n]+)'
        ]
        
        # Extract equations with context
        for pattern in equation_contexts:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                equation = match.strip()
                if len(equation) > 3 and any(symbol in equation for symbol in ['+', '-', '=', '→', '←', '×', '*']):
                    # Try to find a name for this equation
                    equation_name = self._find_equation_name(equation, content)
                    equations[equation_name] = equation
        
        # Extract standalone equations
        for pattern in equation_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                equation = match.strip()
                if len(equation) > 5 and any(symbol in equation for symbol in ['+', '-', '=', '→', '←', '×', '*']):
                    # Clean up the equation
                    equation = re.sub(r'\s+', ' ', equation)
                    equation_name = self._find_equation_name(equation, content) or "formula"
                    equations[equation_name] = equation
    
    def _find_equation_name(self, equation: str, content: str) -> str:
        """Find a descriptive name for an equation"""
        # Look for context around the equation
        equation_escaped = re.escape(equation)
        
        # Look for patterns like "photosynthesis equation", "overall reaction", etc.
        name_patterns = [
            rf'([a-zA-Z\s]+)\s+(?:equation|formula|reaction)[:\s]*{equation_escaped}',
            rf'(?:equation|formula|reaction)\s+(?:for|of)\s+([a-zA-Z\s]+)[:\s]*{equation_escaped}',
            rf'([a-zA-Z\s]+)[:\s]*{equation_escaped}'
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                name = match.group(1).strip().lower()
                if len(name) > 2 and name not in ['the', 'this', 'that', 'overall', 'general']:
                    return name
        
        return "equation"
    
    def _extract_applications(self, content: str, applications: Dict[str, List[str]]):
        """Extract applications and uses"""
        # Look for application patterns
        app_patterns = [
            r'(?:used\s+(?:in|for)|applications?|examples?)\s*[:\-]?\s*([^.!?]+[.!?])',
            r'([A-Z][a-z]+(?:\s+[a-z]+)*)\s+is\s+used\s+(?:in|for)\s+([^.!?]+[.!?])'
        ]
        
        for pattern in app_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    app_list = match[1] if len(match) > 1 else match[0]
                else:
                    app_list = match
                
                # Split applications by commas
                apps = [app.strip() for app in app_list.split(',')]
                for app in apps:
                    if len(app) > 5:
                        if 'general' not in applications:
                            applications['general'] = []
                        applications['general'].append(app)
    
    def _understand_question_intent(self, question: str) -> Dict[str, Any]:
        """
        Understand what the user is really asking for
        """
        question_lower = question.lower()
        
        intent = {
            'type': 'general',
            'main_concept': None,
            'specific_aspect': None,
            'question_words': [],
            'key_terms': []
        }
        
        # Identify question type and intent
        if any(phrase in question_lower for phrase in ['what is', 'what are', 'define']):
            intent['type'] = 'definition'
        elif any(phrase in question_lower for phrase in ['how does', 'how do', 'explain how', 'describe how']):
            intent['type'] = 'process_explanation'
        elif any(phrase in question_lower for phrase in ['why is', 'why does', 'why do']):
            intent['type'] = 'reasoning'
        elif any(phrase in question_lower for phrase in ['what happens', 'what occurs']):
            intent['type'] = 'process_description'
        elif any(phrase in question_lower for phrase in ['what are the', 'list', 'types of']):
            intent['type'] = 'listing'
        elif any(phrase in question_lower for phrase in ['equation', 'formula']):
            intent['type'] = 'equation'
        elif any(phrase in question_lower for phrase in ['importance', 'important', 'significance']):
            intent['type'] = 'importance'
        elif any(phrase in question_lower for phrase in ['difference', 'compare']):
            intent['type'] = 'comparison'
        
        # Extract key terms (remove question words and common words)
        stop_words = {'what', 'is', 'are', 'how', 'does', 'do', 'why', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'can', 'could', 'would', 'should', 'will', 'have', 'has', 'had', 'be', 'been', 'being', 'this', 'that', 'these', 'those', 'explain', 'describe', 'tell', 'me', 'about'}
        
        words = re.findall(r'\b[a-zA-Z]{2,}\b', question_lower)
        intent['key_terms'] = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Identify main concept (usually the most important noun)
        if intent['key_terms']:
            intent['main_concept'] = intent['key_terms'][0]
        
        return intent
    
    def _generate_conceptual_response(self, question: str, intent: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate an intelligent, conceptual response based on understanding
        """
        main_concept = intent.get('main_concept', '').lower()
        question_type = intent.get('type', 'general')
        key_terms = intent.get('key_terms', [])
        
        logger.info(f"Generating conceptual response for: {main_concept} (type: {question_type})")
        
        # Find relevant knowledge
        relevant_info = self._find_relevant_knowledge(main_concept, key_terms, knowledge)
        
        if not relevant_info:
            return f"I couldn't find specific information about '{main_concept}' in your uploaded documents. Could you try asking about other topics covered in the documents?"
        
        # Generate response based on question type
        if question_type == 'definition':
            return self._generate_definition_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'process_explanation' or question_type == 'process_description':
            return self._generate_process_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'reasoning':
            return self._generate_reasoning_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'listing':
            return self._generate_listing_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'equation':
            return self._generate_equation_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'importance':
            return self._generate_importance_answer(main_concept, relevant_info, knowledge)
        elif question_type == 'comparison':
            return self._generate_comparison_answer(key_terms, relevant_info, knowledge)
        else:
            return self._generate_comprehensive_answer(main_concept, relevant_info, knowledge)
    
    def _find_relevant_knowledge(self, main_concept: str, key_terms: List[str], knowledge: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find relevant knowledge from the knowledge base
        """
        relevant = {
            'definitions': {},
            'processes': {},
            'concepts': {},
            'relationships': {},
            'facts': {},
            'equations': {},
            'applications': {}
        }
        
        search_terms = [main_concept] + key_terms
        
        for category, data in knowledge.items():
            if not isinstance(data, dict):
                continue
                
            for key, value in data.items():
                # Check if any search term matches the key or is contained in the value
                if any(term in key.lower() for term in search_terms):
                    relevant[category][key] = value
                elif isinstance(value, str) and any(term in value.lower() for term in search_terms):
                    relevant[category][key] = value
                elif isinstance(value, list) and any(
                    any(term in item.lower() for term in search_terms) 
                    for item in value if isinstance(item, str)
                ):
                    relevant[category][key] = value
        
        return relevant
    
    def _generate_definition_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a comprehensive definition-based answer
        """
        response = f"**What is {concept.title()}?**\n\n"
        
        # Look for direct definitions
        definitions = relevant_info.get('definitions', {})
        concepts = relevant_info.get('concepts', {})
        
        found_definition = False
        
        # Check for exact matches first
        for term, definition in definitions.items():
            if concept in term or term in concept:
                response += f"**Definition:** {concept.title()} is {definition.rstrip('.')}\n\n"
                found_definition = True
                break
        
        if not found_definition:
            # Look in concepts
            for term, description in concepts.items():
                if concept in term or term in concept:
                    response += f"**Overview:** {concept.title()} {description.rstrip('.')}\n\n"
                    found_definition = True
                    break
        
        if not found_definition:
            # Look for any related information
            all_info = []
            for category in ['definitions', 'concepts', 'facts']:
                for key, value in relevant_info.get(category, {}).items():
                    if isinstance(value, str) and len(value) > 20:
                        all_info.append(value)
                    elif isinstance(value, list):
                        all_info.extend([item for item in value if isinstance(item, str) and len(item) > 20])
            
            if all_info:
                # Clean up the description
                description = all_info[0].strip()
                if not description.endswith('.'):
                    description += '.'
                response += f"**Definition:** {concept.title()} is {description}\n\n"
        
        # Add detailed process information
        processes = relevant_info.get('processes', {})
        if processes:
            response += "**Key Processes:**\n"
            for process_name, steps in processes.items():
                if steps and len(steps) > 0:
                    response += f"\n*{process_name.title()}:*\n"
                    for i, step in enumerate(steps, 1):
                        # Clean up step description
                        step_clean = re.sub(r'^.*?:\s*', '', step).strip()
                        if step_clean and len(step_clean) > 10:
                            response += f"{i}. {step_clean}\n"
                    response += "\n"
        
        # Add equations and formulas
        equations = relevant_info.get('equations', {})
        if equations:
            response += "**Key Equations:**\n"
            for eq_name, equation in equations.items():
                response += f"\n*{eq_name.title()}:*\n"
                response += f"```\n{equation}\n```\n"
        
        # Add relationships and connections
        relationships = relevant_info.get('relationships', {})
        if relationships:
            response += "**Key Relationships:**\n"
            for source, targets in relationships.items():
                for target in targets[:3]:  # Show first 3 relationships
                    target_clean = target.strip().rstrip('.')
                    response += f"• {source.title()} → {target_clean}\n"
            response += "\n"
        
        # Add comprehensive applications
        applications = relevant_info.get('applications', {})
        if applications:
            response += "**Applications & Importance:**\n"
            app_count = 0
            for app_category, apps in applications.items():
                for app in apps:
                    if app_count < 5:  # Show more applications
                        app_clean = app.strip().rstrip('.')
                        response += f"• {app_clean}\n"
                        app_count += 1
            response += "\n"
        
        # Add interesting facts
        facts = relevant_info.get('facts', {})
        if facts:
            response += "**Key Facts:**\n"
            fact_count = 0
            for fact_category, fact_list in facts.items():
                for fact in fact_list:
                    if fact_count < 3 and len(fact) > 20:
                        fact_clean = fact.strip().rstrip('.')
                        response += f"• {fact_clean}\n"
                        fact_count += 1
        
        return response.strip()
    
    def _generate_process_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a process-focused answer
        """
        response = f"**How {concept.title()} Works:**\n\n"
        
        processes = relevant_info.get('processes', {})
        
        if processes:
            for process_name, steps in processes.items():
                if steps and len(steps) > 0:
                    response += f"The process involves these key stages:\n\n"
                    for i, step in enumerate(steps, 1):
                        # Clean up step description
                        step_clean = re.sub(r'^(First|Second|Third|Fourth|Fifth|Next|Then|Finally)[,:]?\s*', '', step, flags=re.IGNORECASE)
                        step_clean = re.sub(r'^\d+[.:]?\s*', '', step_clean)
                        step_clean = re.sub(r'^.*?:\s*', '', step_clean)  # Remove any remaining prefixes
                        if step_clean:
                            response += f"**Stage {i}:** {step_clean.strip()}\n\n"
                    break
        else:
            # Look for process descriptions in other categories
            all_descriptions = []
            for category in ['concepts', 'definitions', 'facts']:
                for key, value in relevant_info.get(category, {}).items():
                    if isinstance(value, str) and any(word in value.lower() for word in ['occurs', 'happens', 'process', 'involves', 'stages']):
                        all_descriptions.append(value)
            
            if all_descriptions:
                description = all_descriptions[0].strip()
                response += f"{description}\n\n"
        
        # Add relationships if available
        relationships = relevant_info.get('relationships', {})
        if relationships:
            response += "**Key Relationships:**\n"
            for source, targets in relationships.items():
                for target in targets[:2]:  # Show first 2 relationships
                    target_clean = target.strip().rstrip('.')
                    response += f"• {source.title()} leads to {target_clean}\n"
        
        return response.strip()
    
    def _generate_reasoning_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a reasoning-based answer (why questions)
        """
        response = f"**Why {concept.title()} is Important:**\n\n"
        
        # Look for importance indicators
        facts = relevant_info.get('facts', {})
        applications = relevant_info.get('applications', {})
        relationships = relevant_info.get('relationships', {})
        
        reasons = []
        
        # Extract reasons from facts
        for key, fact_list in facts.items():
            for fact in fact_list:
                if any(word in fact.lower() for word in ['essential', 'important', 'because', 'since', 'due to']):
                    reasons.append(fact)
        
        # Extract reasons from relationships
        for source, targets in relationships.items():
            for target in targets:
                if any(word in target.lower() for word in ['produces', 'creates', 'enables', 'allows']):
                    reasons.append(f"{source.title()} is important because it {target}")
        
        if reasons:
            for i, reason in enumerate(reasons[:3], 1):
                response += f"{i}. {reason}\n\n"
        else:
            # Fallback to general information
            all_info = []
            for category in ['definitions', 'concepts', 'facts']:
                for key, value in relevant_info.get(category, {}).items():
                    if isinstance(value, str):
                        all_info.append(value)
            
            if all_info:
                response += f"Based on the document: {all_info[0]}\n\n"
        
        # Add applications as reasons
        if applications:
            response += "**Applications that show its importance:**\n"
            for app_category, apps in applications.items():
                for app in apps[:3]:
                    response += f"• {app}\n"
        
        return response.strip()
    
    def _generate_listing_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a list-based answer
        """
        response = f"**Types/Components of {concept.title()}:**\n\n"
        
        # Look for lists in processes
        processes = relevant_info.get('processes', {})
        if processes:
            for process_name, steps in processes.items():
                if len(steps) > 1:
                    response += f"**{process_name.title()} includes:**\n"
                    for i, step in enumerate(steps, 1):
                        step_clean = re.sub(r'^.*?:\s*', '', step)  # Remove step indicators
                        response += f"{i}. {step_clean}\n"
                    response += "\n"
        
        # Look for applications
        applications = relevant_info.get('applications', {})
        if applications:
            response += "**Applications:**\n"
            count = 1
            for app_category, apps in applications.items():
                for app in apps:
                    response += f"{count}. {app}\n"
                    count += 1
            response += "\n"
        
        # Look for related concepts
        concepts = relevant_info.get('concepts', {})
        if concepts:
            response += "**Related Concepts:**\n"
            count = 1
            for concept_name, description in concepts.items():
                response += f"{count}. **{concept_name.title()}**: {description}\n"
                count += 1
        
        return response.strip()
    
    def _generate_equation_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a comprehensive equation-focused answer with full mathematical context
        """
        response = f"**Mathematical Representation of {concept.title()}:**\n\n"
        
        equations = relevant_info.get('equations', {})
        
        if equations:
            response += "**🧮 Key Equations:**\n\n"
            for eq_name, equation in equations.items():
                response += f"**{eq_name.title()}:**\n"
                response += f"```\n{equation}\n```\n\n"
                
                # Add explanation for each component if available
                response += "*Components:*\n"
                self._explain_equation_components(equation, response, relevant_info)
                response += "\n"
        else:
            # Look for equations in other text with enhanced extraction
            all_text = []
            for category in ['definitions', 'concepts', 'facts']:
                for key, value in relevant_info.get(category, {}).items():
                    if isinstance(value, str):
                        all_text.append(value)
            
            # Enhanced equation search
            equations_found = []
            for text in all_text:
                # Multiple equation patterns
                patterns = [
                    r'([^.!?\n]*(?:\+|\-|\=|\→|\←)[^.!?\n]*)',
                    r'([A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*\s*→\s*[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*)',
                    r'(\d+[A-Z][a-z]?\d*\s*\+\s*\d+[A-Z][a-z]?\d*.*?→.*?[A-Z][a-z]?\d*\s*\+\s*\d+[A-Z][a-z]?\d*)'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    for match in matches:
                        equation = match.strip()
                        if len(equation) > 5 and any(symbol in equation for symbol in ['+', '-', '=', '→', '←']):
                            equations_found.append(equation)
            
            if equations_found:
                response += "**🧮 Mathematical Equations:**\n\n"
                for i, eq in enumerate(equations_found[:3], 1):  # Show up to 3 equations
                    response += f"**Equation {i}:**\n"
                    response += f"```\n{eq}\n```\n\n"
        
        # Add detailed explanation
        definitions = relevant_info.get('definitions', {})
        concepts = relevant_info.get('concepts', {})
        
        response += "**📖 Mathematical Explanation:**\n"
        explanation_found = False
        
        for term, definition in definitions.items():
            if any(word in definition.lower() for word in ['equation', 'formula', 'mathematical', 'calculation']):
                response += f"{definition}\n\n"
                explanation_found = True
                break
        
        if not explanation_found:
            for term, concept_desc in concepts.items():
                if any(word in concept_desc.lower() for word in ['equation', 'formula', 'mathematical']):
                    response += f"{concept_desc}\n\n"
                    break
        
        # Add process context for the equation
        processes = relevant_info.get('processes', {})
        if processes:
            response += "**⚙️ Process Context:**\n"
            for process_name, steps in processes.items():
                if steps:
                    response += f"The equation represents the {process_name} which involves:\n"
                    for i, step in enumerate(steps[:3], 1):
                        step_clean = re.sub(r'^.*?:\s*', '', step).strip()
                        if step_clean:
                            response += f"{i}. {step_clean}\n"
                    response += "\n"
                    break
        
        # Add applications of the equation
        applications = relevant_info.get('applications', {})
        if applications:
            response += "**🌍 Applications:**\n"
            response += "This mathematical relationship is used in:\n"
            app_count = 0
            for app_category, apps in applications.items():
                for app in apps:
                    if app_count < 4:
                        response += f"• {app.strip()}\n"
                        app_count += 1
        
        return response.strip()
    
    def _explain_equation_components(self, equation: str, response: str, relevant_info: Dict[str, Any]):
        """Explain the components of an equation"""
        # Extract chemical formulas or variables
        components = re.findall(r'[A-Z][a-z]?\d*|[a-zA-Z]+', equation)
        
        for component in components[:5]:  # Limit to 5 components
            # Look for explanations of this component in the content
            for category in ['definitions', 'concepts', 'facts']:
                for key, value in relevant_info.get(category, {}).items():
                    if isinstance(value, str) and component.lower() in value.lower():
                        # Extract relevant sentence
                        sentences = re.split(r'[.!?]+', value)
                        for sentence in sentences:
                            if component.lower() in sentence.lower():
                                response += f"• {component}: {sentence.strip()}\n"
                                break
                        break
    
    def _generate_importance_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate an importance-focused answer
        """
        return self._generate_reasoning_answer(concept, relevant_info, knowledge)
    
    def _generate_comparison_answer(self, key_terms: List[str], relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a comparison-based answer
        """
        response = f"**Comparison:**\n\n"
        
        # Find information about each term
        for term in key_terms[:2]:  # Compare first two terms
            term_info = self._find_relevant_knowledge(term, [term], knowledge)
            
            response += f"**{term.title()}:**\n"
            
            # Add definition
            definitions = term_info.get('definitions', {})
            concepts = term_info.get('concepts', {})
            
            for def_term, definition in definitions.items():
                if term in def_term or def_term in term:
                    response += f"• {definition}\n"
                    break
            else:
                for concept_term, description in concepts.items():
                    if term in concept_term or concept_term in term:
                        response += f"• {description}\n"
                        break
            
            response += "\n"
        
        return response.strip()
    
    def _generate_comprehensive_answer(self, concept: str, relevant_info: Dict[str, Any], knowledge: Dict[str, Any]) -> str:
        """
        Generate a comprehensive answer covering all aspects with complete information
        """
        response = f"**Complete Guide to {concept.title()}:**\n\n"
        
        # 1. Definition and Overview
        definitions = relevant_info.get('definitions', {})
        concepts = relevant_info.get('concepts', {})
        
        definition_found = False
        for term, definition in definitions.items():
            if concept in term or term in concept:
                response += f"**📖 Definition:**\n{definition}\n\n"
                definition_found = True
                break
        
        if not definition_found:
            for term, description in concepts.items():
                if concept in term or term in concept:
                    response += f"**📖 Overview:**\n{description}\n\n"
                    break
        
        # 2. Detailed Process Information
        processes = relevant_info.get('processes', {})
        if processes:
            response += "**⚙️ How It Works:**\n"
            for process_name, steps in processes.items():
                if steps and len(steps) > 0:
                    response += f"\n*{process_name.title()} Process:*\n"
                    for i, step in enumerate(steps, 1):
                        step_clean = re.sub(r'^.*?:\s*', '', step).strip()
                        if step_clean and len(step_clean) > 5:
                            response += f"**Step {i}:** {step_clean}\n"
                    response += "\n"
        
        # 3. Mathematical Equations and Formulas
        equations = relevant_info.get('equations', {})
        if equations:
            response += "**🧮 Key Equations:**\n"
            for eq_name, equation in equations.items():
                response += f"\n*{eq_name.title()}:*\n"
                response += f"```\n{equation}\n```\n"
                
                # Try to find explanation for this equation
                for category in ['definitions', 'concepts', 'facts']:
                    for key, value in relevant_info.get(category, {}).items():
                        if isinstance(value, str) and equation.lower() in value.lower():
                            explanation = value.strip()
                            response += f"*Explanation:* {explanation}\n\n"
                            break
        
        # 4. Relationships and Connections
        relationships = relevant_info.get('relationships', {})
        if relationships:
            response += "**🔗 Key Relationships:**\n"
            for source, targets in relationships.items():
                response += f"\n*{source.title()} leads to:*\n"
                for target in targets:
                    target_clean = target.strip().rstrip('.')
                    response += f"• {target_clean}\n"
            response += "\n"
        
        # 5. Applications and Real-World Uses
        applications = relevant_info.get('applications', {})
        if applications:
            response += "**🌍 Applications & Importance:**\n"
            for app_category, apps in applications.items():
                if apps:
                    response += f"\n*{app_category.title()} Applications:*\n"
                    for app in apps:
                        app_clean = app.strip().rstrip('.')
                        response += f"• {app_clean}\n"
            response += "\n"
        
        # 6. Important Facts and Details
        facts = relevant_info.get('facts', {})
        if facts:
            response += "**💡 Key Facts:**\n"
            for fact_category, fact_list in facts.items():
                for fact in fact_list:
                    if len(fact) > 15:
                        fact_clean = fact.strip().rstrip('.')
                        response += f"• {fact_clean}\n"
            response += "\n"
        
        # 7. Visual Elements (if any diagrams or figures are mentioned)
        visual_elements = self._extract_visual_references(relevant_info)
        if visual_elements:
            response += "**📊 Visual Elements:**\n"
            for visual in visual_elements:
                response += f"• {visual}\n"
            response += "\n"
        
        # 8. Summary and Conclusion
        response += "**📝 Summary:**\n"
        response += f"{concept.title()} is a fundamental concept that involves multiple interconnected processes and has significant real-world applications. "
        
        if equations:
            response += "The mathematical relationships help quantify and predict outcomes. "
        
        if applications:
            response += "Its applications span across various fields, making it essential for understanding related phenomena."
        
        return response.strip()
    
    def _extract_visual_references(self, relevant_info: Dict[str, Any]) -> List[str]:
        """Extract references to visual elements like diagrams, figures, charts"""
        visual_refs = []
        
        visual_keywords = ['diagram', 'figure', 'chart', 'graph', 'illustration', 'image', 'picture', 'visual', 'schematic']
        
        for category, data in relevant_info.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, str):
                        for keyword in visual_keywords:
                            if keyword in value.lower():
                                # Extract the sentence containing the visual reference
                                sentences = re.split(r'[.!?]+', value)
                                for sentence in sentences:
                                    if keyword in sentence.lower():
                                        visual_refs.append(sentence.strip())
                                        break
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, str):
                                for keyword in visual_keywords:
                                    if keyword in item.lower():
                                        visual_refs.append(item.strip())
        
        return list(set(visual_refs))  # Remove duplicates
    

    

    
