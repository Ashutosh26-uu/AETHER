import platform
import psutil
import socket
import uuid
import subprocess
import os
from datetime import datetime
from typing import Dict, Any

class DeviceInfoManager:
    def __init__(self):
        self.device_info = self._collect_device_info()
    
    def _collect_device_info(self) -> Dict[str, Any]:
        """Collect comprehensive device information"""
        try:
            # Basic system info
            uname = platform.uname()
            
            # CPU information
            cpu_info = self._get_cpu_info()
            
            # Memory information
            memory_info = self._get_memory_info()
            
            # Disk information
            disk_info = self._get_disk_info()
            
            # Network information
            network_info = self._get_network_info()
            
            # GPU information
            gpu_info = self._get_gpu_info()
            
            # Battery information
            battery_info = self._get_battery_info()
            
            return {
                'system': {
                    'os': uname.system,
                    'os_version': uname.version,
                    'os_release': uname.release,
                    'architecture': uname.machine,
                    'processor': uname.processor,
                    'platform': platform.platform(),
                    'python_version': platform.python_version(),
                    'hostname': uname.node,
                    'username': self._get_username(),
                    'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
                },
                'hardware': {
                    'cpu': cpu_info,
                    'memory': memory_info,
                    'disk': disk_info,
                    'gpu': gpu_info,
                    'battery': battery_info
                },
                'network': network_info,
                'device_id': self._generate_device_id(),
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': f'Failed to collect device info: {str(e)[:100]}'}
    
    def _get_cpu_info(self) -> Dict[str, Any]:
        """Get CPU information"""
        try:
            freq = psutil.cpu_freq()
            return {
                'physical_cores': psutil.cpu_count(logical=False) or 'Unknown',
                'logical_cores': psutil.cpu_count(logical=True) or 'Unknown',
                'max_frequency': f"{freq.max:.2f} MHz" if freq and freq.max else "Unknown",
                'current_frequency': f"{freq.current:.2f} MHz" if freq and freq.current else "Unknown",
                'usage_per_core': psutil.cpu_percent(percpu=True, interval=0.1),
                'total_usage': psutil.cpu_percent(interval=0.1),
                'architecture': platform.machine() or 'Unknown',
                'processor_name': platform.processor() or 'Unknown'
            }
        except Exception:
            return {'error': 'CPU info unavailable'}
    
    def _get_memory_info(self) -> Dict[str, Any]:
        """Get memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'total': f"{memory.total / (1024**3):.2f} GB",
                'available': f"{memory.available / (1024**3):.2f} GB",
                'used': f"{memory.used / (1024**3):.2f} GB",
                'percentage': f"{memory.percent}%",
                'swap_total': f"{swap.total / (1024**3):.2f} GB",
                'swap_used': f"{swap.used / (1024**3):.2f} GB",
                'swap_percentage': f"{swap.percent}%"
            }
        except Exception:
            return {'error': 'Memory info unavailable'}
    
    def _get_disk_info(self) -> Dict[str, Any]:
        """Get disk information"""
        try:
            disk_usage = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            disk_io = psutil.disk_io_counters()
            
            # Get all disk partitions
            partitions = []
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    partitions.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'file_system': partition.fstype,
                        'total': f"{partition_usage.total / (1024**3):.2f} GB",
                        'used': f"{partition_usage.used / (1024**3):.2f} GB",
                        'free': f"{partition_usage.free / (1024**3):.2f} GB",
                        'percentage': f"{(partition_usage.used / partition_usage.total) * 100:.1f}%"
                    })
                except PermissionError:
                    continue
            
            return {
                'main_disk': {
                    'total': f"{disk_usage.total / (1024**3):.2f} GB",
                    'used': f"{disk_usage.used / (1024**3):.2f} GB",
                    'free': f"{disk_usage.free / (1024**3):.2f} GB",
                    'percentage': f"{(disk_usage.used / disk_usage.total) * 100:.1f}%"
                },
                'io_stats': {
                    'read_bytes': f"{disk_io.read_bytes / (1024**3):.2f} GB" if disk_io else "Unknown",
                    'write_bytes': f"{disk_io.write_bytes / (1024**3):.2f} GB" if disk_io else "Unknown",
                    'read_count': disk_io.read_count if disk_io else "Unknown",
                    'write_count': disk_io.write_count if disk_io else "Unknown"
                },
                'partitions': partitions
            }
        except Exception:
            return {'error': 'Disk info unavailable'}
    
    def _get_network_info(self) -> Dict[str, Any]:
        """Get network information"""
        try:
            # Get network interfaces
            interfaces = []
            for interface_name, interface_addresses in psutil.net_if_addrs().items():
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        interfaces.append({
                            'interface': interface_name,
                            'ip_address': address.address,
                            'netmask': address.netmask,
                            'broadcast': address.broadcast
                        })
            
            # Get network IO stats
            net_io = psutil.net_io_counters()
            
            return {
                'hostname': socket.gethostname(),
                'ip_address': socket.gethostbyname(socket.gethostname()),
                'interfaces': interfaces,
                'io_stats': {
                    'bytes_sent': f"{net_io.bytes_sent / (1024**2):.2f} MB",
                    'bytes_recv': f"{net_io.bytes_recv / (1024**2):.2f} MB",
                    'packets_sent': net_io.packets_sent,
                    'packets_recv': net_io.packets_recv
                }
            }
        except Exception:
            return {'error': 'Network info unavailable'}
    
    def _get_gpu_info(self) -> Dict[str, Any]:
        """Get GPU information"""
        try:
            gpu_info = {'gpus': []}
            
            # Try to get GPU info on Windows
            if platform.system() == 'Windows':
                try:
                    result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[1:]:  # Skip header
                            if line.strip():
                                gpu_info['gpus'].append({'name': line.strip()})
                except Exception:
                    pass
            
            # Fallback
            if not gpu_info['gpus']:
                gpu_info = {'info': 'GPU information not available'}
            
            return gpu_info
        except Exception:
            return {'error': 'GPU info unavailable'}
    
    def _get_battery_info(self) -> Dict[str, Any]:
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                return {
                    'percentage': f"{battery.percent}%",
                    'plugged_in': battery.power_plugged,
                    'time_left': f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
                }
            else:
                return {'info': 'No battery detected (Desktop/Server)'}
        except Exception:
            return {'error': 'Battery info unavailable'}
    
    def _generate_device_id(self) -> str:
        """Generate unique device ID"""
        try:
            mac_int = uuid.getnode()
            mac = ':'.join(['{:02x}'.format((mac_int >> elements) & 0xff) 
                           for elements in range(0,2*6,2)][::-1])
            hostname = socket.gethostname()
            return f"{hostname}_{mac}_{abs(hash(platform.machine())) % 10000}"
        except Exception:
            return f"DEVICE_{abs(hash(platform.node() + platform.machine())) % 10000}"
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get current device information"""
        return self.device_info
    
    def refresh_device_info(self) -> Dict[str, Any]:
        """Refresh and return updated device information"""
        self.device_info = self._collect_device_info()
        return self.device_info
    
    def get_system_summary(self) -> Dict[str, Any]:
        """Get a summary of key system information"""
        try:
            battery = psutil.sensors_battery()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\' if platform.system() == 'Windows' else '/')
            
            return {
                'device_type': 'Laptop' if battery else 'Desktop',
                'os': f"{platform.system()} {platform.release()}",
                'cpu': f"{psutil.cpu_count(logical=True)} cores",
                'memory': f"{memory.total / (1024**3):.2f} GB",
                'disk': f"{disk.total / (1024**3):.2f} GB",
                'hostname': platform.node(),
                'uptime': self._calculate_uptime()
            }
        except Exception:
            return {'error': 'Summary unavailable'}
    
    def _calculate_uptime(self) -> str:
        """Calculate system uptime"""
        try:
            boot_time = psutil.boot_time()
            uptime_seconds = datetime.now().timestamp() - boot_time
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{days}d {hours}h {minutes}m"
        except Exception:
            return "0d 0h 0m"

    def _get_username(self) -> str:
        """Get current username safely"""
        try:
            if hasattr(os, 'getlogin'):
                return os.getlogin()
            elif 'USERNAME' in os.environ:
                return os.environ['USERNAME']
            elif 'USER' in os.environ:
                return os.environ['USER']
            else:
                return 'Unknown'
        except Exception:
            return 'Unknown'

# Global device info manager
device_manager = DeviceInfoManager()