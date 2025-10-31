import React, { useState, useEffect } from 'react';

function RealSystemDashboard() {
  const [vehicleData, setVehicleData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [systemAnalysis, setSystemAnalysis] = useState(null);

  useEffect(() => {
    // WebSocket connection for real-time data
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setConnected(true);
      console.log('Connected to AETHER Real System Backend');
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

    // Get system analysis
    fetch('http://localhost:8000/api/system-analysis')
      .then(res => res.json())
      .then(data => setSystemAnalysis(data))
      .catch(err => console.error('Analysis error:', err));

    return () => ws.close();
  }, []);

  const triggerStressTest = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/stress-test');
      const result = await response.json();
      alert(`🏎️ ${result.message}`);
    } catch (error) {
      console.error('Stress test error:', error);
    }
  };

  if (!vehicleData) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', color: 'white' }}>
        <h1>🚗 AETHER Real System Monitor</h1>
        <p>Status: {connected ? '🟢 Connected to your laptop' : '🔴 Connecting to system...'}</p>
        <p>Converting your laptop into a vehicle simulator...</p>
      </div>
    );
  }

  const systemInfo = vehicleData.system_info;
  const isOverheating = vehicleData.health.engine_temp > 70;
  const isHighLoad = systemInfo.real_cpu_usage > 70;

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', color: 'white' }}>
      
      {/* Header */}
      <header style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '2.5em' }}>🚗 AETHER Real System Vehicle</h1>
        <p style={{ margin: '10px 0', fontSize: '1.2em' }}>
          Vehicle: {vehicleData.vehicle_id} • Status: {connected ? '🟢 LIVE MONITORING' : '🔴 OFFLINE'}
        </p>
        <p style={{ margin: '5px 0', opacity: 0.8 }}>
          System: {systemInfo.system_name} • Processor: {systemInfo.processor}
        </p>
      </header>

      {/* Real System Mapping */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🔄 Real System → Vehicle Mapping</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '2em' }}>🌡️</div>
            <div>CPU Temp → Engine Heat</div>
            <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{vehicleData.health.engine_temp.toFixed(1)}°C</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '2em' }}>🔋</div>
            <div>Battery → Vehicle Power</div>
            <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{vehicleData.health.battery_level.toFixed(1)}%</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '2em' }}>⚡</div>
            <div>CPU Load → Vehicle Speed</div>
            <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{vehicleData.navigation.current_speed.toFixed(1)} km/h</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '2em' }}>💾</div>
            <div>Memory → System Health</div>
            <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{systemInfo.real_memory_usage.toFixed(1)}%</div>
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        
        {/* Engine Health (CPU) */}
        <div style={{ 
          backgroundColor: isOverheating ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `2px solid ${isOverheating ? '#EF4444' : '#10B981'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: isOverheating ? '#FEE2E2' : '#D1FAE5' }}>
            🌡️ Engine Temperature (CPU)
          </h3>
          <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: isOverheating ? '#FCA5A5' : '#6EE7B7' }}>
            {vehicleData.health.engine_temp.toFixed(1)}°C
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Real CPU Usage: {systemInfo.real_cpu_usage.toFixed(1)}%
          </p>
          {isOverheating && (
            <div style={{ marginTop: '10px', padding: '10px', backgroundColor: 'rgba(239, 68, 68, 0.3)', borderRadius: '8px' }}>
              ⚠️ OVERHEATING DETECTED - Reduce system load!
            </div>
          )}
        </div>

        {/* Vehicle Speed (CPU Load) */}
        <div style={{ 
          backgroundColor: isHighLoad ? 'rgba(245, 158, 11, 0.2)' : 'rgba(59, 130, 246, 0.2)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `2px solid ${isHighLoad ? '#F59E0B' : '#3B82F6'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: isHighLoad ? '#FEF3C7' : '#DBEAFE' }}>
            🚗 Vehicle Speed (CPU Load)
          </h3>
          <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: isHighLoad ? '#FBBF24' : '#60A5FA' }}>
            {vehicleData.navigation.current_speed.toFixed(1)} km/h
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            System Load: {isHighLoad ? 'HIGH' : 'NORMAL'}
          </p>
        </div>

        {/* Battery Status */}
        <div style={{ 
          backgroundColor: 'rgba(168, 85, 247, 0.2)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: '2px solid #A855F7',
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E9D5FF' }}>🔋 Power Level</h3>
          <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#C084FC' }}>
            {vehicleData.health.battery_level.toFixed(1)}%
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Real Battery: {systemInfo.real_battery ? `${systemInfo.real_battery.toFixed(1)}%` : 'AC Power'}
          </p>
        </div>

        {/* System Health */}
        <div style={{ 
          backgroundColor: 'rgba(34, 197, 94, 0.2)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: '2px solid #22C55E',
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#DCFCE7' }}>💚 Overall Health</h3>
          <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#4ADE80' }}>
            {vehicleData.health.overall_score.toFixed(1)}%
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Memory: {systemInfo.real_memory_usage.toFixed(1)}% • Disk: {systemInfo.real_disk_usage.toFixed(1)}%
          </p>
        </div>
      </div>

      {/* Control Panel */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🎮 Vehicle Control Panel</h3>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', flexWrap: 'wrap' }}>
          <button 
            onClick={triggerStressTest}
            style={{ 
              padding: '12px 24px', 
              backgroundColor: '#EF4444', 
              color: 'white', 
              border: 'none', 
              borderRadius: '8px', 
              cursor: 'pointer',
              fontSize: '1em',
              fontWeight: 'bold'
            }}
          >
            🏎️ Simulate Highway Driving
          </button>
          <button 
            onClick={() => window.open('http://localhost:8000/api/system-analysis', '_blank')}
            style={{ 
              padding: '12px 24px', 
              backgroundColor: '#3B82F6', 
              color: 'white', 
              border: 'none', 
              borderRadius: '8px', 
              cursor: 'pointer',
              fontSize: '1em',
              fontWeight: 'bold'
            }}
          >
            📊 System Analysis
          </button>
        </div>
      </div>

      {/* Real-time Alerts */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🚨 Real-time System Alerts</h3>
        
        {isOverheating && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(239, 68, 68, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #EF4444' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>🔥 ENGINE OVERHEATING</div>
            <div>CPU temperature is {vehicleData.health.engine_temp.toFixed(1)}°C - Close applications to cool down</div>
          </div>
        )}

        {isHighLoad && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(245, 158, 11, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #F59E0B' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>⚡ HIGH SYSTEM LOAD</div>
            <div>CPU usage is {systemInfo.real_cpu_usage.toFixed(1)}% - Vehicle speed: {vehicleData.navigation.current_speed.toFixed(1)} km/h</div>
          </div>
        )}

        {systemInfo.real_memory_usage > 80 && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(239, 68, 68, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #EF4444' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>💾 MEMORY CRITICAL</div>
            <div>Memory usage is {systemInfo.real_memory_usage.toFixed(1)}% - System performance degraded</div>
          </div>
        )}

        {!isOverheating && !isHighLoad && systemInfo.real_memory_usage < 70 && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(16, 185, 129, 0.3)', borderRadius: '8px', border: '2px solid #10B981' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>✅ ALL SYSTEMS OPTIMAL</div>
            <div>Vehicle running smoothly - All parameters within normal range</div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', opacity: 0.8 }}>
        <p>🚗 AETHER Real System Vehicle Simulator</p>
        <p>Uptime: {systemInfo.uptime_hours.toFixed(1)} hours • Last Update: {new Date().toLocaleTimeString()}</p>
      </footer>
    </div>
  );
}

export default RealSystemDashboard;