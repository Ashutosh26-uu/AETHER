import numpy as np
import tensorflow as tf
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime, timedelta
import json

class VehicleHealthMonitor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.health_model = None
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic vehicle sensor data for training"""
        np.random.seed(42)
        
        # Normal operating conditions
        normal_data = {
            'engine_temp': np.random.normal(90, 10, n_samples),
            'vibration_x': np.random.normal(0.5, 0.2, n_samples),
            'vibration_y': np.random.normal(0.5, 0.2, n_samples),
            'vibration_z': np.random.normal(0.5, 0.2, n_samples),
            'oil_pressure': np.random.normal(40, 5, n_samples),
            'rpm': np.random.normal(2000, 500, n_samples),
            'battery_voltage': np.random.normal(12.6, 0.5, n_samples),
            'brake_temp': np.random.normal(150, 30, n_samples)
        }
        
        # Add some anomalous data
        anomaly_indices = np.random.choice(n_samples, size=int(n_samples * 0.1), replace=False)
        
        for idx in anomaly_indices:
            normal_data['engine_temp'][idx] = np.random.uniform(120, 140)  # Overheating
            normal_data['vibration_x'][idx] = np.random.uniform(2, 5)      # High vibration
            normal_data['oil_pressure'][idx] = np.random.uniform(10, 20)   # Low pressure
        
        return np.column_stack(list(normal_data.values()))
    
    def train_model(self):
        """Train the vehicle health monitoring model"""
        print("Training Vehicle Health Monitor...")
        
        # Generate training data
        training_data = self.generate_synthetic_data(2000)
        
        # Fit scaler and anomaly detector
        scaled_data = self.scaler.fit_transform(training_data)
        self.anomaly_detector.fit(scaled_data)
        
        # Create a simple neural network for health score prediction
        self.health_model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(8,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')  # Health score 0-1
        ])
        
        self.health_model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        # Generate health scores (inverse of anomaly scores)
        anomaly_scores = self.anomaly_detector.decision_function(scaled_data)
        health_scores = (anomaly_scores - anomaly_scores.min()) / (anomaly_scores.max() - anomaly_scores.min())
        
        # Train the model
        self.health_model.fit(
            scaled_data, health_scores,
            epochs=50,
            batch_size=32,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained = True
        print("Vehicle Health Monitor trained successfully!")
    
    def predict_health(self, sensor_data):
        """Predict vehicle health from sensor data"""
        if not self.is_trained:
            self.train_model()
        
        # Convert sensor data to numpy array
        if isinstance(sensor_data, dict):
            data_array = np.array([
                sensor_data.get('engine_temp', 90),
                sensor_data.get('vibration_x', 0.5),
                sensor_data.get('vibration_y', 0.5),
                sensor_data.get('vibration_z', 0.5),
                sensor_data.get('oil_pressure', 40),
                sensor_data.get('rpm', 2000),
                sensor_data.get('battery_voltage', 12.6),
                sensor_data.get('brake_temp', 150)
            ]).reshape(1, -1)
        else:
            data_array = np.array(sensor_data).reshape(1, -1)
        
        # Scale the data
        scaled_data = self.scaler.transform(data_array)
        
        # Predict health score
        health_score = self.health_model.predict(scaled_data, verbose=0)[0][0]
        
        # Detect anomalies
        anomaly_score = self.anomaly_detector.decision_function(scaled_data)[0]
        is_anomaly = self.anomaly_detector.predict(scaled_data)[0] == -1
        
        # Generate maintenance recommendations
        recommendations = self._generate_recommendations(sensor_data, health_score, is_anomaly)
        
        return {
            'health_score': float(health_score * 100),  # Convert to percentage
            'is_anomaly': bool(is_anomaly),
            'anomaly_score': float(anomaly_score),
            'status': 'CRITICAL' if health_score < 0.3 else 'WARNING' if health_score < 0.7 else 'GOOD',
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, sensor_data, health_score, is_anomaly):
        """Generate maintenance recommendations based on sensor data"""
        recommendations = []
        
        if isinstance(sensor_data, dict):
            if sensor_data.get('engine_temp', 90) > 110:
                recommendations.append("Engine overheating detected - Check coolant levels")
            
            if sensor_data.get('oil_pressure', 40) < 25:
                recommendations.append("Low oil pressure - Schedule oil change immediately")
            
            if sensor_data.get('battery_voltage', 12.6) < 12.0:
                recommendations.append("Battery voltage low - Check charging system")
            
            vibration = max(
                sensor_data.get('vibration_x', 0.5),
                sensor_data.get('vibration_y', 0.5),
                sensor_data.get('vibration_z', 0.5)
            )
            if vibration > 1.5:
                recommendations.append("High vibration detected - Check engine mounts and balance")
        
        if health_score < 0.5:
            recommendations.append("Overall health critical - Schedule comprehensive inspection")
        elif health_score < 0.7:
            recommendations.append("Preventive maintenance recommended")
        
        if is_anomaly:
            recommendations.append("Unusual patterns detected - Professional diagnosis recommended")
        
        return recommendations
    
    def save_model(self, filepath):
        """Save the trained model"""
        if self.is_trained:
            self.health_model.save(f"{filepath}_health_model.h5")
            joblib.dump(self.scaler, f"{filepath}_scaler.pkl")
            joblib.dump(self.anomaly_detector, f"{filepath}_anomaly_detector.pkl")
    
    def load_model(self, filepath):
        """Load a pre-trained model"""
        try:
            self.health_model = tf.keras.models.load_model(f"{filepath}_health_model.h5")
            self.scaler = joblib.load(f"{filepath}_scaler.pkl")
            self.anomaly_detector = joblib.load(f"{filepath}_anomaly_detector.pkl")
            self.is_trained = True
            return True
        except:
            return False

# Example usage
if __name__ == "__main__":
    monitor = VehicleHealthMonitor()
    
    # Example sensor data
    test_data = {
        'engine_temp': 95,
        'vibration_x': 0.6,
        'vibration_y': 0.5,
        'vibration_z': 0.7,
        'oil_pressure': 38,
        'rpm': 2200,
        'battery_voltage': 12.4,
        'brake_temp': 160
    }
    
    result = monitor.predict_health(test_data)
    print(json.dumps(result, indent=2))