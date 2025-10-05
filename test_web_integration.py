#!/usr/bin/env python3
"""
Test web integration for document analysis
"""

import requests
import json

def test_web_integration():
    """Test the web API with document analysis"""
    
    base_url = "http://localhost:5000"
    
    print("🌐 Testing Acadefy Web Integration")
    print("=" * 40)
    
    # Test 1: Upload a document
    print("\n1. Testing document upload...")
    
    # Create test file content
    test_content = """
    Photosynthesis Process
    
    Photosynthesis is the process by which plants convert light energy into chemical energy.
    This process occurs in the chloroplasts of plant cells and involves two main stages:
    
    1. Light-dependent reactions (Photo reactions):
       - Occur in the thylakoid membranes
       - Chlorophyll absorbs light energy
       - Water molecules are split, releasing oxygen
       - ATP and NADPH are produced
    
    2. Light-independent reactions (Calvin Cycle):
       - Occur in the stroma of chloroplasts
       - CO2 is fixed into organic molecules
       - Uses ATP and NADPH from light reactions
       - Produces glucose (C6H12O6)
    
    The overall equation for photosynthesis is:
    6CO2 + 6H2O + light energy → C6H12O6 + 6O2
    
    Photosynthesis is essential for life on Earth as it produces oxygen and forms the base of most food chains.
    """
    
    # Upload document via text
    upload_data = {
        'content': test_content,
        'title': 'Photosynthesis Process',
        'source': 'manual'
    }
    
    try:
        response = requests.post(f"{base_url}/api/documents/add-text", json=upload_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Document uploaded: {result['title']}")
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return
    
    # Test 2: Ask questions about the document
    test_questions = [
        "What is photosynthesis?",
        "Explain the light-dependent reactions",
        "What happens in the Calvin cycle?",
        "What is the equation for photosynthesis?"
    ]
    
    print("\n2. Testing AI responses with document context...")
    print("-" * 40)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n🤔 Question {i}: {question}")
        
        chat_data = {
            'message': question,
            'session_id': 'test_session_123'
        }
        
        try:
            response = requests.post(f"{base_url}/api/tutor", json=chat_data)
            if response.status_code == 200:
                result = response.json()
                print("📝 AI Response:")
                print(result['response'])
                print(f"⏱️  Response time: {result.get('response_time', 'N/A')}s")
            else:
                print(f"❌ Chat failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Chat error: {e}")
        
        print("-" * 40)
    
    print("\n✅ Web integration test completed!")

if __name__ == "__main__":
    test_web_integration()