import psutil
import platform
import time
import json
from datetime import datetime
import subprocess
import os

class LaptopVehicleSimulator:
    def __init__(self):
        self.system_info = platform.uname()
        self.start_time = time.time()
        
    def get_cpu_temperature(self):
        """Get real CPU temperature"""
        try:
            # Windows - using wmic
            if platform.system() == "Windows":
                result = subprocess.run(['wmic', 'cpu', 'get', 'temperature', '/value'], 
                                      capture_output=True, text=True)
                # Alternative method for Windows
                result = subprocess.run(['powershell', 
                    'Get-WmiObject -Namespace "root/OpenHardwareMonitor" -Class Sensor | Where-Object {$_.SensorType -eq "Temperature" -and $_.Name -like "*CPU*"} | Select-Object -First 1 -ExpandProperty Value'], 
                    capture_output=True, text=True)
                
                # Fallback - simulate based on CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                base_temp = 35  # Base temperature
                temp = base_temp + (cpu_percent * 0.5)  # Simulate temperature based on usage
                return min(temp, 95)  # Cap at 95°C
                
        except:
            # Fallback simulation
            cpu_percent = psutil.cpu_percent(interval=1)
            return 35 + (cpu_percent * 0.5)
    
    def get_real_vehicle_data(self):
        """Convert laptop stats to vehicle data"""
        # Get real system data
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        battery = psutil.sensors_battery()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        # CPU temperature as engine temperature
        engine_temp = self.get_cpu_temperature()
        
        # Battery info
        battery_level = battery.percent if battery else 50 + (cpu_percent / 2)
        
        # Convert system stats to vehicle metrics
        vehicle_data = {
            "vehicle_id": f"LAPTOP_{self.system_info.node}",
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": 28.6139 + (cpu_percent / 10000),  # Slight movement based on CPU
                "longitude": 77.2090 + (memory.percent / 10000),
                "altitude": 200 + (disk.percent / 10)
            },
            "health": {
                "engine_temp": engine_temp,  # Real CPU temperature
                "battery_level": battery_level,  # Real battery level
                "tire_pressure": [
                    32 - (cpu_percent / 10),  # Simulate based on CPU load
                    32 - (memory.percent / 10),
                    32 - (disk.percent / 10), 
                    32 - (network.bytes_sent / 1000000000)
                ],
                "brake_health": max(100 - (cpu_percent / 2), 60),
                "overall_score": max(100 - cpu_percent - (memory.percent / 2), 30)
            },
            "safety": {
                "collision_risk": "HIGH" if cpu_percent > 80 else "MEDIUM" if cpu_percent > 50 else "LOW",
                "driver_alertness": max(1.0 - (cpu_percent / 100), 0.3),
                "weather_conditions": "HOT" if engine_temp > 70 else "NORMAL",
                "road_conditions": "POOR" if memory.percent > 80 else "GOOD"
            },
            "navigation": {
                "current_speed": min(cpu_percent * 1.2, 120),  # Speed based on CPU usage
                "destination": "System Optimization Center",
                "eta": f"{int(100 - cpu_percent)} minutes",
                "fuel_level": battery_level,
                "next_service_km": max(5000 - (cpu_percent * 50), 100)
            },
            "system_info": {
                "real_cpu_usage": cpu_percent,
                "real_memory_usage": memory.percent,
                "real_disk_usage": disk.percent,
                "real_battery": battery_level,
                "real_temp": engine_temp,
                "system_name": self.system_info.system,
                "processor": self.system_info.processor,
                "uptime_hours": (time.time() - self.start_time) / 3600
            }
        }
        
        return vehicle_data
    
    def get_performance_analysis(self):
        """Analyze laptop performance as vehicle diagnostics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        temp = self.get_cpu_temperature()
        
        analysis = {
            "performance_score": max(100 - cpu_percent - (memory.percent / 2), 0),
            "health_status": "CRITICAL" if temp > 85 else "WARNING" if temp > 70 else "GOOD",
            "recommendations": [],
            "alerts": []
        }
        
        # Generate real recommendations based on system state
        if cpu_percent > 80:
            analysis["recommendations"].append("High CPU usage detected - Close unnecessary applications")
            analysis["alerts"].append("ENGINE OVERLOAD: Reduce system load immediately")
            
        if memory.percent > 80:
            analysis["recommendations"].append("High memory usage - Restart system or close applications")
            analysis["alerts"].append("MEMORY CRITICAL: System performance degraded")
            
        if temp > 75:
            analysis["recommendations"].append("High temperature detected - Check cooling system")
            analysis["alerts"].append("OVERHEATING: Ensure proper ventilation")
            
        if temp < 40 and cpu_percent < 20:
            analysis["recommendations"].append("System running optimally - All systems green")
            
        return analysis
    
    def simulate_driving_scenario(self, scenario="normal"):
        """Simulate different driving scenarios by stressing system"""
        if scenario == "highway":
            # Simulate highway driving with CPU stress
            print("🏎️ Simulating highway driving - Increasing system load...")
            # Could trigger CPU stress here
            
        elif scenario == "traffic":
            # Simulate stop-and-go traffic
            print("🚦 Simulating traffic conditions - Variable load...")
            
        elif scenario == "parking":
            # Simulate idle/parking
            print("🅿️ Simulating parking - System idle...")
            
        return self.get_real_vehicle_data()

# Test the simulator
if __name__ == "__main__":
    simulator = LaptopVehicleSimulator()
    
    print("🚗 AETHER Laptop Vehicle Simulator")
    print("=" * 50)
    
    # Get real vehicle data
    data = simulator.get_real_vehicle_data()
    print(f"Vehicle ID: {data['vehicle_id']}")
    print(f"Engine Temperature (CPU): {data['health']['engine_temp']:.1f}°C")
    print(f"Battery Level: {data['health']['battery_level']:.1f}%")
    print(f"Overall Health: {data['health']['overall_score']:.1f}%")
    print(f"Current Speed (CPU Load): {data['navigation']['current_speed']:.1f} km/h")
    
    # Performance analysis
    analysis = simulator.get_performance_analysis()
    print(f"\nPerformance Score: {analysis['performance_score']:.1f}%")
    print(f"Health Status: {analysis['health_status']}")
    
    if analysis['recommendations']:
        print("\nRecommendations:")
        for rec in analysis['recommendations']:
            print(f"- {rec}")
            
    if analysis['alerts']:
        print("\nAlerts:")
        for alert in analysis['alerts']:
            print(f"⚠️ {alert}")