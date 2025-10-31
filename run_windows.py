#!/usr/bin/env python3
"""
AETHER Auto-Start Universal Monitor - Windows Compatible
"""

import uvicorn
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.auto_start_backend_windows import app

if __name__ == "__main__":
    print("AETHER Auto-Start Universal Monitor")
    print("=" * 60)
    print("Starting backend on port 8003...")
    print("Frontend: http://localhost:3000")
    print("Backend: http://localhost:8004")
    print("API Docs: http://localhost:8004/docs")
    
    uvicorn.run(app, host="127.0.0.1", port=8003)