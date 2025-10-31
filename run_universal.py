#!/usr/bin/env python3
"""
AETHER Universal Device Health Monitor
Works on ANY electronic device - Laptops, Desktops, Tablets, Raspberry Pi, Android, IoT devices
"""

import uvicorn
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.universal_backend import app

if __name__ == "__main__":
    print("🌐 AETHER Universal Device Health Monitor")
    print("=" * 60)
    print("📱 WORKS ON ANY DEVICE:")
    print("  💻 Laptops (Windows, Mac, Linux)")
    print("  🖥️ Desktops (All platforms)")
    print("  📱 Tablets (Windows, Android)")
    print("  🤖 Raspberry Pi & IoT devices")
    print("  📱 Android devices (with Termux)")
    print("  🐧 Linux embedded systems")
    print("\n🔄 ADAPTIVE FEATURES:")
    print("  🌡️ Device-specific temperature monitoring")
    print("  🔋 Platform-appropriate battery tracking")
    print("  ⚡ Optimized performance thresholds")
    print("  🚗 Custom vehicle analogies per device")
    print("  📊 Tailored health recommendations")
    print("\n✅ Starting universal monitor...")
    print("📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n🎮 Features:")
    print("  ⚡ Device-appropriate stress testing")
    print("  📊 Real-time adaptive health monitoring")
    print("  🚨 Smart alerts based on device type")
    print("  🔍 Detailed device-specific analysis")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)