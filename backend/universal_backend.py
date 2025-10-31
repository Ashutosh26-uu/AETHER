from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
from datetime import datetime
from universal_device_analyzer import UniversalDeviceAnalyzer
from dynamic_device_detector import DynamicDeviceDetector

app = FastAPI(title="AETHER Universal Device Health Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize dynamic detector and universal analyzer
detector = DynamicDeviceDetector()
analyzer = UniversalDeviceAnalyzer()

@app.get("/")
async def root():
    device_data = detector.get_comprehensive_device_data()
    device_info = device_data['device_info']
    manufacturer = device_data['manufacturer_info']
    vehicle_type = device_data['device_config']['vehicle_analogy']
    
    return HTMLResponse(f"""
    <html>
        <head><title>AETHER Dynamic Device Monitor</title></head>
        <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1>🌐 AETHER Dynamic Device Health Monitor</h1>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h2>📱 Detected Device</h2>
                <p><strong>Type:</strong> {device_info['type'].replace('_', ' ').title()}</p>
                <p><strong>Category:</strong> {device_info['category'].replace('_', ' ').title()}</p>
                <p><strong>Subcategory:</strong> {device_info['subcategory'].replace('_', ' ').title()}</p>
                <p><strong>Manufacturer:</strong> {manufacturer['brand']}</p>
                <p><strong>Model:</strong> {manufacturer['model']}</p>
                <p><strong>Form Factor:</strong> {device_info['form_factor'].replace('_', ' ').title()}</p>
                <p><strong>Mobility:</strong> {device_info['mobility'].title()}</p>
                <p><strong>Power Source:</strong> {device_info['power_source'].replace('_', ' ').title()}</p>
                <p><strong>Vehicle Analogy:</strong> {vehicle_type}</p>
                <p><strong>Device ID:</strong> {device_info['device_id']}</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                <h2>🔧 Dynamic Features</h2>
                <p>✅ Advanced device type detection (Mobile, IoT, Automotive)</p>
                <p>✅ Manufacturer identification and optimization</p>
                <p>✅ Adaptive health thresholds per device category</p>
                <p>✅ Device-specific vehicle analogies</p>
                <p>✅ Form factor and mobility awareness</p>
                <p>✅ Power source optimization</p>
                <p>✅ Real-time capability detection</p>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                <h2>🌐 API Endpoints</h2>
                <p>📊 <a href="/api/device-health" style="color: #FFD700;">Device Health Data</a></p>
                <p>🔍 <a href="/api/device-detection" style="color: #FFD700;">Dynamic Device Detection</a></p>
                <p>🏭 <a href="/api/manufacturer-info" style="color: #FFD700;">Manufacturer Information</a></p>
                <p>📈 <a href="/api/health-analysis" style="color: #FFD700;">Health Analysis</a></p>
                <p>🚗 <a href="/api/vehicle-analogy" style="color: #FFD700;">Vehicle Analogy Data</a></p>
                <p>⚙️ <a href="/api/device-capabilities" style="color: #FFD700;">Device Capabilities</a></p>
                <p>💡 <a href="/api/optimization-tips" style="color: #FFD700;">Optimization Tips</a></p>
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
    """Get detected device information (legacy endpoint)"""
    return {
        "device_info": analyzer.device_info,
        "device_config": analyzer.device_config,
        "supported_metrics": analyzer.device_config["health_metrics"],
        "vehicle_analogy": analyzer.device_config["vehicle_analogy"]
    }

@app.get("/api/device-detection")
async def get_device_detection():
    """Get comprehensive dynamic device detection data"""
    return detector.get_comprehensive_device_data()

@app.get("/api/manufacturer-info")
async def get_manufacturer_info():
    """Get manufacturer information"""
    return detector.manufacturer_info

@app.get("/api/device-capabilities")
async def get_device_capabilities():
    """Get device capabilities"""
    return detector.get_device_capabilities()

@app.get("/api/optimization-tips")
async def get_optimization_tips():
    """Get device-specific optimization tips"""
    return {
        "device_type": detector.device_info["type"],
        "manufacturer": detector.manufacturer_info["brand"],
        "optimization_tips": detector.get_optimization_tips(),
        "recommended_features": detector.get_recommended_features()
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
            
            # Adaptive update frequency based on device configuration
            update_interval = detector.device_config["update_interval"]
            await asyncio.sleep(update_interval)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    
    device_info = analyzer.device_info
    device_data = detector.get_comprehensive_device_data()
    device_info = device_data['device_info']
    manufacturer = device_data['manufacturer_info']
    
    print("🌐 AETHER Dynamic Device Health Monitor")
    print("=" * 60)
    print(f"📱 Device Type: {device_info['type'].replace('_', ' ').title()}")
    print(f"🏭 Manufacturer: {manufacturer['brand']} {manufacturer['model']}")
    print(f"🖥️ System: {device_info['system'].title()} ({device_info['architecture']})")
    print(f"📦 Form Factor: {device_info['form_factor'].replace('_', ' ').title()}")
    print(f"🔋 Power Source: {device_info['power_source'].replace('_', ' ').title()}")
    print(f"🚗 Vehicle Analogy: {device_data['device_config']['vehicle_analogy']}")
    print(f"📊 Health Metrics: {', '.join(device_data['device_config']['health_metrics'])}")
    print(f"⚡ Update Interval: {device_data['device_config']['update_interval']}s")
    
    print("\n🎯 Device Capabilities:")
    capabilities = detector.get_device_capabilities()
    for capability, value in capabilities.items():
        status = "✅" if value else "❌"
        print(f"  {status} {capability.replace('_', ' ').title()}")
    
    print("\n✅ Starting dynamic health monitor...")
    print("🌐 Supports: Mobile, IoT, Automotive, Desktop, Laptop devices")
    print("📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)