import React, { useState, useEffect } from 'react';

function AutoStartDashboard() {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [monitoringMode, setMonitoringMode] = useState(null);
  const [backendStarted, setBackendStarted] = useState(false);

  useEffect(() => {
    // Try to start backend automatically
    startBackendIfNeeded();
    
    // Try to connect with retries
    const connectWithRetry = () => {
      connectToBackend();
      // Retry every 3 seconds if not connected
      if (!connected) {
        setTimeout(connectWithRetry, 3000);
      }
    };
    
    connectWithRetry();
  }, []);

  const startBackendIfNeeded = async () => {
    try {
      // Check if backend is already running
      const response = await fetch('http://localhost:8003/api/monitoring-mode');
      if (response.ok) {
        setBackendStarted(true);
        return;
      }
    } catch (error) {
      // Backend not running, try to start it
      console.log('Backend not running, attempting to start...');
      
      try {
        // Try to trigger backend startup
        await fetch('http://localhost:8003/api/start-frontend', { method: 'POST' });
        setBackendStarted(true);
      } catch (startError) {
        console.log('Could not auto-start backend, manual start required');
      }
    }
  };

  const connectToBackend = async () => {
    try {
      // Get monitoring mode
      const modeResponse = await fetch('http://localhost:8003/api/monitoring-mode');
      if (modeResponse.ok) {
        const modeData = await modeResponse.json();
        setMonitoringMode(modeData);
        setBackendStarted(true);
      }

      // Connect WebSocket
      const ws = new WebSocket('ws://localhost:8003/ws');
      
      ws.onopen = () => {
        setConnected(true);
        console.log('Connected to AETHER Auto-Start Backend');
      };

      ws.onmessage = (event) => {
        try {
          const receivedData = JSON.parse(event.data);
          setData(receivedData);
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
      console.error('Connection error:', error);
    }
  };

  const getMonitoringIcon = () => {
    if (!monitoringMode) return '🔍';
    
    if (monitoringMode.mode === 'vehicle') {
      const vehicleName = monitoringMode.target.toLowerCase();
      if (vehicleName.includes('truck')) return '🚛';
      if (vehicleName.includes('bus')) return '🚌';
      if (vehicleName.includes('motorcycle')) return '🏍️';
      return '🚗';
    } else {
      const deviceType = monitoringMode.target;
      if (deviceType === 'laptop') return '💻';
      if (deviceType === 'desktop') return '🖥️';
      if (deviceType === 'tablet') return '📱';
      if (deviceType === 'raspberry_pi') return '🤖';
      return '📟';
    }
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

  // Loading state
  if (!backendStarted || !connected || !data || !monitoringMode) {
    return (
      <div style={{ 
        padding: '20px', 
        fontFamily: 'Arial, sans-serif', 
        background: 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)', 
        minHeight: '100vh', 
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center', maxWidth: '600px' }}>
          <h1 style={{ fontSize: '3em', margin: '20px 0' }}>🚀 AETHER</h1>
          <h2>Auto-Start Universal Monitor</h2>
          
          <div style={{ margin: '30px 0', padding: '20px', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '15px' }}>
            <div style={{ fontSize: '2em', margin: '10px 0' }}>🔍</div>
            <p>Auto-detecting monitoring target...</p>
            <p style={{ fontSize: '0.9em', opacity: 0.8 }}>
              {!backendStarted ? '⏳ Starting backend server...' :
               !connected ? '📡 Connecting to backend...' :
               !monitoringMode ? '🔍 Detecting vehicle or device...' :
               '📊 Loading dashboard...'}
            </p>
          </div>

          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', textAlign: 'left' }}>
            <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🎯 Detection Process</h3>
            <p>✅ Checking for real vehicles (OBD-II, CAN bus, Bluetooth)</p>
            <p>✅ Scanning for automotive interfaces</p>
            <p>✅ Fallback to device monitoring if no vehicle found</p>
            <p>✅ Auto-configuring thresholds and analogies</p>
          </div>

          <p style={{ marginTop: '30px', fontSize: '0.9em', opacity: 0.7 }}>
            Backend will start automatically • No manual commands needed
          </p>
        </div>
      </div>
    );
  }

  // Determine if we're monitoring a vehicle or device
  const isVehicleMode = monitoringMode.mode === 'vehicle';
  const targetName = monitoringMode.target;

  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif', 
      background: isVehicleMode 
        ? 'linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)' 
        : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
      minHeight: '100vh', 
      color: 'white' 
    }}>
      
      {/* Header */}
      <header style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '2.5em' }}>
          🚀 AETHER Auto-Monitor
        </h1>
        <div style={{ fontSize: '4em', margin: '10px 0' }}>
          {getMonitoringIcon()}
        </div>
        <h2 style={{ margin: '10px 0', fontSize: '1.5em' }}>
          {isVehicleMode ? `🚗 ${targetName}` : `📱 ${targetName.replace('_', ' ').toUpperCase()}`}
        </h2>
        <p style={{ margin: '5px 0', opacity: 0.8 }}>
          Mode: {monitoringMode.mode.toUpperCase()} • Status: {connected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </p>
      </header>

      {/* Vehicle Mode Display */}
      {isVehicleMode && data.engine && (
        <>
          {/* Vehicle Status Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            
            {/* Engine RPM */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.engine.rpm > 4000 ? '#F59E0B' : '#10B981'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🔧 Engine RPM</h3>
              <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: data.engine.rpm > 4000 ? '#FBBF24' : '#6EE7B7' }}>
                {Math.round(data.engine.rpm)}
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Engine Load: {data.engine.load?.toFixed(1) || 0}%
              </p>
            </div>

            {/* Vehicle Speed */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: '3px solid #3B82F6',
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🚗 Speed</h3>
              <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#60A5FA' }}>
                {Math.round(data.performance?.speed || 0)} km/h
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Throttle: {data.performance?.throttle_position?.toFixed(1) || 0}%
              </p>
            </div>

            {/* Engine Temperature */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.engine.temperature > 105 ? '#EF4444' : '#10B981'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🌡️ Engine Temperature</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: data.engine.temperature > 105 ? '#FCA5A5' : '#6EE7B7'
              }}>
                {Math.round(data.engine.temperature)}°C
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Oil Pressure: {data.engine.oil_pressure?.toFixed(1) || 0} PSI
              </p>
            </div>

            {/* Fuel Level */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.performance?.fuel_level < 20 ? '#EF4444' : '#8B5CF6'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>⛽ Fuel Level</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: data.performance?.fuel_level < 20 ? '#FCA5A5' : '#C084FC'
              }}>
                {Math.round(data.performance?.fuel_level || 0)}%
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Battery: {data.electrical?.battery_voltage?.toFixed(1) || 12.6}V
              </p>
            </div>
          </div>
        </>
      )}

      {/* Device Mode Display */}
      {!isVehicleMode && data.raw_metrics && (
        <>
          {/* Device Status Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            
            {/* System Temperature */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.raw_metrics.temperature > 70 ? '#EF4444' : '#10B981'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🌡️ System Temperature</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: data.raw_metrics.temperature > 70 ? '#FCA5A5' : '#6EE7B7'
              }}>
                {data.raw_metrics.temperature.toFixed(1)}°C
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                CPU Usage: {data.raw_metrics.cpu_usage.toFixed(1)}%
              </p>
            </div>

            {/* Performance Load */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.raw_metrics.cpu_usage > 70 ? '#F59E0B' : '#3B82F6'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>⚡ Performance Load</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: data.raw_metrics.cpu_usage > 70 ? '#FBBF24' : '#60A5FA'
              }}>
                {data.raw_metrics.cpu_usage.toFixed(1)}%
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Vehicle Speed: {data.vehicle_analogy?.speed?.toFixed(1) || 0} km/h
              </p>
            </div>

            {/* Memory Usage */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${data.raw_metrics.memory_usage > 80 ? '#EF4444' : '#8B5CF6'}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>💾 Memory Usage</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: data.raw_metrics.memory_usage > 80 ? '#FCA5A5' : '#C084FC'
              }}>
                {data.raw_metrics.memory_usage.toFixed(1)}%
              </div>
              <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
                Disk Usage: {data.raw_metrics.disk_usage.toFixed(1)}%
              </p>
            </div>

            {/* Overall Health */}
            <div style={{ 
              backgroundColor: 'rgba(255,255,255,0.1)', 
              padding: '20px', 
              borderRadius: '15px', 
              border: `3px solid ${getStatusColor(data.health_analysis?.status)}`,
              backdropFilter: 'blur(10px)'
            }}>
              <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>💚 Overall Health</h3>
              <div style={{ 
                fontSize: '2.5em', 
                fontWeight: 'bold', 
                color: getStatusColor(data.health_analysis?.status)
              }}>
                {data.health_analysis?.overall_score?.toFixed(1) || 0}%
              </div>
              <div style={{ 
                fontSize: '1.2em', 
                fontWeight: 'bold', 
                color: getStatusColor(data.health_analysis?.status),
                marginTop: '10px'
              }}>
                {data.health_analysis?.status || 'UNKNOWN'}
              </div>
            </div>
          </div>
        </>
      )}

      {/* Health Alerts */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🚨 Health Status</h3>
        
        {data.health_analysis?.critical_alerts?.length > 0 && data.health_analysis.critical_alerts.map((alert, index) => (
          <div key={index} style={{ padding: '15px', backgroundColor: 'rgba(239, 68, 68, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #EF4444' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>🚨 CRITICAL: {alert}</div>
          </div>
        ))}

        {data.health_analysis?.issues?.length > 0 && data.health_analysis.issues.map((issue, index) => (
          <div key={index} style={{ padding: '15px', backgroundColor: 'rgba(245, 158, 11, 0.3)', borderRadius: '8px', marginBottom: '10px', border: '2px solid #F59E0B' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>⚠️ WARNING: {issue}</div>
          </div>
        ))}

        {(!data.health_analysis?.critical_alerts?.length && !data.health_analysis?.issues?.length) && (
          <div style={{ padding: '15px', backgroundColor: 'rgba(16, 185, 129, 0.3)', borderRadius: '8px', border: '2px solid #10B981' }}>
            <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>✅ ALL SYSTEMS OPTIMAL</div>
            <div>{isVehicleMode ? 'Vehicle' : 'Device'} running perfectly!</div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', opacity: 0.8 }}>
        <p>🚀 AETHER Auto-Start Universal Monitor</p>
        <p>Target: {targetName} • Mode: {monitoringMode.mode.toUpperCase()} • Last Update: {new Date().toLocaleTimeString()}</p>
      </footer>
    </div>
  );
}

export default AutoStartDashboard;