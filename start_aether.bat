@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║     🌐 AETHER: AI-Powered Satellite-Integrated Intelligent Mobility System  ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Starting AETHER System...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js.
    pause
    exit /b 1
)

REM Install Python dependencies if needed
if not exist "backend\__pycache__" (
    echo 📦 Installing Python dependencies...
    pip install -r requirements.txt
)

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

echo.
echo ✅ Starting AETHER unified system...
echo.

REM Start the unified system
python start_aether.py

pause