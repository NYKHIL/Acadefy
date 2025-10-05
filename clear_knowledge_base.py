#!/usr/bin/env python3
"""
Clear the knowledge base and start fresh
"""

import sys
import os
sys.path.append('backend')

from services.document_service import DocumentService

def clear_knowledge_base():
    """Clear all documents from the knowledge base"""
    
    print("🧹 Clearing Knowledge Base")
    print("=" * 30)
    
    doc_service = DocumentService()
    
    # Get all documents
    documents = doc_service.list_documents()
    print(f"Found {len(documents)} document(s) to remove")
    
    # Remove each document
    for doc in documents:
        success = doc_service.remove_document(doc['id'])
        if success:
            print(f"✅ Removed: {doc['title']}")
        else:
            print(f"❌ Failed to remove: {doc['title']}")
    
    # Verify empty
    remaining = doc_service.list_documents()
    print(f"\n📚 Remaining documents: {len(remaining)}")
    
    if len(remaining) == 0:
        print("✅ Knowledge base cleared successfully!")
    else:
        print("❌ Some documents remain")

if __name__ == "__main__":
    clear_knowledge_base()