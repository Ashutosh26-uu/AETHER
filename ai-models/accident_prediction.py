import numpy as np
import cv2
import tensorflow as tf
from ultralytics import YOLO
import json
from datetime import datetime
import threading
import queue

class AccidentPredictionSystem:
    def __init__(self):
        self.yolo_model = None
        self.collision_model = None
        self.driver_state_model = None
        self.is_initialized = False
        self.alert_queue = queue.Queue()
        
    def initialize_models(self):
        """Initialize YOLO and custom models"""
        print("Initializing Accident Prediction System...")
        
        try:
            # Load YOLO for object detection
            self.yolo_model = YOLO('yolov8n.pt')  # Nano version for speed
            
            # Create collision prediction model
            self.collision_model = self._create_collision_model()
            
            # Create driver state model
            self.driver_state_model = self._create_driver_state_model()
            
            self.is_initialized = True
            print("Accident Prediction System initialized successfully!")
            
        except Exception as e:
            print(f"Error initializing models: {e}")
            # Use simplified models for demo
            self._initialize_demo_models()
    
    def _create_collision_model(self):
        """Create neural network for collision prediction"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(3, activation='softmax')  # LOW, MEDIUM, HIGH risk
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train with synthetic data
        self._train_collision_model(model)
        return model
    
    def _create_driver_state_model(self):
        """Create model for driver drowsiness/attention detection"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(6,)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')  # Alertness score
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        # Train with synthetic data
        self._train_driver_state_model(model)
        return model
    
    def _train_collision_model(self, model):
        """Train collision prediction model with synthetic data"""
        # Generate synthetic training data
        n_samples = 5000
        
        # Features: speed, distance_to_object, relative_speed, weather, road_condition, etc.
        X = np.random.rand(n_samples, 10)
        
        # Simulate risk levels based on conditions
        y = np.zeros((n_samples, 3))  # One-hot encoded: [LOW, MEDIUM, HIGH]
        
        for i in range(n_samples):
            speed = X[i, 0] * 120  # Speed in km/h
            distance = X[i, 1] * 100  # Distance in meters
            relative_speed = X[i, 2] * 50  # Relative speed
            
            # Risk calculation logic
            if speed > 80 and distance < 20 and relative_speed > 30:
                y[i, 2] = 1  # HIGH risk
            elif speed > 60 and distance < 50 and relative_speed > 20:
                y[i, 1] = 1  # MEDIUM risk
            else:
                y[i, 0] = 1  # LOW risk
        
        model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2, verbose=0)
    
    def _train_driver_state_model(self, model):
        """Train driver state model with synthetic data"""
        n_samples = 3000
        
        # Features: eye_closure_rate, head_pose, steering_variance, etc.
        X = np.random.rand(n_samples, 6)
        
        # Alertness score (0 = drowsy, 1 = alert)
        y = np.random.rand(n_samples)
        
        # Simulate drowsiness based on features
        for i in range(n_samples):
            eye_closure = X[i, 0]
            head_nod = X[i, 1]
            
            if eye_closure > 0.7 or head_nod > 0.8:
                y[i] = np.random.uniform(0, 0.3)  # Drowsy
            else:
                y[i] = np.random.uniform(0.7, 1.0)  # Alert
        
        model.fit(X, y, epochs=30, batch_size=32, validation_split=0.2, verbose=0)
    
    def _initialize_demo_models(self):
        """Initialize simplified models for demo purposes"""
        self.collision_model = self._create_collision_model()
        self.driver_state_model = self._create_driver_state_model()
        self.is_initialized = True
    
    def analyze_frame(self, frame, vehicle_data=None):
        """Analyze video frame for potential hazards"""
        if not self.is_initialized:
            self.initialize_models()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'collision_risk': 'LOW',
            'driver_alertness': 0.85,
            'detected_objects': [],
            'hazards': [],
            'recommendations': []
        }
        
        try:
            if self.yolo_model and frame is not None:
                # Object detection
                detections = self.yolo_model(frame, verbose=False)
                
                for detection in detections:
                    boxes = detection.boxes
                    if boxes is not None:
                        for box in boxes:
                            class_id = int(box.cls[0])
                            confidence = float(box.conf[0])
                            
                            if confidence > 0.5:
                                class_name = self.yolo_model.names[class_id]
                                results['detected_objects'].append({
                                    'class': class_name,
                                    'confidence': confidence,
                                    'bbox': box.xyxy[0].tolist()
                                })
            
            # Predict collision risk
            if vehicle_data:
                collision_features = self._extract_collision_features(vehicle_data, results['detected_objects'])
                risk_probs = self.collision_model.predict(collision_features.reshape(1, -1), verbose=0)[0]
                risk_level = ['LOW', 'MEDIUM', 'HIGH'][np.argmax(risk_probs)]
                results['collision_risk'] = risk_level
                results['risk_probability'] = float(np.max(risk_probs))
            
            # Analyze driver state (simplified for demo)
            driver_features = self._extract_driver_features(frame)
            if driver_features is not None:
                alertness = self.driver_state_model.predict(driver_features.reshape(1, -1), verbose=0)[0][0]
                results['driver_alertness'] = float(alertness)
            
            # Generate hazard alerts and recommendations
            results['hazards'] = self._identify_hazards(results)
            results['recommendations'] = self._generate_safety_recommendations(results)
            
        except Exception as e:
            print(f"Error in frame analysis: {e}")
        
        return results
    
    def _extract_collision_features(self, vehicle_data, detected_objects):
        """Extract features for collision prediction"""
        features = np.zeros(10)
        
        if vehicle_data:
            features[0] = vehicle_data.get('speed', 50) / 120.0  # Normalized speed
            features[1] = vehicle_data.get('acceleration', 0) / 10.0
            features[2] = 1.0 if vehicle_data.get('weather') == 'RAIN' else 0.0
            features[3] = 1.0 if vehicle_data.get('road_condition') == 'POOR' else 0.0
        
        # Object-based features
        features[4] = len([obj for obj in detected_objects if obj['class'] in ['car', 'truck', 'bus']]) / 10.0
        features[5] = len([obj for obj in detected_objects if obj['class'] == 'person']) / 5.0
        features[6] = np.random.uniform(0.1, 1.0)  # Simulated distance to nearest object
        features[7] = np.random.uniform(-0.5, 0.5)  # Simulated relative speed
        features[8] = np.random.uniform(0, 1)  # Time of day factor
        features[9] = np.random.uniform(0, 1)  # Traffic density
        
        return features
    
    def _extract_driver_features(self, frame):
        """Extract driver state features (simplified)"""
        if frame is None:
            return None
        
        # Simplified feature extraction for demo
        features = np.random.rand(6)  # In real implementation, use face detection and analysis
        return features
    
    def _identify_hazards(self, analysis_results):
        """Identify potential hazards from analysis"""
        hazards = []
        
        if analysis_results['collision_risk'] == 'HIGH':
            hazards.append({
                'type': 'COLLISION_RISK',
                'severity': 'HIGH',
                'description': 'High collision risk detected',
                'time_to_impact': '3-5 seconds'
            })
        
        if analysis_results['driver_alertness'] < 0.5:
            hazards.append({
                'type': 'DRIVER_DROWSINESS',
                'severity': 'MEDIUM',
                'description': 'Driver drowsiness detected',
                'recommendation': 'Take a break'
            })
        
        # Check for specific object hazards
        for obj in analysis_results['detected_objects']:
            if obj['class'] == 'person' and obj['confidence'] > 0.8:
                hazards.append({
                    'type': 'PEDESTRIAN_DETECTED',
                    'severity': 'MEDIUM',
                    'description': 'Pedestrian in vicinity'
                })
        
        return hazards
    
    def _generate_safety_recommendations(self, analysis_results):
        """Generate safety recommendations"""
        recommendations = []
        
        if analysis_results['collision_risk'] == 'HIGH':
            recommendations.extend([
                'Reduce speed immediately',
                'Increase following distance',
                'Prepare for emergency braking'
            ])
        
        if analysis_results['driver_alertness'] < 0.6:
            recommendations.extend([
                'Pull over safely when possible',
                'Take a 15-minute break',
                'Consider switching drivers'
            ])
        
        if any(h['type'] == 'PEDESTRIAN_DETECTED' for h in analysis_results['hazards']):
            recommendations.append('Exercise extra caution - pedestrians nearby')
        
        return recommendations
    
    def process_video_stream(self, video_source=0):
        """Process live video stream for real-time analysis"""
        cap = cv2.VideoCapture(video_source)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Analyze frame
            results = self.analyze_frame(frame)
            
            # Display results on frame
            self._draw_results_on_frame(frame, results)
            
            cv2.imshow('AETHER - Accident Prevention', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def _draw_results_on_frame(self, frame, results):
        """Draw analysis results on video frame"""
        height, width = frame.shape[:2]
        
        # Draw collision risk indicator
        risk_color = (0, 255, 0) if results['collision_risk'] == 'LOW' else \
                    (0, 255, 255) if results['collision_risk'] == 'MEDIUM' else (0, 0, 255)
        
        cv2.rectangle(frame, (10, 10), (300, 60), risk_color, -1)
        cv2.putText(frame, f"Risk: {results['collision_risk']}", (20, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Draw alertness indicator
        alertness_color = (0, 255, 0) if results['driver_alertness'] > 0.7 else \
                         (0, 255, 255) if results['driver_alertness'] > 0.5 else (0, 0, 255)
        
        cv2.rectangle(frame, (10, 70), (300, 120), alertness_color, -1)
        cv2.putText(frame, f"Alertness: {results['driver_alertness']:.2f}", (20, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Example usage
if __name__ == "__main__":
    predictor = AccidentPredictionSystem()
    
    # Test with dummy data
    test_vehicle_data = {
        'speed': 75,
        'acceleration': 2.5,
        'weather': 'CLEAR',
        'road_condition': 'GOOD'
    }
    
    # Create dummy frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    result = predictor.analyze_frame(dummy_frame, test_vehicle_data)
    print(json.dumps(result, indent=2))