import React, { useState, useEffect } from 'react';

function DynamicDeviceDashboard() {
  const [deviceData, setDeviceData] = useState(null);
  const [connected, setConnected] = useState(false);
  const [detectionData, setDetectionData] = useState(null);
  const [capabilities, setCapabilities] = useState(null);

  useEffect(() => {
    // Get comprehensive device detection data
    fetch('http://localhost:8000/api/device-detection')
      .then(res => res.json())
      .then(data => {
        setDetectionData(data);
        console.log('Device Detection:', data);
      })
      .catch(err => console.error('Device detection error:', err));

    // Get device capabilities
    fetch('http://localhost:8000/api/device-capabilities')
      .then(res => res.json())
      .then(data => setCapabilities(data))
      .catch(err => console.error('Capabilities error:', err));

    // WebSocket connection with adaptive frequency
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      setConnected(true);
      console.log('Connected to Dynamic Device Monitor');
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

  const getDeviceIcon = (deviceType) => {
    const icons = {
      // Mobile Devices
      'android_phone': '📱',
      'iphone': '📱',
      'windows_tablet': '📱',
      'surface_tablet': '📱',
      'ipad': '📱',
      
      // Laptops
      'windows_laptop': '💻',
      'gaming_laptop': '🎮',
      'macbook_apple_silicon': '💻',
      'macbook_intel': '💻',
      'windows_arm_laptop': '💻',
      
      // Desktops
      'desktop_pc': '🖥️',
      'workstation': '🖥️',
      'imac': '🖥️',
      'mac_studio': '🖥️',
      
      // IoT Devices
      'raspberry_pi': '🤖',
      'nvidia_jetson': '🤖',
      'arduino_compatible': '⚙️',
      'arm_linux': '🔧',
      'embedded_device': '⚙️',
      
      // Vehicle Systems
      'automotive_ecu': '🚗',
      'truck_telematics': '🚛'
    };
    return icons[deviceType] || '📟';
  };

  const getVehicleIcon = (vehicleType) => {
    const icons = {
      'Electric Scooter': '🛴',
      'Tesla Model S': '🚗',
      'Hybrid Car': '🚗',
      'BMW i3': '🚗',
      'Sedan Car': '🚗',
      'Sports Car': '🏎️',
      'Tesla Model 3': '🚗',
      'Pickup Truck': '🚛',
      'Heavy Duty Truck': '🚛',
      'Drone': '🚁',
      'AI Robot': '🤖',
      'Car ECU': '🚗',
      'Truck Telematics': '🚛'
    };
    return icons[vehicleType] || '🚗';
  };

  const getManufacturerIcon = (manufacturer) => {
    const icons = {
      'apple': '🍎',
      'microsoft': '🪟',
      'google': '🔍',
      'samsung': '📱',
      'dell': '💻',
      'hp': '🖥️',
      'lenovo': '💻',
      'asus': '⚡',
      'acer': '💻',
      'raspberry pi foundation': '🍓',
      'nvidia': '🎮'
    };
    return icons[manufacturer.toLowerCase()] || '🏭';
  };

  const getCategoryColor = (category) => {
    const colors = {
      'mobile_device': '#10B981',
      'computer': '#3B82F6',
      'iot_device': '#8B5CF6',
      'vehicle_system': '#F59E0B',
      'generic': '#6B7280'
    };
    return colors[category] || '#6B7280';
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

  const renderDeviceSpecificMetrics = () => {
    if (!deviceData || !detectionData) return null;

    const device = detectionData.device_info;
    const metrics = deviceData.raw_metrics;
    const config = detectionData.device_config;

    // Mobile device specific metrics
    if (device.category === 'mobile_device') {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '20px' }}>
          {capabilities?.has_battery && (
            <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🔋</div>
              <div style={{ fontWeight: 'bold' }}>Battery</div>
              <div style={{ fontSize: '1.2em', color: metrics.battery?.percent < 20 ? '#EF4444' : '#10B981' }}>
                {metrics.battery?.percent?.toFixed(1) || 'N/A'}%
              </div>
            </div>
          )}
          
          {capabilities?.has_gps && (
            <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>📍</div>
              <div style={{ fontWeight: 'bold' }}>GPS Status</div>
              <div style={{ color: '#10B981' }}>Active</div>
            </div>
          )}
          
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>📶</div>
            <div style={{ fontWeight: 'bold' }}>Network</div>
            <div style={{ color: '#3B82F6' }}>Connected</div>
          </div>
        </div>
      );
    }

    // IoT device specific metrics
    if (device.category === 'iot_device') {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '20px' }}>
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🔌</div>
            <div style={{ fontWeight: 'bold' }}>Power Source</div>
            <div style={{ color: '#10B981' }}>{device.power_source.replace('_', ' ').toUpperCase()}</div>
          </div>
          
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>📡</div>
            <div style={{ fontWeight: 'bold' }}>Connectivity</div>
            <div style={{ color: '#3B82F6' }}>Online</div>
          </div>
          
          {device.type === 'raspberry_pi' && (
            <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
              <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🔧</div>
              <div style={{ fontWeight: 'bold' }}>GPIO Status</div>
              <div style={{ color: '#8B5CF6' }}>Available</div>
            </div>
          )}
        </div>
      );
    }

    // Vehicle system specific metrics
    if (device.category === 'vehicle_system') {
      return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px', marginBottom: '20px' }}>
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>🚗</div>
            <div style={{ fontWeight: 'bold' }}>Vehicle Status</div>
            <div style={{ color: '#10B981' }}>Running</div>
          </div>
          
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>📍</div>
            <div style={{ fontWeight: 'bold' }}>GPS Tracking</div>
            <div style={{ color: '#3B82F6' }}>Active</div>
          </div>
          
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px', textAlign: 'center' }}>
            <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>⛽</div>
            <div style={{ fontWeight: 'bold' }}>Fuel/Power</div>
            <div style={{ color: '#F59E0B' }}>Monitoring</div>
          </div>
        </div>
      );
    }

    return null;
  };

  const renderOptimizationTips = () => {
    if (!detectionData) return null;

    const tips = detectionData.recommended_features?.optimization_tips || [];
    
    return (
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '20px' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>💡 Device-Specific Optimization Tips</h3>
        <div style={{ display: 'grid', gap: '10px' }}>
          {tips.map((tip, index) => (
            <div key={index} style={{ 
              padding: '12px', 
              backgroundColor: 'rgba(59, 130, 246, 0.3)', 
              borderRadius: '8px', 
              border: '1px solid #3B82F6' 
            }}>
              • {tip}
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (!deviceData || !detectionData) {
    return (
      <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', minHeight: '100vh', color: 'white' }}>
        <h1>🌐 AETHER Dynamic Device Monitor</h1>
        <p>Status: {connected ? '🟢 Connected' : '🔴 Connecting...'}</p>
        <p>Performing comprehensive device detection and analysis...</p>
        <div style={{ marginTop: '20px' }}>
          <div style={{ fontSize: '2em' }}>🔍</div>
          <p>Detecting device type, manufacturer, and capabilities...</p>
        </div>
      </div>
    );
  }

  const device = detectionData.device_info;
  const manufacturer = detectionData.manufacturer_info;
  const health = deviceData.health_analysis;
  const metrics = deviceData.raw_metrics;
  const vehicle = deviceData.vehicle_analogy;
  const config = detectionData.device_config;

  return (
    <div style={{ 
      padding: '20px', 
      fontFamily: 'Arial, sans-serif', 
      background: `linear-gradient(135deg, ${getCategoryColor(device.category)}22 0%, #764ba2 100%)`, 
      minHeight: '100vh', 
      color: 'white' 
    }}>
      
      {/* Dynamic Header */}
      <header style={{ marginBottom: '30px', textAlign: 'center' }}>
        <h1 style={{ margin: 0, fontSize: '2.5em' }}>
          🌐 AETHER Dynamic Device Monitor
        </h1>
        <div style={{ fontSize: '4em', margin: '15px 0' }}>
          {getManufacturerIcon(manufacturer.brand)} {getDeviceIcon(device.type)} ➜ {getVehicleIcon(vehicle.vehicle_type)}
        </div>
        <p style={{ margin: '10px 0', fontSize: '1.3em', fontWeight: 'bold' }}>
          {manufacturer.brand} {manufacturer.model}
        </p>
        <p style={{ margin: '10px 0', fontSize: '1.1em' }}>
          {device.type.replace('_', ' ').toUpperCase()} → {vehicle.vehicle_type.toUpperCase()}
        </p>
        <p style={{ margin: '5px 0', opacity: 0.8 }}>
          {device.form_factor.replace('_', ' ').toUpperCase()} • {device.mobility.toUpperCase()} • Status: {connected ? '🟢 LIVE' : '🔴 OFFLINE'}
        </p>
      </header>

      {/* Comprehensive Device Information */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 20px 0', textAlign: 'center' }}>📱 Comprehensive Device Profile</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
          
          {/* Device Identity */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🏷️ Device Identity</h4>
            <p><strong>Type:</strong> {device.type.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Category:</strong> {device.category.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Subcategory:</strong> {device.subcategory.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Device ID:</strong> {device.device_id}</p>
          </div>

          {/* Manufacturer Info */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🏭 Manufacturer</h4>
            <p><strong>Brand:</strong> {manufacturer.brand}</p>
            <p><strong>Model:</strong> {manufacturer.model}</p>
            <p><strong>OEM:</strong> {manufacturer.oem}</p>
            <p><strong>Detection:</strong> {manufacturer.detection_method}</p>
          </div>

          {/* Physical Characteristics */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>📐 Physical Profile</h4>
            <p><strong>Form Factor:</strong> {device.form_factor.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Mobility:</strong> {device.mobility.toUpperCase()}</p>
            <p><strong>Power Source:</strong> {device.power_source.replace('_', ' ').toUpperCase()}</p>
            <p><strong>Architecture:</strong> {device.architecture}</p>
          </div>

          {/* System Information */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '15px', borderRadius: '10px' }}>
            <h4 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>💻 System Info</h4>
            <p><strong>OS:</strong> {device.system.toUpperCase()}</p>
            <p><strong>Machine:</strong> {device.machine.toUpperCase()}</p>
            <p><strong>Hostname:</strong> {device.hostname}</p>
            <p><strong>Update Interval:</strong> {config.update_interval}s</p>
          </div>
        </div>
      </div>

      {/* Device Capabilities */}
      {capabilities && (
        <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
          <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🎯 Device Capabilities</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
            {Object.entries(capabilities).map(([capability, value]) => (
              <div key={capability} style={{ 
                textAlign: 'center', 
                padding: '15px', 
                backgroundColor: value ? 'rgba(16, 185, 129, 0.3)' : 'rgba(107, 114, 128, 0.3)',
                borderRadius: '10px',
                border: `2px solid ${value ? '#10B981' : '#6B7280'}`
              }}>
                <div style={{ fontSize: '1.5em', marginBottom: '5px' }}>
                  {value ? '✅' : '❌'}
                </div>
                <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                  {capability.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </div>
                <div style={{ opacity: 0.8 }}>
                  {value ? 'Available' : 'Not Available'}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Device-Specific Metrics */}
      {renderDeviceSpecificMetrics()}

      {/* Core Health Metrics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        
        {/* Overall Health */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${getStatusColor(health.status)}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>💚 Overall Health</h3>
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
          border: `3px solid ${metrics.temperature > config.temp_thresholds.warning ? '#EF4444' : '#10B981'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>🌡️ Temperature</h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.temperature > config.temp_thresholds.warning ? '#FCA5A5' : '#6EE7B7'
          }}>
            {metrics.temperature.toFixed(1)}°C
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            Normal: &lt;{config.temp_thresholds.normal}°C • Warning: &gt;{config.temp_thresholds.warning}°C
          </p>
        </div>

        {/* Performance */}
        <div style={{ 
          backgroundColor: 'rgba(255,255,255,0.1)', 
          padding: '20px', 
          borderRadius: '15px', 
          border: `3px solid ${metrics.cpu_usage > config.cpu_thresholds.warning ? '#F59E0B' : '#3B82F6'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>⚡ Performance</h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.cpu_usage > config.cpu_thresholds.warning ? '#FBBF24' : '#60A5FA'
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
          border: `3px solid ${metrics.memory_usage > config.memory_thresholds.warning ? '#EF4444' : '#8B5CF6'}`,
          backdropFilter: 'blur(10px)'
        }}>
          <h3 style={{ margin: '0 0 10px 0', color: '#E5E7EB' }}>💾 Memory</h3>
          <div style={{ 
            fontSize: '2.5em', 
            fontWeight: 'bold', 
            color: metrics.memory_usage > config.memory_thresholds.warning ? '#FCA5A5' : '#C084FC'
          }}>
            {metrics.memory_usage.toFixed(1)}%
          </div>
          <p style={{ margin: '5px 0', fontSize: '0.9em', opacity: 0.8 }}>
            {device.category === 'iot_device' ? 'System Memory' : 'RAM Usage'}
          </p>
        </div>
      </div>

      {/* Vehicle Analogy Details */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🚗 {vehicle.vehicle_type} System Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          {Object.entries(vehicle).filter(([key]) => !['vehicle_type', 'vehicle_id', 'engine_temp', 'speed', 'fuel_level', 'health_score', 'status'].includes(key)).map(([key, value]) => (
            <div key={key} style={{ textAlign: 'center', padding: '15px', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '10px' }}>
              <div style={{ fontWeight: 'bold', marginBottom: '5px' }}>
                {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
              </div>
              <div style={{ opacity: 0.8 }}>{value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Device Features */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', marginBottom: '30px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0', textAlign: 'center' }}>🔧 Device Features</h3>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', justifyContent: 'center' }}>
          {config.features?.map((feature, index) => (
            <div key={index} style={{ 
              padding: '8px 16px', 
              backgroundColor: 'rgba(139, 92, 246, 0.3)', 
              borderRadius: '20px', 
              border: '1px solid #8B5CF6',
              fontSize: '0.9em'
            }}>
              {feature.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </div>
          ))}
        </div>
      </div>

      {/* Optimization Tips */}
      {renderOptimizationTips()}

      {/* Health Alerts */}
      <div style={{ backgroundColor: 'rgba(255,255,255,0.1)', padding: '20px', borderRadius: '15px', backdropFilter: 'blur(10px)' }}>
        <h3 style={{ margin: '0 0 15px 0' }}>🚨 Health Status & Recommendations</h3>
        
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
            <h4 style={{ margin: '0 0 10px 0' }}>💡 System Recommendations:</h4>
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
            <div>Your {manufacturer.brand} {device.type.replace('_', ' ')} is running perfectly!</div>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', opacity: 0.8 }}>
        <p>🌐 AETHER Dynamic Device Health Monitor</p>
        <p>{manufacturer.brand} {manufacturer.model} • {device.hostname} • Last Update: {new Date().toLocaleTimeString()}</p>
        <p>Monitoring: {config.health_metrics.join(', ')}</p>
      </footer>
    </div>
  );
}

export default DynamicDeviceDashboard;