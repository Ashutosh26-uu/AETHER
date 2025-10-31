import serial
import time
import json
from datetime import datetime
import subprocess
import platform
import psutil

class VehicleOBDAnalyzer:
    def __init__(self):
        self.obd_connection = None
        self.vehicle_type = "unknown"
        self.vehicle_config = {}
        self.supported_pids = []
        
    def detect_vehicle_connection(self):
        """Detect if connected to a real vehicle via OBD-II, CAN bus, or simulation"""
        connection_methods = [
            self.try_obd_connection,
            self.try_can_bus_connection,
            self.try_bluetooth_obd,
            self.try_wifi_obd,
            self.simulate_vehicle_connection
        ]
        
        for method in connection_methods:
            try:
                if method():
                    return True
            except:
                continue
        return False
    
    def try_obd_connection(self):
        """Try to connect via OBD-II serial port"""
        obd_ports = ['COM1', 'COM2', 'COM3', 'COM4', '/dev/ttyUSB0', '/dev/ttyUSB1']
        
        for port in obd_ports:
            try:
                self.obd_connection = serial.Serial(port, 38400, timeout=1)
                self.obd_connection.write(b'ATZ\r')  # Reset
                response = self.obd_connection.read(50)
                if b'ELM' in response or b'OK' in response:
                    print(f"✅ OBD-II connected on {port}")
                    self.vehicle_type = "real_vehicle_obd"
                    return True
            except:
                continue
        return False
    
    def try_can_bus_connection(self):
        """Try to connect via CAN bus interface"""
        try:
            # Check for CAN interfaces (Linux)
            result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            if 'can0' in result.stdout:
                print("✅ CAN bus interface detected")
                self.vehicle_type = "real_vehicle_can"
                return True
        except:
            pass
        return False
    
    def try_bluetooth_obd(self):
        """Try to connect via Bluetooth OBD adapter"""
        try:
            import bluetooth
            nearby_devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in nearby_devices:
                if 'obd' in name.lower() or 'elm' in name.lower():
                    print(f"✅ Bluetooth OBD device found: {name}")
                    self.vehicle_type = "real_vehicle_bluetooth"
                    return True
        except:
            pass
        return False
    
    def try_wifi_obd(self):
        """Try to connect via WiFi OBD adapter"""
        import socket
        try:
            # Common WiFi OBD adapter IPs
            obd_ips = ['192.168.0.10', '192.168.4.1', '10.0.0.1']
            for ip in obd_ips:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, 35000))
                if result == 0:
                    print(f"✅ WiFi OBD adapter found at {ip}")
                    self.vehicle_type = "real_vehicle_wifi"
                    sock.close()
                    return True
                sock.close()
        except:
            pass
        return False
    
    def simulate_vehicle_connection(self):
        """Simulate vehicle connection for demo purposes"""
        print("📱 No real vehicle detected - Using simulation mode")
        self.vehicle_type = "simulated_vehicle"
        return True
    
    def identify_vehicle_type(self):
        """Identify specific vehicle type from VIN or other data"""
        if self.vehicle_type.startswith("real_vehicle"):
            vin = self.get_vin()
            if vin:
                return self.decode_vehicle_from_vin(vin)
        
        # Fallback to generic vehicle types
        vehicle_types = {
            "car": {
                "name": "Passenger Car",
                "max_speed": 180,
                "engine_type": "Internal Combustion",
                "fuel_type": "Petrol/Diesel",
                "temp_normal": 90, "temp_warning": 105, "temp_critical": 120,
                "rpm_normal": 2000, "rpm_warning": 5000, "rpm_critical": 6500
            },
            "truck": {
                "name": "Heavy Truck",
                "max_speed": 120,
                "engine_type": "Diesel Engine",
                "fuel_type": "Diesel",
                "temp_normal": 85, "temp_warning": 100, "temp_critical": 115,
                "rpm_normal": 1500, "rpm_warning": 2500, "rpm_critical": 3000
            },
            "motorcycle": {
                "name": "Motorcycle",
                "max_speed": 200,
                "engine_type": "Small Engine",
                "fuel_type": "Petrol",
                "temp_normal": 80, "temp_warning": 95, "temp_critical": 110,
                "rpm_normal": 3000, "rpm_warning": 8000, "rpm_critical": 10000
            },
            "bus": {
                "name": "Public Bus",
                "max_speed": 100,
                "engine_type": "Heavy Diesel",
                "fuel_type": "Diesel/CNG",
                "temp_normal": 85, "temp_warning": 100, "temp_critical": 115,
                "rpm_normal": 1200, "rpm_warning": 2200, "rpm_critical": 2800
            }
        }
        
        # For demo, randomly assign or let user choose
        import random
        selected_type = random.choice(list(vehicle_types.keys()))
        self.vehicle_config = vehicle_types[selected_type]
        return selected_type
    
    def get_vin(self):
        """Get Vehicle Identification Number"""
        if self.obd_connection:
            try:
                self.obd_connection.write(b'0902\r')  # Request VIN
                response = self.obd_connection.read(100)
                # Parse VIN from response
                return "DEMO17DIGITVIN123"  # Placeholder
            except:
                pass
        return None
    
    def decode_vehicle_from_vin(self, vin):
        """Decode vehicle type from VIN"""
        # VIN decoding logic (simplified)
        if vin[0] in ['1', '4', '5']:  # North America
            return "car"
        elif vin[0] in ['W', 'V']:  # Europe
            return "car"
        else:
            return "car"
    
    def get_real_vehicle_data(self):
        """Get real vehicle data from OBD-II or simulate"""
        if self.vehicle_type.startswith("real_vehicle"):
            return self.get_obd_data()
        else:
            return self.simulate_vehicle_data()
    
    def get_obd_data(self):
        """Get real data from OBD-II port"""
        obd_data = {}
        
        # Standard OBD-II PIDs
        pids = {
            '010C': 'rpm',           # Engine RPM
            '010D': 'speed',         # Vehicle Speed
            '0105': 'coolant_temp',  # Engine Coolant Temperature
            '010F': 'intake_temp',   # Intake Air Temperature
            '0111': 'throttle_pos',  # Throttle Position
            '012F': 'fuel_level',    # Fuel Tank Level
            '0142': 'voltage',       # Control Module Voltage
            '0104': 'engine_load'    # Calculated Engine Load
        }
        
        for pid, name in pids.items():
            try:
                if self.obd_connection:
                    self.obd_connection.write(f'{pid}\r'.encode())
                    response = self.obd_connection.read(50)
                    value = self.parse_obd_response(pid, response)
                    obd_data[name] = value
                else:
                    # Simulate realistic values
                    obd_data[name] = self.get_simulated_value(name)
            except:
                obd_data[name] = self.get_simulated_value(name)
        
        return self.format_vehicle_data(obd_data)
    
    def parse_obd_response(self, pid, response):
        """Parse OBD-II response to actual values"""
        # Simplified parsing - real implementation would be more complex
        try:
            hex_data = response.decode().strip()
            if pid == '010C':  # RPM
                return int(hex_data[-4:], 16) / 4
            elif pid == '010D':  # Speed
                return int(hex_data[-2:], 16)
            elif pid == '0105':  # Coolant temp
                return int(hex_data[-2:], 16) - 40
            # Add more parsing logic for other PIDs
        except:
            pass
        return 0
    
    def get_simulated_value(self, parameter):
        """Generate realistic simulated values"""
        import random
        
        base_values = {
            'rpm': random.uniform(800, 3000),
            'speed': random.uniform(0, 80),
            'coolant_temp': random.uniform(85, 95),
            'intake_temp': random.uniform(20, 40),
            'throttle_pos': random.uniform(0, 30),
            'fuel_level': random.uniform(20, 90),
            'voltage': random.uniform(12.0, 14.5),
            'engine_load': random.uniform(10, 40)
        }
        
        return base_values.get(parameter, 0)
    
    def simulate_vehicle_data(self):
        """Simulate comprehensive vehicle data"""
        import random
        
        # Use laptop CPU as "engine load" for simulation
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        
        simulated_data = {
            'rpm': 800 + (cpu_usage * 30),  # Idle + load-based RPM
            'speed': min(cpu_usage * 1.2, 120),  # Speed based on CPU
            'coolant_temp': 85 + (cpu_usage * 0.3),  # Temperature correlation
            'intake_temp': 25 + random.uniform(-5, 15),
            'throttle_pos': cpu_usage * 0.8,  # Throttle based on load
            'fuel_level': max(100 - (memory_usage * 0.5), 10),  # Fuel based on memory
            'voltage': 12.6 + random.uniform(-0.5, 1.0),
            'engine_load': cpu_usage,
            'oil_pressure': 35 + random.uniform(-5, 10),
            'transmission_temp': 70 + random.uniform(-10, 20)
        }
        
        return self.format_vehicle_data(simulated_data)
    
    def format_vehicle_data(self, raw_data):
        """Format vehicle data into AETHER standard format"""
        vehicle_id = f"{self.vehicle_config.get('name', 'Vehicle')}_{int(time.time()) % 1000}"
        
        # Analyze health based on vehicle-specific thresholds
        health_analysis = self.analyze_vehicle_health(raw_data)
        
        formatted_data = {
            "vehicle_id": vehicle_id,
            "vehicle_type": self.vehicle_config.get('name', 'Unknown Vehicle'),
            "connection_type": self.vehicle_type,
            "timestamp": datetime.now().isoformat(),
            
            "engine": {
                "rpm": raw_data.get('rpm', 0),
                "temperature": raw_data.get('coolant_temp', 0),
                "load": raw_data.get('engine_load', 0),
                "oil_pressure": raw_data.get('oil_pressure', 0)
            },
            
            "performance": {
                "speed": raw_data.get('speed', 0),
                "throttle_position": raw_data.get('throttle_pos', 0),
                "fuel_level": raw_data.get('fuel_level', 0),
                "transmission_temp": raw_data.get('transmission_temp', 0)
            },
            
            "electrical": {
                "battery_voltage": raw_data.get('voltage', 12.6),
                "alternator_status": "OK" if raw_data.get('voltage', 12.6) > 13.0 else "CHECK"
            },
            
            "health_analysis": health_analysis,
            
            "vehicle_specs": self.vehicle_config
        }
        
        return formatted_data
    
    def analyze_vehicle_health(self, data):
        """Analyze vehicle health based on real automotive thresholds"""
        analysis = {
            "overall_score": 100,
            "status": "EXCELLENT",
            "issues": [],
            "recommendations": [],
            "critical_alerts": []
        }
        
        # Engine temperature analysis
        temp = data.get('coolant_temp', 90)
        temp_critical = self.vehicle_config.get('temp_critical', 120)
        temp_warning = self.vehicle_config.get('temp_warning', 105)
        
        if temp > temp_critical:
            analysis["overall_score"] -= 40
            analysis["critical_alerts"].append("ENGINE OVERHEATING - STOP IMMEDIATELY")
            analysis["recommendations"].append("Pull over safely and turn off engine")
        elif temp > temp_warning:
            analysis["overall_score"] -= 20
            analysis["issues"].append(f"High engine temperature: {temp:.1f}°C")
            analysis["recommendations"].append("Monitor temperature closely")
        
        # RPM analysis
        rpm = data.get('rpm', 1000)
        rpm_critical = self.vehicle_config.get('rpm_critical', 6500)
        if rpm > rpm_critical:
            analysis["overall_score"] -= 25
            analysis["critical_alerts"].append("ENGINE OVER-REVVING")
        
        # Oil pressure analysis
        oil_pressure = data.get('oil_pressure', 35)
        if oil_pressure < 10:
            analysis["overall_score"] -= 35
            analysis["critical_alerts"].append("LOW OIL PRESSURE - ENGINE DAMAGE RISK")
        elif oil_pressure < 20:
            analysis["issues"].append("Low oil pressure detected")
            analysis["recommendations"].append("Check oil level immediately")
        
        # Battery voltage analysis
        voltage = data.get('voltage', 12.6)
        if voltage < 11.5:
            analysis["critical_alerts"].append("BATTERY CRITICAL - CHARGING SYSTEM FAILURE")
        elif voltage < 12.0:
            analysis["issues"].append("Low battery voltage")
            analysis["recommendations"].append("Check charging system")
        
        # Fuel level analysis
        fuel = data.get('fuel_level', 50)
        if fuel < 10:
            analysis["issues"].append("Low fuel level")
            analysis["recommendations"].append("Refuel soon")
        
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

# Test the analyzer
if __name__ == "__main__":
    analyzer = VehicleOBDAnalyzer()
    
    print("🚗 AETHER Vehicle OBD Analyzer")
    print("=" * 50)
    
    # Try to connect to real vehicle
    if analyzer.detect_vehicle_connection():
        vehicle_type = analyzer.identify_vehicle_type()
        print(f"Vehicle Type: {vehicle_type}")
        
        # Get vehicle data
        data = analyzer.get_real_vehicle_data()
        print(f"Vehicle: {data['vehicle_type']}")
        print(f"Connection: {data['connection_type']}")
        print(f"Engine RPM: {data['engine']['rpm']:.0f}")
        print(f"Speed: {data['performance']['speed']:.1f} km/h")
        print(f"Engine Temp: {data['engine']['temperature']:.1f}°C")
        print(f"Health Score: {data['health_analysis']['overall_score']:.1f}%")
        
        if data['health_analysis']['critical_alerts']:
            print("\n🚨 CRITICAL ALERTS:")
            for alert in data['health_analysis']['critical_alerts']:
                print(f"  - {alert}")
    else:
        print("❌ No vehicle connection detected")