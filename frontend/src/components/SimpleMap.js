import React, { useState } from 'react';

const SimpleMap = ({ vehicleData }) => {
  const [mapMode, setMapMode] = useState('satellite');
  const lat = vehicleData?.location?.latitude || 28.6139;
  const lon = vehicleData?.location?.longitude || 77.2090;

  return (
    <div className="relative w-full h-96 bg-gradient-to-br from-blue-900 via-blue-700 to-blue-500 rounded-xl overflow-hidden">
      <div className="absolute top-4 right-4 z-10 space-y-2">
        <button
          onClick={() => setMapMode(mapMode === 'satellite' ? 'street' : 'satellite')}
          className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-lg text-white text-sm hover:bg-white/30"
        >
          {mapMode === 'satellite' ? '🛰️ Satellite' : '🗺️ Street'}
        </button>
      </div>

      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div className="relative">
          <div className="w-6 h-6 bg-red-500 rounded-full animate-pulse shadow-lg"></div>
          <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-black/70 text-white px-2 py-1 rounded text-xs whitespace-nowrap">
            🚗 AETHER_001
          </div>
        </div>
      </div>

      <div className="absolute bottom-4 right-4 bg-black/50 text-white px-3 py-1 rounded-lg text-xs">
        📍 {lat.toFixed(4)}, {lon.toFixed(4)}
      </div>
    </div>
  );
};

export default SimpleMap;