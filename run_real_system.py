#!/usr/bin/env python3
"""
AETHER Real System Runner
Uses your laptop as a vehicle simulator with real system data
"""

import uvicorn
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.real_system_backend import app

if __name__ == "__main__":
    print("🚗 AETHER Real System Vehicle Simulator")
    print("=" * 50)
    print("🔄 Converting your laptop into a vehicle...")
    print("🌡️ CPU Temperature → Engine Temperature")
    print("🔋 Battery Level → Vehicle Battery")
    print("⚡ CPU Usage → Vehicle Speed")
    print("💾 Memory Usage → System Health")
    print("📊 Real-time monitoring active")
    print("\n✅ Starting server...")
    print("📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n🎮 Try the stress test to simulate highway driving!")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)