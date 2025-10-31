from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json
import asyncio
from datetime import datetime
import random

app = FastAPI(title="AETHER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_vehicle_data():
    return {
        "vehicle_id": "AETHER_001",
        "timestamp": datetime.now().isoformat(),
        "location": {
            "latitude": 28.6139 + random.uniform(-0.01, 0.01),
            "longitude": 77.2090 + random.uniform(-0.01, 0.01)
        },
        "health": {
            "engine_temp": 85 + random.uniform(-10, 15),
            "battery_level": 85 + random.uniform(-20, 15),
            "overall_score": 88 + random.uniform(-15, 12)
        },
        "safety": {
            "collision_risk": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "driver_alertness": random.uniform(0.7, 1.0)
        },
        "navigation": {
            "current_speed": random.uniform(40, 80),
            "fuel_level": 65 + random.uniform(-20, 20)
        }
    }

@app.get("/")
async def root():
    return HTMLResponse("""
    <html>
        <head><title>AETHER Dashboard</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>🚀 AETHER System Running</h1>
            <p>✅ Backend API: Active</p>
            <p>📡 WebSocket: ws://localhost:8000/ws</p>
            <p>📖 API Docs: <a href="/docs">/docs</a></p>
            <p>📊 Vehicle Data: <a href="/api/vehicle/AETHER_001">/api/vehicle/AETHER_001</a></p>
            <h2>Real-time Data:</h2>
            <div id="data"></div>
            <script>
                const ws = new WebSocket('ws://localhost:8000/ws');
                ws.onmessage = function(event) {
                    document.getElementById('data').innerHTML = '<pre>' + event.data + '</pre>';
                };
            </script>
        </body>
    </html>
    """)

@app.get("/api/vehicle/{vehicle_id}")
async def get_vehicle_data(vehicle_id: str):
    return generate_vehicle_data()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = generate_vehicle_data()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)
    except:
        pass