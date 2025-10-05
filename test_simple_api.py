#!/usr/bin/env python3
"""
Simple API test
"""

import requests
import json

def test_simple():
    """Test with a simple question"""
    
    base_url = "http://localhost:5000"
    
    # Test with a very simple question
    chat_data = {
        'message': 'hello',
        'session_id': 'test_simple'
    }
    
    try:
        print("Testing simple 'hello' message...")
        response = requests.post(f"{base_url}/api/tutor", json=chat_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Response received:")
            print(f"📝 {result['response']}")
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - server is hanging")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_simple()