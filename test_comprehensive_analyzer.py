#!/usr/bin/env python3
"""
Test comprehensive document analyzer with rich content
"""

import sys
import os
sys.path.append('backend')

from services.document_service import DocumentService
from services.document_analyzer import DocumentAnalyzer

def test_comprehensive_analyzer():
    """Test the document analyzer with comprehensive content"""
    
    print("🔬 Comprehensive Document Analyzer Test")
    print("=" * 50)
    
    # Initialize services
    doc_service = DocumentService()
    analyzer = DocumentAnalyzer(doc_service)
    
    # Clear any existing documents
    documents = doc_service.list_documents()
    for doc in documents:
        doc_service.remove_document(doc['id'])
    
    print(f"✅ Cleared {len(documents)} existing documents")
    
    # Add a comprehensive test document with equations and visual elements
    comprehensive_content = """
    Photosynthesis: The Complete Process
    
    Photosynthesis is the biological process by which plants, algae, and certain bacteria convert light energy, usually from the sun, into chemical energy stored in glucose molecules.
    
    The Overall Equation for Photosynthesis:
    6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    
    This equation shows that six molecules of carbon dioxide plus six molecules of water, in the presence of light energy, produce one molecule of glucose and six molecules of oxygen.
    
    Key Stages of Photosynthesis:
    
    1. Light-Dependent Reactions (Photo Reactions):
    - Occur in the thylakoid membranes of chloroplasts
    - Chlorophyll absorbs light energy and becomes excited
    - Water molecules (H2O) are split, releasing oxygen (O2) as a byproduct
    - ATP (adenosine triphosphate) and NADPH are produced as energy carriers
    - The reaction can be represented as: 2H2O + light energy → 4H+ + 4e- + O2
    
    2. Light-Independent Reactions (Calvin Cycle):
    - Occur in the stroma of chloroplasts
    - Carbon dioxide (CO2) is fixed into organic molecules
    - Uses ATP and NADPH produced in the light reactions
    - Produces glucose (C6H12O6) through a series of enzymatic reactions
    - The key enzyme is RuBisCO (ribulose-1,5-bisphosphate carboxylase/oxygenase)
    
    Importance and Applications:
    
    Photosynthesis is essential for life on Earth because:
    - It produces oxygen that most organisms need for respiration
    - It forms the base of most food chains by converting inorganic carbon into organic compounds
    - It removes carbon dioxide from the atmosphere, helping regulate climate
    - It provides the energy source for nearly all ecosystems
    
    The process is used in:
    - Agriculture for crop production and yield optimization
    - Environmental science for understanding carbon cycles
    - Biotechnology for developing artificial photosynthesis systems
    - Renewable energy research for solar energy conversion
    
    Visual Elements:
    The process can be illustrated through diagrams showing the chloroplast structure, with thylakoids arranged in stacks called grana, surrounded by the stroma. Figure 1 typically shows the light reactions occurring in the thylakoid membranes, while Figure 2 demonstrates the Calvin cycle in the stroma.
    
    Mathematical Relationships:
    The efficiency of photosynthesis can be calculated using the quantum yield equation:
    Quantum Yield = (Moles of CO2 fixed) / (Moles of photons absorbed)
    
    The rate of photosynthesis is often expressed as:
    Rate = k × [CO2] × [H2O] × Light Intensity
    
    Where k is the rate constant that depends on temperature and enzyme activity.
    """
    
    result = doc_service.add_document_from_text(
        content=comprehensive_content,
        title="Photosynthesis: Complete Process",
        source="comprehensive_test"
    )
    
    print(f"📄 Added document: {result['title']} (Success: {result['success']})")
    
    # Test comprehensive questions
    test_questions = [
        "What is photosynthesis?",
        "What is the equation for photosynthesis?",
        "Explain the light-dependent reactions",
        "What happens in the Calvin cycle?",
        "Why is photosynthesis important?"
    ]
    
    print("\n🤔 Testing Comprehensive Questions:")
    print("-" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nQ{i}: {question}")
        print("=" * 40)
        
        response = analyzer.analyze_question_and_respond(question)
        
        # Print full response (no truncation)
        print(response)
        print("-" * 60)
    
    print("\n✅ Comprehensive analyzer test completed!")

if __name__ == "__main__":
    test_comprehensive_analyzer()