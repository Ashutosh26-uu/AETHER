from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
import subprocess
import os
import sys
import threading
import time
from datetime import datetime
from vehicle_obd_analyzer import VehicleOBDAnalyzer
from universal_device_analyzer import UniversalDeviceAnalyzer

app = FastAPI(title="AETHER Auto-Start Universal Monitor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
vehicle_analyzer = VehicleOBDAnalyzer()
device_analyzer = UniversalDeviceAnalyzer()

# Auto-detect what we're monitoring
monitoring_mode = "device"  # Default to device monitoring

@app.on_event("startup")
async def startup_event():
    """Auto-detect monitoring mode on startup"""
    global monitoring_mode
    
    print("🔍 Auto-detecting monitoring target...")
    
    # Try to detect real vehicle first
    if vehicle_analyzer.detect_vehicle_connection():
        vehicle_analyzer.identify_vehicle_type()
        monitoring_mode = "vehicle"
        print(f"✅ Real vehicle detected: {vehicle_analyzer.vehicle_config.get('name', 'Unknown')}")
    else:
        monitoring_mode = "device"
        print(f"📱 Device monitoring mode: {device_analyzer.device_info['type']}")

@app.get("/")
async def root():
    if monitoring_mode == "vehicle":
        vehicle_name = vehicle_analyzer.vehicle_config.get('name', 'Vehicle')
        connection_type = vehicle_analyzer.vehicle_type
        
        return HTMLResponse(f"""
        <html>
            <head><title>AETHER Vehicle Monitor</title></head>
            <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%); color: white;">
                <h1>🚗 AETHER Real Vehicle Monitor</h1>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h2>🚗 Connected Vehicle</h2>
                    <p><strong>Vehicle Type:</strong> {vehicle_name}</p>
                    <p><strong>Connection:</strong> {connection_type.replace('_', ' ').title()}</p>
                    <p><strong>Status:</strong> ✅ Real-time OBD monitoring active</p>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    <h2>🔧 Vehicle Features</h2>
                    <p>✅ Real OBD-II data from vehicle ECU</p>
                    <p>✅ Engine RPM, temperature, load monitoring</p>
                    <p>✅ Speed, throttle, fuel level tracking</p>
                    <p>✅ Battery voltage and electrical system</p>
                    <p>✅ Automotive-grade health analysis</p>
                    <p>✅ Critical engine alerts and warnings</p>
                </div>
                
                <p style="margin-top: 30px;">📡 WebSocket: ws://localhost:8003/ws</p>
                <p>📖 API Docs: <a href="/docs" style="color: #FFD700;">/docs</a></p>
            </body>
        </html>
        """)
    else:
        device_type = device_analyzer.device_info['type']
        vehicle_analogy = device_analyzer.device_config['vehicle_analogy']
        
        return HTMLResponse(f"""
        <html>
            <head><title>AETHER Device Monitor</title></head>
            <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h1>📱 AETHER Device Monitor</h1>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h2>📱 Connected Device</h2>
                    <p><strong>Device Type:</strong> {device_type.replace('_', ' ').title()}</p>
                    <p><strong>Vehicle Analogy:</strong> {vehicle_analogy}</p>
                    <p><strong>Status:</strong> ✅ Real-time system monitoring active</p>
                </div>
                
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;">
                    <h2>🔧 Device Features</h2>
                    <p>✅ Real system temperature monitoring</p>
                    <p>✅ CPU usage as vehicle speed</p>
                    <p>✅ Battery level tracking (if available)</p>
                    <p>✅ Memory usage as system health</p>
                    <p>✅ Device-specific health thresholds</p>
                    <p>✅ Adaptive performance analysis</p>
                </div>
                
                <p style="margin-top: 30px;">📡 WebSocket: ws://localhost:8003/ws</p>
                <p>📖 API Docs: <a href="/docs" style="color: #FFD700;">/docs</a></p>
            </body>
        </html>
        """)

@app.get("/api/monitoring-mode")
async def get_monitoring_mode():
    """Get current monitoring mode and target info"""
    if monitoring_mode == "vehicle":
        return {
            "mode": "vehicle",
            "target": vehicle_analyzer.vehicle_config.get('name', 'Unknown Vehicle'),
            "connection": vehicle_analyzer.vehicle_type,
            "specs": vehicle_analyzer.vehicle_config
        }
    else:
        return {
            "mode": "device", 
            "target": device_analyzer.device_info['type'],
            "vehicle_analogy": device_analyzer.device_config['vehicle_analogy'],
            "device_info": device_analyzer.device_info
        }

@app.get("/api/health-data")
async def get_health_data():
    """Get health data based on monitoring mode"""
    if monitoring_mode == "vehicle":
        return vehicle_analyzer.get_real_vehicle_data()
    else:
        return device_analyzer.get_device_health_data()

@app.post("/api/start-frontend")
async def start_frontend():
    """Auto-start frontend when requested"""
    try:
        frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
        
        def start_frontend_process():
            try:
                # Change to frontend directory and start
                os.chdir(frontend_path)
                subprocess.run(['npm', 'start'], shell=True)
            except Exception as e:
                print(f"Frontend start error: {e}")
        
        # Start frontend in background thread
        frontend_thread = threading.Thread(target=start_frontend_process)
        frontend_thread.daemon = True
        frontend_thread.start()
        
        return {"message": "Frontend starting...", "url": "http://localhost:3000"}
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Get data based on monitoring mode
            if monitoring_mode == "vehicle":
                data = vehicle_analyzer.get_real_vehicle_data()
            else:
                data = device_analyzer.get_device_health_data()
            
            # Add monitoring mode info
            data["monitoring_mode"] = monitoring_mode
            
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)  # Update every 2 seconds
    except:
        pass

# Auto-start function
def auto_start_backend():
    """Function to auto-start backend when frontend requests it"""
    import uvicorn
    
    print("🚀 AETHER Auto-Start Backend")
    print("=" * 50)
    print("🔍 Auto-detecting monitoring target...")
    print("🚗 Checking for real vehicles (OBD-II, CAN, Bluetooth)")
    print("📱 Fallback to device monitoring if no vehicle found")
    print("✅ Backend will start automatically")
    print("🌐 Frontend can trigger backend startup")
    print("\n📱 Frontend: http://localhost:3000")
    print("🖥️ Backend: http://localhost:8003")
    
    uvicorn.run(app, host="127.0.0.1", port=8003)

if __name__ == "__main__":
    auto_start_backend()