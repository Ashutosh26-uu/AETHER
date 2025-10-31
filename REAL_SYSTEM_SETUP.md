# 🚗 AETHER Real System Vehicle Simulator

## 🎯 **Your Laptop = Your Vehicle**

This version uses your **actual laptop system data** as vehicle metrics:

### 🔄 **Real System Mapping:**
- **🌡️ CPU Temperature** → Engine Temperature
- **🔋 Battery Level** → Vehicle Battery
- **⚡ CPU Usage** → Vehicle Speed  
- **💾 Memory Usage** → System Health
- **💽 Disk Usage** → Tire Pressure
- **🌐 Network Activity** → Road Conditions

## 🚀 **Setup (2 Steps):**

### **Step 1: Backend (Terminal 1)**
```bash
cd "C:\Users\Ashutosh Mishra\OneDrive\Desktop\EY hackethon\AETHER"
pip install psutil
python run_real_system.py
```

### **Step 2: Frontend (Terminal 2)**
```bash
cd frontend
copy src\RealSystemDashboard.js src\App.js
npm start
```

## 🎮 **Interactive Features:**

### **Real-time Monitoring:**
- ✅ **Live CPU temperature** as engine heat
- ✅ **Real battery percentage** as vehicle power
- ✅ **Actual CPU load** as vehicle speed
- ✅ **Memory usage** as system health
- ✅ **System uptime** as trip duration

### **Simulation Controls:**
- 🏎️ **Highway Driving** - Triggers CPU stress test
- 📊 **System Analysis** - Detailed performance report
- 🚨 **Real Alerts** - Based on actual system conditions

### **Smart Alerts:**
- 🔥 **Overheating Warning** - When CPU > 70°C
- ⚡ **High Load Alert** - When CPU > 70%
- 💾 **Memory Critical** - When RAM > 80%
- ✅ **Optimal Status** - When all systems normal

## 🌐 **Access Points:**
- **Dashboard**: http://localhost:3000
- **Backend**: http://localhost:8000
- **System Analysis**: http://localhost:8000/api/system-analysis
- **Real Vehicle Data**: http://localhost:8000/api/real-vehicle

## 🧪 **Test Scenarios:**

### **Simulate Highway Driving:**
1. Click "🏎️ Simulate Highway Driving" button
2. Watch CPU temperature rise (engine heat)
3. See speed increase with CPU load
4. Get real overheating alerts

### **Monitor Real Performance:**
- Open multiple applications → See "speed" increase
- Run heavy software → Watch "engine temperature" rise
- Low battery → Vehicle power decreases
- High memory usage → Health score drops

## 💡 **Why This is Innovative:**
- **Real Data Integration** - Not just simulation
- **Cross-platform Monitoring** - Works on any laptop
- **Practical Application** - Actual system health insights
- **Interactive Testing** - Stress tests show real effects
- **Educational Value** - Learn system monitoring through vehicle metaphors

**Your laptop is now a fully functional AETHER vehicle with real-time monitoring!** 🚗✨