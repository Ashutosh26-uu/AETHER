#!/usr/bin/env python3
"""
AETHER Dynamic System Launcher
Automatically detects device type and launches appropriate configuration
"""

import os
import sys
import subprocess
import time
import platform
import json
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from dynamic_device_detector import DynamicDeviceDetector

class DynamicSystemLauncher:
    def __init__(self):
        self.detector = DynamicDeviceDetector()
        self.device_data = self.detector.get_comprehensive_device_data()
        self.project_root = Path(__file__).parent
        
    def display_device_info(self):
        """Display comprehensive device information"""
        device = self.device_data['device_info']
        manufacturer = self.device_data['manufacturer_info']
        config = self.device_data['device_config']
        capabilities = self.detector.get_device_capabilities()
        
        print("🌐 AETHER Dynamic System Launcher")
        print("=" * 70)
        print(f"🔍 Device Detection Complete")
        print("-" * 40)
        print(f"📱 Device Type: {device['type'].replace('_', ' ').title()}")
        print(f"🏭 Manufacturer: {manufacturer['brand']} {manufacturer['model']}")
        print(f"💻 System: {device['system'].title()} ({device['architecture']})")
        print(f"📦 Category: {device['category'].replace('_', ' ').title()}")
        print(f"📐 Form Factor: {device['form_factor'].replace('_', ' ').title()}")
        print(f"🔋 Power Source: {device['power_source'].replace('_', ' ').title()}")
        print(f"🚗 Vehicle Analogy: {config['vehicle_analogy']}")
        print(f"⚡ Update Interval: {config['update_interval']}s")
        
        print(f"\n🎯 Device Capabilities:")
        for capability, available in capabilities.items():
            status = "✅" if available else "❌"
            print(f"  {status} {capability.replace('_', ' ').title()}")
        
        print(f"\n📊 Health Metrics: {', '.join(config['health_metrics'])}")
        print(f"🔧 Features: {', '.join(config.get('features', [])[:5])}...")
        
        return device, manufacturer, config, capabilities
    
    def get_optimal_configuration(self):
        """Get optimal configuration based on device type"""
        device = self.device_data['device_info']
        config = self.device_data['device_config']
        
        # Device-specific configurations
        configurations = {
            # Mobile Devices
            'android_phone': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 1,
                'frontend_build': 'development',
                'features': ['mobile_optimized', 'battery_aware', 'touch_interface']
            },
            'iphone': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 1,
                'frontend_build': 'development',
                'features': ['ios_optimized', 'battery_aware', 'touch_interface']
            },
            
            # Tablets
            'windows_tablet': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 2,
                'frontend_build': 'development',
                'features': ['tablet_optimized', 'touch_interface', 'hybrid_mode']
            },
            'ipad': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 2,
                'frontend_build': 'development',
                'features': ['ipad_optimized', 'touch_interface', 'apple_pencil']
            },
            
            # Laptops
            'windows_laptop': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 2,
                'frontend_build': 'development',
                'features': ['laptop_optimized', 'battery_management', 'performance_mode']
            },
            'gaming_laptop': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 4,
                'frontend_build': 'production',
                'features': ['gaming_optimized', 'high_performance', 'thermal_monitoring']
            },
            'macbook_apple_silicon': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 3,
                'frontend_build': 'development',
                'features': ['apple_silicon_optimized', 'energy_efficient', 'macos_integration']
            },
            
            # Desktops
            'desktop_pc': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 4,
                'frontend_build': 'production',
                'features': ['desktop_optimized', 'high_performance', 'multi_monitor']
            },
            'workstation': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 8,
                'frontend_build': 'production',
                'features': ['workstation_optimized', 'enterprise_grade', 'professional_tools']
            },
            
            # IoT Devices
            'raspberry_pi': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 1,
                'frontend_build': 'lightweight',
                'features': ['iot_optimized', 'low_power', 'gpio_support']
            },
            'nvidia_jetson': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 2,
                'frontend_build': 'development',
                'features': ['ai_optimized', 'cuda_support', 'edge_computing']
            },
            
            # Vehicle Systems
            'automotive_ecu': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 1,
                'frontend_build': 'embedded',
                'features': ['automotive_grade', 'real_time', 'can_bus_support']
            },
            'truck_telematics': {
                'backend_port': 8000,
                'frontend_port': 3000,
                'backend_workers': 2,
                'frontend_build': 'embedded',
                'features': ['fleet_optimized', 'gps_tracking', 'driver_monitoring']
            }
        }
        
        device_type = device['type']
        return configurations.get(device_type, configurations['desktop_pc'])
    
    def setup_environment(self, config):
        """Setup environment variables and configurations"""
        os.environ['AETHER_DEVICE_TYPE'] = self.device_data['device_info']['type']
        os.environ['AETHER_MANUFACTURER'] = self.device_data['manufacturer_info']['brand']
        os.environ['AETHER_BACKEND_PORT'] = str(config['backend_port'])
        os.environ['AETHER_FRONTEND_PORT'] = str(config['frontend_port'])
        os.environ['AETHER_UPDATE_INTERVAL'] = str(self.device_data['device_config']['update_interval'])
        
        # Create device-specific config file
        config_file = self.project_root / 'device_config.json'
        with open(config_file, 'w') as f:
            json.dump({
                'device_data': self.device_data,
                'runtime_config': config,
                'launch_timestamp': time.time()
            }, f, indent=2)
        
        print(f"✅ Environment configured for {self.device_data['device_info']['type']}")
    
    def install_dependencies(self, config):
        """Install device-specific dependencies"""
        print("📦 Installing dependencies...")
        
        # Backend dependencies
        backend_requirements = self.project_root / 'requirements.txt'
        if backend_requirements.exists():
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(backend_requirements)], 
                             check=True, capture_output=True)
                print("✅ Backend dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Warning: Some backend dependencies failed to install: {e}")
        
        # Frontend dependencies
        frontend_dir = self.project_root / 'frontend'
        package_json = frontend_dir / 'package.json'
        
        if package_json.exists():
            try:
                # Check if npm is available
                subprocess.run(['npm', '--version'], check=True, capture_output=True)
                
                # Install frontend dependencies
                subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True, capture_output=True)
                print("✅ Frontend dependencies installed")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️ Warning: npm not found or frontend dependencies failed to install")
    
    def launch_backend(self, config):
        """Launch the backend server"""
        backend_script = self.project_root / 'backend' / 'universal_backend.py'
        
        if not backend_script.exists():
            print("❌ Backend script not found!")
            return None
        
        print(f"🚀 Launching backend server on port {config['backend_port']}...")
        
        # Launch backend with device-specific configuration
        cmd = [
            sys.executable, 
            str(backend_script)
        ]
        
        try:
            backend_process = subprocess.Popen(
                cmd,
                cwd=self.project_root / 'backend',
                env=os.environ.copy()
            )
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            if backend_process.poll() is None:
                print(f"✅ Backend server started (PID: {backend_process.pid})")
                return backend_process
            else:
                print("❌ Backend server failed to start")
                return None
                
        except Exception as e:
            print(f"❌ Error launching backend: {e}")
            return None
    
    def launch_frontend(self, config):
        """Launch the frontend development server"""
        frontend_dir = self.project_root / 'frontend'
        package_json = frontend_dir / 'package.json'
        
        if not package_json.exists():
            print("⚠️ Frontend not found, backend-only mode")
            return None
        
        print(f"🎨 Launching frontend server on port {config['frontend_port']}...")
        
        try:
            # Check if npm is available
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
            
            # Update App.js to use DynamicDeviceDashboard
            self.update_frontend_app()
            
            # Launch frontend
            env = os.environ.copy()
            env['PORT'] = str(config['frontend_port'])
            
            frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=frontend_dir,
                env=env
            )
            
            print(f"✅ Frontend server started (PID: {frontend_process.pid})")
            return frontend_process
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ npm not found, backend-only mode")
            return None
        except Exception as e:
            print(f"❌ Error launching frontend: {e}")
            return None
    
    def update_frontend_app(self):
        """Update frontend App.js to use DynamicDeviceDashboard"""
        app_js_path = self.project_root / 'frontend' / 'src' / 'App.js'
        
        if app_js_path.exists():
            app_content = f'''import React from 'react';
import './App.css';
import DynamicDeviceDashboard from './DynamicDeviceDashboard';

function App() {{
  return (
    <div className="App">
      <DynamicDeviceDashboard />
    </div>
  );
}}

export default App;
'''
            with open(app_js_path, 'w') as f:
                f.write(app_content)
            print("✅ Frontend configured for dynamic device dashboard")
    
    def launch_system(self):
        """Launch the complete dynamic system"""
        print("🚀 AETHER Dynamic System Launch Sequence")
        print("=" * 50)
        
        # Display device information
        device, manufacturer, config, capabilities = self.display_device_info()
        
        # Get optimal configuration
        runtime_config = self.get_optimal_configuration()
        
        print(f"\n⚙️ Optimal Configuration:")
        print(f"  Backend Workers: {runtime_config['backend_workers']}")
        print(f"  Frontend Build: {runtime_config['frontend_build']}")
        print(f"  Features: {', '.join(runtime_config['features'])}")
        
        # Setup environment
        self.setup_environment(runtime_config)
        
        # Install dependencies
        self.install_dependencies(runtime_config)
        
        print(f"\n🚀 Starting services...")
        
        # Launch backend
        backend_process = self.launch_backend(runtime_config)
        
        if not backend_process:
            print("❌ Failed to start backend. Exiting.")
            return
        
        # Launch frontend
        frontend_process = self.launch_frontend(runtime_config)
        
        # Display access information
        print(f"\n✅ AETHER Dynamic System Running!")
        print("=" * 50)
        print(f"🌐 Device: {manufacturer['brand']} {device['type'].replace('_', ' ').title()}")
        print(f"🖥️ Backend: http://localhost:{runtime_config['backend_port']}")
        if frontend_process:
            print(f"🎨 Frontend: http://localhost:{runtime_config['frontend_port']}")
        print(f"📊 API Docs: http://localhost:{runtime_config['backend_port']}/docs")
        print(f"🔧 Device Config: {self.project_root}/device_config.json")
        
        print(f"\n💡 Device-Specific Features:")
        for feature in runtime_config['features']:
            print(f"  ✅ {feature.replace('_', ' ').title()}")
        
        print(f"\n🎯 Optimization Tips:")
        for tip in self.detector.get_optimization_tips()[:3]:
            print(f"  • {tip}")
        
        print(f"\n⚠️ Press Ctrl+C to stop all services")
        
        try:
            # Keep the launcher running
            while True:
                time.sleep(1)
                
                # Check if processes are still running
                if backend_process.poll() is not None:
                    print("❌ Backend process stopped unexpectedly")
                    break
                    
                if frontend_process and frontend_process.poll() is not None:
                    print("⚠️ Frontend process stopped")
                    frontend_process = None
                    
        except KeyboardInterrupt:
            print(f"\n🛑 Shutting down AETHER Dynamic System...")
            
            # Terminate processes
            if backend_process:
                backend_process.terminate()
                print("✅ Backend stopped")
                
            if frontend_process:
                frontend_process.terminate()
                print("✅ Frontend stopped")
                
            print("👋 AETHER Dynamic System shutdown complete")

def main():
    """Main entry point"""
    try:
        launcher = DynamicSystemLauncher()
        launcher.launch_system()
    except KeyboardInterrupt:
        print("\n👋 Launch cancelled by user")
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()