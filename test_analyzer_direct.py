#!/usr/bin/env python3
"""
Direct test of document analyzer functionality
"""

import sys
import os
sys.path.append('backend')

from services.document_service import DocumentService
from services.document_analyzer import DocumentAnalyzer

def test_analyzer_direct():
    """Test the document analyzer directly"""
    
    print("🔬 Direct Document Analyzer Test")
    print("=" * 40)
    
    # Initialize services
    doc_service = DocumentService()
    analyzer = DocumentAnalyzer(doc_service)
    
    # Clear any existing documents
    documents = doc_service.list_documents()
    for doc in documents:
        doc_service.remove_document(doc['id'])
    
    print(f"✅ Cleared {len(documents)} existing documents")
    
    # Add a simple test document
    test_content = """
    Photosynthesis Explained
    
    Photosynthesis is the biological process by which plants convert light energy into chemical energy.
    
    This process occurs in two main stages:
    
    1. Light-dependent reactions: These occur in the thylakoid membranes where chlorophyll absorbs light energy. Water molecules are split, releasing oxygen as a byproduct. ATP and NADPH are produced during this stage.
    
    2. Light-independent reactions (Calvin Cycle): These occur in the stroma of chloroplasts. Carbon dioxide is fixed into organic molecules using the ATP and NADPH produced in the light reactions. The end product is glucose.
    
    The overall equation for photosynthesis is:
    6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    
    Photosynthesis is essential for life on Earth because it produces oxygen and forms the base of most food chains.
    """
    
    result = doc_service.add_document_from_text(
        content=test_content,
        title="Photosynthesis Explained",
        source="test"
    )
    
    print(f"📄 Added document: {result['title']} (Success: {result['success']})")
    
    # Verify document was added
    documents = doc_service.list_documents()
    print(f"📚 Total documents: {len(documents)}")
    
    # Test specific questions
    test_questions = [
        "What is photosynthesis?",
        "Explain the light-dependent reactions",
        "What happens in the Calvin cycle?",
        "What is the equation for photosynthesis?",
        "Why is photosynthesis important?"
    ]
    
    print("\n🤔 Testing Questions:")
    print("-" * 40)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQ{i}: {question}")
        print("A:", end=" ")
        
        response = analyzer.analyze_question_and_respond(question)
        
        # Print first 200 characters of response
        if len(response) > 200:
            print(f"{response[:200]}...")
        else:
            print(response)
        
        print("-" * 40)
    
    print("\n✅ Direct analyzer test completed!")

if __name__ == "__main__":
    test_analyzer_direct()