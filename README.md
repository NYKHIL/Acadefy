# 🎓 Acadefy - AI-Powered Personalized Tutor Platform

<div align="center">

![Acadefy Logo](https://img.shields.io/badge/🎓-Acadefy-6366f1?style=for-the-badge&labelColor=1f2937)

**Transform your learning experience with AI-driven personalized tutoring**

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-f7df1e?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

[🚀 Live Demo](#-quick-start) • [📖 Documentation](#-documentation) • [🤝 Contributing](#-contributing) • [📄 License](#-license)

</div>

---

## 🌟 Overview

**Acadefy** is a cutting-edge AI tutor platform that delivers **adaptive, context-aware learning support** for students across multiple subjects. Built with modern web technologies and powered by advanced LLM integration, Acadefy provides personalized educational experiences that adapt to each learner's unique needs and progress.

### ✨ Key Features

🤖 **Intelligent AI Tutor**
- Context-aware conversations that remember your learning journey
- Adaptive responses based on your skill level and progress
- Multi-subject support (Math, Science, English, Programming, History)

📊 **Advanced Progress Tracking**
- Visual dashboards with interactive progress bars
- Real-time analytics and learning insights
- Skill level assessment and milestone tracking

🎯 **Personalized Recommendations**
- Smart suggestions based on learning patterns
- Adaptive difficulty adjustment
- Custom learning path generation

🎨 **Modern User Experience**
- Clean, responsive design with smooth animations
- Mobile-first approach for learning on-the-go
- Intuitive navigation and user-friendly interface

---

## 🚀 Quick Start

### Option 1: One-Click Setup (Recommended)

**Windows:**
```bash
# Simply double-click or run:
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

**Cross-platform:**
```bash
python start_app.py
```

### Option 2: Manual Setup

<details>
<summary>Click to expand manual setup instructions</summary>

#### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

#### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/acadefy.git
cd acadefy
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration (optional)
# The default settings work out of the box
```

5. **Initialize database**
```bash
python backend/init_db.py
```

6. **Start the application**
```bash
python start_app.py
```

7. **Access the application**
   - Open your browser to: `http://localhost:5000`
   - Start learning with your AI tutor! 🎉

</details>

---

## 🏗️ Architecture & Tech Stack

<div align="center">

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Python Flask | RESTful API & Business Logic |
| **Frontend** | HTML5, CSS3, Vanilla JS | Responsive User Interface |
| **Database** | SQLAlchemy + SQLite/PostgreSQL | Data Persistence |
| **AI Engine** | LLM Integration (OpenRouter) | Intelligent Tutoring |
| **Styling** | Modern CSS with Grid/Flexbox | Beautiful, Responsive Design |

</div>

### 📁 Project Structure

```
acadefy/
├── 🔧 backend/
│   ├── app.py                 # Flask application entry point
│   ├── models.py              # Database models & schemas
│   ├── init_db.py             # Database initialization
│   ├── 🛣️ routes/
│   │   ├── tutor_routes.py    # AI tutor API endpoints
│   │   └── progress_routes.py # Progress tracking APIs
│   └── 🧠 services/
│       ├── ai_service.py      # LLM integration & context management
│       └── recommendation_service.py # Personalized recommendations
├── 🎨 frontend/
│   ├── 📄 templates/          # HTML templates (Jinja2)
│   └── 📦 static/
│       ├── css/main.css       # Comprehensive styling
│       └── js/                # Interactive JavaScript modules
├── 🔧 Configuration Files
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── .gitignore            # Git ignore rules
└── 📚 Documentation
    ├── README.md             # This file
    └── DEPLOYMENT.md         # Deployment guide
```

---

## 🎯 Features Deep Dive

### 🤖 AI Tutor Chat (`/tutor`)
- **Real-time Conversations**: Instant responses with typing indicators
- **Context Awareness**: Remembers previous interactions and learning progress
- **Multi-subject Support**: Mathematics, Science, English, Programming, History
- **Adaptive Responses**: Adjusts complexity based on user's skill level
- **Session Management**: Persistent chat history and context

### 📊 Learning Dashboard (`/dashboard`)
- **Progress Visualization**: Interactive charts and progress bars
- **Subject Analytics**: Detailed breakdown by subject and topic
- **Performance Metrics**: Accuracy rates, interaction counts, skill levels
- **Learning Streaks**: Gamified progress tracking
- **Smart Recommendations**: AI-generated learning suggestions

### 👤 User Profile (`/profile`)
- **Learning Preferences**: Customizable difficulty and learning style
- **Goal Management**: Set and track personal learning objectives
- **Statistics Overview**: Comprehensive learning analytics
- **Data Export**: Download your learning data and progress

### 🏠 Landing Page (`/`)
- **Feature Showcase**: Interactive demonstration of capabilities
- **Modern Design**: Gradient-based UI with smooth animations
- **Call-to-Action**: Clear pathways to start learning

---

## 🔌 API Documentation

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/tutor` | Send message to AI tutor |
| `GET` | `/api/tutor/history/{session_id}` | Retrieve chat history |
| `GET` | `/api/progress?session_id={id}` | Get learning progress |
| `POST` | `/api/progress` | Update progress data |
| `GET` | `/api/recommendations?session_id={id}` | Get personalized recommendations |
| `GET` | `/api/analytics?session_id={id}` | Get learning analytics |
| `GET` | `/health` | Health check endpoint |

<details>
<summary>📋 API Request/Response Examples</summary>

#### Send Message to AI Tutor
```bash
POST /api/tutor
Content-Type: application/json

{
  "message": "Can you help me understand calculus derivatives?",
  "session_id": "session_123456"
}
```

**Response:**
```json
{
  "response": "I'd be happy to help you with calculus derivatives! A derivative represents the rate of change...",
  "session_id": "session_123456",
  "response_time": 1.23,
  "context_updated": true
}
```

#### Get Learning Progress
```bash
GET /api/progress?session_id=session_123456
```

**Response:**
```json
{
  "session_id": "session_123456",
  "progress": [
    {
      "subject": "mathematics",
      "skill_level": 7,
      "completion_percentage": 75.5,
      "accuracy_rate": 85.2
    }
  ],
  "overall_stats": {
    "total_subjects": 3,
    "average_skill_level": 6.2,
    "total_interactions": 45
  }
}
```

</details>

---

## 🛠️ Development

### Setting Up Development Environment

1. **Fork and clone the repository**
2. **Install development dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up pre-commit hooks** (optional)
```bash
pip install pre-commit
pre-commit install
```

4. **Run in development mode**
```bash
export FLASK_ENV=development
python start_app.py
```

### Code Style & Standards

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: ES6+ with consistent formatting
- **CSS**: BEM methodology for class naming
- **Documentation**: Comprehensive docstrings and comments

### Testing

```bash
# Run backend tests
python -m pytest backend/tests/

# Run frontend tests (if applicable)
npm test
```

---

## 🚀 Deployment

### Production Deployment Options

<details>
<summary>🐳 Docker Deployment</summary>

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "start_app.py"]
```

```bash
docker build -t acadefy .
docker run -p 5000:5000 acadefy
```

</details>

<details>
<summary>☁️ Cloud Platform Deployment</summary>

**Heroku:**
```bash
git push heroku main
```

**Railway:**
```bash
railway login
railway deploy
```

**Vercel/Netlify:** 
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `python start_app.py`

</details>

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment mode | `development` |
| `SECRET_KEY` | Flask secret key | Auto-generated |
| `DATABASE_URL` | Database connection string | `sqlite:///acadefy.db` |
| `LLM_API_KEY` | AI service API key | Provided |
| `LLM_MODEL` | AI model identifier | `moonshotai/kimi-k2:free` |

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? [Open an issue](../../issues)
- 💡 **Feature Requests**: Have an idea? [Start a discussion](../../discussions)
- 🔧 **Code Contributions**: Submit a pull request
- 📖 **Documentation**: Improve our docs
- 🎨 **Design**: Enhance UI/UX

### Contribution Process

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Write clear, concise commit messages
- Add tests for new features
- Update documentation as needed
- Follow existing code style
- Be respectful and inclusive

---

## 📊 Project Stats

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/yourusername/acadefy?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/acadefy?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/acadefy)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/acadefy)

</div>

---

## 🙏 Acknowledgments

- **OpenRouter** for LLM API services
- **Flask** community for the excellent web framework
- **Contributors** who help make Acadefy better
- **Educators** who inspire personalized learning

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 📞 Support & Contact

<div align="center">

**Need help or have questions?**

[![GitHub Issues](https://img.shields.io/badge/GitHub-Issues-red?style=flat-square&logo=github)](../../issues)
[![Discussions](https://img.shields.io/badge/GitHub-Discussions-blue?style=flat-square&logo=github)](../../discussions)
[![Email](https://img.shields.io/badge/Email-Contact-green?style=flat-square&logo=gmail)](mailto:your-email@example.com)

**⭐ If you find Acadefy helpful, please consider giving it a star!**

</div>

---

<div align="center">

**Built with ❤️ for the future of personalized education**

*Acadefy - Where AI meets personalized learning*

</div>