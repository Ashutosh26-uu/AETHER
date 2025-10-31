#!/usr/bin/env python3
"""
Simple AETHER Demo Runner
"""
import uvicorn
from backend.main import app

if __name__ == "__main__":
    print("🚀 Starting AETHER Backend Server...")
    print("📊 Dashboard will be available at: http://localhost:8000")
    print("📡 WebSocket endpoint: ws://localhost:8000/ws")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("\n✅ Server starting...")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)