# 🚀 AETHER: Universal Auto-Start Vehicle & Device Health Monitor

## 🎯 Project Overview
AETHER is a **revolutionary universal monitoring system** that automatically detects and monitors **ANY target** - from real vehicles (cars, trucks, motorcycles) via OBD-II to electronic devices (laptops, tablets, IoT devices) with **auto-start backend** and **adaptive intelligence**.

## 🌟 Key Innovations
- **🔍 Universal Auto-Detection** - Automatically identifies vehicles or devices
- **⚡ Auto-Start Backend** - No manual commands needed
- **🚗 Real Vehicle Support** - OBD-II, CAN bus, Bluetooth integration
- **📱 Device Adaptation** - Smart analogies for any electronic device
- **🎛️ Adaptive Thresholds** - Different limits per target type
- **🚨 Context-Aware Alerts** - Automotive-grade or device-appropriate warnings

## 🏗️ Architecture
```
AETHER/
├── frontend/                    # React.js universal dashboard
│   ├── AutoStartDashboard.js   # Auto-detecting interface
│   ├── UniversalDeviceDashboard.js # Device monitoring
│   └── RealSystemDashboard.js  # System simulation
├── backend/                     # FastAPI auto-start server
│   ├── auto_start_backend.py   # Main auto-start backend
│   ├── vehicle_obd_analyzer.py # Real vehicle OBD-II integration
│   ├── universal_device_analyzer.py # Device health monitoring
│   └── laptop_vehicle_simulator.py # System-as-vehicle simulation
├── ai-models/                   # ML models for prediction
├── iot-layer/                   # Hardware integration
├── drone-system/               # Drone control and coordination
├── satellite-integration/      # NavIC/GPS communication
├── security/                   # Blockchain security
└── docs/                       # Documentation and guides
```

## 🚀 Quick Start (One Command!)

### **Auto-Start Universal Monitor:**
```bash
cd AETHER
pip install psutil pyserial
python run_auto_start.py
```

### **Frontend (New Terminal):**
```bash
cd frontend
copy src\AutoStartDashboard.js src\App.js
npm install
npm start
```

**Access:** http://localhost:3000

## 🎯 Monitoring Targets

### **🚗 Real Vehicles (Auto-Detected):**
- **Cars** - Petrol, Diesel, Hybrid, Electric
- **Trucks** - Commercial, Freight, Heavy-duty
- **Motorcycles** - Sport bikes, Cruisers, Scooters
- **Buses** - Public transport, School buses
- **Specialized** - Agricultural, Construction vehicles

**Connection Methods:**
- 🔌 **OBD-II Ports** (COM1-4, /dev/ttyUSB0-1)
- 🌐 **CAN Bus** (can0, can1 interfaces)
- 📱 **Bluetooth OBD** (ELM327 adapters)
- 📡 **WiFi OBD** (192.168.x.x adapters)

### **📱 Electronic Devices (Fallback):**
- **💻 Laptops** → Car analogy (hybrid engine)
- **🖥️ Desktops** → Truck analogy (high performance)
- **📱 Tablets** → Motorcycle analogy (efficient)
- **🤖 Raspberry Pi** → Drone analogy (micro propulsion)
- **📱 Android** → Electric Scooter analogy

## 🎛️ Core Features

### **Real Vehicle Monitoring:**
- ✅ **Engine RPM** - Real-time from ECU
- ✅ **Vehicle Speed** - Actual speedometer data
- ✅ **Engine Temperature** - Coolant sensor readings
- ✅ **Fuel Level** - Tank percentage
- ✅ **Battery Voltage** - Electrical system health
- ✅ **Oil Pressure** - Engine lubrication status
- ✅ **Throttle Position** - Accelerator input
- ✅ **Transmission Temperature** - Gearbox health

### **Device Health Monitoring:**
- ✅ **CPU Temperature** → Engine Temperature
- ✅ **CPU Usage** → Vehicle Speed
- ✅ **Memory Usage** → System Health
- ✅ **Battery Level** → Fuel Level
- ✅ **Disk Usage** → Tire Pressure
- ✅ **Network Activity** → Road Conditions

### **Smart Alert System:**
- 🚨 **Critical Alerts** - Engine overheating, low oil pressure
- ⚠️ **Warning Alerts** - High temperature, low fuel
- 💡 **Recommendations** - Maintenance suggestions
- 🔧 **Adaptive Thresholds** - Different per target type

## 🛠️ Tech Stack
- **Frontend**: React.js, Real-time WebSocket
- **Backend**: FastAPI, Auto-start architecture
- **Vehicle Integration**: OBD-II, CAN bus, Serial communication
- **Device Monitoring**: psutil, System sensors
- **AI/ML**: TensorFlow, PyTorch, Predictive models
- **Security**: Blockchain, JWT, Encryption
- **Database**: PostgreSQL, MongoDB
- **Cloud**: AWS IoT Core, Lambda, S3

## 🎮 Usage Examples

### **With Real Car:**
1. Connect OBD-II adapter to vehicle
2. Run `python run_auto_start.py`
3. System detects vehicle automatically
4. Shows real engine RPM, speed, temperature
5. Automotive-grade alerts and recommendations

### **With Laptop:**
1. Run `python run_auto_start.py`
2. No vehicle detected - switches to device mode
3. CPU becomes "engine", memory becomes "fuel"
4. Device-appropriate thresholds and analogies

### **Auto-Start Demo:**
1. Backend starts automatically when frontend loads
2. No manual backend startup commands needed
3. System adapts interface based on detected target

## 🌐 Alternative Setups

### **Real System Vehicle Simulator:**
```bash
python run_real_system.py  # Port 8001
```
Uses your laptop's real system data as vehicle metrics.

### **Universal Device Monitor:**
```bash
python run_universal.py   # Port 8002
```
Adapts to any electronic device with custom analogies.

### **Simple Demo:**
```bash
python run_demo.py        # Port 8000
```
Basic vehicle simulation with WebSocket updates.

## 📊 API Endpoints
- **Health Data**: `/api/health-data`
- **Monitoring Mode**: `/api/monitoring-mode`
- **Device Info**: `/api/device-info`
- **Vehicle Data**: `/api/real-vehicle`
- **System Analysis**: `/api/system-analysis`
- **WebSocket**: `ws://localhost:8003/ws`

## 🔧 Configuration

### **Vehicle Thresholds:**
- **Cars**: Temp critical >120°C, RPM critical >6500
- **Trucks**: Temp critical >115°C, RPM critical >3000
- **Motorcycles**: Temp critical >110°C, RPM critical >10000

### **Device Thresholds:**
- **Laptops**: Temp critical >85°C, CPU critical >90%
- **Desktops**: Temp critical >80°C, CPU critical >85%
- **Tablets**: Temp critical >65°C, CPU critical >80%

## 🚨 Troubleshooting

### **Vehicle Not Detected:**
- Check OBD-II adapter connection
- Verify COM port availability
- Try different USB ports
- System falls back to device mode

### **Backend Won't Start:**
- Check port availability (8003)
- Install dependencies: `pip install psutil pyserial`
- Run with admin privileges if needed

### **Frontend Connection Issues:**
- Ensure backend is running first
- Check WebSocket connection
- Try refreshing browser

## 🎯 Future Enhancements
- **Fleet Management** - Multi-vehicle monitoring
- **Mobile App** - Android/iOS companion
- **Cloud Integration** - AWS IoT deployment
- **AI Predictions** - Advanced ML models
- **Drone Integration** - Aerial monitoring
- **Blockchain Security** - Data integrity

## 📞 Support
- **Documentation**: `/docs/` folder
- **API Reference**: `http://localhost:8003/docs`
- **Setup Guides**: `AUTO_START_SETUP.md`
- **Project Presentation**: `docs/PROJECT_PRESENTATION.md`

---

**🚀 AETHER: One system monitors everything - from your car's engine to your laptop's CPU!**