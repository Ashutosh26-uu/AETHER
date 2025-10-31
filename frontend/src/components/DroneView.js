import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Drone, Camera, Radar, Zap, MapPin, AlertCircle } from 'lucide-react';

const DroneView = () => {
  const [droneStatus, setDroneStatus] = useState('active');
  const [missionType, setMissionType] = useState('surveillance');
  const [droneData, setDroneData] = useState({
    altitude: 45,
    battery: 78,
    speed: 25,
    temperature: 28,
    signal: 95
  });

  const [detectedObjects, setDetectedObjects] = useState([
    { id: 1, type: 'vehicle', confidence: 95, x: 120, y: 80 },
    { id: 2, type: 'person', confidence: 87, x: 200, y: 150 },
    { id: 3, type: 'obstacle', confidence: 92, x: 300, y: 200 }
  ]);

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
      {/* Drone Control Panel */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 rounded-xl p-6 text-white"
      >
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            >
              <Drone className="h-8 w-8 text-blue-400" />
            </motion.div>
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

        {/* Drone Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[
            { label: 'Altitude', value: `${droneData.altitude.toFixed(1)}m`, icon: '📏' },
            { label: 'Battery', value: `${droneData.battery.toFixed(1)}%`, icon: '🔋' },
            { label: 'Speed', value: `${droneData.speed.toFixed(1)} km/h`, icon: '⚡' },
            { label: 'Signal', value: `${droneData.signal.toFixed(0)}%`, icon: '📡' },
            { label: 'Temp', value: `${droneData.temperature}°C`, icon: '🌡️' }
          ].map((stat, index) => (
            <motion.div
              key={index}
              whileHover={{ scale: 1.05 }}
              className="bg-white/10 rounded-lg p-3 text-center"
            >
              <div className="text-2xl mb-1">{stat.icon}</div>
              <div className="text-lg font-bold">{stat.value}</div>
              <div className="text-xs text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Live Drone Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Camera Feed */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-black rounded-xl overflow-hidden"
        >
          <div className="bg-red-600 text-white px-4 py-2 flex items-center space-x-2">
            <div className="w-3 h-3 bg-white rounded-full animate-pulse"></div>
            <span className="text-sm font-semibold">LIVE FEED</span>
            <Camera className="h-4 w-4 ml-auto" />
          </div>
          
          <div className="relative h-64 bg-gradient-to-br from-gray-800 to-gray-900">
            {/* Simulated camera view */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
            
            {/* Object Detection Overlays */}
            <AnimatePresence>
              {detectedObjects.map((obj) => (
                <motion.div
                  key={obj.id}
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0 }}
                  className="absolute border-2 border-green-400 rounded"
                  style={{
                    left: obj.x,
                    top: obj.y,
                    width: 60,
                    height: 40
                  }}
                >
                  <div className="bg-green-400 text-black text-xs px-1 -mt-5">
                    {obj.type} {obj.confidence}%
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {/* Crosshair */}
            <div className="absolute inset-0 flex items-center justify-center">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                className="w-16 h-16 border-2 border-green-400 rounded-full border-dashed"
              />
            </div>

            {/* HUD Elements */}
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
        </motion.div>

        {/* Mission Control */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white dark:bg-gray-800 rounded-xl p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Mission Control</h3>
          
          {/* Mission Types */}
          <div className="space-y-3 mb-6">
            {['surveillance', 'emergency', 'inspection', 'patrol'].map((type) => (
              <motion.button
                key={type}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setMissionType(type)}
                className={`w-full p-3 rounded-lg text-left transition-colors ${
                  missionType === type
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
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
              </motion.button>
            ))}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-2 gap-3">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 bg-green-500 text-white rounded-lg text-sm font-semibold"
            >
              🚁 Deploy
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-3 bg-red-500 text-white rounded-lg text-sm font-semibold"
            >
              🏠 Return Home
            </motion.button>
          </div>
        </motion.div>
      </div>

      {/* Detected Threats/Objects */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white dark:bg-gray-800 rounded-xl p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">AI Object Detection</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {detectedObjects.map((obj) => (
            <motion.div
              key={obj.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-4 border border-gray-200 dark:border-gray-600 rounded-lg"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold capitalize text-gray-900 dark:text-white">
                  {obj.type}
                </span>
                <span className="text-sm text-green-600 font-semibold">
                  {obj.confidence}%
                </span>
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                Position: ({obj.x}, {obj.y})
              </div>
              <motion.div
                className="mt-2 h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden"
              >
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${obj.confidence}%` }}
                  transition={{ duration: 1, delay: 0.5 }}
                  className="h-full bg-green-500"
                />
              </motion.div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default DroneView;