import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Car, AlertTriangle, Battery, Navigation, Thermometer, Zap, Shield } from 'lucide-react';
import SimpleMap from '../components/SimpleMap';
import SimpleAI from '../components/SimpleAI';
import SimpleDrone from '../components/SimpleDrone';
import { useWebSocket } from '../services/WebSocketService';

const Dashboard = () => {
  const [vehicleData, setVehicleData] = useState(null);
  const [healthHistory, setHealthHistory] = useState([]);
  const { lastMessage, connectionStatus } = useWebSocket();

  useEffect(() => {
    if (lastMessage) {
      setVehicleData(lastMessage);
      setHealthHistory(prev => [...prev.slice(-20), {
        time: new Date().toLocaleTimeString(),
        health: lastMessage.health?.overall_score || 0,
        battery: lastMessage.health?.battery_level || 0,
        temp: lastMessage.health?.engine_temp || 0
      }]);
    }
  }, [lastMessage]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'LOW': return 'text-green-600';
      case 'MEDIUM': return 'text-yellow-600';
      case 'HIGH': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  if (!vehicleData) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Connecting to vehicle...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 rounded-xl shadow-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">🚀 AETHER Dashboard</h1>
            <p className="text-blue-100">
              Vehicle ID: {vehicleData?.vehicle_id || 'AETHER_001'} • AI-Powered Mobility System
            </p>
          </div>
          <div className={`px-4 py-2 rounded-full text-sm font-semibold animate-pulse ${
            connectionStatus === 'connected' 
              ? 'bg-green-500 text-white' 
              : 'bg-red-500 text-white'
          }`}>
            {connectionStatus === 'connected' ? '🟢 LIVE' : '🔴 OFFLINE'}
          </div>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          {
            icon: Car,
            title: 'Health Score',
            value: `${Math.round(vehicleData?.health?.overall_score || 85)}%`,
            color: 'bg-green-500',
            bgColor: 'bg-green-50 dark:bg-green-900/20'
          },
          {
            icon: Shield,
            title: 'Safety Status',
            value: vehicleData?.safety?.collision_risk || 'OPTIMAL',
            color: 'bg-blue-500',
            bgColor: 'bg-blue-50 dark:bg-blue-900/20'
          },
          {
            icon: Battery,
            title: 'Battery Level',
            value: `${Math.round(vehicleData?.health?.battery_level || 78)}%`,
            color: 'bg-yellow-500',
            bgColor: 'bg-yellow-50 dark:bg-yellow-900/20'
          },
          {
            icon: Zap,
            title: 'Current Speed',
            value: `${Math.round(vehicleData?.navigation?.current_speed || 65)} km/h`,
            color: 'bg-purple-500',
            bgColor: 'bg-purple-50 dark:bg-purple-900/20'
          }
        ].map((card, index) => {
          const Icon = card.icon;
          return (
            <div
              key={index}
              className={`${card.bgColor} rounded-xl shadow-lg p-6 cursor-pointer hover:scale-105 transform transition-transform`}
            >
              <div className="flex items-center justify-between">
                <div className={`p-3 rounded-lg ${card.color}`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-gray-900 dark:text-white animate-pulse">
                    {card.value}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{card.title}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* AI Insights Section */}
      <SimpleAI vehicleData={vehicleData} />

      {/* Map and Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-2 mb-4">
            <div className="animate-spin">🛰️</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Satellite Navigation</h3>
          </div>
          <SimpleMap vehicleData={vehicleData} />
        </div>

        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">📊 Real-time Analytics</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={healthHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#6B7280" />
              <YAxis stroke="#6B7280" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#F9FAFB'
                }} 
              />
              <Line type="monotone" dataKey="health" stroke="#10B981" strokeWidth={3} />
              <Line type="monotone" dataKey="battery" stroke="#F59E0B" strokeWidth={3} />
              <Line type="monotone" dataKey="temp" stroke="#EF4444" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Drone Control Section */}
      <SimpleDrone />

      {/* Smart Alerts */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">🚨 Smart Alerts & Notifications</h3>
        <div className="space-y-3">
          {[
            {
              condition: (vehicleData?.health?.overall_score || 85) < 70,
              icon: '⚠️',
              message: 'Vehicle health below optimal level - AI recommends service check',
              color: 'yellow'
            },
            {
              condition: vehicleData?.safety?.collision_risk === 'HIGH',
              icon: '🚨',
              message: 'High collision risk detected - Activating emergency protocols',
              color: 'red'
            },
            {
              condition: (vehicleData?.health?.battery_level || 78) < 20,
              icon: '🔋',
              message: 'Low battery level - Nearest charging station: 2.3km',
              color: 'orange'
            },
            {
              condition: true,
              icon: '✅',
              message: 'All systems operational - AI monitoring 847 data points',
              color: 'green'
            }
          ].filter(alert => alert.condition).map((alert, index) => (
            <div
              key={index}
              className={`flex items-center p-4 bg-${alert.color}-50 dark:bg-${alert.color}-900/20 rounded-lg border-l-4 border-${alert.color}-500`}
            >
              <div className="text-2xl mr-3 animate-pulse">
                {alert.icon}
              </div>
              <span className={`text-${alert.color}-800 dark:text-${alert.color}-200 flex-1`}>
                {alert.message}
              </span>
              <button className={`px-3 py-1 bg-${alert.color}-500 text-white rounded-lg text-sm hover:opacity-80`}>
                Action
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;