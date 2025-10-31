import psutil
import platform
import json
import subprocess
import time
from datetime import datetime
import socket
import uuid

class UniversalDeviceAnalyzer:
    def __init__(self):
        self.device_info = self.detect_device_type()
        self.device_config = self.get_device_config()
        
    def detect_device_type(self):
        """Detect what type of device this is running on"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        processor = platform.processor().lower()
        
        device_info = {
            "system": system,
            "machine": machine,
            "processor": processor,
            "hostname": socket.gethostname(),
            "device_id": str(uuid.uuid4())[:8]
        }
        
        # Detect device type based on system characteristics
        if system == "windows":
            if "arm" in machine or "qualcomm" in processor:
                device_info["type"] = "tablet"
                device_info["category"] = "mobile_device"
            else:
                device_info["type"] = "laptop" if psutil.sensors_battery() else "desktop"
                device_info["category"] = "computer"
                
        elif system == "darwin":  # macOS
            if "ipad" in machine or "arm64" in machine:
                device_info["type"] = "tablet"
                device_info["category"] = "mobile_device"
            else:
                device_info["type"] = "macbook" if psutil.sensors_battery() else "imac"
                device_info["category"] = "computer"
                
        elif system == "linux":
            # Check if it's a Raspberry Pi or IoT device
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                if 'raspberry' in cpuinfo or 'bcm' in cpuinfo:
                    device_info["type"] = "raspberry_pi"
                    device_info["category"] = "iot_device"
                elif 'arm' in machine:
                    device_info["type"] = "embedded_device"
                    device_info["category"] = "iot_device"
                else:
                    device_info["type"] = "linux_computer"
                    device_info["category"] = "computer"
            except:
                device_info["type"] = "linux_device"
                device_info["category"] = "computer"
                
        elif system == "android":
            device_info["type"] = "android_device"
            device_info["category"] = "mobile_device"
            
        else:
            device_info["type"] = "unknown_device"
            device_info["category"] = "generic"
            
        return device_info
    
    def get_device_config(self):
        """Get device-specific configuration and thresholds"""
        device_type = self.device_info["type"]
        
        configs = {
            "laptop": {
                "temp_normal": 45, "temp_warning": 70, "temp_critical": 85,
                "cpu_normal": 30, "cpu_warning": 70, "cpu_critical": 90,
                "memory_normal": 50, "memory_warning": 75, "memory_critical": 90,
                "battery_low": 20, "battery_critical": 10,
                "health_metrics": ["cpu_temp", "battery", "memory", "disk", "cpu_usage"],
                "vehicle_analogy": "Car"
            },
            "desktop": {
                "temp_normal": 40, "temp_warning": 65, "temp_critical": 80,
                "cpu_normal": 25, "cpu_warning": 60, "cpu_critical": 85,
                "memory_normal": 40, "memory_warning": 70, "memory_critical": 85,
                "battery_low": None, "battery_critical": None,
                "health_metrics": ["cpu_temp", "memory", "disk", "cpu_usage"],
                "vehicle_analogy": "Truck"
            },
            "tablet": {
                "temp_normal": 35, "temp_warning": 50, "temp_critical": 65,
                "cpu_normal": 20, "cpu_warning": 60, "cpu_critical": 80,
                "memory_normal": 60, "memory_warning": 80, "memory_critical": 95,
                "battery_low": 15, "battery_critical": 5,
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage"],
                "vehicle_analogy": "Motorcycle"
            },
            "raspberry_pi": {
                "temp_normal": 45, "temp_warning": 60, "temp_critical": 75,
                "cpu_normal": 40, "cpu_warning": 70, "cpu_critical": 90,
                "memory_normal": 60, "memory_warning": 80, "memory_critical": 95,
                "battery_low": None, "battery_critical": None,
                "health_metrics": ["cpu_temp", "memory", "cpu_usage", "disk"],
                "vehicle_analogy": "Drone"
            },
            "android_device": {
                "temp_normal": 30, "temp_warning": 45, "temp_critical": 60,
                "cpu_normal": 25, "cpu_warning": 65, "cpu_critical": 85,
                "memory_normal": 70, "memory_warning": 85, "memory_critical": 95,
                "battery_low": 20, "battery_critical": 10,
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage"],
                "vehicle_analogy": "Electric Scooter"
            }
        }
        
        return configs.get(device_type, configs["laptop"])
    
    def get_device_health_data(self):
        """Get comprehensive device health data adapted to device type"""
        try:
            # Basic system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Temperature (device-specific methods)
            temperature = self.get_device_temperature()
            
            # Battery (if available)
            battery_info = self.get_battery_info()
            
            # Network stats
            network = psutil.net_io_counters()
            
            # Device-specific health analysis
            health_analysis = self.analyze_device_health(
                cpu_percent, memory.percent, temperature, battery_info
            )
            
            # Convert to vehicle analogy based on device type
            vehicle_data = self.convert_to_vehicle_analogy(
                cpu_percent, memory.percent, temperature, battery_info, health_analysis
            )
            
            return {
                "device_info": self.device_info,
                "raw_metrics": {
                    "cpu_usage": cpu_percent,
                    "memory_usage": memory.percent,
                    "disk_usage": disk.percent,
                    "temperature": temperature,
                    "battery": battery_info,
                    "network_sent": network.bytes_sent,
                    "network_recv": network.bytes_recv
                },
                "health_analysis": health_analysis,
                "vehicle_analogy": vehicle_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e), "timestamp": datetime.now().isoformat()}
    
    def get_device_temperature(self):
        """Get temperature using device-specific methods"""
        device_type = self.device_info["type"]
        
        try:
            if device_type == "raspberry_pi":
                # Raspberry Pi specific temperature
                with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                    temp = float(f.read()) / 1000.0
                return temp
                
            elif self.device_info["system"] == "darwin":  # macOS
                try:
                    result = subprocess.run(['sudo', 'powermetrics', '--samplers', 'smc', '-n', '1'], 
                                          capture_output=True, text=True, timeout=5)
                    # Parse temperature from output
                    return 45 + (psutil.cpu_percent() * 0.4)  # Fallback estimation
                except:
                    return 40 + (psutil.cpu_percent() * 0.5)
                    
            elif self.device_info["system"] == "linux":
                # Linux thermal zones
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp = float(f.read()) / 1000.0
                    return temp
                except:
                    return 35 + (psutil.cpu_percent() * 0.6)
                    
            else:  # Windows and others
                # Estimate based on CPU usage
                base_temp = self.device_config["temp_normal"]
                return base_temp + (psutil.cpu_percent() * 0.5)
                
        except:
            # Fallback estimation
            return self.device_config["temp_normal"] + (psutil.cpu_percent() * 0.4)
    
    def get_battery_info(self):
        """Get battery information if available"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    "percent": battery.percent,
                    "plugged": battery.power_plugged,
                    "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
                }
            else:
                return {"percent": None, "plugged": True, "time_left": None}
        except:
            return {"percent": None, "plugged": None, "time_left": None}
    
    def analyze_device_health(self, cpu_usage, memory_usage, temperature, battery_info):
        """Analyze device health based on device-specific thresholds"""
        config = self.device_config
        analysis = {
            "overall_score": 100,
            "status": "EXCELLENT",
            "issues": [],
            "recommendations": [],
            "critical_alerts": []
        }
        
        # Temperature analysis
        if temperature > config["temp_critical"]:
            analysis["overall_score"] -= 30
            analysis["issues"].append(f"Critical temperature: {temperature:.1f}°C")
            analysis["critical_alerts"].append("OVERHEATING - Immediate action required")
            analysis["recommendations"].append("Shut down device immediately to prevent damage")
        elif temperature > config["temp_warning"]:
            analysis["overall_score"] -= 15
            analysis["issues"].append(f"High temperature: {temperature:.1f}°C")
            analysis["recommendations"].append("Reduce workload and improve ventilation")
        
        # CPU usage analysis
        if cpu_usage > config["cpu_critical"]:
            analysis["overall_score"] -= 25
            analysis["issues"].append(f"Critical CPU load: {cpu_usage:.1f}%")
            analysis["recommendations"].append("Close unnecessary applications immediately")
        elif cpu_usage > config["cpu_warning"]:
            analysis["overall_score"] -= 10
            analysis["issues"].append(f"High CPU usage: {cpu_usage:.1f}%")
            analysis["recommendations"].append("Monitor running processes")
        
        # Memory analysis
        if memory_usage > config["memory_critical"]:
            analysis["overall_score"] -= 20
            analysis["issues"].append(f"Critical memory usage: {memory_usage:.1f}%")
            analysis["critical_alerts"].append("MEMORY EXHAUSTED - System may crash")
            analysis["recommendations"].append("Restart device or close applications")
        elif memory_usage > config["memory_warning"]:
            analysis["overall_score"] -= 10
            analysis["issues"].append(f"High memory usage: {memory_usage:.1f}%")
            analysis["recommendations"].append("Close unused applications")
        
        # Battery analysis (if applicable)
        if battery_info["percent"] is not None:
            if battery_info["percent"] < config["battery_critical"]:
                analysis["overall_score"] -= 15
                analysis["critical_alerts"].append("BATTERY CRITICAL - Connect charger immediately")
            elif battery_info["percent"] < config["battery_low"]:
                analysis["issues"].append(f"Low battery: {battery_info['percent']:.1f}%")
                analysis["recommendations"].append("Connect to power source")
        
        # Determine overall status
        if analysis["overall_score"] >= 90:
            analysis["status"] = "EXCELLENT"
        elif analysis["overall_score"] >= 75:
            analysis["status"] = "GOOD"
        elif analysis["overall_score"] >= 50:
            analysis["status"] = "WARNING"
        else:
            analysis["status"] = "CRITICAL"
        
        return analysis
    
    def convert_to_vehicle_analogy(self, cpu_usage, memory_usage, temperature, battery_info, health_analysis):
        """Convert device metrics to vehicle analogy based on device type"""
        vehicle_type = self.device_config["vehicle_analogy"]
        
        # Base vehicle data structure
        vehicle_data = {
            "vehicle_type": vehicle_type,
            "vehicle_id": f"{vehicle_type}_{self.device_info['hostname']}",
            "engine_temp": temperature,
            "speed": min(cpu_usage * 1.2, 120),
            "fuel_level": battery_info["percent"] if battery_info["percent"] else 100,
            "health_score": health_analysis["overall_score"],
            "status": health_analysis["status"]
        }
        
        # Device-specific vehicle mappings
        if self.device_info["type"] == "laptop":
            vehicle_data.update({
                "engine_type": "Hybrid Engine",
                "max_speed": "120 km/h",
                "fuel_type": "Battery + AC Power",
                "cooling_system": "Fan Cooling",
                "performance_mode": "Balanced" if cpu_usage < 50 else "Performance"
            })
            
        elif self.device_info["type"] == "desktop":
            vehicle_data.update({
                "engine_type": "High Performance Engine",
                "max_speed": "150 km/h",
                "fuel_type": "AC Power",
                "cooling_system": "Advanced Cooling",
                "performance_mode": "Always On"
            })
            
        elif self.device_info["type"] == "tablet":
            vehicle_data.update({
                "engine_type": "Efficient Motor",
                "max_speed": "80 km/h",
                "fuel_type": "Battery",
                "cooling_system": "Passive Cooling",
                "performance_mode": "Eco Mode" if cpu_usage < 30 else "Normal"
            })
            
        elif self.device_info["type"] == "raspberry_pi":
            vehicle_data.update({
                "engine_type": "Micro Propulsion",
                "max_speed": "60 km/h",
                "fuel_type": "USB Power",
                "cooling_system": "Heat Sink",
                "performance_mode": "IoT Mode"
            })
        
        return vehicle_data

# Test the analyzer
if __name__ == "__main__":
    analyzer = UniversalDeviceAnalyzer()
    
    print(f"🔍 Universal Device Analyzer")
    print("=" * 50)
    
    data = analyzer.get_device_health_data()
    
    print(f"Device Type: {data['device_info']['type'].title()}")
    print(f"Vehicle Analogy: {data['vehicle_analogy']['vehicle_type']}")
    print(f"Health Score: {data['health_analysis']['overall_score']:.1f}%")
    print(f"Status: {data['health_analysis']['status']}")
    print(f"Temperature: {data['raw_metrics']['temperature']:.1f}°C")
    
    if data['health_analysis']['critical_alerts']:
        print("\n🚨 CRITICAL ALERTS:")
        for alert in data['health_analysis']['critical_alerts']:
            print(f"  - {alert}")
    
    if data['health_analysis']['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        for rec in data['health_analysis']['recommendations']:
            print(f"  - {rec}")