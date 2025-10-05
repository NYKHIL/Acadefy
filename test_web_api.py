#!/usr/bin/env python3
"""
Test the web API directly
"""

import requests
import json
import time

def test_web_api():
    """Test the web API with a simple question"""
    
    print("🌐 Testing Web API")
    print("=" * 30)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    base_url = "http://localhost:5000"
    
    # Test the tutor endpoint
    question = "What is photosynthesis?"
    
    chat_data = {
        'message': question,
        'session_id': 'test_session_web'
    }
    
    try:
        print(f"🤔 Asking: {question}")
        response = requests.post(f"{base_url}/api/tutor", json=chat_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Response received:")
            print(f"📝 {result['response']}")
            print(f"⏱️  Response time: {result.get('response_time', 'N/A')}s")
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_web_api()