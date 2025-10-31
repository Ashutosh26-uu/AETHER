import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Zap, Shield, TrendingUp, AlertTriangle } from 'lucide-react';

const AIInsights = ({ vehicleData }) => {
  const [activeInsight, setActiveInsight] = useState(0);
  const [predictions, setPredictions] = useState([]);

  const insights = [
    {
      icon: Brain,
      title: "AI Health Prediction",
      value: "95%",
      trend: "+2%",
      color: "from-purple-500 to-pink-500",
      description: "Vehicle health optimal for next 2,500km"
    },
    {
      icon: Shield,
      title: "Safety Score",
      value: "98/100",
      trend: "+5",
      color: "from-green-500 to-emerald-500",
      description: "Excellent safety conditions detected"
    },
    {
      icon: Zap,
      title: "Efficiency AI",
      value: "87%",
      trend: "+12%",
      color: "from-yellow-500 to-orange-500",
      description: "Fuel efficiency optimized by AI routing"
    },
    {
      icon: TrendingUp,
      title: "Predictive Analytics",
      value: "Next Service",
      trend: "45 days",
      color: "from-blue-500 to-cyan-500",
      description: "AI predicts optimal maintenance timing"
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveInsight((prev) => (prev + 1) % insights.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Simulate AI predictions
    const newPredictions = [
      { time: "2 min", event: "Traffic congestion ahead", probability: 85, type: "warning" },
      { time: "15 min", event: "Optimal fuel stop available", probability: 92, type: "info" },
      { time: "1 hour", event: "Weather change predicted", probability: 78, type: "weather" },
      { time: "2 days", event: "Tire pressure check recommended", probability: 95, type: "maintenance" }
    ];
    setPredictions(newPredictions);
  }, [vehicleData]);

  return (
    <div className="space-y-6">
      {/* AI Insights Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {insights.map((insight, index) => {
          const Icon = insight.icon;
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={`relative overflow-hidden rounded-xl bg-gradient-to-br ${insight.color} p-6 text-white cursor-pointer`}
              whileHover={{ scale: 1.05, rotateY: 5 }}
              onClick={() => setActiveInsight(index)}
            >
              <div className="flex items-center justify-between">
                <Icon className="h-8 w-8" />
                <motion.div
                  animate={{ rotate: activeInsight === index ? 360 : 0 }}
                  transition={{ duration: 0.5 }}
                  className="text-right"
                >
                  <div className="text-2xl font-bold">{insight.value}</div>
                  <div className="text-sm opacity-80">{insight.trend}</div>
                </motion.div>
              </div>
              <div className="mt-4">
                <div className="font-semibold">{insight.title}</div>
                <div className="text-sm opacity-90">{insight.description}</div>
              </div>
              
              {/* Active indicator */}
              {activeInsight === index && (
                <motion.div
                  layoutId="activeIndicator"
                  className="absolute bottom-0 left-0 right-0 h-1 bg-white"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ duration: 0.3 }}
                />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* AI Predictions Timeline */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
      >
        <div className="flex items-center space-x-2 mb-4">
          <Brain className="h-6 w-6 text-purple-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">AI Predictions</h3>
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-2 h-2 bg-purple-600 rounded-full"
          />
        </div>

        <div className="space-y-3">
          <AnimatePresence>
            {predictions.map((prediction, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center space-x-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-700"
              >
                <div className="flex-shrink-0">
                  <div className={`w-3 h-3 rounded-full ${
                    prediction.type === 'warning' ? 'bg-yellow-500' :
                    prediction.type === 'info' ? 'bg-blue-500' :
                    prediction.type === 'weather' ? 'bg-cyan-500' :
                    'bg-green-500'
                  }`} />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900 dark:text-white">
                    {prediction.event}
                  </div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    In {prediction.time} • {prediction.probability}% confidence
                  </div>
                </div>
                <motion.div
                  className="text-xs bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-2 py-1 rounded"
                  whileHover={{ scale: 1.1 }}
                >
                  AI
                </motion.div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Real-time AI Processing */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-xl p-6 text-white"
      >
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold">AI Processing Status</h3>
            <p className="text-sm opacity-90">Real-time analysis of 847 data points</p>
          </div>
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-12 h-12 border-4 border-white/30 border-t-white rounded-full"
          />
        </div>
        
        <div className="mt-4 grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold">127ms</div>
            <div className="text-xs opacity-80">Response Time</div>
          </div>
          <div>
            <div className="text-2xl font-bold">99.8%</div>
            <div className="text-xs opacity-80">Accuracy</div>
          </div>
          <div>
            <div className="text-2xl font-bold">24/7</div>
            <div className="text-xs opacity-80">Monitoring</div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default AIInsights;