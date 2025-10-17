#!/usr/bin/env python3
"""
Test iperf3 server connection and performance
"""

import subprocess
import json
import time
import sys

def test_iperf3_server(host, port=5201, duration=10):
    """Test iperf3 server and return results"""
    try:
        print(f"Testing iperf3 server: {host}:{port}")
        print(f"Duration: {duration} seconds")
        print("-" * 50)
        
        # Test download speed
        print("Testing download speed...")
        download_cmd = [
            'iperf3', '-c', host, '-p', str(port), 
            '-t', str(duration), '-f', 'm', '--json'
        ]
        
        result = subprocess.run(download_cmd, capture_output=True, text=True, timeout=duration+10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            download_mbps = data['end']['sum_received']['bits_per_second'] / 1000000
            print(f"✅ Download: {download_mbps:.2f} Mbps")
        else:
            print(f"❌ Download test failed: {result.stderr}")
            return False
        
        # Test upload speed
        print("Testing upload speed...")
        upload_cmd = [
            'iperf3', '-c', host, '-p', str(port), 
            '-t', str(duration), '-f', 'm', '--json', '-R'
        ]
        
        result = subprocess.run(upload_cmd, capture_output=True, text=True, timeout=duration+10)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            upload_mbps = data['end']['sum_sent']['bits_per_second'] / 1000000
            print(f"✅ Upload: {upload_mbps:.2f} Mbps")
        else:
            print(f"❌ Upload test failed: {result.stderr}")
            return False
        
        print("-" * 50)
        print(f"🎉 Server is working!")
        print(f"Download: {download_mbps:.2f} Mbps")
        print(f"Upload: {upload_mbps:.2f} Mbps")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_iperf3_server.py <SERVER_IP> [PORT] [DURATION]")
        print("Example: python test_iperf3_server.py 3.15.123.45 5201 10")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5201
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    success = test_iperf3_server(host, port, duration)
    
    if success:
        print("\n✅ Your iperf3 server is ready!")
        print("You can now update your monitoring app with this server IP.")
    else:
        print("\n❌ Server test failed. Check your server configuration.")

if __name__ == "__main__":
    main()
