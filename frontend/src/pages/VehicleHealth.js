import React from 'react';
import { Activity, AlertTriangle, CheckCircle } from 'lucide-react';

const VehicleHealth = () => {
  const healthData = {
    overall_score: 85,
    engine_temp: 92,
    battery_level: 78,
    oil_pressure: 42,
    brake_health: 95
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Vehicle Health</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <Activity className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Overall Health</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{healthData.overall_score}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertTriangle className="h-8 w-8 text-orange-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Engine Temp</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{healthData.engine_temp}°C</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <CheckCircle className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Battery</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{healthData.battery_level}%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VehicleHealth;