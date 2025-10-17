#!/usr/bin/env python3
"""
Update AWS iperf3 Server IP in monitoring app
"""

import re
import sys

def update_aws_server_ip(ip_address):
    """Update the AWS server IP in app.py"""
    try:
        # Read the current app.py
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Replace the commented AWS server line with the actual IP
        pattern = r"# \{'host': 'YOUR_AWS_EC2_IP', 'port': 5201\},"
        replacement = f"{{'host': '{ip_address}', 'port': 5201}},"
        
        new_content = re.sub(pattern, replacement, content)
        
        # Write back to file
        with open('app.py', 'w') as f:
            f.write(new_content)
        
        print(f"SUCCESS: Updated AWS server IP to {ip_address}")
        print("Restart your monitoring app to use the new server")
        
    except Exception as e:
        print(f"Error updating server IP: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python update_aws_server.py <AWS_EC2_IP>")
        print("Example: python update_aws_server.py 3.15.123.45")
        sys.exit(1)
    
    ip_address = sys.argv[1]
    update_aws_server_ip(ip_address)

if __name__ == "__main__":
    main()
