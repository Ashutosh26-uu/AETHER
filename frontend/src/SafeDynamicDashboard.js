import React, { useState, useEffect } from 'react';
import AutoBackendStarter from './AutoBackendStarter';

function SafeDynamicDashboard() {
  const [systemData, setSystemData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [backendReady, setBackendReady] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [animationClass, setAnimationClass] = useState('');

  useEffect(() => {
    if (!backendReady) return;
    
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setConnected(true);
      setAnimationClass('animate-fadeIn');
      console.log('Connected to AETHER System');
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setSystemData(data);
      } catch (e) {
        console.error('Error parsing system data:', e);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      console.log('Disconnected from AETHER system');
    };

    return () => ws.close();
  }, [backendReady]);

  const getStatusColor = (value, thresholds = { good: 70, warning: 40 }) => {
    if (value >= thresholds.good) return '#10B981';
    if (value >= thresholds.warning) return '#F59E0B';
    return '#EF4444';
  };

  const getProgressBarWidth = (value) => {
    return Math.min(Math.max(value, 0), 100);
  };

  const getRiskColor = (risk) => {
    const colors = {
      'LOW': '#10B981',
      'MEDIUM': '#F59E0B', 
      'HIGH': '#EF4444'
    };
    return colors[risk] || '#6B7280';
  };

  const tabs = [
    { id: 'overview', label: '🏠 Overview', icon: '🏠' },
    { id: 'vehicle', label: '🚗 Vehicle Health', icon: '🚗' },
    { id: 'ai', label: '🤖 AI Predictions', icon: '🤖' },
    { id: 'drone', label: '🚁 Drone System', icon: '🚁' },
    { id: 'navigation', label: '🗺️ Navigation', icon: '🗺️' },
    { id: 'environmental', label: '🌍 Environment', icon: '🌍' },
    { id: 'iot', label: '📡 IoT Sensors', icon: '📡' },
    { id: 'blockchain', label: '🔐 Blockchain', icon: '🔐' },
    { id: 'swarm', label: '🤖 Swarm Intel', icon: '🤖' },
    { id: 'fleet', label: '🚛 Fleet Management', icon: '🚛' },
    { id: 'emergency', label: '🚨 Emergency', icon: '🚨' }
  ];

  if (!backendReady) {
    return <AutoBackendStarter onBackendReady={setBackendReady} />;
  }

  if (!systemData) {
    return (
      <div style={{ 
        padding: '20px', 
        fontFamily: 'Arial, sans-serif', 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
        minHeight: '100vh', 
        color: 'white',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center', maxWidth: '600px' }}>
          <h1 style={{ fontSize: '3em', marginBottom: '20px', textShadow: '2px 2px 4px rgba(0,0,0,0.3)' }}>🌐 AETHER System</h1>
          <div style={{ 
            background: 'rgba(255,255,255,0.1)', 
            padding: '20px', 
            borderRadius: '15px', 
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255,255,255,0.2)'
          }}>
            <p style={{ fontSize: '1.2em', marginBottom: '10px' }}>Status: {connected ? '🟢 Connected' : '🔴 Connecting...'}</p>
            <p style={{ fontSize: '1.1em', marginBottom: '20px' }}>Loading AETHER AI-Powered System...</p>
            <div style={{ marginTop: '30px' }}>
              <div style={{ 
                fontSize: '4em', 
                animation: 'spin 2s linear infinite',
                marginBottom: '20px'
              }}>⚡</div>
              <p style={{ marginTop: '15px', fontSize: '1.1em' }}>Initializing satellite connectivity...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const { dynamic_system, aether_data } = systemData;
  const deviceInfo = dynamic_system?.device_info || {};
  const deviceType = dynamic_system?.device_type || 'laptop';
  const realTimeMetrics = dynamic_system?.real_time_metrics || {};
  
  const vehicleHealth = aether_data?.vehicle_health || {};
  const aiPredictions = aether_data?.ai_predictions || {};
  const environmentalData = aether_data?.environmental_data || {};
  const droneStatus = aether_data?.drone_status || {};
  const navigation = aether_data?.navigation || {};
  const emergencyAlerts = aether_data?.emergency_alerts || [];
  const fleetData = aether_data?.fleet_management || {};
  const iotData = aether_data?.iot_sensors || {};
  const blockchainData = aether_data?.blockchain_security || {};
  const quantumData = aether_data?.quantum_encryption || {};
  const swarmData = aether_data?.swarm_intelligence || {};

  return (
    <div style={{ 
      fontFamily: 'Arial, sans-serif', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 
      minHeight: '100vh', 
      color: 'white'
    }}>
      <style>
        {`
          @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
          @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
          @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
          .animate-fadeIn { animation: fadeIn 0.6s ease-out; }
          .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); transition: all 0.3s ease; }
          .tab-button { transition: all 0.3s ease; cursor: pointer; }
          .tab-button:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
          .metric-card { transition: all 0.3s ease; cursor: pointer; }
          .metric-card:hover { transform: scale(1.05); box-shadow: 0 8px 20px rgba(0,0,0,0.3); }
        `}
      </style>
      
      {/* Header */}
      <header style={{ 
        padding: '20px', 
        textAlign: 'center', 
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)',
        borderBottom: '1px solid rgba(255,255,255,0.2)'
      }}>
        <div className={animationClass}>
          <h1 style={{ 
            margin: 0, 
            fontSize: '2.8em', 
            textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
            background: 'linear-gradient(45deg, #fff, #e0e7ff)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🌐 AETHER: AI-Powered Intelligent Mobility System
          </h1>
          <div style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            background: 'rgba(255,255,255,0.1)', 
            padding: '10px 20px', 
            borderRadius: '25px', 
            margin: '15px 0',
            border: '1px solid rgba(255,255,255,0.2)'
          }}>
            <div style={{ 
              width: '12px', 
              height: '12px', 
              borderRadius: '50%', 
              background: connected ? '#10B981' : '#EF4444',
              marginRight: '10px',
              animation: connected ? 'pulse 2s infinite' : 'none'
            }}></div>
            <span style={{ fontSize: '1.1em', fontWeight: 'bold' }}>
              {connected ? '🟢 LIVE SYSTEM' : '🔴 OFFLINE'}
            </span>
          </div>
          <p style={{ margin: '10px 0', fontSize: '1.2em', opacity: 0.9 }}>
            {deviceInfo.manufacturer || 'Unknown'} {deviceInfo.model || 'Device'} • Satellite Connected
          </p>
        </div>
        
        {/* Navigation Tabs */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          gap: '8px', 
          marginTop: '20px',
          flexWrap: 'wrap'
        }}>
          {tabs.map(tab => (
            <button
              key={tab.id}
              className="tab-button"
              onClick={() => setActiveTab(tab.id)}
              style={{
                padding: '10px 16px',
                borderRadius: '20px',
                border: 'none',
                background: activeTab === tab.id 
                  ? 'rgba(255,255,255,0.3)' 
                  : 'rgba(255,255,255,0.1)',
                color: 'white',
                fontSize: '0.9em',
                fontWeight: activeTab === tab.id ? 'bold' : 'normal',
                backdropFilter: 'blur(10px)',
                border: activeTab === tab.id 
                  ? '2px solid rgba(255,255,255,0.5)' 
                  : '1px solid rgba(255,255,255,0.2)'
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </header>

      {/* Main Content */}
      <div style={{ padding: '20px' }}>
        {activeTab === 'overview' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              {/* System Status */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>⚡ System Overview</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', fontSize: '0.9em' }}>
                  <div>Vehicle Health: <span style={{ color: '#10B981', fontWeight: 'bold' }}>{vehicleHealth.overall_score?.toFixed(1) || 'N/A'}%</span></div>
                  <div>AI Status: <span style={{ color: '#10B981', fontWeight: 'bold' }}>Active</span></div>
                  <div>Drone: <span style={{ color: droneStatus.status === 'ACTIVE' ? '#10B981' : '#F59E0B', fontWeight: 'bold' }}>{droneStatus.status || 'N/A'}</span></div>
                  <div>Satellites: <span style={{ color: '#10B981', fontWeight: 'bold' }}>{navigation.satellite_connectivity?.satellite_count || 'N/A'}</span></div>
                  <div>Blockchain: <span style={{ color: blockchainData.chain_integrity ? '#10B981' : '#EF4444', fontWeight: 'bold' }}>{blockchainData.chain_integrity ? 'Secure' : 'Error'}</span></div>
                  <div>IoT Sensors: <span style={{ color: '#10B981', fontWeight: 'bold' }}>{Object.keys(iotData).length - 2 || 0} Active</span></div>
                  <div>Swarm Intel: <span style={{ color: '#10B981', fontWeight: 'bold' }}>{swarmData.active_vehicles || 0} Vehicles</span></div>
                  <div>Quantum Secure: <span style={{ color: quantumData.quantum_encryption_active ? '#10B981' : '#EF4444', fontWeight: 'bold' }}>{quantumData.quantum_encryption_active ? 'Active' : 'Inactive'}</span></div>
                </div>
              </div>

              {/* Quick Alerts */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🚨 Active Alerts</h3>
                {emergencyAlerts.length > 0 ? (
                  emergencyAlerts.slice(0, 2).map((alert, index) => (
                    <div key={index} style={{ 
                      background: 'rgba(239, 68, 68, 0.2)', 
                      padding: '10px', 
                      borderRadius: '8px', 
                      marginBottom: '10px',
                      border: '1px solid #EF4444'
                    }}>
                      <div style={{ fontWeight: 'bold', fontSize: '0.9em' }}>{alert.type}</div>
                      <div style={{ fontSize: '0.8em', opacity: 0.9 }}>{alert.message}</div>
                    </div>
                  ))
                ) : (
                  <div style={{ textAlign: 'center', opacity: 0.7 }}>
                    <div style={{ fontSize: '2em', marginBottom: '10px' }}>✅</div>
                    <div>All systems normal</div>
                  </div>
                )}
              </div>

            </div>
          </div>
        )}

        {activeTab === 'vehicle' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
              
              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🔋</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Battery Level</h3>
                <div style={{ fontSize: '2.5em', fontWeight: 'bold', marginBottom: '10px' }}>
                  {vehicleHealth.battery_level?.toFixed(1) || 'N/A'}%
                </div>
              </div>

              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🌡️</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Engine Temp</h3>
                <div style={{ fontSize: '2.5em', fontWeight: 'bold', marginBottom: '10px' }}>
                  {vehicleHealth.engine_temp?.toFixed(1) || 'N/A'}°C
                </div>
              </div>

              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🛞</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Tire Pressure</h3>
                <div style={{ fontSize: '1.2em' }}>
                  {vehicleHealth.tire_pressure?.map((pressure, index) => (
                    <div key={index}>Tire {index + 1}: {pressure?.toFixed(1)} PSI</div>
                  )) || 'N/A'}
                </div>
              </div>

              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🛡️</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Brake Health</h3>
                <div style={{ fontSize: '2.5em', fontWeight: 'bold', marginBottom: '10px' }}>
                  {vehicleHealth.brake_health?.toFixed(1) || 'N/A'}%
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'ai' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🚗 Collision Prevention</h3>
                <div style={{ textAlign: 'center', marginBottom: '15px' }}>
                  <div style={{ 
                    fontSize: '3em', 
                    color: getRiskColor(aiPredictions.collision_risk),
                    fontWeight: 'bold'
                  }}>
                    {aiPredictions.collision_risk || 'LOW'}
                  </div>
                  <div style={{ fontSize: '0.9em', opacity: 0.8 }}>
                    Risk Level: {(aiPredictions.collision_probability * 100)?.toFixed(1) || 'N/A'}%
                  </div>
                </div>
                {aiPredictions.time_to_collision && (
                  <div style={{ 
                    background: 'rgba(239, 68, 68, 0.2)', 
                    padding: '10px', 
                    borderRadius: '8px',
                    textAlign: 'center'
                  }}>
                    ⚠️ Collision in {aiPredictions.time_to_collision.toFixed(1)}s
                  </div>
                )}
              </div>

              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>👁️ Driver Monitoring</h3>
                <div style={{ marginBottom: '15px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <span>Alertness</span>
                    <span style={{ fontWeight: 'bold' }}>{(aiPredictions.driver_alertness * 100)?.toFixed(1) || 'N/A'}%</span>
                  </div>
                  <div style={{
                    width: '100%',
                    height: '8px',
                    background: 'rgba(255,255,255,0.2)',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${(aiPredictions.driver_alertness * 100) || 0}%`,
                      height: '100%',
                      background: getStatusColor(aiPredictions.driver_alertness * 100),
                      borderRadius: '4px',
                      transition: 'width 0.5s ease'
                    }}></div>
                  </div>
                </div>
                {aiPredictions.drowsiness_detected && (
                  <div style={{ 
                    background: 'rgba(245, 158, 11, 0.2)', 
                    padding: '10px', 
                    borderRadius: '8px',
                    textAlign: 'center'
                  }}>
                    😴 Drowsiness detected
                  </div>
                )}
              </div>

              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>⛽ Fuel Optimization</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ marginBottom: '10px' }}>
                    Current Efficiency: <span style={{ fontWeight: 'bold' }}>{aiPredictions.fuel_optimization?.current_efficiency?.toFixed(1) || 'N/A'} km/l</span>
                  </div>
                  <div style={{ marginBottom: '10px' }}>
                    Optimal Speed: <span style={{ fontWeight: 'bold' }}>{aiPredictions.fuel_optimization?.optimal_speed || 'N/A'} km/h</span>
                  </div>
                  <div style={{ 
                    background: 'rgba(16, 185, 129, 0.2)', 
                    padding: '8px', 
                    borderRadius: '6px',
                    fontSize: '0.8em'
                  }}>
                    💡 {aiPredictions.fuel_optimization?.suggested_route || 'Route optimization active'}
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'drone' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🚁 Drone Status</h3>
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                  <div style={{ fontSize: '3em', marginBottom: '10px' }}>
                    {droneStatus.status === 'ACTIVE' ? '🟢' : droneStatus.status === 'CHARGING' ? '🔋' : '⚪'}
                  </div>
                  <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>{droneStatus.status || 'STANDBY'}</div>
                  <div style={{ fontSize: '0.9em', opacity: 0.8 }}>ID: {droneStatus.drone_id || 'N/A'}</div>
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Battery:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.battery_level?.toFixed(1) || 'N/A'}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Altitude:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.altitude?.toFixed(1) || 'N/A'}m</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Speed:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.speed?.toFixed(1) || 'N/A'} km/h</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Mission:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.mission || 'STANDBY'}</span>
                  </div>
                </div>
              </div>

              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>📹 Camera Feed</h3>
                <div style={{ 
                  background: 'rgba(0,0,0,0.5)', 
                  height: '150px', 
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  marginBottom: '15px'
                }}>
                  <div style={{ textAlign: 'center' }}>
                    <div style={{ fontSize: '2em', marginBottom: '10px' }}>📹</div>
                    <div style={{ fontSize: '0.9em' }}>{droneStatus.camera_feed || 'OFFLINE'}</div>
                  </div>
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Thermal Imaging:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.thermal_imaging ? '✅' : '❌'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Objects Detected:</span>
                    <span style={{ fontWeight: 'bold' }}>{droneStatus.detected_objects || 0}</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'navigation' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🛰️ Satellite Connectivity</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <span>NavIC Signal:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>
                      {(navigation.satellite_connectivity?.navic_signal * 100)?.toFixed(1) || 'N/A'}%
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <span>GPS Accuracy:</span>
                    <span style={{ fontWeight: 'bold' }}>{navigation.satellite_connectivity?.gps_accuracy?.toFixed(1) || 'N/A'}m</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <span>Satellites:</span>
                    <span style={{ fontWeight: 'bold' }}>{navigation.satellite_connectivity?.satellite_count || 'N/A'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Signal Strength:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>
                      {navigation.satellite_connectivity?.signal_strength || 'N/A'}
                    </span>
                  </div>
                </div>
              </div>

              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🗺️ Route Information</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ marginBottom: '10px' }}>
                    <strong>From:</strong> {navigation.current_location?.address || 'Current Location'}
                  </div>
                  <div style={{ marginBottom: '15px' }}>
                    <strong>To:</strong> {navigation.destination?.address || 'Destination'}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Distance:</span>
                    <span style={{ fontWeight: 'bold' }}>{navigation.route_info?.distance_km?.toFixed(1) || 'N/A'} km</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>ETA:</span>
                    <span style={{ fontWeight: 'bold' }}>{navigation.route_info?.eta_minutes || 'N/A'} min</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Fuel Required:</span>
                    <span style={{ fontWeight: 'bold' }}>{navigation.route_info?.fuel_required?.toFixed(1) || 'N/A'}L</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'environmental' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px' }}>
              
              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #06B6D4 0%, #0891B2 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🌤️</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Weather</h3>
                <div style={{ fontSize: '1.8em', fontWeight: 'bold', marginBottom: '10px' }}>
                  {environmentalData.weather?.temperature?.toFixed(1) || 'N/A'}°C
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  {environmentalData.weather?.condition || 'Unknown'} • {environmentalData.weather?.humidity?.toFixed(1) || 'N/A'}% Humidity
                </div>
              </div>

              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🌬️</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Air Quality</h3>
                <div style={{ fontSize: '1.8em', fontWeight: 'bold', marginBottom: '10px' }}>
                  AQI {environmentalData.air_quality?.aqi || 'N/A'}
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  PM2.5: {environmentalData.air_quality?.pm25?.toFixed(1) || 'N/A'} µg/m³
                </div>
              </div>

              <div className="metric-card" style={{ 
                background: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)', 
                padding: '25px', 
                borderRadius: '20px', 
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '2.5em', marginBottom: '10px' }}>🛣️</div>
                <h3 style={{ margin: '0 0 15px 0' }}>Road Conditions</h3>
                <div style={{ fontSize: '1.2em', fontWeight: 'bold', marginBottom: '10px' }}>
                  {environmentalData.road_conditions?.surface || 'Unknown'}
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  Visibility: {environmentalData.road_conditions?.visibility || 'N/A'}
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'fleet' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
              
              {[
                { label: 'Total Vehicles', value: fleetData.total_vehicles, icon: '🚗', color: '#3B82F6' },
                { label: 'Active Vehicles', value: fleetData.active_vehicles, icon: '✅', color: '#10B981' },
                { label: 'Maintenance Required', value: fleetData.maintenance_required, icon: '🔧', color: '#F59E0B' },
                { label: 'Avg Health Score', value: `${fleetData.avg_health_score?.toFixed(1) || 'N/A'}%`, icon: '❤️', color: '#EF4444' },
                { label: 'Fuel Efficiency', value: `${fleetData.fuel_efficiency?.toFixed(1) || 'N/A'} km/l`, icon: '⛽', color: '#8B5CF6' },
                { label: 'Distance Today', value: `${fleetData.total_distance_today?.toFixed(0) || 'N/A'} km`, icon: '📏', color: '#06B6D4' }
              ].map((item, index) => (
                <div key={index} className="metric-card" style={{ 
                  background: `linear-gradient(135deg, ${item.color}20 0%, ${item.color}40 100%)`, 
                  padding: '20px', 
                  borderRadius: '15px', 
                  textAlign: 'center',
                  border: `1px solid ${item.color}40`
                }}>
                  <div style={{ fontSize: '2em', marginBottom: '10px' }}>{item.icon}</div>
                  <div style={{ fontSize: '1.8em', fontWeight: 'bold', marginBottom: '5px', color: item.color }}>
                    {item.value}
                  </div>
                  <div style={{ fontSize: '0.9em', opacity: 0.9 }}>{item.label}</div>
                </div>
              ))}

            </div>
          </div>
        )}

        {activeTab === 'iot' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              {/* Accelerometer */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>📱 Accelerometer</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>X-Axis:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.accelerometer?.x?.toFixed(2) || 'N/A'} m/s²</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Y-Axis:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.accelerometer?.y?.toFixed(2) || 'N/A'} m/s²</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Z-Axis:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.accelerometer?.z?.toFixed(2) || 'N/A'} m/s²</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Movement:</span>
                    <span style={{ fontWeight: 'bold', color: iotData.accelerometer?.movement_detected ? '#F59E0B' : '#10B981' }}>
                      {iotData.accelerometer?.movement_detected ? 'Detected' : 'Stable'}
                    </span>
                  </div>
                </div>
              </div>

              {/* GPS Sensor */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🛰️ GPS Sensor</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Latitude:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.gps?.latitude?.toFixed(4) || 'N/A'}°</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Longitude:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.gps?.longitude?.toFixed(4) || 'N/A'}°</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Speed:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.gps?.speed?.toFixed(1) || 'N/A'} km/h</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Accuracy:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>{iotData.gps?.accuracy?.toFixed(1) || 'N/A'}m</span>
                  </div>
                </div>
              </div>

              {/* Temperature Sensors */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🌡️ Temperature</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Engine:</span>
                    <span style={{ fontWeight: 'bold', color: (iotData.temperature?.engine_temp || 0) > 85 ? '#EF4444' : '#10B981' }}>
                      {iotData.temperature?.engine_temp?.toFixed(1) || 'N/A'}°C
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Ambient:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.temperature?.ambient_temp?.toFixed(1) || 'N/A'}°C</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Battery:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.temperature?.battery_temp?.toFixed(1) || 'N/A'}°C</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Status:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>{iotData.temperature?.status || 'N/A'}</span>
                  </div>
                </div>
              </div>

              {/* Camera Sensor */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>📹 Camera System</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Resolution:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.camera?.resolution?.width || 'N/A'}x{iotData.camera?.resolution?.height || 'N/A'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Objects:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.camera?.objects_detected || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Vehicles:</span>
                    <span style={{ fontWeight: 'bold' }}>{iotData.camera?.vehicles || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Quality:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>{iotData.camera?.image_quality || 'N/A'}</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'blockchain' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              {/* Blockchain Status */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🔐 Blockchain Security</h3>
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                  <div style={{ fontSize: '3em', marginBottom: '10px' }}>
                    {blockchainData.chain_integrity ? '🟢' : '🔴'}
                  </div>
                  <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>
                    {blockchainData.chain_integrity ? 'SECURE' : 'COMPROMISED'}
                  </div>
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Total Blocks:</span>
                    <span style={{ fontWeight: 'bold' }}>{blockchainData.total_blocks || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Security Level:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>{blockchainData.security_level || 'N/A'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Tamper Proof:</span>
                    <span style={{ fontWeight: 'bold', color: blockchainData.data_tamper_proof ? '#10B981' : '#EF4444' }}>
                      {blockchainData.data_tamper_proof ? 'YES' : 'NO'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Quantum Encryption */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>⚛️ Quantum Encryption</h3>
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                  <div style={{ fontSize: '3em', marginBottom: '10px' }}>
                    {quantumData.quantum_encryption_active ? '🔒' : '🔓'}
                  </div>
                  <div style={{ fontSize: '1.2em', fontWeight: 'bold' }}>
                    {quantumData.quantum_encryption_active ? 'ACTIVE' : 'INACTIVE'}
                  </div>
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Encryption:</span>
                    <span style={{ fontWeight: 'bold' }}>{quantumData.encryption_strength || 'N/A'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Key Rotation:</span>
                    <span style={{ fontWeight: 'bold' }}>{quantumData.key_rotation_interval || 'N/A'}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Quantum Resistant:</span>
                    <span style={{ fontWeight: 'bold', color: quantumData.quantum_resistance ? '#10B981' : '#EF4444' }}>
                      {quantumData.quantum_resistance ? 'YES' : 'NO'}
                    </span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'swarm' && (
          <div className="animate-fadeIn">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
              
              {/* Swarm Status */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🤖 Swarm Intelligence</h3>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Total Vehicles:</span>
                    <span style={{ fontWeight: 'bold' }}>{swarmData.total_vehicles || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Active Vehicles:</span>
                    <span style={{ fontWeight: 'bold', color: '#10B981' }}>{swarmData.active_vehicles || 0}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Coordination:</span>
                    <span style={{ fontWeight: 'bold' }}>{swarmData.coordination_efficiency?.toFixed(1) || 'N/A'}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Data Sharing:</span>
                    <span style={{ fontWeight: 'bold' }}>{swarmData.data_sharing_rate?.toFixed(1) || 'N/A'}%</span>
                  </div>
                </div>
              </div>

              {/* Collective Intelligence */}
              <div className="card-hover" style={{ 
                background: 'rgba(255,255,255,0.1)', 
                padding: '25px', 
                borderRadius: '20px', 
                backdropFilter: 'blur(10px)',
                border: '1px solid rgba(255,255,255,0.2)'
              }}>
                <h3 style={{ margin: '0 0 20px 0', fontSize: '1.4em' }}>🧠 Collective Intelligence</h3>
                <div style={{ textAlign: 'center', marginBottom: '20px' }}>
                  <div style={{ fontSize: '2.5em', fontWeight: 'bold', color: '#10B981' }}>
                    {swarmData.collective_intelligence_score?.toFixed(1) || 'N/A'}%
                  </div>
                  <div style={{ fontSize: '0.9em', opacity: 0.8 }}>Intelligence Score</div>
                </div>
                <div style={{ fontSize: '0.9em' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span>Knowledge Quality:</span>
                    <span style={{ fontWeight: 'bold' }}>{swarmData.shared_knowledge_quality?.toFixed(1) || 'N/A'}%</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>Swarm Groups:</span>
                    <span style={{ fontWeight: 'bold' }}>{swarmData.swarm_groups || 0}</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        )}

        {activeTab === 'emergency' && (
          <div className="animate-fadeIn">
            <div style={{ 
              background: 'rgba(255,255,255,0.1)', 
              padding: '30px', 
              borderRadius: '20px', 
              backdropFilter: 'blur(10px)',
              border: '1px solid rgba(255,255,255,0.2)'
            }}>
              <h2 style={{ margin: '0 0 30px 0', textAlign: 'center', fontSize: '1.8em' }}>🚨 Emergency Response System</h2>
              
              {emergencyAlerts.length > 0 ? (
                <div style={{ display: 'grid', gap: '15px' }}>
                  {emergencyAlerts.map((alert, index) => (
                    <div key={index} className="card-hover" style={{ 
                      background: alert.severity === 'CRITICAL' ? 'rgba(239, 68, 68, 0.3)' : 
                                 alert.severity === 'HIGH' ? 'rgba(245, 158, 11, 0.3)' : 
                                 'rgba(59, 130, 246, 0.3)',
                      padding: '20px', 
                      borderRadius: '15px',
                      border: `2px solid ${alert.severity === 'CRITICAL' ? '#EF4444' : 
                                          alert.severity === 'HIGH' ? '#F59E0B' : 
                                          '#3B82F6'}`,
                      display: 'flex',
                      alignItems: 'center',
                      gap: '15px'
                    }}>
                      <div style={{ fontSize: '2.5em' }}>
                        {alert.type === 'COLLISION_WARNING' ? '⚠️' : 
                         alert.type === 'MEDICAL_EMERGENCY' ? '🏥' : 
                         alert.type === 'VEHICLE_BREAKDOWN' ? '🔧' : '🚨'}
                      </div>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 'bold', fontSize: '1.2em', marginBottom: '5px' }}>
                          {alert.type.replace('_', ' ')}
                        </div>
                        <div style={{ opacity: 0.9, marginBottom: '5px' }}>{alert.message}</div>
                        <div style={{ fontSize: '0.9em', opacity: 0.7 }}>
                          {new Date(alert.timestamp).toLocaleTimeString()} • {alert.auto_response}
                        </div>
                      </div>
                      <div style={{ 
                        background: alert.severity === 'CRITICAL' ? '#EF4444' : 
                                   alert.severity === 'HIGH' ? '#F59E0B' : '#3B82F6',
                        color: 'white',
                        padding: '5px 10px',
                        borderRadius: '15px',
                        fontSize: '0.8em',
                        fontWeight: 'bold'
                      }}>
                        {alert.severity}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ textAlign: 'center', padding: '40px' }}>
                  <div style={{ fontSize: '4em', marginBottom: '20px' }}>✅</div>
                  <h3 style={{ marginBottom: '10px' }}>All Systems Normal</h3>
                  <p style={{ opacity: 0.8 }}>No emergency alerts detected. All safety systems are operational.</p>
              <div style={{ marginTop: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
                <div style={{ background: 'rgba(16, 185, 129, 0.2)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🔐</div>
                  <div style={{ fontSize: '0.9em' }}>Blockchain Secure</div>
                </div>
                <div style={{ background: 'rgba(59, 130, 246, 0.2)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🛰️</div>
                  <div style={{ fontSize: '0.9em' }}>Satellite Connected</div>
                </div>
                <div style={{ background: 'rgba(139, 92, 246, 0.2)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🤖</div>
                  <div style={{ fontSize: '0.9em' }}>AI Monitoring</div>
                </div>
                <div style={{ background: 'rgba(245, 158, 11, 0.2)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>📡</div>
                  <div style={{ fontSize: '0.9em' }}>IoT Active</div>
                </div>
              </div>
                </div>
              )}
            </div>
          </div>
        )}

      </div>

      <footer style={{ 
        padding: '20px', 
        textAlign: 'center', 
        background: 'rgba(255,255,255,0.05)',
        backdropFilter: 'blur(10px)',
        borderTop: '1px solid rgba(255,255,255,0.1)', 
        marginTop: '30px' 
      }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          gap: '20px', 
          flexWrap: 'wrap',
          marginBottom: '10px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div style={{ 
              width: '8px', 
              height: '8px', 
              borderRadius: '50%', 
              background: '#10B981',
              animation: 'pulse 2s infinite'
            }}></div>
            <span>🌐 AETHER AI-Powered Mobility System</span>
          </div>
          <span>•</span>
          <span>🛰️ Satellite-Integrated Intelligence</span>
        </div>
        <p style={{ margin: 0, opacity: 0.8, fontSize: '0.9em' }}>
          {deviceInfo.manufacturer || 'Unknown'} {deviceInfo.model || 'Device'} • 
          Last Update: {new Date().toLocaleTimeString()} • 
          Satellites: {navigation.satellite_connectivity?.satellite_count || 'N/A'} Connected
        </p>
      </footer>
    </div>
  );
}

export default SafeDynamicDashboard;