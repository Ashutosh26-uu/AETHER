import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import VehicleHealth from './pages/VehicleHealth';
import FleetManagement from './pages/FleetManagement';
import Navigation from './components/Navigation';
import { WebSocketProvider } from './services/WebSocketService';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <WebSocketProvider>
      <Router>
        <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
          <div className="bg-gray-50 dark:bg-gray-900 min-h-screen">
            <Navigation darkMode={darkMode} setDarkMode={setDarkMode} />
            <main className="container mx-auto px-4 py-8">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/health" element={<VehicleHealth />} />
                <Route path="/fleet" element={<FleetManagement />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </WebSocketProvider>
  );
}

export default App;