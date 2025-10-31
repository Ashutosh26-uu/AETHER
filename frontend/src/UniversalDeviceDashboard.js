import React, { useState, useEffect } from 'react';

function UniversalDeviceDashboard() {
  const [deviceData, setDeviceData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [deviceInfo, setDeviceInfo] = useState(null);

  useEffect(() => {
    // Get device info first
    fetch('http://localhost:8000/api/device-info')
      .then(res => res.json())
      .then(data => setDeviceInfo(data))
      .catch(err => console.error('Device info error:', err));

    // WebSocket connection
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setConnected(true);
      console.log('Connected to Universal Device Monitor');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setDeviceData(data);
      } catch (e) {
        console.error('Error parsing data:', e);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      console.log('Disconnected from device monitor');
    };

    return () => ws.close();
  }, []);

  const triggerDeviceStressTest = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/device-stress-test', {
        method: 'POST'
      });
      const result = await response.json();
      alert(`⚡ ${result.message}\n⚠️ ${result.warning}`);
    } catch (error) {
      console.error('Stress test error:', error);
    }
  };

  const getDeviceIcon = (deviceType) => {
    const icons = {
      'laptop': '💻',
      'desktop': '🖥️',
      'tablet': '📱',
      'raspberry_pi': '🤖',
      'android_device': '📱',
      'macbook': '💻',
      'imac': '🖥️',
      'embedded_device': '⚙️',
      'linux_computer': '🐧'
    };
    return icons[deviceType] || '📟';
  };

  const getVehicleIcon = (vehicleType) => {
    const icons = {
      'Car': '🚗',
      'Truck': '🚛',
      'Motorcycle': '🏍️',
      'Drone': '🚁',
      'Electric Scooter': '🛴'
    };
    return icons[vehicleType] || '🚗';
  };

  const getStatusColor = (status) => {
    const colors = {
      'EXCELLENT': '#10B981',
      'GOOD': '#3B82F6',
      'WARNING': '#F59E0B',
      'CRITICAL': '#EF4444'
    };
    return colors[status] || '#6B7280';
  };

  if (!deviceData || !deviceInfo) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', color: 'white' }}>
        <h1>🌐 AETHER Universal Device Monitor</h1>
        <p>Status: {connected ? '🟢 Connected' : '🔴 Connecting...'}</p>
        <p>Detecting device type and initializing health monitoring...</p>
      </div>
    );
  }

  const device = deviceData.device_info;
  const health = deviceData.health_analysis;
  const metrics = deviceData.raw_metrics;
  const vehicle = deviceData.vehicle_analogy;

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', color: 'white' }}>
      
      {/* Header */}
      <header style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '2.5em' }}>
          🌐 AETHER Universal Device Monitor
        </h1>
        <div style={{ fontSize: '3em', margin: '10px 0' }}>
          {getDeviceIcon(device.type)} ➜ {getVehicleIcon(vehicle.vehicle_type)}
        </div>
        <p style={{ margin: '10px 0', fontSize: '1.2em' }}>
          {device.type.replace('_', ' ').toUpperCase()} → {vehicle.vehicle_type.toUpperCase()}
        </p>
        <p style={{ margin: '5px 0', opacity: 0.8 }}>
          System: {device.system.toUpperCase()} • Status: {connected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </p>
      </header>

      {/* Device Information */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>📱 Device Information</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🏷️</div>
            <div style={{ fontWeight: 'bold' }}>Device Type</div>
            <div>{device.type.replace('_', ' ').toUpperCase()}</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🖥️</div>
            <div style={{ fontWeight: 'bold' }}>System</div>
            <div>{device.system.toUpperCase()}</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🚗</div>
            <div style={{ fontWeight: 'bold' }}>Vehicle Analogy</div>
            <div>{vehicle.vehicle_type}</div>
          </div>
          <div style={{ textAlign: 'center', padding: '10px' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🆔</div>
            <div style={{ fontWeight: 'bold' }}>Device ID</div>
            <div>{device.device_id}</div>
          </div>
        </div>
      </div>

      {/* Health Status Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        
        {/* Overall Health */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${getStatusColor(health.status)}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>
            💚 Overall Health
          </h3>
          <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: getStatusColor(health.status) }}>
            {health.overall_score.toFixed(1)}%
          </div>
          <div style={{ 
            fontSize: '1.2em', 
            fontWeight: 'bold', 
            color: getStatusColor(health.status),
            marginTop: '10px'
          }}>
            {health.status}
          </div>
        </div>

        {/* Temperature */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${metrics.temperature > deviceInfo.device_config.temp_warning ? '#EF4444' : '#10B981'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>
            🌡️ {device.type === 'raspberry_pi' ? 'CPU Temperature' : 'System Temperature'}
          </h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.temperature > deviceInfo.device_config.temp_warning ? '#FCA5A5' : '#6EE7B7'
          }}>
            {metrics.temperature.toFixed(1)}°C
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Normal: &lt;{deviceInfo.device_config.temp_normal}°C • Warning: &gt;{deviceInfo.device_config.temp_warning}°C
          </p>
        </div>

        {/* Performance */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${metrics.cpu_usage > deviceInfo.device_config.cpu_warning ? '#F59E0B' : '#3B82F6'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>
            ⚡ Performance Load
          </h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.cpu_usage > deviceInfo.device_config.cpu_warning ? '#FBBF24' : '#60A5FA'
          }}>
            {metrics.cpu_usage.toFixed(1)}%
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Vehicle Speed: {vehicle.speed.toFixed(1)} km/h
          </p>
        </div>

        {/* Memory */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${metrics.memory_usage > deviceInfo.device_config.memory_warning ? '#EF4444' : '#8B5CF6'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>
            💾 Memory Usage
          </h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.memory_usage > deviceInfo.device_config.memory_warning ? '#FCA5A5' : '#C084FC'
          }}>
            {metrics.memory_usage.toFixed(1)}%
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            {device.type === 'raspberry_pi' ? 'System Memory' : 'RAM Usage'}
          </p>
        </div>
      </div>

      {/* Battery (if available) */}
      {metrics.battery.percent !== null && (
        <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
          <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🔋 Battery Status</h3>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: metrics.battery.percent < 20 ? '#EF4444' : '#10B981' }}>
              {metrics.battery.percent.toFixed(1)}%
            </div>
            <p style={{ margin: '10px 0', opacity: 0.8 }}>
              {metrics.battery.plugged ? '🔌 Plugged In' : '🔋 On Battery'}
              {metrics.battery.time_left && ` • ${Math.floor(metrics.battery.time_left / 3600)}h ${Math.floor((metrics.battery.time_left % 3600) / 60)}m remaining`}
            </p>
          </div>
        </div>
      )}

      {/* Vehicle Analogy Details */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🚗 Vehicle System Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          {Object.entries(vehicle).filter(([key]) => !['vehicle_type', 'vehicle_id', 'engine_temp', 'speed', 'fuel_level', 'health_score', 'status'].includes(key)).map(([key, value]) => (
            <div key={key} style={{ textAlign: 'center', padding: '10px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </div>
              <div style={{ opacity: 0.8 }}>{value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Control Panel */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🎮 Device Control Panel</h3>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '15px', flexWrap: 'wrap' }}>
          <button 
            onClick={triggerDeviceStressTest}
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
            ⚡ Device Stress Test
          </button>
          <button 
            onClick={() => window.open('http://localhost:8000/api/health-analysis', '_blank')}
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
            📊 Health Analysis
          </button>
        </div>
      </div>

      {/* Health Alerts */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🚨 Health Alerts & Recommendations</h3>
        
        {health.critical_alerts.length > 0 && health.critical_alerts.map((alert, index) => (
          <div key={index} style={{ padding: '15px', backgroundColor: 'rgba(239, 68, 68, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #EF4444' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>🚨 CRITICAL: {alert}</div>
          </div>
        ))}

        {health.issues.length > 0 && health.issues.map((issue, index) => (
          <div key={index} style={{ padding: '15px', backgroundColor: 'rgba(245, 158, 11, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #F59E0B' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>⚠️ WARNING: {issue}</div>
          </div>
        ))}

        {health.recommendations.length > 0 && (
          <div style={{ marginTop: '15px' }}>
            <h4 style={{ margin: '0 0 10px 0' }}>💡 Recommendations:</h4>
            {health.recommendations.map((rec, index) => (
              <div key={index} style={{ padding: '10px', backgroundColor: 'rgba(59, 130, 246, 0.3)', borderRadius: '8px', marginBottom: '5px', border: '1px solid #3B82F6' }}>
                • {rec}
              </div>
            ))}
          </div>
        )}

        {health.critical_alerts.length === 0 && health.issues.length === 0 && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(16, 185, 129, 0.3)', borderRadius: '8px', border: '2px solid #10B981' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>✅ ALL SYSTEMS OPTIMAL</div>
            <div>Your {device.type.replace('_', ' ')} is running perfectly!</div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', opacity: 0.8 }}>
        <p>🌐 AETHER Universal Device Health Monitor</p>
        <p>Device: {device.hostname} • Last Update: {new Date().toLocaleTimeString()}</p>
      </footer>
    </div>
  );
}

export default UniversalDeviceDashboard;