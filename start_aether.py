#!/usr/bin/env python3
"""
AETHER: AI-Powered Satellite-Integrated Intelligent Mobility System
Unified Startup Script

This script starts both backend and frontend as a single unified system.
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def print_banner():
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║     🌐 AETHER: AI-Powered Satellite-Integrated Intelligent Mobility System  ║
    ║                                                                              ║
    ║     ✅ AI-Based Vehicle Health Monitoring                                    ║
    ║     ✅ Predictive Accident Prevention System                                 ║
    ║     ✅ AI-Integrated Navigation with Satellite Connectivity                  ║
    ║     ✅ Smart Drone Assistance System                                         ║
    ║     ✅ Real-Time Environmental Awareness                                     ║
    ║     ✅ Predictive Traffic and Fuel Optimization                              ║
    ║     ✅ AI Emergency Response & Safety Cloud                                  ║
    ║     ✅ Driver Behavior & Emotion Analysis                                    ║
    ║     ✅ Universal Fleet Management Dashboard                                  ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python packages
    required_packages = [
        'fastapi', 'uvicorn', 'psutil', 'requests', 'numpy', 'cv2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
            return False
    
    # Check Node.js and npm for frontend
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("  ✅ Node.js and npm")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ❌ Node.js/npm not found. Please install Node.js")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies"""
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return False
    
    print("📦 Installing frontend dependencies...")
    try:
        subprocess.run(
            ["npm", "install"], 
            cwd=frontend_path, 
            check=True,
            capture_output=True
        )
        print("✅ Frontend dependencies installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False

def start_backend():
    """Start the AETHER backend"""
    print("🚀 Starting AETHER Backend...")
    backend_path = Path("backend")
    
    try:
        # Start backend in a separate process
        process = subprocess.Popen(
            [sys.executable, "universal_backend.py"],
            cwd=backend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        if process.poll() is None:  # Process is still running
            print("✅ Backend started successfully!")
            print("🌐 Backend URL: http://localhost:8000")
            print("📡 WebSocket: ws://localhost:8000/ws")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the AETHER frontend"""
    print("🎨 Starting AETHER Frontend...")
    frontend_path = Path("frontend")
    
    try:
        # Start frontend in a separate process
        process = subprocess.Popen(
            ["npm", "start"],
            cwd=frontend_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for frontend to start
        time.sleep(5)
        
        if process.poll() is None:  # Process is still running
            print("✅ Frontend started successfully!")
            print("🖥️  Frontend URL: http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitor both processes and restart if needed"""
    print("\n👁️  Monitoring AETHER system...")
    print("Press Ctrl+C to stop the system")
    
    try:
        while True:
            time.sleep(5)
            
            # Check backend
            if backend_process and backend_process.poll() is not None:
                print("⚠️  Backend process stopped. Restarting...")
                backend_process = start_backend()
            
            # Check frontend
            if frontend_process and frontend_process.poll() is not None:
                print("⚠️  Frontend process stopped. Restarting...")
                frontend_process = start_frontend()
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AETHER system...")
        
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
            
        print("👋 AETHER system shutdown complete!")

def main():
    """Main function to start the unified AETHER system"""
    print_banner()
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the AETHER root directory")
        print("   Expected structure: AETHER/backend/ and AETHER/frontend/")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required packages.")
        return
    
    # Install frontend dependencies if needed
    if not Path("frontend/node_modules").exists():
        if not install_frontend_dependencies():
            return
    
    print("\n" + "="*80)
    print("🚀 Starting AETHER Unified System...")
    print("="*80)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Wait a moment for backend to fully initialize
    time.sleep(2)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend.")
        backend_process.terminate()
        return
    
    print("\n" + "="*80)
    print("✅ AETHER System Started Successfully!")
    print("="*80)
    print("🌐 Backend:  http://localhost:8000")
    print("🖥️  Frontend: http://localhost:3000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("📡 WebSocket: ws://localhost:8000/ws")
    print("="*80)
    
    # Monitor processes
    monitor_processes(backend_process, frontend_process)

if __name__ == "__main__":
    main()