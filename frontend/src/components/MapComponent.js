import React, { useRef, useEffect } from 'react';

const MapComponent = ({ latitude, longitude, vehicleData }) => {
  const mapContainer = useRef(null);
  const map = useRef(null);

  useEffect(() => {
    // Simple map implementation without external dependencies
    if (mapContainer.current && !map.current) {
      // Create a simple map visualization
      const mapDiv = mapContainer.current;
      mapDiv.innerHTML = `
        <div class="relative w-full h-64 bg-gray-200 dark:bg-gray-700 rounded-lg overflow-hidden">
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="text-center">
              <div class="w-4 h-4 bg-blue-600 rounded-full mx-auto mb-2 animate-pulse"></div>
              <p class="text-sm text-gray-600 dark:text-gray-300">
                Lat: ${latitude.toFixed(4)}, Lon: ${longitude.toFixed(4)}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Speed: ${Math.round(vehicleData?.navigation?.current_speed || 0)} km/h
              </p>
            </div>
          </div>
          <div class="absolute top-2 left-2 bg-white dark:bg-gray-800 px-2 py-1 rounded text-xs">
            Live Tracking
          </div>
        </div>
      `;
    }
  }, [latitude, longitude, vehicleData]);

  return <div ref={mapContainer} className="w-full h-64"></div>;
};

export default MapComponent;