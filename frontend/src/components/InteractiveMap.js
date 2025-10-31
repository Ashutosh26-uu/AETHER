import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const InteractiveMap = ({ vehicleData }) => {
  const [mapMode, setMapMode] = useState('satellite');
  const [showTraffic, setShowTraffic] = useState(true);
  const [showWeather, setShowWeather] = useState(true);

  const lat = vehicleData?.location?.latitude || 28.6139;
  const lon = vehicleData?.location?.longitude || 77.2090;

  return (
    <div className="relative w-full h-96 bg-gradient-to-br from-blue-900 via-blue-700 to-blue-500 rounded-xl overflow-hidden">
      {/* Map Controls */}
      <div className="absolute top-4 right-4 z-10 space-y-2">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setMapMode(mapMode === 'satellite' ? 'street' : 'satellite')}
          className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-lg text-white text-sm"
        >
          {mapMode === 'satellite' ? '🛰️ Satellite' : '🗺️ Street'}
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          onClick={() => setShowTraffic(!showTraffic)}
          className={`px-3 py-1 backdrop-blur-sm rounded-lg text-white text-sm ${showTraffic ? 'bg-green-500/30' : 'bg-white/20'}`}
        >
          🚦 Traffic
        </motion.button>
        <motion.button
          whileHover={{ scale: 1.05 }}
          onClick={() => setShowWeather(!showWeather)}
          className={`px-3 py-1 backdrop-blur-sm rounded-lg text-white text-sm ${showWeather ? 'bg-blue-500/30' : 'bg-white/20'}`}
        >
          🌤️ Weather
        </motion.button>
      </div>

      {/* Vehicle Position */}
      <motion.div
        animate={{ 
          x: [0, 10, 0], 
          y: [0, -5, 0] 
        }}
        transition={{ 
          duration: 3, 
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
      >
        <div className="relative">
          <div className="w-6 h-6 bg-red-500 rounded-full animate-pulse shadow-lg"></div>
          <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/70 text-white px-2 py-1 rounded text-xs whitespace-nowrap">
            🚗 AETHER_001
          </div>
        </div>
      </motion.div>

      {/* Route Path */}
      <svg className="absolute inset-0 w-full h-full">
        <motion.path
          d="M 50 300 Q 200 200 350 150 T 550 100"
          stroke="#00ff88"
          strokeWidth="3"
          fill="none"
          strokeDasharray="10,5"
          initial={{ pathLength: 0 }}
          animate={{ pathLength: 1 }}
          transition={{ duration: 2, ease: "easeInOut" }}
        />
      </svg>

      {/* Traffic Indicators */}
      {showTraffic && (
        <div className="absolute bottom-4 left-4 space-y-1">
          <div className="flex items-center space-x-2 text-white text-sm">
            <div className="w-3 h-3 bg-green-400 rounded-full"></div>
            <span>Light Traffic</span>
          </div>
          <div className="flex items-center space-x-2 text-white text-sm">
            <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
            <span>Moderate Traffic</span>
          </div>
        </div>
      )}

      {/* Weather Overlay */}
      {showWeather && (
        <div className="absolute top-4 left-4 bg-white/20 backdrop-blur-sm rounded-lg p-3 text-white">
          <div className="text-sm">🌤️ Clear Sky</div>
          <div className="text-xs">28°C • Visibility: 10km</div>
        </div>
      )}

      {/* Coordinates */}
      <div className="absolute bottom-4 right-4 bg-black/50 text-white px-3 py-1 rounded-lg text-xs">
        📍 {lat.toFixed(4)}, {lon.toFixed(4)}
      </div>
    </div>
  );
};

export default InteractiveMap;