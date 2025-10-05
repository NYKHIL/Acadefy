@echo off
echo.
echo ========================================
echo   Acadefy - AI Tutor Platform
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Setup environment file
if not exist ".env" (
    if exist ".env.example" (
        echo 📝 Creating .env file...
        copy .env.example .env
        echo ✅ .env file created
    )
)

REM Initialize database
echo 🗄️ Initializing database...
cd backend
python init_db.py
if errorlevel 1 (
    echo ⚠️ Database initialization had issues, continuing...
)
cd ..

echo.
echo 🎉 Setup complete!
echo 🌐 Starting Acadefy...
echo 📱 Open your browser to: http://localhost:5000
echo ⏹️ Press Ctrl+C to stop the server
echo.
echo ========================================

REM Start the application
cd backend
python app.py

pause