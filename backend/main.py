from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import random

app = FastAPI(title="AETHER API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

# Simulated vehicle data
def generate_vehicle_data():
    return {
        "vehicle_id": "AETHER_001",
        "timestamp": datetime.now().isoformat(),
        "location": {
            "latitude": 28.6139 + random.uniform(-0.1, 0.1),
            "longitude": 77.2090 + random.uniform(-0.1, 0.1),
            "altitude": 200 + random.uniform(-50, 50)
        },
        "health": {
            "engine_temp": 85 + random.uniform(-10, 15),
            "battery_level": 85 + random.uniform(-20, 15),
            "tire_pressure": [32, 31, 33, 32],
            "brake_health": 95 + random.uniform(-10, 5),
            "overall_score": 88 + random.uniform(-15, 12)
        },
        "safety": {
            "collision_risk": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "driver_alertness": random.uniform(0.7, 1.0),
            "weather_conditions": random.choice(["CLEAR", "RAIN", "FOG"]),
            "road_conditions": random.choice(["GOOD", "MODERATE", "POOR"])
        },
        "navigation": {
            "current_speed": random.uniform(40, 80),
            "destination": "Connaught Place, Delhi",
            "eta": "15 minutes",
            "fuel_level": 65 + random.uniform(-20, 20),
            "next_service_km": 2500 - random.randint(0, 500)
        }
    }

@app.get("/")
async def root():
    return {"message": "AETHER API is running", "version": "1.0.0"}

@app.get("/api/vehicle/{vehicle_id}")
async def get_vehicle_data(vehicle_id: str):
    return generate_vehicle_data()

@app.get("/api/fleet/status")
async def get_fleet_status():
    return {
        "total_vehicles": 25,
        "active_vehicles": 23,
        "maintenance_required": 2,
        "emergency_alerts": 0,
        "avg_health_score": 87.5
    }

@app.post("/api/emergency/alert")
async def emergency_alert(alert_data: dict):
    alert = {
        "type": "EMERGENCY",
        "timestamp": datetime.now().isoformat(),
        "data": alert_data
    }
    await manager.broadcast(alert)
    return {"status": "Alert sent", "alert_id": f"ALERT_{datetime.now().timestamp()}"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send real-time vehicle data every 2 seconds
            data = generate_vehicle_data()
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)