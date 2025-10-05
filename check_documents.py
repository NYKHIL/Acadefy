#!/usr/bin/env python3
"""
Check what documents are currently in the knowledge base
"""

import sys
import os
sys.path.append('backend')

from services.document_service import DocumentService

def check_documents():
    """Check current documents in the knowledge base"""
    
    print("📚 Checking Current Documents in Knowledge Base")
    print("=" * 50)
    
    doc_service = DocumentService()
    
    # List all documents
    documents = doc_service.list_documents()
    
    print(f"Found {len(documents)} document(s):")
    print()
    
    for i, doc in enumerate(documents, 1):
        print(f"{i}. Title: {doc['title']}")
        print(f"   ID: {doc['id']}")
        print(f"   URL: {doc['url']}")
        print(f"   Type: {doc['content_type']}")
        print(f"   Chunks: {doc['chunks_count']}")
        print(f"   Keywords: {doc['keywords_count']}")
        print()
    
    # Test search for photosynthesis
    print("🔍 Testing search for 'photosynthesis':")
    results = doc_service.search_documents("photosynthesis", max_results=5)
    
    for result in results:
        print(f"- {result['title']} (Score: {result['relevance_score']})")
    
    print()
    print("🔍 Testing search for 'light-dependent reactions':")
    results = doc_service.search_documents("light-dependent reactions", max_results=5)
    
    for result in results:
        print(f"- {result['title']} (Score: {result['relevance_score']})")

if __name__ == "__main__":
    check_documents()