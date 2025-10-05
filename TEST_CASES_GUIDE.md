# 🧪 Acadefy Test Cases Guide

## 📚 Pre-defined Learning Topics

Acadefy includes 5 comprehensive test cases that provide detailed responses even when the LLM API is unavailable. These cover key academic subjects:

---

## 🔢 **1. Integral Calculus [Mathematics]**

### **Trigger Keywords:**
- `integral`, `integration`, `calculus`, `antiderivative`, `definite integral`, `indefinite integral`

### **Sample Questions:**
- "Can you help me with integral calculus?"
- "What is integration in mathematics?"
- "How do I solve definite integrals?"
- "Explain antiderivatives"

### **Response Includes:**
- Basic integration rules and formulas
- Types of integrals (definite vs indefinite)
- Step-by-step example problem
- Common integration techniques

---

## 🌡️ **2. Thermodynamics [Science]**

### **Trigger Keywords:**
- `thermodynamics`, `heat`, `temperature`, `entropy`, `enthalpy`, `first law`, `second law`, `thermal`

### **Sample Questions:**
- "Explain thermodynamics to me"
- "What are the laws of thermodynamics?"
- "How does heat transfer work?"
- "What is entropy?"

### **Response Includes:**
- Four laws of thermodynamics
- Key concepts (heat, work, internal energy)
- Mathematical relationships (ΔU = Q - W)
- Practical example problem

---

## ⚛️ **3. P-Block Elements [Science]**

### **Trigger Keywords:**
- `p-block`, `p block`, `boron`, `carbon`, `nitrogen`, `oxygen`, `fluorine`, `noble gases`, `halogens`

### **Sample Questions:**
- "Tell me about p-block elements"
- "What are the properties of halogens?"
- "Explain the p block in periodic table"
- "What are noble gases?"

### **Response Includes:**
- Complete overview of groups 13-18
- Electronic configurations and trends
- Special properties of each group
- Examples and explanations

---

## 📝 **4. English Tenses [English]**

### **Trigger Keywords:**
- `tense`, `tenses`, `past tense`, `present tense`, `future tense`, `grammar`, `verb forms`

### **Sample Questions:**
- "I need help with English tenses"
- "What are the different verb tenses?"
- "Explain past tense and present tense"
- "How do I use future perfect tense?"

### **Response Includes:**
- All 12 English tenses with examples
- Clear categorization (Present, Past, Future)
- Usage rules and time markers
- Practice sentences and tips

---

## 💻 **5. Graph Data Structures [Programming]**

### **Trigger Keywords:**
- `graph`, `graphs`, `node`, `edge`, `vertex`, `adjacency`, `dfs`, `bfs`, `tree`, `algorithm`

### **Sample Questions:**
- "How do graph algorithms work?"
- "What is DFS and BFS in programming?"
- "Explain graph data structures"
- "How do I implement adjacency lists?"

### **Response Includes:**
- Graph types and representations
- Complete code examples (Python)
- DFS and BFS implementations
- Real-world applications

---

## 🚀 **How to Test**

### **Method 1: Use the Web Interface**
1. Start the app: `python start_app.py`
2. Go to http://localhost:5000/tutor
3. Type any of the sample questions above
4. Get instant detailed responses!

### **Method 2: Run Test Script**
```bash
python test_cases.py
```

### **Method 3: Try Variations**
The system is smart enough to detect variations:
- "Help with calculus integration" ✅
- "What's thermodynamics about?" ✅  
- "Explain English grammar tenses" ✅
- "Graph algorithms in coding" ✅
- "P block elements chemistry" ✅

---

## 🎯 **Benefits**

✅ **Instant Responses** - No waiting for API calls
✅ **Comprehensive Content** - Detailed explanations with examples
✅ **Educational Quality** - Structured learning material
✅ **Always Available** - Works offline or when API is down
✅ **Smart Detection** - Recognizes topic variations and synonyms

---

## 🔧 **For Developers**

The predefined cases are implemented in `backend/services/ai_service.py` in the `_check_predefined_cases()` method. You can easily:

- Add more topics by extending the `test_cases` dictionary
- Modify existing responses
- Add more trigger keywords
- Customize the response format

Each test case includes:
- **Keywords**: List of trigger words/phrases
- **Response**: Comprehensive educational content
- **Examples**: Practical problems and solutions
- **Follow-up**: Questions to encourage further learning

---

**🎓 Ready to learn? Try asking about any of these 5 topics and get instant, detailed tutoring!**