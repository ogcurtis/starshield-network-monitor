#!/usr/bin/env python3
"""
AWS EC2 iperf3 Server Cleanup Script
Terminates the iperf3 server instance and cleans up resources
"""

import boto3
import json
import os

def cleanup_iperf3_server():
    """Clean up iperf3 server resources"""
    try:
        # Load server info
        if not os.path.exists('iperf3_server_info.json'):
            print("No server info file found. Nothing to clean up.")
            return
        
        with open('iperf3_server_info.json', 'r') as f:
            server_info = json.load(f)
        
        instance_id = server_info['instance_id']
        security_group_id = server_info['security_group_id']
        key_name = server_info['key_name']
        
        print(f"Cleaning up iperf3 server: {instance_id}")
        
        # Initialize EC2 client
        ec2 = boto3.client('ec2', region_name='eu-central-1')  # Frankfurt region
        
        # Terminate instance
        print("Terminating instance...")
        ec2.terminate_instances(InstanceIds=[instance_id])
        
        # Wait for instance to be terminated
        print("Waiting for instance to terminate...")
        waiter = ec2.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[instance_id])
        
        # Delete security group
        print("Deleting security group...")
        ec2.delete_security_group(GroupId=security_group_id)
        
        # Delete key pair
        print("Deleting key pair...")
        ec2.delete_key_pair(KeyName=key_name)
        
        # Delete key file
        key_file = f"{key_name}.pem"
        if os.path.exists(key_file):
            os.remove(key_file)
            print(f"Deleted key file: {key_file}")
        
        # Delete server info file
        os.remove('iperf3_server_info.json')
        print("Deleted server info file")
        
        print("✅ Cleanup completed successfully!")
        
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == "__main__":
    cleanup_iperf3_server()
