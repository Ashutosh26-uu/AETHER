-- AETHER Database Schema
-- PostgreSQL with PostGIS for spatial data

-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Vehicles table
CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) UNIQUE NOT NULL,
    make VARCHAR(50),
    model VARCHAR(50),
    year INTEGER,
    vin VARCHAR(17),
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vehicle locations (with spatial data)
CREATE TABLE vehicle_locations (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    location GEOMETRY(POINT, 4326),
    altitude FLOAT,
    speed FLOAT,
    heading FLOAT,
    accuracy FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX USING GIST (location)
);

-- Vehicle health data
CREATE TABLE vehicle_health (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    engine_temp FLOAT,
    battery_level FLOAT,
    oil_pressure FLOAT,
    tire_pressure JSONB,
    brake_health FLOAT,
    overall_score FLOAT,
    health_status VARCHAR(20),
    recommendations JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Safety events
CREATE TABLE safety_events (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    event_type VARCHAR(50),
    severity VARCHAR(20),
    collision_risk VARCHAR(20),
    driver_alertness FLOAT,
    weather_conditions VARCHAR(50),
    road_conditions VARCHAR(50),
    location GEOMETRY(POINT, 4326),
    event_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Drone missions
CREATE TABLE drone_missions (
    id SERIAL PRIMARY KEY,
    mission_id VARCHAR(50) UNIQUE NOT NULL,
    drone_id VARCHAR(50),
    mission_type VARCHAR(50),
    status VARCHAR(20),
    start_location GEOMETRY(POINT, 4326),
    target_location GEOMETRY(POINT, 4326),
    mission_data JSONB,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Satellite data
CREATE TABLE satellite_data (
    id SERIAL PRIMARY KEY,
    satellite_system VARCHAR(20),
    data_type VARCHAR(50),
    location GEOMETRY(POINT, 4326),
    imagery_url VARCHAR(255),
    weather_data JSONB,
    traffic_data JSONB,
    analysis_results JSONB,
    capture_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Routes and navigation
CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    route_id VARCHAR(50) UNIQUE NOT NULL,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    start_location GEOMETRY(POINT, 4326),
    end_location GEOMETRY(POINT, 4326),
    waypoints JSONB,
    distance_km FLOAT,
    estimated_time INTEGER,
    fuel_consumption FLOAT,
    route_conditions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Emergency alerts
CREATE TABLE emergency_alerts (
    id SERIAL PRIMARY KEY,
    alert_id VARCHAR(50) UNIQUE NOT NULL,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    alert_type VARCHAR(50),
    severity VARCHAR(20),
    location GEOMETRY(POINT, 4326),
    description TEXT,
    response_data JSONB,
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

-- Fleet management
CREATE TABLE fleets (
    id SERIAL PRIMARY KEY,
    fleet_id VARCHAR(50) UNIQUE NOT NULL,
    fleet_name VARCHAR(100),
    organization VARCHAR(100),
    manager_contact JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fleet_vehicles (
    id SERIAL PRIMARY KEY,
    fleet_id VARCHAR(50) REFERENCES fleets(fleet_id),
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sensor data (IoT)
CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    sensor_type VARCHAR(50),
    sensor_data JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI model predictions
CREATE TABLE ai_predictions (
    id SERIAL PRIMARY KEY,
    vehicle_id VARCHAR(50) REFERENCES vehicles(vehicle_id),
    prediction_type VARCHAR(50),
    model_version VARCHAR(20),
    input_data JSONB,
    prediction_result JSONB,
    confidence_score FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blockchain transactions (for security)
CREATE TABLE blockchain_transactions (
    id SERIAL PRIMARY KEY,
    transaction_hash VARCHAR(66) UNIQUE NOT NULL,
    block_number BIGINT,
    transaction_type VARCHAR(50),
    data_hash VARCHAR(66),
    vehicle_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_vehicle_locations_timestamp ON vehicle_locations(timestamp);
CREATE INDEX idx_vehicle_health_timestamp ON vehicle_health(timestamp);
CREATE INDEX idx_safety_events_timestamp ON safety_events(timestamp);
CREATE INDEX idx_sensor_readings_timestamp ON sensor_readings(timestamp);
CREATE INDEX idx_vehicle_locations_vehicle_id ON vehicle_locations(vehicle_id);
CREATE INDEX idx_vehicle_health_vehicle_id ON vehicle_health(vehicle_id);

-- Views for common queries
CREATE VIEW vehicle_current_status AS
SELECT 
    v.vehicle_id,
    v.make,
    v.model,
    l.location,
    l.speed,
    l.timestamp as last_location_update,
    h.overall_score as health_score,
    h.health_status,
    h.timestamp as last_health_update
FROM vehicles v
LEFT JOIN LATERAL (
    SELECT * FROM vehicle_locations vl 
    WHERE vl.vehicle_id = v.vehicle_id 
    ORDER BY timestamp DESC LIMIT 1
) l ON true
LEFT JOIN LATERAL (
    SELECT * FROM vehicle_health vh 
    WHERE vh.vehicle_id = v.vehicle_id 
    ORDER BY timestamp DESC LIMIT 1
) h ON true;

-- Function to calculate distance between points
CREATE OR REPLACE FUNCTION calculate_distance(lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT)
RETURNS FLOAT AS $$
BEGIN
    RETURN ST_Distance(
        ST_GeogFromText('POINT(' || lon1 || ' ' || lat1 || ')'),
        ST_GeogFromText('POINT(' || lon2 || ' ' || lat2 || ')')
    ) / 1000; -- Return distance in kilometers
END;
$$ LANGUAGE plpgsql;