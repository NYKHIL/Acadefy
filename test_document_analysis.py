#!/usr/bin/env python3
"""
Test script for document analysis functionality
"""

import sys
import os
sys.path.append('backend')

from services.document_service import DocumentService
from services.document_analyzer import DocumentAnalyzer

def test_document_analysis():
    """Test the document analysis system"""
    
    print("🧪 Testing Acadefy Document Analysis System")
    print("=" * 50)
    
    # Initialize services
    doc_service = DocumentService()
    analyzer = DocumentAnalyzer(doc_service)
    
    # Test 1: Add a test document
    print("\n1. Adding test document...")
    test_content = """
    Machine Learning Fundamentals
    
    Machine learning is a subset of artificial intelligence (AI) that focuses on algorithms 
    that can learn from and make predictions or decisions based on data. Unlike traditional 
    programming where we write explicit instructions, machine learning algorithms build 
    mathematical models based on training data.
    
    Key Types of Machine Learning:
    
    1. Supervised Learning: Uses labeled training data to learn a mapping from inputs to outputs.
       Examples include classification (predicting categories) and regression (predicting numbers).
    
    2. Unsupervised Learning: Finds hidden patterns in data without labeled examples.
       Examples include clustering and dimensionality reduction.
    
    3. Reinforcement Learning: Learns through interaction with an environment, receiving 
       rewards or penalties for actions taken.
    
    Popular Algorithms:
    - Linear Regression: For predicting continuous values
    - Decision Trees: For both classification and regression
    - Neural Networks: Inspired by biological neurons, can learn complex patterns
    - Support Vector Machines: Effective for classification tasks
    
    Applications:
    Machine learning is used in recommendation systems, image recognition, natural language 
    processing, autonomous vehicles, medical diagnosis, and many other fields.
    """
    
    result = doc_service.add_document_from_text(
        content=test_content,
        title="Machine Learning Fundamentals",
        source="test_document"
    )
    
    if result['success']:
        print(f"✅ Document added successfully: {result['title']}")
        print(f"   Chunks: {result['chunks_count']}")
    else:
        print(f"❌ Failed to add document: {result['error']}")
        return
    
    # Test 2: List documents
    print("\n2. Listing documents...")
    documents = doc_service.list_documents()
    print(f"📚 Found {len(documents)} document(s):")
    for doc in documents:
        print(f"   - {doc['title']} ({doc['chunks_count']} chunks)")
    
    # Test 3: Test various questions
    test_questions = [
        "What is machine learning?",
        "Explain supervised learning",
        "What are the types of machine learning?",
        "Tell me about neural networks",
        "What are some applications of machine learning?",
        "How does reinforcement learning work?",
        "What is the difference between classification and regression?"
    ]
    
    print("\n3. Testing question analysis...")
    print("-" * 40)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🤔 Question {i}: {question}")
        print("📝 Response:")
        
        response = analyzer.analyze_question_and_respond(question)
        print(response)
        print("-" * 40)
    
    print("\n✅ Document analysis test completed!")

if __name__ == "__main__":
    test_document_analysis()