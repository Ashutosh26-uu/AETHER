# 🚀 AETHER Quick Start Guide

## Missing Components Analysis:

### ❌ Currently Missing:
1. **AI Dependencies**: TensorFlow, PyTorch, OpenCV (large downloads)
2. **IoT Hardware**: Physical sensors, MQTT broker
3. **Drone Hardware**: Actual drone connection
4. **Satellite APIs**: NavIC/GPS API keys
5. **Database**: PostgreSQL setup
6. **Cloud Services**: AWS credentials

### ✅ What Works Now:
- Backend API server with simulated data
- WebSocket real-time communication
- Basic dashboard structure
- Simulated vehicle data

## 🏃‍♂️ Quick Demo (2 Minutes):

### Option 1: Backend Only
```bash
cd AETHER
pip install fastapi uvicorn websockets pydantic
python run_simple.py
```
Visit: http://localhost:8000

### Option 2: Full Frontend + Backend
```bash
# Terminal 1 - Backend
cd AETHER
pip install -r requirements_minimal.txt
python run_simple.py

# Terminal 2 - Frontend
cd AETHER/frontend
npm install --legacy-peer-deps
npm start
```
Visit: http://localhost:3000

## 🔧 For Full System:

### Install All Dependencies:
```bash
pip install -r requirements.txt
```

### Start Complete System:
```bash
python main.py
```

## 📊 Demo Features:
- ✅ Real-time vehicle data simulation
- ✅ WebSocket live updates
- ✅ Health monitoring dashboard
- ✅ Fleet management interface
- ✅ API documentation at /docs

## 🚨 Known Issues:
1. Some AI models need training data
2. Hardware sensors are simulated
3. Drone requires physical connection
4. Database needs PostgreSQL setup

## 💡 For Hackathon Demo:
Use **Option 1** for quickest setup - shows core functionality with simulated data.