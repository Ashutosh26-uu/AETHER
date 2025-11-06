import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
import psutil

class SwarmVehicle:
    def __init__(self, vehicle_id: str, lat: float, lon: float):
        self.vehicle_id = vehicle_id
        self.position = {'lat': lat, 'lon': lon}
        self.status = 'ACTIVE'
        self.health_score = np.random.uniform(80, 95)
        self.fuel_level = np.random.uniform(30, 90)
        self.speed = np.random.uniform(20, 80)
        self.destination = None
        self.route = []
        self.last_update = datetime.now()
        self.shared_data = {}
        
    def update_position(self, lat: float, lon: float):
        self.position = {'lat': lat, 'lon': lon}
        self.last_update = datetime.now()
        
    def share_traffic_data(self, traffic_info: Dict[str, Any]):
        self.shared_data['traffic'] = {
            'timestamp': datetime.now().isoformat(),
            'data': traffic_info
        }
        
    def share_road_conditions(self, road_info: Dict[str, Any]):
        self.shared_data['road_conditions'] = {
            'timestamp': datetime.now().isoformat(),
            'data': road_info
        }

class SwarmIntelligence:
    def __init__(self):
        self.vehicles = {}
        self.swarm_groups = {}
        self.shared_knowledge = {
            'traffic_patterns': {},
            'road_conditions': {},
            'weather_data': {},
            'hazards': [],
            'optimal_routes': {}
        }
        self.coordination_active = True
        self.update_thread = None
        self.start_coordination()
        
    def start_coordination(self):
        # Initialize demo vehicles
        self._initialize_demo_vehicles()
        
        # Start coordination thread
        self.update_thread = threading.Thread(target=self._coordination_loop)
        self.update_thread.daemon = True
        self.update_thread.start()
        
    def _initialize_demo_vehicles(self):
        # Create demo vehicles around Delhi
        base_positions = [
            (28.6139, 77.2090),  # Connaught Place
            (28.5355, 77.3910),  # Noida
            (28.4595, 77.0266),  # Gurgaon
            (28.7041, 77.1025),  # North Delhi
            (28.5244, 77.1855),  # South Delhi
        ]
        
        for i, (lat, lon) in enumerate(base_positions):
            vehicle_id = f"AETHER_VEHICLE_{i+1:03d}"
            self.vehicles[vehicle_id] = SwarmVehicle(vehicle_id, lat, lon)
            
    def _coordination_loop(self):
        while self.coordination_active:
            try:
                self._update_swarm_intelligence()
                self._optimize_routes()
                self._share_knowledge()
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                print(f"Swarm coordination error: {e}")
                time.sleep(5)
                
    def _update_swarm_intelligence(self):
        # Simulate vehicle movement and data collection
        for vehicle in self.vehicles.values():
            # Update position slightly
            lat_change = np.random.uniform(-0.001, 0.001)
            lon_change = np.random.uniform(-0.001, 0.001)
            
            new_lat = vehicle.position['lat'] + lat_change
            new_lon = vehicle.position['lon'] + lon_change
            vehicle.update_position(new_lat, new_lon)
            
            # Update vehicle metrics
            vehicle.health_score = max(70, vehicle.health_score + np.random.uniform(-1, 1))
            vehicle.fuel_level = max(10, vehicle.fuel_level + np.random.uniform(-0.5, 0.1))
            vehicle.speed = max(0, min(120, vehicle.speed + np.random.uniform(-5, 5)))
            
            # Generate traffic data
            traffic_density = self._calculate_traffic_density(vehicle.position)
            vehicle.share_traffic_data({
                'density': traffic_density,
                'average_speed': vehicle.speed,
                'congestion_level': 'HIGH' if traffic_density > 0.8 else 'MEDIUM' if traffic_density > 0.5 else 'LOW'
            })
            
            # Generate road condition data
            road_quality = np.random.uniform(0.6, 1.0)
            vehicle.share_road_conditions({
                'surface_quality': road_quality,
                'visibility': np.random.uniform(0.7, 1.0),
                'weather_impact': np.random.choice(['NONE', 'LIGHT', 'MODERATE'])
            })
            
    def _calculate_traffic_density(self, position: Dict[str, float]) -> float:
        # Simulate traffic density based on location and time
        hour = datetime.now().hour
        
        # Rush hour simulation
        if 7 <= hour <= 10 or 17 <= hour <= 20:
            base_density = 0.7
        elif 22 <= hour or hour <= 6:
            base_density = 0.2
        else:
            base_density = 0.4
            
        # Add location-based variation
        lat, lon = position['lat'], position['lon']
        
        # Central Delhi (higher density)
        if 28.6 <= lat <= 28.65 and 77.2 <= lon <= 77.25:
            base_density += 0.2
            
        return min(1.0, base_density + np.random.uniform(-0.1, 0.1))
        
    def _optimize_routes(self):
        # Swarm-based route optimization
        for vehicle_id, vehicle in self.vehicles.items():
            if vehicle.destination:
                optimal_route = self._calculate_optimal_route(
                    vehicle.position, 
                    vehicle.destination,
                    vehicle_id
                )
                vehicle.route = optimal_route
                
    def _calculate_optimal_route(self, start: Dict[str, float], end: Dict[str, float], vehicle_id: str) -> List[Dict[str, Any]]:
        # Use swarm intelligence to find optimal route
        route_points = []
        
        # Generate intermediate waypoints
        lat_diff = end['lat'] - start['lat']
        lon_diff = end['lon'] - start['lon']
        
        num_waypoints = max(3, int(abs(lat_diff) + abs(lon_diff)) * 100)
        
        for i in range(1, num_waypoints):
            progress = i / num_waypoints
            waypoint = {
                'lat': start['lat'] + lat_diff * progress,
                'lon': start['lon'] + lon_diff * progress,
                'traffic_score': self._get_traffic_score_at_point(
                    start['lat'] + lat_diff * progress,
                    start['lon'] + lon_diff * progress
                ),
                'estimated_time': progress * self._estimate_total_time(start, end)
            }
            route_points.append(waypoint)
            
        return route_points
        
    def _get_traffic_score_at_point(self, lat: float, lon: float) -> float:
        # Get traffic score from swarm knowledge
        nearby_vehicles = self._get_nearby_vehicles({'lat': lat, 'lon': lon}, radius=0.01)
        
        if not nearby_vehicles:
            return 0.5  # Default score
            
        traffic_scores = []
        for vehicle in nearby_vehicles:
            if 'traffic' in vehicle.shared_data:
                traffic_data = vehicle.shared_data['traffic']['data']
                traffic_scores.append(traffic_data.get('density', 0.5))
                
        return np.mean(traffic_scores) if traffic_scores else 0.5
        
    def _estimate_total_time(self, start: Dict[str, float], end: Dict[str, float]) -> float:
        # Estimate travel time in minutes
        distance = self._calculate_distance(start, end)
        average_speed = 40  # km/h in city
        return (distance * 60) / average_speed
        
    def _calculate_distance(self, point1: Dict[str, float], point2: Dict[str, float]) -> float:
        # Haversine formula for distance calculation
        lat1, lon1 = np.radians(point1['lat']), np.radians(point1['lon'])
        lat2, lon2 = np.radians(point2['lat']), np.radians(point2['lon'])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        return 6371 * c  # Earth radius in km
        
    def _get_nearby_vehicles(self, position: Dict[str, float], radius: float = 0.01) -> List[SwarmVehicle]:
        nearby = []
        for vehicle in self.vehicles.values():
            distance = self._calculate_distance(position, vehicle.position)
            if distance <= radius * 111:  # Convert degrees to km approximately
                nearby.append(vehicle)
        return nearby
        
    def _share_knowledge(self):
        # Aggregate knowledge from all vehicles
        all_traffic_data = []
        all_road_conditions = []
        
        for vehicle in self.vehicles.values():
            if 'traffic' in vehicle.shared_data:
                all_traffic_data.append(vehicle.shared_data['traffic'])
            if 'road_conditions' in vehicle.shared_data:
                all_road_conditions.append(vehicle.shared_data['road_conditions'])
                
        # Update shared knowledge
        self.shared_knowledge['traffic_patterns'] = self._aggregate_traffic_data(all_traffic_data)
        self.shared_knowledge['road_conditions'] = self._aggregate_road_data(all_road_conditions)
        self.shared_knowledge['last_update'] = datetime.now().isoformat()
        
    def _aggregate_traffic_data(self, traffic_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not traffic_data:
            return {}
            
        densities = [data['data']['density'] for data in traffic_data if 'density' in data['data']]
        speeds = [data['data']['average_speed'] for data in traffic_data if 'average_speed' in data['data']]
        
        return {
            'average_density': np.mean(densities) if densities else 0.5,
            'average_speed': np.mean(speeds) if speeds else 40,
            'congestion_hotspots': self._identify_congestion_hotspots(traffic_data),
            'sample_size': len(traffic_data)
        }
        
    def _aggregate_road_data(self, road_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not road_data:
            return {}
            
        qualities = [data['data']['surface_quality'] for data in road_data if 'surface_quality' in data['data']]
        visibilities = [data['data']['visibility'] for data in road_data if 'visibility' in data['data']]
        
        return {
            'average_surface_quality': np.mean(qualities) if qualities else 0.8,
            'average_visibility': np.mean(visibilities) if visibilities else 0.9,
            'weather_impacts': [data['data']['weather_impact'] for data in road_data if 'weather_impact' in data['data']],
            'sample_size': len(road_data)
        }
        
    def _identify_congestion_hotspots(self, traffic_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Identify areas with high traffic density
        hotspots = []
        
        high_density_data = [data for data in traffic_data if data['data'].get('density', 0) > 0.7]
        
        if len(high_density_data) > 2:
            hotspots.append({
                'severity': 'HIGH',
                'affected_vehicles': len(high_density_data),
                'average_density': np.mean([data['data']['density'] for data in high_density_data])
            })
            
        return hotspots
        
    def get_swarm_status(self) -> Dict[str, Any]:
        active_vehicles = [v for v in self.vehicles.values() if v.status == 'ACTIVE']
        
        return {
            'total_vehicles': len(self.vehicles),
            'active_vehicles': len(active_vehicles),
            'coordination_efficiency': self._calculate_coordination_efficiency(),
            'shared_knowledge_quality': self._assess_knowledge_quality(),
            'swarm_groups': len(self.swarm_groups),
            'data_sharing_rate': self._calculate_data_sharing_rate(),
            'collective_intelligence_score': self._calculate_intelligence_score(),
            'last_coordination_update': datetime.now().isoformat()
        }
        
    def _calculate_coordination_efficiency(self) -> float:
        # Calculate how well vehicles are coordinating
        vehicles_with_data = sum(1 for v in self.vehicles.values() if v.shared_data)
        total_vehicles = len(self.vehicles)
        
        return (vehicles_with_data / total_vehicles) * 100 if total_vehicles > 0 else 0
        
    def _assess_knowledge_quality(self) -> float:
        # Assess the quality of shared knowledge
        quality_score = 0
        
        if self.shared_knowledge['traffic_patterns']:
            quality_score += 30
        if self.shared_knowledge['road_conditions']:
            quality_score += 30
        if len(self.shared_knowledge['hazards']) > 0:
            quality_score += 20
        if self.shared_knowledge['optimal_routes']:
            quality_score += 20
            
        return quality_score
        
    def _calculate_data_sharing_rate(self) -> float:
        # Calculate rate of data sharing between vehicles
        recent_shares = 0
        cutoff_time = datetime.now() - timedelta(minutes=5)
        
        for vehicle in self.vehicles.values():
            for data_type, data in vehicle.shared_data.items():
                if 'timestamp' in data:
                    share_time = datetime.fromisoformat(data['timestamp'])
                    if share_time > cutoff_time:
                        recent_shares += 1
                        
        return min(100, (recent_shares / len(self.vehicles)) * 10)
        
    def _calculate_intelligence_score(self) -> float:
        # Overall swarm intelligence score
        efficiency = self._calculate_coordination_efficiency()
        knowledge_quality = self._assess_knowledge_quality()
        sharing_rate = self._calculate_data_sharing_rate()
        
        return (efficiency * 0.4 + knowledge_quality * 0.4 + sharing_rate * 0.2)
        
    def get_vehicle_data(self, vehicle_id: str) -> Optional[Dict[str, Any]]:
        if vehicle_id not in self.vehicles:
            return None
            
        vehicle = self.vehicles[vehicle_id]
        return {
            'vehicle_id': vehicle.vehicle_id,
            'position': vehicle.position,
            'status': vehicle.status,
            'health_score': vehicle.health_score,
            'fuel_level': vehicle.fuel_level,
            'speed': vehicle.speed,
            'shared_data': vehicle.shared_data,
            'route': vehicle.route,
            'last_update': vehicle.last_update.isoformat()
        }
        
    def get_all_vehicles_data(self) -> List[Dict[str, Any]]:
        return [self.get_vehicle_data(vid) for vid in self.vehicles.keys()]

# Global swarm intelligence instance
swarm_intelligence = SwarmIntelligence()