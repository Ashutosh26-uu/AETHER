import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import threading
import time
import psutil

class AdvancedAIPredictor:
    def __init__(self):
        self.collision_model = CollisionPredictionModel()
        self.health_model = VehicleHealthModel()
        self.driver_model = DriverBehaviorModel()
        self.emotion_model = EmotionAnalysisModel()
        
    def predict_collision_risk(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.collision_model.predict(sensor_data)
    
    def analyze_vehicle_health(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        return self.health_model.analyze(metrics)
    
    def analyze_driver_behavior(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.driver_model.analyze(behavior_data)
    
    def detect_emotions(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.emotion_model.detect(system_data)

class CollisionPredictionModel:
    def __init__(self):
        self.risk_threshold = 0.7
        self.history = []
        
    def predict(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate advanced collision prediction using real system metrics
        cpu_usage = sensor_data.get('cpu_usage', 50)
        memory_usage = sensor_data.get('memory_usage', 50)
        network_activity = sensor_data.get('network_activity', 0)
        
        # Higher system stress = higher collision risk simulation
        stress_factor = (cpu_usage + memory_usage) / 200
        
        # Time-based risk calculation
        hour = datetime.now().hour
        if 6 <= hour <= 9 or 17 <= hour <= 20:  # Rush hours
            time_risk = 0.3
        elif 22 <= hour or hour <= 5:  # Night time
            time_risk = 0.4
        else:
            time_risk = 0.1
        
        # Calculate collision probability
        collision_prob = min(0.95, stress_factor + time_risk + np.random.uniform(-0.1, 0.1))
        
        # Determine risk level
        if collision_prob > 0.8:
            risk_level = "CRITICAL"
            time_to_collision = np.random.uniform(1, 3)
        elif collision_prob > 0.6:
            risk_level = "HIGH"
            time_to_collision = np.random.uniform(3, 6)
        elif collision_prob > 0.3:
            risk_level = "MEDIUM"
            time_to_collision = np.random.uniform(6, 10)
        else:
            risk_level = "LOW"
            time_to_collision = None
        
        # Advanced predictions
        predictions = {
            "collision_probability": round(collision_prob, 3),
            "risk_level": risk_level,
            "time_to_collision": time_to_collision,
            "contributing_factors": self._analyze_factors(sensor_data),
            "recommended_actions": self._get_recommendations(risk_level),
            "confidence": round(0.85 + np.random.uniform(-0.1, 0.1), 2),
            "prediction_timestamp": datetime.now().isoformat()
        }
        
        self.history.append(predictions)
        if len(self.history) > 100:
            self.history.pop(0)
            
        return predictions
    
    def _analyze_factors(self, sensor_data: Dict[str, Any]) -> List[str]:
        factors = []
        
        if sensor_data.get('cpu_usage', 0) > 80:
            factors.append("High system load detected")
        if sensor_data.get('memory_usage', 0) > 85:
            factors.append("Memory pressure detected")
        
        hour = datetime.now().hour
        if 22 <= hour or hour <= 5:
            factors.append("Night driving conditions")
        elif 6 <= hour <= 9 or 17 <= hour <= 20:
            factors.append("Rush hour traffic")
            
        return factors
    
    def _get_recommendations(self, risk_level: str) -> List[str]:
        recommendations = {
            "CRITICAL": [
                "Immediate attention required",
                "Reduce speed significantly",
                "Increase following distance",
                "Consider stopping safely"
            ],
            "HIGH": [
                "Increase alertness",
                "Reduce speed",
                "Maintain safe distance",
                "Avoid lane changes"
            ],
            "MEDIUM": [
                "Stay alert",
                "Monitor surroundings",
                "Maintain current speed"
            ],
            "LOW": [
                "Continue normal driving",
                "Regular monitoring"
            ]
        }
        return recommendations.get(risk_level, [])

class VehicleHealthModel:
    def __init__(self):
        self.health_history = []
        
    def analyze(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        # Use real system metrics to simulate vehicle health
        cpu_temp = self._get_cpu_temperature()
        cpu_usage = metrics.get('cpu_usage', 50)
        memory_usage = metrics.get('memory_usage', 50)
        disk_usage = metrics.get('disk_usage', 50)
        
        # Engine health based on CPU temperature and usage
        engine_health = max(0, 100 - (cpu_temp - 40) * 2 - (cpu_usage - 50) * 0.5)
        
        # Battery health based on system uptime and memory usage
        uptime_hours = (time.time() - psutil.boot_time()) / 3600
        battery_health = max(20, 100 - (uptime_hours / 24) * 2 - (memory_usage - 50) * 0.3)
        
        # Brake health based on disk activity
        brake_health = max(70, 100 - (disk_usage - 50) * 0.4)
        
        # Overall health score
        overall_health = (engine_health + battery_health + brake_health) / 3
        
        # Predict maintenance needs
        maintenance_prediction = self._predict_maintenance(overall_health, metrics)
        
        analysis = {
            "overall_health_score": round(overall_health, 1),
            "component_health": {
                "engine": round(engine_health, 1),
                "battery": round(battery_health, 1),
                "brakes": round(brake_health, 1),
                "transmission": round(85 + np.random.uniform(-10, 10), 1),
                "tires": round(90 + np.random.uniform(-15, 5), 1)
            },
            "maintenance_prediction": maintenance_prediction,
            "health_trend": self._calculate_trend(),
            "alerts": self._generate_health_alerts(overall_health),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        self.health_history.append(analysis)
        if len(self.health_history) > 50:
            self.health_history.pop(0)
            
        return analysis
    
    def _get_cpu_temperature(self) -> float:
        try:
            # Try to get real CPU temperature
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
        except:
            pass
        return 45 + np.random.uniform(-5, 15)  # Fallback simulation
    
    def _predict_maintenance(self, health_score: float, metrics: Dict[str, Any]) -> Dict[str, Any]:
        if health_score < 70:
            urgency = "URGENT"
            days_until = np.random.randint(1, 7)
        elif health_score < 85:
            urgency = "SOON"
            days_until = np.random.randint(7, 30)
        else:
            urgency = "ROUTINE"
            days_until = np.random.randint(30, 90)
            
        return {
            "urgency": urgency,
            "estimated_days": days_until,
            "recommended_services": self._get_service_recommendations(health_score),
            "estimated_cost": np.random.randint(2000, 15000)
        }
    
    def _get_service_recommendations(self, health_score: float) -> List[str]:
        services = []
        if health_score < 70:
            services.extend(["Engine diagnostic", "Brake inspection", "Battery check"])
        elif health_score < 85:
            services.extend(["Oil change", "Filter replacement"])
        else:
            services.append("Routine inspection")
        return services
    
    def _calculate_trend(self) -> str:
        if len(self.health_history) < 3:
            return "STABLE"
        
        recent_scores = [h["overall_health_score"] for h in self.health_history[-3:]]
        if recent_scores[-1] > recent_scores[0] + 2:
            return "IMPROVING"
        elif recent_scores[-1] < recent_scores[0] - 2:
            return "DECLINING"
        else:
            return "STABLE"
    
    def _generate_health_alerts(self, health_score: float) -> List[Dict[str, Any]]:
        alerts = []
        if health_score < 60:
            alerts.append({
                "type": "CRITICAL",
                "message": "Vehicle health critical - immediate attention required",
                "priority": "HIGH"
            })
        elif health_score < 75:
            alerts.append({
                "type": "WARNING",
                "message": "Vehicle health declining - schedule maintenance",
                "priority": "MEDIUM"
            })
        return alerts

class DriverBehaviorModel:
    def __init__(self):
        self.behavior_history = []
        
    def analyze(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate driver behavior analysis using system activity
        cpu_usage = behavior_data.get('cpu_usage', 50)
        network_activity = behavior_data.get('network_sent', 0) + behavior_data.get('network_recv', 0)
        
        # Alertness based on system activity patterns
        alertness = max(0.3, min(1.0, 1.0 - (cpu_usage - 30) / 100))
        
        # Stress level based on system load
        stress_level = min(1.0, cpu_usage / 80)
        
        # Fatigue based on time and system patterns
        hour = datetime.now().hour
        if 2 <= hour <= 6 or 14 <= hour <= 16:
            fatigue_factor = 0.7
        else:
            fatigue_factor = 0.3
            
        fatigue = min(1.0, fatigue_factor + (100 - alertness * 100) / 200)
        
        # Driving pattern analysis
        driving_pattern = self._analyze_driving_pattern(cpu_usage, network_activity)
        
        analysis = {
            "alertness_score": round(alertness, 2),
            "stress_level": round(stress_level, 2),
            "fatigue_level": round(fatigue, 2),
            "driving_pattern": driving_pattern,
            "recommendations": self._get_behavior_recommendations(alertness, stress_level, fatigue),
            "risk_assessment": self._assess_risk(alertness, stress_level, fatigue),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        self.behavior_history.append(analysis)
        if len(self.behavior_history) > 30:
            self.behavior_history.pop(0)
            
        return analysis
    
    def _analyze_driving_pattern(self, cpu_usage: float, network_activity: int) -> Dict[str, Any]:
        # High CPU usage = aggressive driving simulation
        if cpu_usage > 80:
            pattern = "AGGRESSIVE"
            score = 0.8
        elif cpu_usage > 60:
            pattern = "MODERATE"
            score = 0.5
        else:
            pattern = "CALM"
            score = 0.2
            
        return {
            "pattern_type": pattern,
            "aggressiveness_score": score,
            "consistency": round(np.random.uniform(0.6, 0.9), 2)
        }
    
    def _get_behavior_recommendations(self, alertness: float, stress: float, fatigue: float) -> List[str]:
        recommendations = []
        
        if alertness < 0.6:
            recommendations.append("Take a break to improve alertness")
        if stress > 0.7:
            recommendations.append("Practice calm driving techniques")
        if fatigue > 0.6:
            recommendations.append("Consider resting before continuing")
            
        return recommendations
    
    def _assess_risk(self, alertness: float, stress: float, fatigue: float) -> Dict[str, Any]:
        risk_score = (1 - alertness) * 0.4 + stress * 0.3 + fatigue * 0.3
        
        if risk_score > 0.7:
            risk_level = "HIGH"
        elif risk_score > 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "factors": [f"Alertness: {alertness:.1f}", f"Stress: {stress:.1f}", f"Fatigue: {fatigue:.1f}"]
        }

class EmotionAnalysisModel:
    def __init__(self):
        self.emotion_history = []
        
    def detect(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        # Simulate emotion detection using system patterns
        cpu_usage = system_data.get('cpu_usage', 50)
        memory_usage = system_data.get('memory_usage', 50)
        
        # Map system activity to emotional states
        if cpu_usage > 85:
            primary_emotion = "STRESSED"
            intensity = 0.8
        elif cpu_usage > 70:
            primary_emotion = "ALERT"
            intensity = 0.6
        elif cpu_usage < 30:
            primary_emotion = "CALM"
            intensity = 0.4
        else:
            primary_emotion = "NEUTRAL"
            intensity = 0.5
            
        # Climate control recommendations based on emotion
        climate_recommendations = self._get_climate_recommendations(primary_emotion, intensity)
        
        analysis = {
            "primary_emotion": primary_emotion,
            "emotion_intensity": round(intensity, 2),
            "confidence": round(0.75 + np.random.uniform(-0.1, 0.15), 2),
            "secondary_emotions": self._detect_secondary_emotions(cpu_usage, memory_usage),
            "climate_recommendations": climate_recommendations,
            "comfort_adjustments": self._get_comfort_adjustments(primary_emotion),
            "detection_timestamp": datetime.now().isoformat()
        }
        
        self.emotion_history.append(analysis)
        if len(self.emotion_history) > 20:
            self.emotion_history.pop(0)
            
        return analysis
    
    def _detect_secondary_emotions(self, cpu_usage: float, memory_usage: float) -> List[Dict[str, Any]]:
        emotions = []
        
        if memory_usage > 80:
            emotions.append({"emotion": "OVERWHELMED", "intensity": 0.6})
        if cpu_usage < 20 and memory_usage < 40:
            emotions.append({"emotion": "RELAXED", "intensity": 0.7})
            
        return emotions
    
    def _get_climate_recommendations(self, emotion: str, intensity: float) -> Dict[str, Any]:
        recommendations = {
            "STRESSED": {
                "temperature": 22,
                "fan_speed": "LOW",
                "lighting": "SOFT",
                "music_volume": "LOW"
            },
            "ALERT": {
                "temperature": 21,
                "fan_speed": "MEDIUM",
                "lighting": "BRIGHT",
                "music_volume": "MEDIUM"
            },
            "CALM": {
                "temperature": 23,
                "fan_speed": "LOW",
                "lighting": "WARM",
                "music_volume": "LOW"
            },
            "NEUTRAL": {
                "temperature": 22,
                "fan_speed": "AUTO",
                "lighting": "AUTO",
                "music_volume": "MEDIUM"
            }
        }
        
        return recommendations.get(emotion, recommendations["NEUTRAL"])
    
    def _get_comfort_adjustments(self, emotion: str) -> List[str]:
        adjustments = {
            "STRESSED": ["Reduce cabin lighting", "Lower music volume", "Activate massage seats"],
            "ALERT": ["Increase brightness", "Optimize air circulation"],
            "CALM": ["Maintain current settings", "Soft ambient lighting"],
            "NEUTRAL": ["Auto-adjust based on preferences"]
        }
        
        return adjustments.get(emotion, ["No adjustments needed"])

# Global AI predictor instance
ai_predictor = AdvancedAIPredictor()