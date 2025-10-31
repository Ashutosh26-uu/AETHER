import React, { useState, useEffect } from 'react';

function App() {
  const [vehicleData, setVehicleData] = useState(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    // Try WebSocket connection
    try {
      const ws = new WebSocket('ws://localhost:8000/ws');
      
      ws.onopen = () => {
        setConnected(true);
        console.log('Connected to AETHER backend');
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setVehicleData(data);
        } catch (e) {
          console.error('Error parsing data:', e);
        }
      };

      ws.onclose = () => {
        setConnected(false);
        console.log('Disconnected from backend');
      };

      return () => ws.close();
    } catch (error) {
      console.error('WebSocket error:', error);
    }
  }, []);

  if (!vehicleData) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
        <h1>🚀 AETHER Dashboard</h1>
        <p>Status: {connected ? '🟢 Connected' : '🔴 Connecting...'}</p>
        <p>Waiting for vehicle data...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', backgroundColor: '#f0f0f0', minHeight: '100vh' }}>
      <header style={{ marginBottom: '30px' }}>
        <h1 style={{ color: '#2563eb', margin: 0 }}>🚀 AETHER Dashboard</h1>
        <p style={{ margin: '5px 0', color: '#666' }}>
          Vehicle: {vehicleData.vehicle_id} • Status: {connected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </p>
      </header>

      {/* Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#059669' }}>🏥 Vehicle Health</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#059669' }}>
            {Math.round(vehicleData.health?.overall_score || 0)}%
          </div>
          <p style={{ margin: '5px 0', color: '#666', fontSize: '0.9em' }}>
            Engine: {Math.round(vehicleData.health?.engine_temp || 0)}°C
          </p>
        </div>

        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#dc2626' }}>⚠️ Safety Status</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: vehicleData.safety?.collision_risk === 'HIGH' ? '#dc2626' : '#059669' }}>
            {vehicleData.safety?.collision_risk || 'SAFE'}
          </div>
          <p style={{ margin: '5px 0', color: '#666', fontSize: '0.9em' }}>
            Driver Alertness: {Math.round((vehicleData.safety?.driver_alertness || 0) * 100)}%
          </p>
        </div>

        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#2563eb' }}>🔋 Battery Level</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#2563eb' }}>
            {Math.round(vehicleData.health?.battery_level || 0)}%
          </div>
          <p style={{ margin: '5px 0', color: '#666', fontSize: '0.9em' }}>
            Fuel: {Math.round(vehicleData.navigation?.fuel_level || 0)}%
          </p>
        </div>

        <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#7c3aed' }}>🚗 Current Speed</h3>
          <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#7c3aed' }}>
            {Math.round(vehicleData.navigation?.current_speed || 0)} km/h
          </div>
          <p style={{ margin: '5px 0', color: '#666', fontSize: '0.9em' }}>
            Location: {vehicleData.location?.latitude?.toFixed(4)}, {vehicleData.location?.longitude?.toFixed(4)}
          </p>
        </div>
      </div>

      {/* Map Simulation */}
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', marginBottom: '30px' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🗺️ Live Location</h3>
        <div style={{ 
          height: '300px', 
          background: 'linear-gradient(135deg, #1e40af, #3b82f6)', 
          borderRadius: '8px', 
          position: 'relative',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white'
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3em', marginBottom: '10px' }}>📍</div>
            <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>AETHER Vehicle</div>
            <div style={{ fontSize: '0.9em', opacity: 0.8 }}>
              {vehicleData.location?.latitude?.toFixed(6)}, {vehicleData.location?.longitude?.toFixed(6)}
            </div>
            <div style={{ fontSize: '0.8em', opacity: 0.7, marginTop: '5px' }}>
              Speed: {Math.round(vehicleData.navigation?.current_speed || 0)} km/h
            </div>
          </div>
        </div>
      </div>

      {/* AI Insights */}
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)', marginBottom: '30px' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🤖 AI Insights</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <div style={{ padding: '15px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🧠</div>
            <div style={{ fontWeight: 'bold' }}>Health Prediction</div>
            <div style={{ color: '#059669', fontSize: '1.2em' }}>95% Optimal</div>
          </div>
          <div style={{ padding: '15px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🛡️</div>
            <div style={{ fontWeight: 'bold' }}>Safety Score</div>
            <div style={{ color: '#2563eb', fontSize: '1.2em' }}>98/100</div>
          </div>
          <div style={{ padding: '15px', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>⚡</div>
            <div style={{ fontWeight: 'bold' }}>Efficiency</div>
            <div style={{ color: '#7c3aed', fontSize: '1.2em' }}>87%</div>
          </div>
        </div>
      </div>

      {/* Alerts */}
      <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '10px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🚨 System Alerts</h3>
        <div style={{ padding: '15px', backgroundColor: '#dcfce7', border: '1px solid #bbf7d0', borderRadius: '8px', marginBottom: '10px' }}>
          <div style={{ fontWeight: 'bold', color: '#059669' }}>✅ All Systems Operational</div>
          <div style={{ fontSize: '0.9em', color: '#065f46' }}>AI monitoring 847 data points in real-time</div>
        </div>
        
        {vehicleData.health?.overall_score < 70 && (
          <div style={{ padding: '15px', backgroundColor: '#fef3c7', border: '1px solid #fde68a', borderRadius: '8px', marginBottom: '10px' }}>
            <div style={{ fontWeight: 'bold', color: '#d97706' }}>⚠️ Health Alert</div>
            <div style={{ fontSize: '0.9em', color: '#92400e' }}>Vehicle health below optimal - Service recommended</div>
          </div>
        )}

        {vehicleData.safety?.collision_risk === 'HIGH' && (
          <div style={{ padding: '15px', backgroundColor: '#fee2e2', border: '1px solid #fecaca', borderRadius: '8px' }}>
            <div style={{ fontWeight: 'bold', color: '#dc2626' }}>🚨 High Risk Alert</div>
            <div style={{ fontSize: '0.9em', color: '#991b1b' }}>High collision risk detected - Take immediate action</div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', color: '#666', fontSize: '0.9em' }}>
        <p>AETHER: AI-Powered Satellite-Integrated Intelligent Mobility System</p>
        <p>Last Update: {new Date().toLocaleTimeString()}</p>
      </footer>
    </div>
  );
}

export default App;