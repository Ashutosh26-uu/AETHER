import time
import math
from typing import Dict, List, Tuple

class DroneController:
    def __init__(self, drone_id: str = "AETHER_DRONE_001"):
        self.drone_id = drone_id
        self.is_connected = False
        self.current_position = {'lat': 28.6139, 'lon': 77.2090, 'alt': 0}
        self.home_position = {'lat': 28.6139, 'lon': 77.2090, 'alt': 0}
        self.battery_level = 100
        self.flight_mode = 'STANDBY'
        self.mission_queue = []
        self.sensor_data = {}
        self.is_flying = False
        
        self.max_altitude = 120
        self.max_range = 2000
        self.max_flight_time = 25
        
    def connect_drone(self) -> bool:
        try:
            print(f"Connecting to drone {self.drone_id}...")
            time.sleep(2)
            self.is_connected = True
            self.flight_mode = 'READY'
            self._initialize_systems()
            print(f"Drone {self.drone_id} connected successfully")
            return True
        except Exception as e:
            print(f"Failed to connect to drone: {e}")
            self.is_connected = False
            self.flight_mode = 'ERROR'
            return False
    
    def _initialize_systems(self):
        try:
            self.sensor_data = {
                'gps': {'status': 'active', 'satellites': 12},
                'imu': {'status': 'active', 'calibrated': True},
                'camera': {'status': 'active', 'resolution': (1920, 1080)},
                'gimbal': {'status': 'active', 'stabilized': True}
            }
        except Exception as e:
            print(f"System initialization failed: {e}")
            self.sensor_data = {}
    
    def takeoff(self, altitude: float = 10) -> bool:
        try:
            if not self.is_connected:
                print("Drone not connected")
                return False
            
            if altitude > self.max_altitude:
                print(f"Altitude {altitude}m exceeds maximum {self.max_altitude}m")
                return False
            
            print(f"Taking off to {altitude}m...")
            self.flight_mode = 'TAKEOFF'
            
            for alt in range(0, int(altitude) + 1):
                self.current_position['alt'] = alt
                time.sleep(0.1)
            
            self.flight_mode = 'HOVER'
            self.is_flying = True
            print(f"Takeoff complete. Hovering at {altitude}m")
            return True
        except Exception as e:
            print(f"Takeoff failed: {e}")
            self.flight_mode = 'ERROR'
            return False
    
    def land(self) -> bool:
        try:
            if not self.is_flying:
                print("Drone is not flying")
                return False
            
            print("Landing...")
            self.flight_mode = 'LANDING'
            
            current_alt = self.current_position['alt']
            for alt in range(int(current_alt), -1, -1):
                self.current_position['alt'] = alt
                time.sleep(0.1)
            
            self.flight_mode = 'LANDED'
            self.is_flying = False
            print("Landing complete")
            return True
        except Exception as e:
            print(f"Landing failed: {e}")
            self.flight_mode = 'ERROR'
            return False
    
    def goto_position(self, lat: float, lon: float, alt: float = None) -> bool:
        try:
            if not self.is_flying:
                print("Drone must be flying to move")
                return False
            
            if alt is None:
                alt = self.current_position['alt']
            
            distance = self._calculate_distance(
                (self.current_position['lat'], self.current_position['lon']),
                (lat, lon)
            )
            
            if distance > self.max_range / 1000:
                print(f"Target position {distance:.2f}km exceeds maximum range {self.max_range/1000}km")
                return False
            
            print(f"Flying to position: {lat}, {lon}, {alt}m")
            self.flight_mode = 'WAYPOINT'
            
            steps = 20
            lat_step = (lat - self.current_position['lat']) / steps
            lon_step = (lon - self.current_position['lon']) / steps
            alt_step = (alt - self.current_position['alt']) / steps
            
            for i in range(steps + 1):
                self.current_position['lat'] += lat_step
                self.current_position['lon'] += lon_step
                self.current_position['alt'] += alt_step
                time.sleep(0.2)
            
            self.flight_mode = 'HOVER'
            print(f"Arrived at destination: {lat}, {lon}, {alt}m")
            return True
        except Exception as e:
            print(f"Navigation failed: {e}")
            self.flight_mode = 'ERROR'
            return False
    
    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        try:
            lat1, lon1 = pos1
            lat2, lon2 = pos2
            R = 6371
            dlat = math.radians(lat2 - lat1)
            dlon = math.radians(lon2 - lon1)
            a = (math.sin(dlat/2) * math.sin(dlat/2) + 
                 math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
                 math.sin(dlon/2) * math.sin(dlon/2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c
        except Exception:
            return 0.0
    

    
    def get_status(self) -> Dict[str, any]:
        try:
            return {
                'drone_id': self.drone_id,
                'connected': self.is_connected,
                'flying': self.is_flying,
                'position': self.current_position,
                'battery': self.battery_level,
                'flight_mode': self.flight_mode,
                'sensor_data': self.sensor_data
            }
        except Exception:
            return {'error': 'Status unavailable'}