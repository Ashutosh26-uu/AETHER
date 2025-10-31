import React, { useState, useEffect } from 'react';
import { Camera, Radar, Zap, MapPin, AlertCircle } from 'lucide-react';

const SimpleDrone = () => {
  const [droneStatus, setDroneStatus] = useState('active');
  const [droneData, setDroneData] = useState({
    altitude: 45,
    battery: 78,
    speed: 25,
    temperature: 28,
    signal: 95
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setDroneData(prev => ({
        ...prev,
        altitude: prev.altitude + (Math.random() - 0.5) * 2,
        battery: Math.max(0, prev.battery - 0.1),
        speed: prev.speed + (Math.random() - 0.5) * 5,
        signal: 90 + Math.random() * 10
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 rounded-xl p-6 text-white">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="animate-spin">
              🚁
            </div>
            <div>
              <h3 className="text-xl font-bold">AETHER Drone Control</h3>
              <p className="text-sm text-gray-300">Autonomous Surveillance Active</p>
            </div>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm ${
            droneStatus === 'active' ? 'bg-green-500' : 'bg-red-500'
          }`}>
            {droneStatus.toUpperCase()}
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[
            { label: 'Altitude', value: `${droneData.altitude.toFixed(1)}m`, icon: '📏' },
            { label: 'Battery', value: `${droneData.battery.toFixed(1)}%`, icon: '🔋' },
            { label: 'Speed', value: `${droneData.speed.toFixed(1)} km/h`, icon: '⚡' },
            { label: 'Signal', value: `${droneData.signal.toFixed(0)}%`, icon: '📡' },
            { label: 'Temp', value: `${droneData.temperature}°C`, icon: '🌡️' }
          ].map((stat, index) => (
            <div
              key={index}
              className="bg-white/10 rounded-lg p-3 text-center hover:bg-white/20 transition-colors"
            >
              <div className="text-2xl mb-1">{stat.icon}</div>
              <div className="text-lg font-bold">{stat.value}</div>
              <div className="text-xs text-gray-400">{stat.label}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-black rounded-xl overflow-hidden">
          <div className="bg-red-600 text-white px-4 py-2 flex items-center space-x-2">
            <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold">LIVE FEED</span>
            <Camera className="h-4 w-4 ml-auto" />
          </div>
          
          <div className="relative h-64 bg-gradient-to-br from-gray-800 to-gray-900">
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
            
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-16 h-16 border-2 border-green-400 rounded-full border-dashed animate-spin"></div>
            </div>

            <div className="absolute top-4 left-4 text-green-400 text-xs font-mono">
              <div>ALT: {droneData.altitude.toFixed(1)}M</div>
              <div>SPD: {droneData.speed.toFixed(1)}KM/H</div>
              <div>BAT: {droneData.battery.toFixed(1)}%</div>
            </div>

            <div className="absolute bottom-4 right-4 text-green-400 text-xs font-mono">
              <div>28.6139°N 77.2090°E</div>
              <div>{new Date().toLocaleTimeString()}</div>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Mission Control</h3>
          
          <div className="space-y-3 mb-6">
            {['surveillance', 'emergency', 'inspection', 'patrol'].map((type) => (
              <button
                key={type}
                className="w-full p-3 rounded-lg text-left transition-colors bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600"
              >
                <div className="flex items-center space-x-3">
                  <div className="text-xl">
                    {type === 'surveillance' ? '👁️' : 
                     type === 'emergency' ? '🚨' :
                     type === 'inspection' ? '🔍' : '🛡️'}
                  </div>
                  <div>
                    <div className="font-semibold capitalize">{type}</div>
                    <div className="text-sm opacity-70">
                      {type === 'surveillance' ? 'Monitor area for threats' :
                       type === 'emergency' ? 'Respond to emergency calls' :
                       type === 'inspection' ? 'Inspect infrastructure' :
                       'Regular patrol route'}
                    </div>
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <button className="p-3 bg-green-500 text-white rounded-lg text-sm font-semibold hover:bg-green-600">
              🚁 Deploy
            </button>
            <button className="p-3 bg-red-500 text-white rounded-lg text-sm font-semibold hover:bg-red-600">
              🏠 Return Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SimpleDrone;