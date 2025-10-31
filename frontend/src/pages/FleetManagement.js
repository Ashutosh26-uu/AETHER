import React from 'react';
import { Truck, Users, AlertCircle } from 'lucide-react';

const FleetManagement = () => {
  const fleetData = {
    total_vehicles: 25,
    active_vehicles: 23,
    maintenance_required: 2,
    emergency_alerts: 0
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Fleet Management</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <Truck className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Total Vehicles</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{fleetData.total_vehicles}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Active</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{fleetData.active_vehicles}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-yellow-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Maintenance</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{fleetData.maintenance_required}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div className="flex items-center">
            <AlertCircle className="h-8 w-8 text-red-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-600 dark:text-gray-300">Alerts</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">{fleetData.emergency_alerts}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FleetManagement;