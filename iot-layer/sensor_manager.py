import json
import time
import threading
import random
from datetime import datetime
import paho.mqtt.client as mqtt
import serial
import asyncio
from typing import Dict, Any, Callable

class SensorManager:
    def __init__(self, mqtt_broker="localhost", mqtt_port=1883):
        self.mqtt_client = mqtt.Client()
        self.mqtt_broker = mqtt_broker
        self.mqtt_port = mqtt_port
        self.sensors = {}
        self.callbacks = {}
        self.running = False
        self.data_buffer = {}
        
        # Initialize MQTT
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_message = self._on_mqtt_message
        
    def _on_mqtt_connect(self, client, userdata, flags, rc):
        print(f"MQTT Connected with result code {rc}")
        client.subscribe("aether/sensors/+")
        client.subscribe("aether/vehicle/+")
    
    def _on_mqtt_message(self, client, userdata, msg):
        try:
            topic_parts = msg.topic.split('/')
            sensor_type = topic_parts[-1]
            data = json.loads(msg.payload.decode())
            
            self.data_buffer[sensor_type] = {
                'data': data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Trigger callbacks
            if sensor_type in self.callbacks:
                for callback in self.callbacks[sensor_type]:
                    callback(data)
                    
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    def add_sensor(self, sensor_id: str, sensor_config: Dict[str, Any]):
        """Add a new sensor to the system"""
        self.sensors[sensor_id] = {
            'config': sensor_config,
            'status': 'inactive',
            'last_reading': None
        }
        
        if sensor_config.get('type') == 'serial':
            self._initialize_serial_sensor(sensor_id, sensor_config)
        elif sensor_config.get('type') == 'gpio':
            self._initialize_gpio_sensor(sensor_id, sensor_config)
        elif sensor_config.get('type') == 'i2c':
            self._initialize_i2c_sensor(sensor_id, sensor_config)
    
    def _initialize_serial_sensor(self, sensor_id: str, config: Dict[str, Any]):
        """Initialize serial-based sensor (GPS, OBD-II, etc.)"""
        try:
            port = config.get('port', '/dev/ttyUSB0')
            baudrate = config.get('baudrate', 9600)
            
            # For demo purposes, we'll simulate the sensor
            self.sensors[sensor_id]['status'] = 'active'
            print(f"Serial sensor {sensor_id} initialized on {port}")
            
        except Exception as e:
            print(f"Error initializing serial sensor {sensor_id}: {e}")
            self.sensors[sensor_id]['status'] = 'error'
    
    def _initialize_gpio_sensor(self, sensor_id: str, config: Dict[str, Any]):
        """Initialize GPIO-based sensor"""
        try:
            # For demo purposes, simulate GPIO sensor
            self.sensors[sensor_id]['status'] = 'active'
            print(f"GPIO sensor {sensor_id} initialized")
            
        except Exception as e:
            print(f"Error initializing GPIO sensor {sensor_id}: {e}")
            self.sensors[sensor_id]['status'] = 'error'
    
    def _initialize_i2c_sensor(self, sensor_id: str, config: Dict[str, Any]):
        """Initialize I2C-based sensor (accelerometer, gyroscope, etc.)"""
        try:
            # For demo purposes, simulate I2C sensor
            self.sensors[sensor_id]['status'] = 'active'
            print(f"I2C sensor {sensor_id} initialized")
            
        except Exception as e:
            print(f"Error initializing I2C sensor {sensor_id}: {e}")
            self.sensors[sensor_id]['status'] = 'error'
    
    def start_monitoring(self):
        """Start sensor monitoring"""
        self.running = True
        
        # Connect to MQTT broker
        try:
            self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
            self.mqtt_client.loop_start()
        except:
            print("MQTT broker not available, running in simulation mode")
        
        # Start sensor reading threads
        for sensor_id in self.sensors:
            if self.sensors[sensor_id]['status'] == 'active':
                thread = threading.Thread(target=self._sensor_reading_loop, args=(sensor_id,))
                thread.daemon = True
                thread.start()
        
        print("Sensor monitoring started")
    
    def stop_monitoring(self):
        """Stop sensor monitoring"""
        self.running = False
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("Sensor monitoring stopped")
    
    def _sensor_reading_loop(self, sensor_id: str):
        """Main sensor reading loop"""
        sensor_config = self.sensors[sensor_id]['config']
        sensor_type = sensor_config.get('sensor_type', 'generic')
        
        while self.running:
            try:
                # Generate sensor data based on type
                data = self._generate_sensor_data(sensor_type)
                
                # Update sensor status
                self.sensors[sensor_id]['last_reading'] = data
                self.sensors[sensor_id]['last_update'] = datetime.now().isoformat()
                
                # Publish to MQTT
                topic = f"aether/sensors/{sensor_type}"
                self.mqtt_client.publish(topic, json.dumps(data))
                
                # Sleep based on sensor frequency
                frequency = sensor_config.get('frequency', 1)  # Hz
                time.sleep(1.0 / frequency)
                
            except Exception as e:
                print(f"Error reading sensor {sensor_id}: {e}")
                time.sleep(1)
    
    def _generate_sensor_data(self, sensor_type: str) -> Dict[str, Any]:
        """Generate realistic sensor data for different sensor types"""
        timestamp = datetime.now().isoformat()
        
        if sensor_type == 'gps':
            return {
                'latitude': 28.6139 + random.uniform(-0.01, 0.01),
                'longitude': 77.2090 + random.uniform(-0.01, 0.01),
                'altitude': 200 + random.uniform(-10, 10),
                'speed': random.uniform(0, 100),
                'heading': random.uniform(0, 360),
                'satellites': random.randint(4, 12),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'accelerometer':
            return {
                'x': random.uniform(-2, 2),
                'y': random.uniform(-2, 2),
                'z': random.uniform(8, 12),  # Gravity component
                'magnitude': random.uniform(8, 12),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'gyroscope':
            return {
                'x': random.uniform(-50, 50),
                'y': random.uniform(-50, 50),
                'z': random.uniform(-50, 50),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'temperature':
            return {
                'engine_temp': 85 + random.uniform(-10, 20),
                'ambient_temp': 25 + random.uniform(-5, 10),
                'brake_temp': 150 + random.uniform(-30, 50),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'pressure':
            return {
                'tire_fl': 32 + random.uniform(-2, 2),
                'tire_fr': 32 + random.uniform(-2, 2),
                'tire_rl': 32 + random.uniform(-2, 2),
                'tire_rr': 32 + random.uniform(-2, 2),
                'oil_pressure': 40 + random.uniform(-5, 5),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'obd2':
            return {
                'rpm': random.uniform(800, 6000),
                'speed': random.uniform(0, 120),
                'throttle_position': random.uniform(0, 100),
                'engine_load': random.uniform(0, 100),
                'fuel_level': random.uniform(10, 100),
                'battery_voltage': 12.6 + random.uniform(-0.5, 0.5),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'camera':
            return {
                'frame_id': random.randint(1000, 9999),
                'objects_detected': random.randint(0, 10),
                'lane_detection': random.choice(['good', 'poor', 'none']),
                'visibility': random.uniform(0.5, 1.0),
                'timestamp': timestamp
            }
        
        elif sensor_type == 'lidar':
            return {
                'distance_front': random.uniform(5, 100),
                'distance_left': random.uniform(2, 50),
                'distance_right': random.uniform(2, 50),
                'objects_detected': random.randint(0, 5),
                'point_cloud_size': random.randint(1000, 10000),
                'timestamp': timestamp
            }
        
        else:
            return {
                'value': random.uniform(0, 100),
                'status': 'active',
                'timestamp': timestamp
            }
    
    def get_sensor_data(self, sensor_id: str = None) -> Dict[str, Any]:
        """Get current sensor data"""
        if sensor_id:
            return self.sensors.get(sensor_id, {})
        else:
            return self.data_buffer
    
    def register_callback(self, sensor_type: str, callback: Callable):
        """Register callback for sensor data"""
        if sensor_type not in self.callbacks:
            self.callbacks[sensor_type] = []
        self.callbacks[sensor_type].append(callback)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        active_sensors = sum(1 for s in self.sensors.values() if s['status'] == 'active')
        total_sensors = len(self.sensors)
        
        return {
            'total_sensors': total_sensors,
            'active_sensors': active_sensors,
            'error_sensors': total_sensors - active_sensors,
            'system_health': 'good' if active_sensors > total_sensors * 0.8 else 'degraded',
            'last_update': datetime.now().isoformat()
        }

# Example usage and sensor configuration
def setup_default_sensors():
    """Setup default sensor configuration for AETHER"""
    sensor_manager = SensorManager()
    
    # GPS sensor
    sensor_manager.add_sensor('gps_primary', {
        'type': 'serial',
        'sensor_type': 'gps',
        'port': '/dev/ttyUSB0',
        'baudrate': 9600,
        'frequency': 1  # 1 Hz
    })
    
    # Accelerometer
    sensor_manager.add_sensor('accelerometer', {
        'type': 'i2c',
        'sensor_type': 'accelerometer',
        'address': 0x68,
        'frequency': 10  # 10 Hz
    })
    
    # Gyroscope
    sensor_manager.add_sensor('gyroscope', {
        'type': 'i2c',
        'sensor_type': 'gyroscope',
        'address': 0x69,
        'frequency': 10  # 10 Hz
    })
    
    # Temperature sensors
    sensor_manager.add_sensor('temperature', {
        'type': 'gpio',
        'sensor_type': 'temperature',
        'pins': [18, 19, 20],
        'frequency': 0.5  # 0.5 Hz
    })
    
    # Pressure sensors
    sensor_manager.add_sensor('pressure', {
        'type': 'i2c',
        'sensor_type': 'pressure',
        'address': 0x76,
        'frequency': 0.2  # 0.2 Hz
    })
    
    # OBD-II interface
    sensor_manager.add_sensor('obd2', {
        'type': 'serial',
        'sensor_type': 'obd2',
        'port': '/dev/ttyUSB1',
        'baudrate': 38400,
        'frequency': 2  # 2 Hz
    })
    
    # Camera
    sensor_manager.add_sensor('camera_front', {
        'type': 'usb',
        'sensor_type': 'camera',
        'device': '/dev/video0',
        'frequency': 30  # 30 FPS
    })
    
    # LiDAR
    sensor_manager.add_sensor('lidar', {
        'type': 'serial',
        'sensor_type': 'lidar',
        'port': '/dev/ttyUSB2',
        'baudrate': 115200,
        'frequency': 10  # 10 Hz
    })
    
    return sensor_manager

if __name__ == "__main__":
    # Setup and start sensor monitoring
    sensor_manager = setup_default_sensors()
    
    # Register some callbacks
    def gps_callback(data):
        print(f"GPS Update: {data['latitude']}, {data['longitude']}")
    
    def temperature_callback(data):
        if data['engine_temp'] > 100:
            print("WARNING: Engine overheating!")
    
    sensor_manager.register_callback('gps', gps_callback)
    sensor_manager.register_callback('temperature', temperature_callback)
    
    # Start monitoring
    sensor_manager.start_monitoring()
    
    try:
        # Run for demo
        time.sleep(30)
        
        # Print system status
        status = sensor_manager.get_system_status()
        print(f"System Status: {json.dumps(status, indent=2)}")
        
    except KeyboardInterrupt:
        print("Stopping sensor monitoring...")
    finally:
        sensor_manager.stop_monitoring()