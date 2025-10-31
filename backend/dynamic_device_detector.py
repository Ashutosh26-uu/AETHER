import psutil
import platform
import json
import subprocess
import time
import socket
import uuid
import re
import os
from datetime import datetime

class DynamicDeviceDetector:
    def __init__(self):
        self.device_info = self.comprehensive_device_detection()
        self.manufacturer_info = self.detect_manufacturer()
        self.device_config = self.get_dynamic_config()
        
    def comprehensive_device_detection(self):
        """Advanced device detection with manufacturer and specific device type identification"""
        system = platform.system().lower()
        machine = platform.machine().lower()
        processor = platform.processor().lower()
        
        device_info = {
            "system": system,
            "machine": machine,
            "processor": processor,
            "hostname": socket.gethostname(),
            "device_id": str(uuid.uuid4())[:8],
            "platform_details": platform.platform(),
            "python_version": platform.python_version(),
            "architecture": platform.architecture()[0]
        }
        
        # Enhanced device type detection
        device_type, category, subcategory = self.detect_device_type_advanced(system, machine, processor)
        
        device_info.update({
            "type": device_type,
            "category": category,
            "subcategory": subcategory,
            "form_factor": self.determine_form_factor(device_type),
            "mobility": self.determine_mobility(device_type),
            "power_source": self.determine_power_source(device_type)
        })
        
        return device_info
    
    def detect_device_type_advanced(self, system, machine, processor):
        """Advanced device type detection with specific categorization"""
        
        # Mobile Devices
        if system == "android":
            return "android_phone", "mobile_device", "smartphone"
        
        if system == "ios":
            return "iphone", "mobile_device", "smartphone"
            
        # Windows Devices
        if system == "windows":
            if "arm" in machine or "qualcomm" in processor:
                if self.is_tablet_mode():
                    return "windows_tablet", "mobile_device", "tablet"
                return "windows_arm_laptop", "computer", "ultrabook"
            
            # Check for specific Windows device types
            if self.is_surface_device():
                return "surface_tablet", "mobile_device", "2in1_tablet"
            
            if psutil.sensors_battery():
                if self.is_gaming_laptop():
                    return "gaming_laptop", "computer", "high_performance"
                return "windows_laptop", "computer", "laptop"
            else:
                if self.is_workstation():
                    return "workstation", "computer", "high_performance"
                return "desktop_pc", "computer", "desktop"
        
        # macOS Devices
        elif system == "darwin":
            if "ipad" in machine:
                return "ipad", "mobile_device", "tablet"
            elif "arm64" in machine or "m1" in processor.lower() or "m2" in processor.lower():
                if psutil.sensors_battery():
                    return "macbook_apple_silicon", "computer", "laptop"
                return "mac_studio", "computer", "desktop"
            else:
                if psutil.sensors_battery():
                    return "macbook_intel", "computer", "laptop"
                return "imac", "computer", "desktop"
        
        # Linux Devices
        elif system == "linux":
            # IoT and Embedded Devices
            if self.is_raspberry_pi():
                return "raspberry_pi", "iot_device", "single_board_computer"
            
            if self.is_nvidia_jetson():
                return "nvidia_jetson", "iot_device", "ai_computer"
            
            if self.is_arduino_compatible():
                return "arduino_compatible", "iot_device", "microcontroller"
            
            # Vehicle Systems
            if self.is_automotive_system():
                return "automotive_ecu", "vehicle_system", "car_computer"
            
            if self.is_truck_system():
                return "truck_telematics", "vehicle_system", "truck_computer"
            
            # Regular Linux systems
            if "arm" in machine:
                return "arm_linux", "iot_device", "embedded_system"
            else:
                if psutil.sensors_battery():
                    return "linux_laptop", "computer", "laptop"
                return "linux_desktop", "computer", "desktop"
        
        # Default fallback
        return "unknown_device", "generic", "unclassified"
    
    def detect_manufacturer(self):
        """Detect device manufacturer using multiple methods"""
        manufacturer_info = {
            "brand": "Unknown",
            "model": "Unknown",
            "oem": "Unknown",
            "detection_method": "none"
        }
        
        try:
            # Windows WMI detection
            if platform.system().lower() == "windows":
                manufacturer_info.update(self.get_windows_manufacturer())
            
            # Linux DMI detection
            elif platform.system().lower() == "linux":
                manufacturer_info.update(self.get_linux_manufacturer())
            
            # macOS system profiler
            elif platform.system().lower() == "darwin":
                manufacturer_info.update(self.get_macos_manufacturer())
            
        except Exception as e:
            manufacturer_info["error"] = str(e)
        
        return manufacturer_info
    
    def get_windows_manufacturer(self):
        """Get Windows manufacturer info using WMI"""
        try:
            import wmi
            c = wmi.WMI()
            
            # Get computer system info
            for computer in c.Win32_ComputerSystem():
                return {
                    "brand": computer.Manufacturer or "Unknown",
                    "model": computer.Model or "Unknown",
                    "oem": computer.Manufacturer or "Unknown",
                    "detection_method": "wmi"
                }
        except ImportError:
            # Fallback to systeminfo command
            try:
                result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
                output = result.stdout
                
                brand = "Unknown"
                model = "Unknown"
                
                for line in output.split('\n'):
                    if 'System Manufacturer:' in line:
                        brand = line.split(':', 1)[1].strip()
                    elif 'System Model:' in line:
                        model = line.split(':', 1)[1].strip()
                
                return {
                    "brand": brand,
                    "model": model,
                    "oem": brand,
                    "detection_method": "systeminfo"
                }
            except:
                pass
        
        return {"brand": "Windows PC", "model": "Unknown", "oem": "Unknown", "detection_method": "fallback"}
    
    def get_linux_manufacturer(self):
        """Get Linux manufacturer info from DMI"""
        try:
            dmi_paths = [
                "/sys/class/dmi/id/sys_vendor",
                "/sys/class/dmi/id/product_name",
                "/sys/class/dmi/id/board_vendor",
                "/sys/class/dmi/id/board_name"
            ]
            
            brand = "Unknown"
            model = "Unknown"
            
            # Try to read DMI information
            try:
                with open("/sys/class/dmi/id/sys_vendor", "r") as f:
                    brand = f.read().strip()
            except:
                pass
            
            try:
                with open("/sys/class/dmi/id/product_name", "r") as f:
                    model = f.read().strip()
            except:
                pass
            
            # Special cases for known devices
            if self.is_raspberry_pi():
                return {
                    "brand": "Raspberry Pi Foundation",
                    "model": self.get_raspberry_pi_model(),
                    "oem": "Raspberry Pi Foundation",
                    "detection_method": "raspberry_pi_detection"
                }
            
            return {
                "brand": brand if brand != "Unknown" else "Linux Device",
                "model": model,
                "oem": brand,
                "detection_method": "dmi"
            }
            
        except Exception as e:
            return {"brand": "Linux Device", "model": "Unknown", "oem": "Unknown", "detection_method": "error", "error": str(e)}
    
    def get_macos_manufacturer(self):
        """Get macOS manufacturer info"""
        try:
            # Get system info using system_profiler
            result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                  capture_output=True, text=True, timeout=10)
            output = result.stdout
            
            model = "Unknown"
            for line in output.split('\n'):
                if 'Model Name:' in line:
                    model = line.split(':', 1)[1].strip()
                    break
            
            return {
                "brand": "Apple",
                "model": model,
                "oem": "Apple Inc.",
                "detection_method": "system_profiler"
            }
        except:
            return {"brand": "Apple", "model": "Mac", "oem": "Apple Inc.", "detection_method": "fallback"}
    
    def is_raspberry_pi(self):
        """Check if device is a Raspberry Pi"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read().lower()
            return 'raspberry' in cpuinfo or 'bcm' in cpuinfo
        except:
            return False
    
    def get_raspberry_pi_model(self):
        """Get specific Raspberry Pi model"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if line.startswith('Model'):
                        return line.split(':', 1)[1].strip()
        except:
            pass
        return "Raspberry Pi"
    
    def is_nvidia_jetson(self):
        """Check if device is NVIDIA Jetson"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read().lower()
            return 'tegra' in cpuinfo or 'jetson' in cpuinfo
        except:
            return False
    
    def is_arduino_compatible(self):
        """Check if device is Arduino compatible"""
        # This is a simplified check - in reality, Arduino runs different OS
        return False
    
    def is_automotive_system(self):
        """Check if device is an automotive system"""
        try:
            # Check for automotive-specific indicators
            hostname = socket.gethostname().lower()
            automotive_indicators = ['car', 'auto', 'vehicle', 'ecu', 'can', 'obd']
            return any(indicator in hostname for indicator in automotive_indicators)
        except:
            return False
    
    def is_truck_system(self):
        """Check if device is a truck system"""
        try:
            hostname = socket.gethostname().lower()
            truck_indicators = ['truck', 'fleet', 'commercial', 'freight']
            return any(indicator in hostname for indicator in truck_indicators)
        except:
            return False
    
    def is_tablet_mode(self):
        """Check if Windows device is in tablet mode"""
        # Simplified check - would need more sophisticated detection
        return False
    
    def is_surface_device(self):
        """Check if device is Microsoft Surface"""
        try:
            if platform.system().lower() == "windows":
                result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=5)
                return 'surface' in result.stdout.lower()
        except:
            pass
        return False
    
    def is_gaming_laptop(self):
        """Check if device is a gaming laptop"""
        try:
            # Check for gaming-specific indicators
            hostname = socket.gethostname().lower()
            gaming_indicators = ['gaming', 'rog', 'predator', 'alienware', 'msi']
            return any(indicator in hostname for indicator in gaming_indicators)
        except:
            return False
    
    def is_workstation(self):
        """Check if device is a workstation"""
        try:
            # Check for workstation indicators
            hostname = socket.gethostname().lower()
            workstation_indicators = ['workstation', 'ws', 'dev', 'server']
            return any(indicator in hostname for indicator in workstation_indicators)
        except:
            return False
    
    def determine_form_factor(self, device_type):
        """Determine device form factor"""
        form_factors = {
            "android_phone": "handheld",
            "iphone": "handheld",
            "windows_tablet": "tablet",
            "surface_tablet": "2in1",
            "ipad": "tablet",
            "windows_laptop": "clamshell",
            "gaming_laptop": "clamshell",
            "macbook_apple_silicon": "clamshell",
            "macbook_intel": "clamshell",
            "desktop_pc": "tower",
            "workstation": "tower",
            "imac": "all_in_one",
            "raspberry_pi": "single_board",
            "nvidia_jetson": "single_board",
            "automotive_ecu": "embedded",
            "truck_telematics": "embedded"
        }
        return form_factors.get(device_type, "unknown")
    
    def determine_mobility(self, device_type):
        """Determine device mobility"""
        mobile_devices = [
            "android_phone", "iphone", "windows_tablet", "surface_tablet", "ipad",
            "windows_laptop", "gaming_laptop", "macbook_apple_silicon", "macbook_intel"
        ]
        return "mobile" if device_type in mobile_devices else "stationary"
    
    def determine_power_source(self, device_type):
        """Determine primary power source"""
        battery_devices = [
            "android_phone", "iphone", "windows_tablet", "surface_tablet", "ipad",
            "windows_laptop", "gaming_laptop", "macbook_apple_silicon", "macbook_intel"
        ]
        
        if device_type in battery_devices:
            return "battery"
        elif device_type in ["raspberry_pi", "nvidia_jetson"]:
            return "usb_power"
        elif device_type in ["automotive_ecu", "truck_telematics"]:
            return "vehicle_power"
        else:
            return "ac_power"
    
    def get_dynamic_config(self):
        """Get dynamic configuration based on detected device"""
        device_type = self.device_info["type"]
        category = self.device_info["category"]
        
        # Base configurations for different device types
        configs = {
            # Mobile Devices
            "android_phone": {
                "temp_thresholds": {"normal": 35, "warning": 45, "critical": 55},
                "cpu_thresholds": {"normal": 30, "warning": 70, "critical": 90},
                "memory_thresholds": {"normal": 60, "warning": 80, "critical": 95},
                "battery_thresholds": {"low": 20, "critical": 10},
                "update_interval": 5,
                "vehicle_analogy": "Electric Scooter",
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage", "network"],
                "features": ["gps", "accelerometer", "gyroscope", "camera", "microphone"]
            },
            
            "iphone": {
                "temp_thresholds": {"normal": 35, "warning": 45, "critical": 55},
                "cpu_thresholds": {"normal": 25, "warning": 65, "critical": 85},
                "memory_thresholds": {"normal": 70, "warning": 85, "critical": 95},
                "battery_thresholds": {"low": 20, "critical": 10},
                "update_interval": 5,
                "vehicle_analogy": "Tesla Model S",
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage"],
                "features": ["face_id", "touch_id", "camera", "lidar", "5g"]
            },
            
            # Tablets
            "windows_tablet": {
                "temp_thresholds": {"normal": 40, "warning": 55, "critical": 70},
                "cpu_thresholds": {"normal": 35, "warning": 70, "critical": 85},
                "memory_thresholds": {"normal": 60, "warning": 80, "critical": 90},
                "battery_thresholds": {"low": 15, "critical": 8},
                "update_interval": 3,
                "vehicle_analogy": "Hybrid Car",
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage", "disk"],
                "features": ["touchscreen", "stylus", "camera", "wifi", "bluetooth"]
            },
            
            "ipad": {
                "temp_thresholds": {"normal": 35, "warning": 50, "critical": 65},
                "cpu_thresholds": {"normal": 30, "warning": 65, "critical": 80},
                "memory_thresholds": {"normal": 65, "warning": 80, "critical": 95},
                "battery_thresholds": {"low": 20, "critical": 10},
                "update_interval": 4,
                "vehicle_analogy": "BMW i3",
                "health_metrics": ["cpu_temp", "battery", "memory", "cpu_usage"],
                "features": ["apple_pencil", "face_id", "camera", "lidar", "5g"]
            },
            
            # Laptops
            "windows_laptop": {
                "temp_thresholds": {"normal": 45, "warning": 70, "critical": 85},
                "cpu_thresholds": {"normal": 30, "warning": 70, "critical": 90},
                "memory_thresholds": {"normal": 50, "warning": 75, "critical": 90},
                "battery_thresholds": {"low": 20, "critical": 10},
                "update_interval": 2,
                "vehicle_analogy": "Sedan Car",
                "health_metrics": ["cpu_temp", "battery", "memory", "disk", "cpu_usage", "network"],
                "features": ["webcam", "microphone", "wifi", "bluetooth", "usb_ports"]
            },
            
            "gaming_laptop": {
                "temp_thresholds": {"normal": 50, "warning": 80, "critical": 95},
                "cpu_thresholds": {"normal": 40, "warning": 80, "critical": 95},
                "memory_thresholds": {"normal": 60, "warning": 80, "critical": 95},
                "battery_thresholds": {"low": 25, "critical": 15},
                "update_interval": 1,
                "vehicle_analogy": "Sports Car",
                "health_metrics": ["cpu_temp", "gpu_temp", "battery", "memory", "disk", "cpu_usage"],
                "features": ["rgb_lighting", "high_refresh_display", "gaming_keyboard", "advanced_cooling"]
            },
            
            "macbook_apple_silicon": {
                "temp_thresholds": {"normal": 40, "warning": 65, "critical": 80},
                "cpu_thresholds": {"normal": 25, "warning": 60, "critical": 85},
                "memory_thresholds": {"normal": 50, "warning": 70, "critical": 85},
                "battery_thresholds": {"low": 20, "critical": 10},
                "update_interval": 2,
                "vehicle_analogy": "Tesla Model 3",
                "health_metrics": ["cpu_temp", "battery", "memory", "disk", "cpu_usage"],
                "features": ["touch_id", "retina_display", "thunderbolt", "magsafe"]
            },
            
            # Desktops
            "desktop_pc": {
                "temp_thresholds": {"normal": 40, "warning": 65, "critical": 80},
                "cpu_thresholds": {"normal": 25, "warning": 60, "critical": 85},
                "memory_thresholds": {"normal": 40, "warning": 70, "critical": 85},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 2,
                "vehicle_analogy": "Pickup Truck",
                "health_metrics": ["cpu_temp", "memory", "disk", "cpu_usage", "network"],
                "features": ["multiple_monitors", "high_performance", "expandable", "advanced_cooling"]
            },
            
            "workstation": {
                "temp_thresholds": {"normal": 45, "warning": 70, "critical": 85},
                "cpu_thresholds": {"normal": 30, "warning": 70, "critical": 90},
                "memory_thresholds": {"normal": 50, "warning": 75, "critical": 90},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 1,
                "vehicle_analogy": "Heavy Duty Truck",
                "health_metrics": ["cpu_temp", "memory", "disk", "cpu_usage", "network", "gpu_usage"],
                "features": ["ecc_memory", "professional_gpu", "multiple_cpus", "enterprise_features"]
            },
            
            # IoT Devices
            "raspberry_pi": {
                "temp_thresholds": {"normal": 45, "warning": 60, "critical": 75},
                "cpu_thresholds": {"normal": 40, "warning": 70, "critical": 90},
                "memory_thresholds": {"normal": 60, "warning": 80, "critical": 95},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 5,
                "vehicle_analogy": "Drone",
                "health_metrics": ["cpu_temp", "memory", "cpu_usage", "disk", "network"],
                "features": ["gpio_pins", "camera_interface", "low_power", "expandable"]
            },
            
            "nvidia_jetson": {
                "temp_thresholds": {"normal": 50, "warning": 70, "critical": 85},
                "cpu_thresholds": {"normal": 45, "warning": 75, "critical": 90},
                "memory_thresholds": {"normal": 60, "warning": 80, "critical": 95},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 3,
                "vehicle_analogy": "AI Robot",
                "health_metrics": ["cpu_temp", "gpu_temp", "memory", "cpu_usage", "gpu_usage"],
                "features": ["ai_acceleration", "cuda_cores", "camera_interface", "high_performance"]
            },
            
            # Vehicle Systems
            "automotive_ecu": {
                "temp_thresholds": {"normal": 60, "warning": 80, "critical": 100},
                "cpu_thresholds": {"normal": 50, "warning": 80, "critical": 95},
                "memory_thresholds": {"normal": 70, "warning": 85, "critical": 95},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 1,
                "vehicle_analogy": "Car ECU",
                "health_metrics": ["cpu_temp", "memory", "cpu_usage", "can_bus", "sensors"],
                "features": ["can_bus", "obd2", "real_time_os", "automotive_grade"]
            },
            
            "truck_telematics": {
                "temp_thresholds": {"normal": 65, "warning": 85, "critical": 105},
                "cpu_thresholds": {"normal": 55, "warning": 80, "critical": 95},
                "memory_thresholds": {"normal": 70, "warning": 85, "critical": 95},
                "battery_thresholds": {"low": None, "critical": None},
                "update_interval": 1,
                "vehicle_analogy": "Truck Telematics",
                "health_metrics": ["cpu_temp", "memory", "cpu_usage", "gps", "fleet_data"],
                "features": ["gps_tracking", "fleet_management", "driver_monitoring", "fuel_tracking"]
            }
        }
        
        # Get config for detected device type, fallback to generic
        config = configs.get(device_type, configs.get("desktop_pc"))
        
        # Add manufacturer-specific adjustments
        config = self.apply_manufacturer_adjustments(config)
        
        return config
    
    def apply_manufacturer_adjustments(self, config):
        """Apply manufacturer-specific configuration adjustments"""
        manufacturer = self.manufacturer_info.get("brand", "").lower()
        
        # Manufacturer-specific adjustments
        if "apple" in manufacturer:
            config["update_interval"] = max(config["update_interval"], 3)  # Apple devices prefer less frequent updates
            config["features"] = config.get("features", []) + ["premium_build", "optimized_os"]
        
        elif "dell" in manufacturer:
            config["features"] = config.get("features", []) + ["enterprise_support", "business_grade"]
        
        elif "hp" in manufacturer:
            config["features"] = config.get("features", []) + ["hp_support", "business_features"]
        
        elif "lenovo" in manufacturer:
            config["features"] = config.get("features", []) + ["thinkpad_features", "enterprise_grade"]
        
        elif "microsoft" in manufacturer:
            config["features"] = config.get("features", []) + ["surface_features", "windows_integration"]
        
        elif "samsung" in manufacturer:
            config["features"] = config.get("features", []) + ["samsung_features", "android_optimization"]
        
        elif "raspberry" in manufacturer:
            config["features"] = config.get("features", []) + ["open_source", "maker_friendly", "educational"]
        
        return config
    
    def get_comprehensive_device_data(self):
        """Get all device information in a comprehensive format"""
        return {
            "device_info": self.device_info,
            "manufacturer_info": self.manufacturer_info,
            "device_config": self.device_config,
            "detection_timestamp": datetime.now().isoformat(),
            "capabilities": self.get_device_capabilities(),
            "recommended_features": self.get_recommended_features()
        }
    
    def get_device_capabilities(self):
        """Get device capabilities based on type and manufacturer"""
        capabilities = {
            "has_battery": self.device_info["power_source"] == "battery",
            "is_mobile": self.device_info["mobility"] == "mobile",
            "has_gps": "gps" in self.device_config.get("features", []),
            "has_camera": "camera" in self.device_config.get("features", []),
            "has_sensors": any(sensor in self.device_config.get("features", []) 
                             for sensor in ["accelerometer", "gyroscope", "sensors"]),
            "supports_ai": "ai_acceleration" in self.device_config.get("features", []),
            "is_automotive": self.device_info["category"] == "vehicle_system",
            "is_iot": self.device_info["category"] == "iot_device"
        }
        return capabilities
    
    def get_recommended_features(self):
        """Get recommended features based on device type"""
        device_type = self.device_info["type"]
        
        recommendations = {
            "monitoring_frequency": self.device_config["update_interval"],
            "priority_metrics": self.device_config["health_metrics"][:3],
            "vehicle_analogy": self.device_config["vehicle_analogy"],
            "optimization_tips": self.get_optimization_tips()
        }
        
        return recommendations
    
    def get_optimization_tips(self):
        """Get device-specific optimization tips"""
        device_type = self.device_info["type"]
        
        tips = {
            "android_phone": ["Enable battery optimization", "Close background apps", "Use dark mode"],
            "iphone": ["Enable Low Power Mode when needed", "Update iOS regularly", "Manage background refresh"],
            "windows_laptop": ["Use balanced power plan", "Keep drivers updated", "Regular disk cleanup"],
            "gaming_laptop": ["Monitor temperatures during gaming", "Use performance mode when needed", "Clean cooling system"],
            "macbook_apple_silicon": ["Use optimized apps", "Monitor Activity Monitor", "Enable automatic graphics switching"],
            "desktop_pc": ["Ensure proper ventilation", "Regular hardware maintenance", "Monitor system temperatures"],
            "raspberry_pi": ["Use quality power supply", "Monitor CPU temperature", "Use heat sinks"],
            "automotive_ecu": ["Regular diagnostic checks", "Monitor CAN bus health", "Update firmware regularly"],
            "truck_telematics": ["GPS signal quality", "Driver behavior monitoring", "Fuel efficiency tracking"]
        }
        
        return tips.get(device_type, ["Regular system maintenance", "Monitor performance", "Keep software updated"])

# Test the detector
if __name__ == "__main__":
    detector = DynamicDeviceDetector()
    
    print("🔍 Dynamic Device Detection Results")
    print("=" * 60)
    
    data = detector.get_comprehensive_device_data()
    
    print(f"Device Type: {data['device_info']['type']}")
    print(f"Category: {data['device_info']['category']}")
    print(f"Manufacturer: {data['manufacturer_info']['brand']}")
    print(f"Model: {data['manufacturer_info']['model']}")
    print(f"Vehicle Analogy: {data['device_config']['vehicle_analogy']}")
    print(f"Form Factor: {data['device_info']['form_factor']}")
    print(f"Mobility: {data['device_info']['mobility']}")
    print(f"Power Source: {data['device_info']['power_source']}")
    
    print("\n🎯 Device Capabilities:")
    for capability, value in data['capabilities'].items():
        print(f"  {capability}: {'✅' if value else '❌'}")
    
    print(f"\n💡 Optimization Tips:")
    for tip in data['recommended_features']['optimization_tips']:
        print(f"  • {tip}")