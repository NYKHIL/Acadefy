#!/bin/bash

echo ""
echo "========================================"
echo "   Acadefy - AI Tutor Platform"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Setup environment file
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
fi

# Initialize database
echo "🗄️ Initializing database..."
cd backend
python init_db.py
if [ $? -ne 0 ]; then
    echo "⚠️ Database initialization had issues, continuing..."
fi
cd ..

echo ""
echo "🎉 Setup complete!"
echo "🌐 Starting Acadefy..."
echo "📱 Open your browser to: http://localhost:5000"
echo "⏹️ Press Ctrl+C to stop the server"
echo ""
echo "========================================"

# Start the application
cd backend
python app.py