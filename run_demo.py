#!/usr/bin/env python3
import uvicorn
from backend.simple_main import app

if __name__ == "__main__":
    print("🚀 AETHER Demo Server Starting...")
    print("📊 Open: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)