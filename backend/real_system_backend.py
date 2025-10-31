from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
from datetime import datetime
from laptop_vehicle_simulator import LaptopVehicleSimulator

app = FastAPI(title="AETHER Real System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize laptop simulator
simulator = LaptopVehicleSimulator()

@app.get("/")
async def root():
    return HTMLResponse("""
    <html>
        <head><title>AETHER Real System Dashboard</title></head>
        <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1>🚗 AETHER Real System Monitor</h1>
            <p>✅ Using your laptop as a vehicle simulator</p>
            <p>📊 Real-time system data converted to vehicle metrics</p>
            <p>🌡️ CPU Temperature → Engine Temperature</p>
            <p>🔋 Battery Level → Vehicle Battery</p>
            <p>⚡ CPU Usage → Vehicle Speed</p>
            <p>💾 Memory Usage → System Health</p>
            <br>
            <p>📡 WebSocket: ws://localhost:8000/ws</p>
            <p>📖 API Docs: <a href="/docs" style="color: #FFD700;">/docs</a></p>
            <p>📊 Real Vehicle Data: <a href="/api/real-vehicle" style="color: #FFD700;">/api/real-vehicle</a></p>
            <p>🔍 System Analysis: <a href="/api/system-analysis" style="color: #FFD700;">/api/system-analysis</a></p>
        </body>
    </html>
    """)

@app.get("/api/real-vehicle")
async def get_real_vehicle_data():
    """Get real laptop data as vehicle data"""
    return simulator.get_real_vehicle_data()

@app.get("/api/system-analysis")
async def get_system_analysis():
    """Get detailed system performance analysis"""
    return simulator.get_performance_analysis()

@app.post("/api/simulate-scenario")
async def simulate_scenario(scenario: dict):
    """Simulate different driving scenarios"""
    scenario_type = scenario.get("type", "normal")
    return simulator.simulate_driving_scenario(scenario_type)

@app.get("/api/stress-test")
async def stress_test():
    """Trigger system stress test to simulate heavy driving"""
    import threading
    import time
    
    def cpu_stress():
        # Light CPU stress for 10 seconds
        end_time = time.time() + 10
        while time.time() < end_time:
            pass
    
    # Start stress test in background
    thread = threading.Thread(target=cpu_stress)
    thread.start()
    
    return {"message": "Stress test started - simulating highway driving", "duration": "10 seconds"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Get real system data as vehicle data
            data = simulator.get_real_vehicle_data()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)  # Update every 2 seconds
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    print("🚗 Starting AETHER Real System Backend...")
    print("📊 Your laptop is now a vehicle!")
    print("🌡️ Monitoring CPU temperature as engine heat")
    print("🔋 Monitoring battery as vehicle power")
    print("⚡ Monitoring CPU usage as vehicle speed")
    print("\n✅ Server starting on http://localhost:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)