#!/usr/bin/env python3
"""
Clear the backend knowledge base
"""

import sys
import os
sys.path.append('backend')

def clear_backend_kb():
    """Clear the backend knowledge base file"""
    
    print("🧹 Clearing Backend Knowledge Base")
    print("=" * 35)
    
    kb_file = "backend/documents/knowledge_base.json"
    
    if os.path.exists(kb_file):
        # Write empty knowledge base
        with open(kb_file, 'w') as f:
            f.write('{}')
        print("✅ Backend knowledge base cleared")
    else:
        print("❌ Backend knowledge base file not found")
    
    # Also clear the main knowledge base
    main_kb_file = "documents/knowledge_base.json"
    if os.path.exists(main_kb_file):
        with open(main_kb_file, 'w') as f:
            f.write('{}')
        print("✅ Main knowledge base cleared")

if __name__ == "__main__":
    clear_backend_kb()