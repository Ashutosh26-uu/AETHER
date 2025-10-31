#!/usr/bin/env python3
"""
AETHER Auto-Start Universal Monitor
Automatically detects and monitors:
- Real vehicles (cars, trucks, motorcycles, buses) via OBD-II
- Electronic devices (laptops, desktops, tablets, IoT devices)
- Backend starts automatically when frontend loads
"""

import uvicorn
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.auto_start_backend import app

if __name__ == "__main__":
    print("🚀 AETHER Auto-Start Universal Monitor")
    print("=" * 60)
    print("🎯 UNIVERSAL MONITORING SYSTEM:")
    print("  🚗 Real Vehicles: Cars, Trucks, Motorcycles, Buses")
    print("  📱 Electronic Devices: Laptops, Tablets, IoT devices")
    print("  🔌 Connection Methods: OBD-II, CAN bus, Bluetooth, WiFi")
    print("  📟 Device Types: Windows, Mac, Linux, Android, Raspberry Pi")
    print("\n🔍 AUTO-DETECTION PROCESS:")
    print("  1️⃣ Scan for real vehicle connections (OBD-II ports)")
    print("  2️⃣ Check for CAN bus interfaces")
    print("  3️⃣ Search for Bluetooth/WiFi OBD adapters")
    print("  4️⃣ Fallback to device monitoring if no vehicle found")
    print("  5️⃣ Auto-configure thresholds and vehicle analogies")
    print("\n⚡ AUTO-START FEATURES:")
    print("  🔄 Backend starts automatically when frontend loads")
    print("  🎛️ No manual commands needed")
    print("  📊 Real-time adaptive monitoring")
    print("  🚨 Smart alerts based on target type")
    print("\n✅ Starting auto-detection server...")
    print("📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8003")
    print("📖 API Docs: http://localhost:8003/docs")
    print("\n🎮 SUPPORTED VEHICLES:")
    print("  🚗 Passenger Cars (Petrol/Diesel/Hybrid/Electric)")
    print("  🚛 Heavy Trucks and Commercial Vehicles")
    print("  🏍️ Motorcycles and Scooters")
    print("  🚌 Buses and Public Transport")
    print("  🚜 Agricultural and Construction Vehicles")
    print("\n📱 SUPPORTED DEVICES:")
    print("  💻 Laptops (Windows/Mac/Linux)")
    print("  🖥️ Desktop Computers")
    print("  📱 Tablets and Mobile Devices")
    print("  🤖 Raspberry Pi and IoT Devices")
    print("  🐧 Embedded Linux Systems")
    
    uvicorn.run(app, host="127.0.0.1", port=8003)