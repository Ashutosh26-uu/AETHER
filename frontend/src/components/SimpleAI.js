import React, { useState, useEffect } from 'react';
import { Brain, Zap, Shield, TrendingUp } from 'lucide-react';

const SimpleAI = ({ vehicleData }) => {
  const [activeInsight, setActiveInsight] = useState(0);

  const insights = [
    {
      icon: Brain,
      title: "AI Health Prediction",
      value: "95%",
      trend: "+2%",
      color: "bg-purple-500",
      description: "Vehicle health optimal for next 2,500km"
    },
    {
      icon: Shield,
      title: "Safety Score",
      value: "98/100",
      trend: "+5",
      color: "bg-green-500",
      description: "Excellent safety conditions detected"
    },
    {
      icon: Zap,
      title: "Efficiency AI",
      value: "87%",
      trend: "+12%",
      color: "bg-yellow-500",
      description: "Fuel efficiency optimized by AI routing"
    },
    {
      icon: TrendingUp,
      title: "Predictive Analytics",
      value: "Next Service",
      trend: "45 days",
      color: "bg-blue-500",
      description: "AI predicts optimal maintenance timing"
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveInsight((prev) => (prev + 1) % insights.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {insights.map((insight, index) => {
          const Icon = insight.icon;
          return (
            <div
              key={index}
              className={`relative overflow-hidden rounded-xl ${insight.color} p-6 text-white cursor-pointer transform hover:scale-105 transition-transform ${
                activeInsight === index ? 'ring-4 ring-white/50' : ''
              }`}
              onClick={() => setActiveInsight(index)}
            >
              <div className="flex items-center justify-between">
                <Icon className="h-8 w-8" />
                <div className="text-right">
                  <div className="text-2xl font-bold">{insight.value}</div>
                  <div className="text-sm opacity-80">{insight.trend}</div>
                </div>
              </div>
              <div className="mt-4">
                <div className="font-semibold">{insight.title}</div>
                <div className="text-sm opacity-90">{insight.description}</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center space-x-2 mb-4">
          <Brain className="h-6 w-6 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Predictions</h3>
          <div className="w-2 h-2 bg-purple-600 rounded-full animate-pulse" />
        </div>

        <div className="space-y-3">
          {[
            { time: "2 min", event: "Traffic congestion ahead", probability: 85, type: "warning" },
            { time: "15 min", event: "Optimal fuel stop available", probability: 92, type: "info" },
            { time: "1 hour", event: "Weather change predicted", probability: 78, type: "weather" },
            { time: "2 days", event: "Tire pressure check recommended", probability: 95, type: "maintenance" }
          ].map((prediction, index) => (
            <div
              key={index}
              className="flex items-center space-x-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
            >
              <div className={`w-3 h-3 rounded-full ${
                prediction.type === 'warning' ? 'bg-yellow-500' :
                prediction.type === 'info' ? 'bg-blue-500' :
                prediction.type === 'weather' ? 'bg-cyan-500' :
                'bg-green-500'
              }`} />
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900 dark:text-white">
                  {prediction.event}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  In {prediction.time} • {prediction.probability}% confidence
                </div>
              </div>
              <div className="text-xs bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-2 py-1 rounded">
                AI
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default SimpleAI;