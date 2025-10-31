# 🚀 AETHER Auto-Start Universal Monitor

## 🎯 **Ultimate Universal System**

This system automatically detects and monitors **ANY target**:
- **🚗 Real Vehicles** (Cars, Trucks, Motorcycles, Buses)
- **📱 Electronic Devices** (Laptops, Tablets, IoT devices)
- **⚡ Auto-Start Backend** (No manual commands needed)

## 🔍 **Auto-Detection Process:**

### **1. Vehicle Detection (Priority 1):**
- **🔌 OBD-II Ports** - COM1, COM2, COM3, /dev/ttyUSB0
- **🌐 CAN Bus Interfaces** - can0, can1 network interfaces
- **📱 Bluetooth OBD** - ELM327, OBDLink adapters
- **📡 WiFi OBD** - 192.168.0.10, 192.168.4.1 common IPs

### **2. Vehicle Types Supported:**
- **🚗 Passenger Cars** - Petrol, Diesel, Hybrid, Electric
- **🚛 Heavy Trucks** - Commercial, Freight, Delivery
- **🏍️ Motorcycles** - Sport bikes, Cruisers, Scooters
- **🚌 Buses** - Public transport, School buses
- **🚜 Specialized** - Agricultural, Construction vehicles

### **3. Device Fallback (If No Vehicle):**
- **💻 Laptops** → Car analogy
- **🖥️ Desktops** → Truck analogy
- **📱 Tablets** → Motorcycle analogy
- **🤖 Raspberry Pi** → Drone analogy
- **📱 Android** → Electric Scooter analogy

## 🚀 **One-Step Setup:**

### **Step 1: Start Auto-Monitor**
```bash
cd "C:\Users\Ashutosh Mishra\OneDrive\Desktop\EY hackethon\AETHER"
pip install psutil pyserial
python run_auto_start.py
```

### **Step 2: Open Frontend**
```bash
cd frontend
copy src\AutoStartDashboard.js src\App.js
npm start
```

**That's it! Backend starts automatically when frontend loads!**

## 🎛️ **Smart Features:**

### **Real Vehicle Monitoring:**
- ✅ **Engine RPM** - Real-time from ECU
- ✅ **Vehicle Speed** - Actual speedometer data
- ✅ **Engine Temperature** - Coolant temperature sensor
- ✅ **Fuel Level** - Tank level percentage
- ✅ **Battery Voltage** - Electrical system health
- ✅ **Oil Pressure** - Engine lubrication status
- ✅ **Throttle Position** - Accelerator input
- ✅ **Engine Load** - Performance metrics

### **Device Monitoring:**
- ✅ **CPU Temperature** → Engine Temperature
- ✅ **CPU Usage** → Vehicle Speed
- ✅ **Memory Usage** → System Health
- ✅ **Battery Level** → Fuel Level
- ✅ **Disk Usage** → Tire Pressure
- ✅ **Network Activity** → Road Conditions

### **Automotive-Grade Alerts:**
- 🚨 **Engine Overheating** - >120°C critical
- 🚨 **Low Oil Pressure** - <10 PSI danger
- 🚨 **Battery Critical** - <11.5V system failure
- 🚨 **Over-Revving** - >6500 RPM engine damage
- ⚠️ **High Temperature** - >105°C warning
- ⚠️ **Low Fuel** - <10% tank level

## 🌐 **Access Points:**
- **Dashboard**: http://localhost:3000
- **Backend**: http://localhost:8003
- **Monitoring Mode**: http://localhost:8003/api/monitoring-mode
- **Health Data**: http://localhost:8003/api/health-data

## 🧪 **Test Scenarios:**

### **With Real Vehicle:**
1. Connect OBD-II adapter to vehicle
2. Start system - automatically detects vehicle
3. Shows real engine RPM, speed, temperature
4. Automotive-grade alerts and thresholds

### **With Laptop/Device:**
1. No vehicle detected - switches to device mode
2. CPU becomes "engine", memory becomes "fuel"
3. Device-appropriate thresholds and analogies
4. Real system health monitoring

### **Auto-Start Demo:**
1. Just run `python run_auto_start.py`
2. Open frontend - backend connects automatically
3. No manual backend startup needed
4. System detects target and adapts interface

## 💡 **Revolutionary Features:**
- **🔄 Universal Compatibility** - Works with anything
- **🎯 Auto-Detection** - No configuration needed
- **⚡ Auto-Start** - Backend launches automatically
- **🚗 Real Vehicle Support** - Actual OBD-II integration
- **📱 Device Adaptation** - Smart analogies per device
- **🚨 Context-Aware Alerts** - Appropriate warnings per target

**One system monitors everything - from your laptop to your car to your truck!** 🚗💻🚛📱