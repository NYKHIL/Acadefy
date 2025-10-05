#!/usr/bin/env python3
"""
Simple Acadefy App Starter
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change to backend directory
os.chdir(backend_dir)

# Import and run the app
try:
    from app import app
    print("🎓 Starting Acadefy AI Tutor Platform...")
    print("🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install -r requirements.txt")
    
except Exception as e:
    print(f"❌ Error starting app: {e}")
    print("Check the error details above and try again.")