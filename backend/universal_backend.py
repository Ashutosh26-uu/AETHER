from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
from datetime import datetime
from universal_device_analyzer import UniversalDeviceAnalyzer

app = FastAPI(title="AETHER Universal Device Health Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize universal analyzer
analyzer = UniversalDeviceAnalyzer()

@app.get("/")
async def root():
    device_info = analyzer.device_info
    vehicle_type = analyzer.device_config["vehicle_analogy"]
    
    return HTMLResponse(f"""
    <html>
        <head><title>AETHER Universal Device Monitor</title></head>
        <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1>🌐 AETHER Universal Device Health Monitor</h1>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h2>📱 Detected Device</h2>
                <p><strong>Type:</strong> {device_info['type'].title()}</p>
                <p><strong>System:</strong> {device_info['system'].title()}</p>
                <p><strong>Category:</strong> {device_info['category'].title()}</p>
                <p><strong>Vehicle Analogy:</strong> {vehicle_type}</p>
                <p><strong>Device ID:</strong> {device_info['device_id']}</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h2>🔧 Device-Specific Features</h2>
                <p>✅ Adaptive health thresholds based on device type</p>
                <p>✅ Device-specific temperature monitoring</p>
                <p>✅ Custom vehicle analogies per device</p>
                <p>✅ Platform-optimized performance analysis</p>
                <p>✅ Real-time health recommendations</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h2>🌐 API Endpoints</h2>
                <p>📊 <a href="/api/device-health" style="color: #FFD700;">Device Health Data</a></p>
                <p>🔍 <a href="/api/device-info" style="color: #FFD700;">Device Information</a></p>
                <p>📈 <a href="/api/health-analysis" style="color: #FFD700;">Health Analysis</a></p>
                <p>🚗 <a href="/api/vehicle-analogy" style="color: #FFD700;">Vehicle Analogy Data</a></p>
                <p>📖 <a href="/docs" style="color: #FFD700;">API Documentation</a></p>
                <p>📡 WebSocket: ws://localhost:8000/ws</p>
            </div>
        </body>
    </html>
    """)

@app.get("/api/device-health")
async def get_device_health():
    """Get comprehensive device health data"""
    return analyzer.get_device_health_data()

@app.get("/api/device-info")
async def get_device_info():
    """Get detected device information"""
    return {
        "device_info": analyzer.device_info,
        "device_config": analyzer.device_config,
        "supported_metrics": analyzer.device_config["health_metrics"],
        "vehicle_analogy": analyzer.device_config["vehicle_analogy"]
    }

@app.get("/api/health-analysis")
async def get_health_analysis():
    """Get detailed health analysis"""
    data = analyzer.get_device_health_data()
    return {
        "device_type": data["device_info"]["type"],
        "health_analysis": data["health_analysis"],
        "raw_metrics": data["raw_metrics"],
        "timestamp": data["timestamp"]
    }

@app.get("/api/vehicle-analogy")
async def get_vehicle_analogy():
    """Get vehicle analogy data"""
    data = analyzer.get_device_health_data()
    return {
        "device_type": data["device_info"]["type"],
        "vehicle_analogy": data["vehicle_analogy"],
        "health_score": data["health_analysis"]["overall_score"],
        "status": data["health_analysis"]["status"]
    }

@app.post("/api/device-stress-test")
async def device_stress_test():
    """Run device-appropriate stress test"""
    device_type = analyzer.device_info["type"]
    
    stress_messages = {
        "laptop": "🖥️ Laptop stress test - Simulating heavy workload",
        "desktop": "🖥️ Desktop stress test - Maximum performance mode",
        "tablet": "📱 Tablet stress test - Intensive app usage simulation",
        "raspberry_pi": "🤖 IoT device stress test - Sensor data processing",
        "android_device": "📱 Mobile device stress test - Gaming mode simulation"
    }
    
    message = stress_messages.get(device_type, "⚡ Generic device stress test")
    
    # Light stress test appropriate for device
    import threading
    import time
    
    def device_appropriate_stress():
        duration = 5 if device_type in ["tablet", "android_device"] else 10
        end_time = time.time() + duration
        while time.time() < end_time:
            pass
    
    thread = threading.Thread(target=device_appropriate_stress)
    thread.start()
    
    return {
        "message": message,
        "device_type": device_type,
        "duration": "5-10 seconds",
        "warning": "Monitor temperature during test"
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Get real-time device health data
            data = analyzer.get_device_health_data()
            await websocket.send_text(json.dumps(data))
            
            # Adaptive update frequency based on device type
            device_type = analyzer.device_info["type"]
            if device_type in ["tablet", "android_device"]:
                await asyncio.sleep(3)  # Slower updates for mobile devices
            elif device_type == "raspberry_pi":
                await asyncio.sleep(5)  # Even slower for IoT devices
            else:
                await asyncio.sleep(2)  # Standard for computers
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    
    device_info = analyzer.device_info
    print("🌐 AETHER Universal Device Health Monitor")
    print("=" * 50)
    print(f"📱 Detected Device: {device_info['type'].title()}")
    print(f"🖥️ System: {device_info['system'].title()}")
    print(f"🚗 Vehicle Analogy: {analyzer.device_config['vehicle_analogy']}")
    print(f"📊 Health Metrics: {', '.join(analyzer.device_config['health_metrics'])}")
    print("\n✅ Starting universal health monitor...")
    print("🌐 Works on: Laptops, Desktops, Tablets, Raspberry Pi, Android, IoT devices")
    print("📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)