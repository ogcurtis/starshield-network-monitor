#!/usr/bin/env python3
"""
Starshield Network Monitor
Clean Python implementation with interface selection
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import json
import time
import threading
import psutil
from datetime import datetime, timedelta
import os
import requests
from ping3 import ping

app = Flask(__name__)

# Global monitoring data
monitoring_data = {
    'selected_interface': 'Ethernet 4',
    'available_interfaces': [],
    'gateway': '100.64.0.1',
    'dns': '198.54.100.65',
    'status': 'unknown',
    'latency': 0,
    'dns_latency': 0,
    'bandwidth': {'rx': 0, 'tx': 0},
    'uptime': 0,
    'last_check': None,
    'interface_found': False,
    
    # Enhanced metrics
    'last_down_time': None,
    'worst_latency': 0,
    'best_bandwidth': 0,
    'worst_bandwidth': float('inf'),
    'fast_com_speed': None,
    'last_fast_com_test': None,
    'downtime_count': 0,
    'performance_history': []
}

def get_all_interfaces():
    """Get all available network interfaces"""
    interfaces = psutil.net_if_addrs()
    interface_list = []
    
    for name, addresses in interfaces.items():
        # Skip loopback and virtual interfaces
        if name.startswith('lo') or name.startswith('docker') or name.startswith('veth'):
            continue
            
        interface_info = {
            'name': name,
            'addresses': []
        }
        
        for addr in addresses:
            if addr.family == 2:  # IPv4
                interface_info['addresses'].append({
                    'ip': addr.address,
                    'netmask': addr.netmask
                })
        
        if interface_info['addresses']:  # Only include interfaces with IPv4 addresses
            interface_list.append(interface_info)
    
    return interface_list

def get_interface_stats(interface_name):
    """Get statistics for a specific interface"""
    try:
        stats = psutil.net_io_counters(pernic=True)
        if interface_name in stats:
            return {
                'rx': stats[interface_name].bytes_recv,
                'tx': stats[interface_name].bytes_sent
            }
        return {'rx': 0, 'tx': 0}
    except Exception as e:
        print(f"Interface stats error: {e}")
        return {'rx': 0, 'tx': 0}

def ping_host(host, timeout=3):
    """Ping a host and return latency in ms"""
    try:
        # Try ping3 first
        result = ping(host, timeout=timeout)
        if result is not None:
            return round(result * 1000, 2)  # Convert to milliseconds

        # Fallback to subprocess ping
        if os.name == 'nt':  # Windows
            cmd = f"ping -n 1 -w {timeout*1000} {host}"
        else:  # Linux/Mac
            cmd = f"ping -c 1 -W {timeout} {host}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout+2)
        
        if result.returncode == 0:
            # Extract time from ping output
            output = result.stdout
            if "time=" in output:
                time_part = output.split("time=")[1].split()[0]
                time_value = float(time_part.replace("ms", ""))
                return time_value
        return None
    except Exception as e:
        print(f"Ping error for {host}: {e}")
        return None

def check_interface_status(interface_name):
    """Check if the network interface is up"""
    try:
        interfaces = psutil.net_if_addrs()
        if interface_name not in interfaces:
            return False, "Interface not found"
        
        addresses = interfaces[interface_name]
        
        # Check if interface has an IP address
        for addr in addresses:
            if addr.family == 2 and addr.address != '127.0.0.1':  # IPv4 and not localhost
                return True, f"Interface {interface_name} is up with IP {addr.address}"
        
        return False, f"Interface {interface_name} has no IP address"
    except Exception as e:
        return False, f"Error checking interface: {e}"

def run_fast_com_test():
    """Run a speed test using Fast.com API"""
    try:
        # Fast.com provides a simple API
        response = requests.get('https://api.fast.com/netflix/speedtest/v2', timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'targets' in data and data['targets']:
                # Get the first target URL
                target_url = data['targets'][0]['url']
                
                # Run a simple download test
                start_time = time.time()
                test_response = requests.get(target_url, timeout=30)
                end_time = time.time()
                
                if test_response.status_code == 200:
                    # Calculate speed (rough estimate)
                    data_size = len(test_response.content)
                    duration = end_time - start_time
                    speed_mbps = (data_size * 8) / (duration * 1024 * 1024)  # Convert to Mbps
                    
                    return {
                        'download_mbps': round(speed_mbps, 2),
                        'duration': round(duration, 2),
                        'data_size': data_size,
                        'timestamp': datetime.now().isoformat()
                    }
        
        # Fallback to ping-based test
        return run_ping_speed_test()
        
    except Exception as e:
        print(f"Fast.com test error: {e}")
        return run_ping_speed_test()

def run_ping_speed_test():
    """Fallback ping-based speed test"""
    try:
        results = []
        for size in [32, 64, 128, 512, 1024]:
            if os.name == 'nt':  # Windows
                cmd = f"ping -n 4 -l {size} {monitoring_data['gateway']}"
            else:
                cmd = f"ping -c 4 -s {size} {monitoring_data['gateway']}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Average' in line or 'avg' in line.lower():
                        avg_time = line.split('=')[-1].strip().replace('ms', '')
                        try:
                            results.append(float(avg_time))
                        except:
                            pass
                        break
        
        if results:
            avg_ping = sum(results) / len(results)
            return {
                'ping_results': results,
                'average_ping': round(avg_ping, 2),
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {'error': 'No ping results'}
            
    except Exception as e:
        return {'error': str(e)}

def update_performance_metrics(latency, bandwidth):
    """Update performance tracking metrics"""
    global monitoring_data
    
    # Update worst latency
    if latency and latency > monitoring_data['worst_latency']:
        monitoring_data['worst_latency'] = latency
    
    # Calculate current bandwidth in Mbps
    current_bandwidth = (bandwidth['rx'] + bandwidth['tx']) / (1024 * 1024)
    
    # Update best/worst bandwidth
    if current_bandwidth > monitoring_data['best_bandwidth']:
        monitoring_data['best_bandwidth'] = current_bandwidth
    
    if current_bandwidth < monitoring_data['worst_bandwidth'] and current_bandwidth > 0:
        monitoring_data['worst_bandwidth'] = current_bandwidth
    
    # Add to performance history (keep last 100 entries)
    monitoring_data['performance_history'].append({
        'timestamp': datetime.now().isoformat(),
        'latency': latency,
        'bandwidth': current_bandwidth
    })
    
    if len(monitoring_data['performance_history']) > 100:
        monitoring_data['performance_history'].pop(0)

def monitor_network():
    """Main monitoring function"""
    global monitoring_data
    
    try:
        # Update available interfaces
        monitoring_data['available_interfaces'] = get_all_interfaces()
        
        # Use selected interface
        selected_interface = monitoring_data.get('selected_interface')
        
        # Check interface status
        interface_up, status_msg = check_interface_status(selected_interface)
        
        # Track downtime
        if not interface_up and monitoring_data['status'] == 'online':
            monitoring_data['last_down_time'] = datetime.now().isoformat()
            monitoring_data['downtime_count'] += 1
        
        # Get interface info
        monitoring_data['interface_found'] = selected_interface in [iface['name'] for iface in monitoring_data['available_interfaces']]
        
        # Measure latency
        gateway_latency = ping_host(monitoring_data['gateway'])
        dns_latency = ping_host(monitoring_data['dns'])
        
        # Get bandwidth usage
        bandwidth = get_interface_stats(selected_interface)
        
        # Update performance metrics
        update_performance_metrics(gateway_latency, bandwidth)
        
        # Update monitoring data
        monitoring_data.update({
            'status': 'online' if interface_up else 'offline',
            'latency': gateway_latency or 0,
            'dns_latency': dns_latency or 0,
            'bandwidth': bandwidth,
            'uptime': monitoring_data['uptime'] + 1,
            'last_check': datetime.now().isoformat()
        })
        
        print(f"Monitor check: Status={monitoring_data['status']}, "
              f"Latency={monitoring_data['latency']}ms, "
              f"Interface={selected_interface}, "
              f"Worst Latency={monitoring_data['worst_latency']}ms")
              
    except Exception as e:
        print(f"Monitoring error: {e}")
        monitoring_data['status'] = 'error'

def run_scheduled_fast_com_test():
    """Run Fast.com speed test every 10 minutes"""
    try:
        print("Running Fast.com speed test...")
        speed_result = run_fast_com_test()
        monitoring_data['fast_com_speed'] = speed_result
        monitoring_data['last_fast_com_test'] = datetime.now().isoformat()
        print(f"Fast.com test completed: {speed_result}")
    except Exception as e:
        print(f"Fast.com test error: {e}")

def start_monitoring():
    """Start the monitoring thread"""
    def run_monitor():
        while True:
            monitor_network()
            time.sleep(5)  # Check every 5 seconds
    
    def run_scheduler():
        while True:
            # Run Fast.com test every 10 minutes
            if datetime.now().minute % 10 == 0 and datetime.now().second < 5:
                run_scheduled_fast_com_test()
            time.sleep(1)
    
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    
    monitor_thread.start()
    scheduler_thread.start()

# Flask Routes
@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/status')
def api_status():
    """API endpoint for monitoring data"""
    return jsonify(monitoring_data)

@app.route('/api/interfaces')
def get_interfaces():
    """Get all available network interfaces"""
    interfaces = get_all_interfaces()
    return jsonify({'interfaces': interfaces})

@app.route('/api/select-interface', methods=['POST'])
def select_interface():
    """Select a network interface to monitor"""
    global monitoring_data
    data = request.get_json()
    interface_name = data.get('interface_name')
    
    if interface_name:
        # Verify interface exists
        interfaces = psutil.net_if_addrs()
        if interface_name in interfaces:
            monitoring_data['selected_interface'] = interface_name
            return jsonify({'success': True, 'message': f'Switched to interface: {interface_name}'})
        else:
            return jsonify({'success': False, 'message': 'Interface not found'})
    else:
        return jsonify({'success': False, 'message': 'No interface specified'})

@app.route('/api/run-speed-test')
def run_speed_test():
    """Run a speed test"""
    try:
        speed_result = run_fast_com_test()
        monitoring_data['fast_com_speed'] = speed_result
        monitoring_data['last_fast_com_test'] = datetime.now().isoformat()
        return jsonify({'success': True, 'result': speed_result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/reset-metrics')
def reset_metrics():
    """Reset performance metrics"""
    global monitoring_data
    monitoring_data['worst_latency'] = 0
    monitoring_data['best_bandwidth'] = 0
    monitoring_data['worst_bandwidth'] = float('inf')
    monitoring_data['performance_history'] = []
    monitoring_data['downtime_count'] = 0
    return jsonify({'success': True, 'message': 'Metrics reset'})

if __name__ == '__main__':
    # Start monitoring
    start_monitoring()
    print("Starting Starshield Network Monitor...")
    print("Features: Interface selection, last down time, worst latency, bandwidth tracking, Fast.com integration")
    print("Access at: http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)