import psutil
import platform
import time
import json
import threading
from datetime import datetime
from typing import Dict, Any, List
import random
import math

class IoTSensorManager:
    def __init__(self):
        self.sensors = {
            'accelerometer': AccelerometerSensor(),
            'gyroscope': GyroscopeSensor(),
            'gps': GPSSensor(),
            'temperature': TemperatureSensor(),
            'pressure': PressureSensor(),
            'camera': CameraSensor(),
            'lidar': LiDARSensor(),
            'radar': RadarSensor()
        }
        self.sensor_data = {}
        self.is_running = False
        self.update_thread = None
    
    def start_monitoring(self):
        self.is_running = True
        self.update_thread = threading.Thread(target=self._continuous_monitoring)
        self.update_thread.daemon = True
        self.update_thread.start()
    
    def stop_monitoring(self):
        self.is_running = False
        if self.update_thread:
            self.update_thread.join()
    
    def _continuous_monitoring(self):
        while self.is_running:
            self.sensor_data = self.get_all_sensor_data()
            time.sleep(0.5)  # Update every 500ms
    
    def get_all_sensor_data(self) -> Dict[str, Any]:
        data = {}
        for sensor_name, sensor in self.sensors.items():
            try:
                data[sensor_name] = sensor.read()
            except Exception as e:
                data[sensor_name] = {"error": str(e), "status": "offline"}
        
        data['timestamp'] = datetime.now().isoformat()
        data['system_metrics'] = self._get_system_metrics()
        return data
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        try:
            return {
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent if platform.system() != 'Windows' else psutil.disk_usage('C:').percent,
                'network_io': dict(psutil.net_io_counters()._asdict()),
                'boot_time': psutil.boot_time(),
                'process_count': len(psutil.pids())
            }
        except Exception as e:
            return {"error": str(e)}

class AccelerometerSensor:
    def __init__(self):
        self.baseline = {'x': 0, 'y': 0, 'z': 9.81}  # Standard gravity
        
    def read(self) -> Dict[str, Any]:
        # Simulate accelerometer using system activity
        cpu_usage = psutil.cpu_percent()
        
        # Higher CPU usage = more "movement"
        movement_factor = cpu_usage / 100.0
        
        return {
            'x': self.baseline['x'] + random.uniform(-1, 1) * movement_factor,
            'y': self.baseline['y'] + random.uniform(-1, 1) * movement_factor,
            'z': self.baseline['z'] + random.uniform(-0.5, 0.5) * movement_factor,
            'magnitude': math.sqrt(sum([v**2 for v in self.baseline.values()])),
            'movement_detected': movement_factor > 0.5,
            'vibration_level': movement_factor,
            'status': 'active'
        }

class GyroscopeSensor:
    def __init__(self):
        self.baseline = {'pitch': 0, 'roll': 0, 'yaw': 0}
        
    def read(self) -> Dict[str, Any]:
        # Simulate gyroscope using network activity
        network = psutil.net_io_counters()
        activity = (network.bytes_sent + network.bytes_recv) / 1000000  # MB
        
        rotation_factor = min(1.0, activity / 100)
        
        return {
            'pitch': self.baseline['pitch'] + random.uniform(-5, 5) * rotation_factor,
            'roll': self.baseline['roll'] + random.uniform(-5, 5) * rotation_factor,
            'yaw': self.baseline['yaw'] + random.uniform(-10, 10) * rotation_factor,
            'angular_velocity': rotation_factor * 10,
            'stability': 1.0 - rotation_factor,
            'status': 'active'
        }

class GPSSensor:
    def __init__(self):
        # Delhi coordinates as base
        self.base_lat = 28.6139
        self.base_lon = 77.2090
        self.altitude = 216  # Delhi altitude
        
    def read(self) -> Dict[str, Any]:
        # Simulate GPS movement using system uptime
        uptime = time.time() - psutil.boot_time()
        
        # Small movement simulation
        lat_offset = math.sin(uptime / 1000) * 0.001
        lon_offset = math.cos(uptime / 1000) * 0.001
        
        return {
            'latitude': self.base_lat + lat_offset,
            'longitude': self.base_lon + lon_offset,
            'altitude': self.altitude + random.uniform(-5, 5),
            'speed': random.uniform(0, 60),  # km/h
            'heading': random.uniform(0, 360),
            'accuracy': random.uniform(1, 5),  # meters
            'satellite_count': random.randint(8, 15),
            'fix_quality': 'GPS_FIX',
            'status': 'active'
        }

class TemperatureSensor:
    def __init__(self):
        self.ambient_temp = 25
        
    def read(self) -> Dict[str, Any]:
        # Use CPU temperature if available, otherwise simulate
        try:
            temps = psutil.sensors_temperatures()
            cpu_temp = 45  # Default
            
            if temps:
                for name, entries in temps.items():
                    if entries:
                        cpu_temp = entries[0].current
                        break
        except:
            cpu_temp = 45 + np.random.uniform(-5, 15)
        
        return {
            'engine_temp': cpu_temp + np.random.uniform(10, 25),
            'ambient_temp': self.ambient_temp + np.random.uniform(-3, 3),
            'coolant_temp': cpu_temp + np.random.uniform(5, 15),
            'exhaust_temp': cpu_temp + np.random.uniform(50, 100),
            'battery_temp': cpu_temp + np.random.uniform(-5, 10),
            'critical_threshold': 95,
            'warning_threshold': 85,
            'status': 'active'
        }

class PressureSensor:
    def __init__(self):
        self.standard_pressure = 1013.25  # hPa
        
    def read(self) -> Dict[str, Any]:
        # Simulate pressure variations
        memory_usage = psutil.virtual_memory().percent
        pressure_variation = (memory_usage - 50) / 10  # Pressure changes with "load"
        
        return {
            'atmospheric_pressure': self.standard_pressure + pressure_variation,
            'tire_pressure': {
                'front_left': 32 + random.uniform(-2, 2),
                'front_right': 32 + random.uniform(-2, 2),
                'rear_left': 30 + random.uniform(-2, 2),
                'rear_right': 30 + random.uniform(-2, 2)
            },
            'brake_pressure': 50 + random.uniform(-5, 5),
            'fuel_pressure': 40 + random.uniform(-3, 3),
            'status': 'active'
        }

class CameraSensor:
    def __init__(self):
        self.resolution = {'width': 1920, 'height': 1080}
        self.fps = 30
        
    def read(self) -> Dict[str, Any]:
        # Simulate camera data
        cpu_usage = psutil.cpu_percent()
        
        return {
            'resolution': self.resolution,
            'fps': self.fps,
            'exposure': random.uniform(1/60, 1/1000),
            'iso': random.randint(100, 1600),
            'focus_distance': random.uniform(0.5, 100),  # meters
            'objects_detected': random.randint(0, 10),
            'lane_detection': {
                'left_lane': np.random.choice([True, False]),
                'right_lane': np.random.choice([True, False]),
                'lane_departure_warning': cpu_usage > 80
            },
            'traffic_signs': random.randint(0, 3),
            'pedestrians': random.randint(0, 5),
            'vehicles': random.randint(0, 8),
            'image_quality': 'HIGH' if cpu_usage < 70 else 'MEDIUM',
            'status': 'active'
        }

class LiDARSensor:
    def __init__(self):
        self.range_max = 200  # meters
        self.resolution = 0.1  # degrees
        
    def read(self) -> Dict[str, Any]:
        # Simulate LiDAR data
        disk_usage = psutil.disk_usage('C:' if platform.system() == 'Windows' else '/').percent
        
        return {
            'range_max': self.range_max,
            'resolution': self.resolution,
            'point_cloud_size': random.randint(10000, 100000),
            'obstacles_detected': random.randint(0, 15),
            'closest_obstacle': random.uniform(1, 50),  # meters
            'scan_frequency': 10,  # Hz
            'accuracy': random.uniform(0.02, 0.05),  # meters
            'environmental_mapping': {
                'buildings': random.randint(0, 5),
                'trees': random.randint(0, 10),
                'road_boundaries': True,
                'terrain_type': np.random.choice(['URBAN', 'HIGHWAY', 'RURAL'])
            },
            'data_quality': 'HIGH' if disk_usage < 80 else 'MEDIUM',
            'status': 'active'
        }

class RadarSensor:
    def __init__(self):
        self.frequency = 77  # GHz
        self.range_max = 250  # meters
        
    def read(self) -> Dict[str, Any]:
        # Simulate radar data
        network = psutil.net_io_counters()
        activity = (network.bytes_sent + network.bytes_recv) / 1000000
        
        return {
            'frequency': self.frequency,
            'range_max': self.range_max,
            'targets_detected': random.randint(0, 20),
            'moving_targets': random.randint(0, 10),
            'stationary_targets': random.randint(0, 15),
            'doppler_data': {
                'relative_velocity': random.uniform(-50, 50),  # km/h
                'approach_rate': random.uniform(-10, 10)  # m/s
            },
            'weather_penetration': np.random.choice(['EXCELLENT', 'GOOD', 'FAIR']),
            'interference_level': min(100, activity / 10),
            'blind_spot_monitoring': {
                'left_blind_spot': np.random.choice([True, False]),
                'right_blind_spot': np.random.choice([True, False])
            },
            'status': 'active'
        }

# Global IoT sensor manager
iot_manager = IoTSensorManager()