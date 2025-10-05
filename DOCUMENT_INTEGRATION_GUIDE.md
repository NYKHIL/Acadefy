# 📚 Document Integration Guide

## 🎯 Overview

Acadefy now supports **document-based knowledge retrieval**! You can add reference materials (books, articles, PDFs, etc.) that the AI tutor will automatically reference when answering related questions.

---

## 🚀 **How It Works**

### **1. RAG (Retrieval-Augmented Generation)**
- Upload documents or provide URLs to reference materials
- AI automatically searches through your documents for relevant information
- Provides answers based on your specific materials + general knowledge

### **2. Smart Context Detection**
- When you ask a question, the system searches your knowledge base
- Finds relevant chunks of information from your documents
- Includes this context in the AI's response for accurate, source-based answers

---

## 📖 **Adding Documents**

### **Method 1: From URL**
```
1. Go to Profile page (/profile)
2. Scroll to "Knowledge Base" section
3. Enter URL of document/webpage
4. Add optional title
5. Click "Add URL"
```

**Supported URL Types:**
- ✅ Web pages (HTML)
- ✅ Direct text files (.txt)
- ✅ PDF files (basic extraction)
- ✅ Online articles and documentation

### **Method 2: Direct Text Input**
```
1. Go to Profile page (/profile)
2. Scroll to "Knowledge Base" section
3. Enter document title
4. Paste your text content
5. Click "Add Text"
```

**Use Cases:**
- ✅ Copy-paste from textbooks
- ✅ Add lecture notes
- ✅ Include research papers
- ✅ Add custom study materials

---

## 🎯 **Example Usage**

### **Scenario: Adding a Calculus Textbook**

1. **Add Document:**
   ```
   Title: "Calculus Fundamentals - Chapter 5"
   Content: [Paste chapter content about integration techniques]
   ```

2. **Ask Questions:**
   ```
   User: "How do I solve integration by parts?"
   AI: "Based on your Calculus Fundamentals textbook, integration by parts follows the formula: ∫u dv = uv - ∫v du..."
   ```

### **Scenario: Adding Course Notes**

1. **Add Document:**
   ```
   URL: "https://university.edu/physics/thermodynamics-notes.pdf"
   Title: "Physics 201 - Thermodynamics Notes"
   ```

2. **Ask Questions:**
   ```
   User: "What's the second law of thermodynamics?"
   AI: "According to your Physics 201 notes, the second law states that..."
   ```

---

## 🔧 **API Endpoints**

### **Document Management**
```bash
# List all documents
GET /api/documents

# Add document from URL
POST /api/documents/add-url
{
  "url": "https://example.com/document.pdf",
  "title": "Optional Title"
}

# Add document from text
POST /api/documents/add-text
{
  "content": "Your text content here...",
  "title": "Document Title"
}

# Remove document
DELETE /api/documents/{document_id}

# Search documents
POST /api/documents/search
{
  "query": "search terms",
  "max_results": 3
}
```

---

## 🎨 **Frontend Interface**

### **Profile Page Integration**
- **Knowledge Base Section**: Manage your reference documents
- **Add from URL**: Quick document addition from web links
- **Add from Text**: Direct text input for custom content
- **Document List**: View and manage all added documents
- **Remove Documents**: Clean up your knowledge base

### **Chat Integration**
- **Automatic Context**: AI automatically uses relevant documents
- **Source Attribution**: Responses reference your specific materials
- **Seamless Experience**: No extra steps needed during chat

---

## 🧠 **How the AI Uses Documents**

### **1. Query Analysis**
```
User asks: "Explain photosynthesis"
↓
System searches documents for: "photosynthesis", "plants", "chlorophyll"
↓
Finds relevant chunks from biology textbook
↓
Includes context in AI prompt
```

### **2. Context Integration**
```
AI Prompt includes:
- System instructions (be a helpful tutor)
- Document context (relevant chunks from your materials)
- Conversation history
- Current user question
```

### **3. Enhanced Response**
```
AI Response:
"Based on your Biology 101 textbook, photosynthesis is the process by which plants convert light energy into chemical energy..."
```

---

## 📊 **Document Processing**

### **Text Chunking**
- Documents are split into ~500-word chunks
- Maintains context while enabling efficient search
- Overlapping chunks prevent information loss

### **Keyword Extraction**
- Automatic keyword identification
- Improved search relevance
- Better topic matching

### **Relevance Scoring**
- Multiple factors determine document relevance
- Title matching, keyword presence, content similarity
- Top 3 most relevant documents used for context

---

## 🔍 **Search Algorithm**

### **Multi-Factor Relevance**
1. **Title Match** (+10 points): Query terms in document title
2. **Keyword Match** (+5 points): Query terms in extracted keywords  
3. **Content Match** (+3 points): Query terms in document chunks
4. **Chunk Relevance**: Percentage of query words found in chunk

### **Context Selection**
- Top 3 most relevant documents
- Best 2 chunks per document
- Maximum context length maintained for AI processing

---

## 💡 **Best Practices**

### **Document Quality**
- ✅ Use clear, well-structured content
- ✅ Include comprehensive topic coverage
- ✅ Add descriptive titles for better organization
- ✅ Remove irrelevant formatting when pasting text

### **Organization Tips**
- 📚 Group related documents by subject
- 🏷️ Use consistent naming conventions
- 🔄 Update documents when materials change
- 🗑️ Remove outdated or duplicate content

### **Query Optimization**
- 🎯 Ask specific questions related to your documents
- 📖 Reference topics you know are in your materials
- 🔍 Use terminology from your textbooks/notes
- 💬 Ask follow-up questions for deeper understanding

---

## 🚀 **Advanced Features (Future)**

### **Planned Enhancements**
- 📄 **File Upload**: Direct PDF, DOCX, TXT file uploads
- 🔗 **Web Scraping**: Automatic content extraction from complex sites
- 🏷️ **Document Tagging**: Organize documents by subject/topic
- 📊 **Usage Analytics**: See which documents are most referenced
- 🔄 **Auto-Updates**: Monitor URLs for content changes
- 🤖 **Smart Summaries**: AI-generated document summaries

---

## 🛠️ **Technical Implementation**

### **Backend Architecture**
```
DocumentService
├── Document Processing (chunking, keywords)
├── Search & Retrieval (relevance scoring)
├── Context Generation (for AI prompts)
└── Storage Management (JSON-based knowledge base)

AIService Integration
├── Query → Document Search
├── Context Injection → AI Prompt
└── Enhanced Response Generation
```

### **Data Storage**
```
documents/
├── knowledge_base.json    # Document metadata and content
└── [future: uploaded files]
```

---

## 🎓 **Example Workflows**

### **Study Session Workflow**
1. **Preparation**: Add textbook chapters, lecture notes, assignments
2. **Learning**: Ask questions during study - get textbook-based answers
3. **Review**: AI references your specific materials for consistency
4. **Practice**: Request problems similar to those in your materials

### **Research Workflow**
1. **Gather Sources**: Add research papers, articles, documentation
2. **Analysis**: Ask comparative questions across multiple sources
3. **Synthesis**: Get AI help connecting concepts from different materials
4. **Writing**: Reference specific sources in your knowledge base

---

## 🎉 **Get Started**

### **Quick Start**
1. **Add Your First Document**: Go to Profile → Knowledge Base
2. **Test It**: Add a simple text document about any topic
3. **Ask Questions**: Chat with AI about that topic
4. **See the Magic**: Notice how AI references your specific content!

### **Sample Test**
```
1. Add text: "The mitochondria is the powerhouse of the cell. It produces ATP through cellular respiration."
2. Ask: "What produces ATP in cells?"
3. Get response: "Based on your reference material, the mitochondria produces ATP through cellular respiration..."
```

---

**🚀 Ready to enhance your AI tutor with your own knowledge base? Start adding documents and experience personalized, source-based learning!**