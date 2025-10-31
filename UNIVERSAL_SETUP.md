# 🌐 AETHER Universal Device Health Monitor

## 🎯 **Works on ANY Electronic Device!**

This system automatically detects your device type and adapts all monitoring, thresholds, and vehicle analogies accordingly.

### 📱 **Supported Devices:**
- **💻 Laptops** (Windows, Mac, Linux) → Car Analogy
- **🖥️ Desktops** (All platforms) → Truck Analogy  
- **📱 Tablets** (Windows, Android) → Motorcycle Analogy
- **🤖 Raspberry Pi** → Drone Analogy
- **📱 Android Devices** → Electric Scooter Analogy
- **🐧 Linux Embedded** → Custom IoT Vehicle
- **⚙️ IoT Devices** → Specialized analogies

### 🔄 **Adaptive Features:**

#### **Device-Specific Thresholds:**
- **Laptop**: Temp warning at 70°C, critical at 85°C
- **Desktop**: Temp warning at 65°C, critical at 80°C  
- **Tablet**: Temp warning at 50°C, critical at 65°C
- **Raspberry Pi**: Temp warning at 60°C, critical at 75°C
- **Android**: Temp warning at 45°C, critical at 60°C

#### **Custom Vehicle Analogies:**
- **Laptop** = Car (hybrid engine, fan cooling)
- **Desktop** = Truck (high performance, advanced cooling)
- **Tablet** = Motorcycle (efficient motor, passive cooling)
- **Raspberry Pi** = Drone (micro propulsion, heat sink)
- **Android** = Electric Scooter (battery optimized)

## 🚀 **Setup (2 Steps):**

### **Step 1: Universal Backend (Terminal 1)**
```bash
cd "C:\Users\Ashutosh Mishra\OneDrive\Desktop\EY hackethon\AETHER"
pip install psutil
python run_universal.py
```

### **Step 2: Universal Frontend (Terminal 2)**
```bash
cd frontend
copy src\UniversalDeviceDashboard.js src\App.js
npm start
```

## 🎮 **Smart Features:**

### **Auto-Detection:**
- ✅ **Device Type** - Automatically identifies laptop, desktop, tablet, etc.
- ✅ **Operating System** - Windows, macOS, Linux, Android
- ✅ **Hardware Category** - Computer, mobile, IoT device
- ✅ **Vehicle Analogy** - Assigns appropriate vehicle metaphor

### **Adaptive Monitoring:**
- ✅ **Temperature Monitoring** - Device-specific thermal sensors
- ✅ **Battery Tracking** - Only for devices with batteries
- ✅ **Performance Thresholds** - Optimized per device type
- ✅ **Health Recommendations** - Tailored to device capabilities

### **Device-Specific Tests:**
- **💻 Laptop**: Heavy workload simulation
- **🖥️ Desktop**: Maximum performance mode
- **📱 Tablet**: Intensive app usage simulation  
- **🤖 Raspberry Pi**: Sensor data processing test
- **📱 Android**: Gaming mode simulation

## 🌐 **Access Points:**
- **Dashboard**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Device Info**: http://localhost:8000/api/device-info
- **Health Analysis**: http://localhost:8000/api/health-analysis

## 🧪 **Test on Different Devices:**

### **On Your Laptop:**
- Shows as "Car" with engine temperature (CPU temp)
- Battery monitoring if available
- Fan cooling system simulation

### **On Raspberry Pi:**
- Shows as "Drone" with micro propulsion
- Real CPU temperature from thermal sensor
- IoT-optimized thresholds

### **On Android (with Termux):**
- Shows as "Electric Scooter"
- Mobile-optimized performance monitoring
- Battery-focused health analysis

### **On Desktop:**
- Shows as "Truck" with high-performance engine
- No battery monitoring (AC powered)
- Advanced cooling system simulation

## 💡 **Why This is Revolutionary:**
- **Universal Compatibility** - One system works on everything
- **Intelligent Adaptation** - Automatically adjusts to device capabilities
- **Device-Appropriate Analogies** - Makes sense for each device type
- **Real Hardware Integration** - Uses actual sensors when available
- **Cross-Platform** - Python + React works everywhere

**Install once, monitor any device! Your laptop becomes a car, your Raspberry Pi becomes a drone, your tablet becomes a motorcycle!** 🚗🚁🏍️📱