#!/usr/bin/env python3
"""
AWS EC2 iperf3 Server Setup Script
Creates an EC2 instance with iperf3 server running
"""

import boto3
import time
import json
import subprocess
import sys

def create_security_group(ec2, group_name="iperf3-server-sg"):
    """Create security group for iperf3 server"""
    try:
        # Check if security group already exists
        response = ec2.describe_security_groups(
            Filters=[{'Name': 'group-name', 'Values': [group_name]}]
        )
        
        if response['SecurityGroups']:
            print(f"Security group {group_name} already exists")
            return response['SecurityGroups'][0]['GroupId']
        
        # Create security group
        response = ec2.create_security_group(
            GroupName=group_name,
            Description='Security group for iperf3 server'
        )
        security_group_id = response['GroupId']
        
        # Add inbound rules for iperf3 (port 5201) and SSH (port 22)
        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 5201,
                    'ToPort': 5201,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                }
            ]
        )
        
        print(f"Created security group: {security_group_id}")
        return security_group_id
        
    except Exception as e:
        print(f"Error creating security group: {e}")
        return None

def create_key_pair(ec2, key_name="iperf3-server-key"):
    """Create or use existing key pair"""
    try:
        # Check if key pair exists
        response = ec2.describe_key_pairs(
            Filters=[{'Name': 'key-name', 'Values': [key_name]}]
        )
        
        if response['KeyPairs']:
            print(f"Key pair {key_name} already exists")
            return key_name
        
        # Create key pair
        response = ec2.create_key_pair(KeyName=key_name)
        
        # Save private key to file
        with open(f"{key_name}.pem", 'w') as f:
            f.write(response['KeyMaterial'])
        
        print(f"Created key pair: {key_name}")
        print(f"Private key saved to: {key_name}.pem")
        return key_name
        
    except Exception as e:
        print(f"Error creating key pair: {e}")
        return None

def create_iperf3_server(ec2, security_group_id, key_name):
    """Create EC2 instance with iperf3 server"""
    try:
        # User data script to install and start iperf3
        user_data = """#!/bin/bash
yum update -y
yum install -y epel-release
yum install -y iperf3
systemctl enable iperf3
systemctl start iperf3

# Create iperf3 systemd service
cat > /etc/systemd/system/iperf3-server.service << 'EOF'
[Unit]
Description=iperf3 Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/iperf3 -s -p 5201
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable iperf3-server
systemctl start iperf3-server

# Allow iperf3 through firewall
firewall-cmd --permanent --add-port=5201/tcp
firewall-cmd --reload

# Log completion
echo "iperf3 server setup completed at $(date)" >> /var/log/iperf3-setup.log
"""
        
        # Launch instance
        response = ec2.run_instances(
            ImageId='ami-0c02fb55956c7d316',  # Amazon Linux 2 AMI
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',  # Free tier eligible
            KeyName=key_name,
            SecurityGroupIds=[security_group_id],
            UserData=user_data,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'iperf3-server'},
                        {'Key': 'Purpose', 'Value': 'Speed Testing'}
                    ]
                }
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Created instance: {instance_id}")
        
        # Wait for instance to be running
        print("Waiting for instance to be running...")
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get public IP
        response = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        
        print(f"Instance is running!")
        print(f"Public IP: {public_ip}")
        print(f"Instance ID: {instance_id}")
        
        return instance_id, public_ip
        
    except Exception as e:
        print(f"Error creating instance: {e}")
        return None, None

def test_iperf3_connection(public_ip):
    """Test connection to iperf3 server"""
    try:
        print(f"Testing iperf3 connection to {public_ip}...")
        
        # Wait a bit for iperf3 to start
        time.sleep(30)
        
        # Test with iperf3 client
        result = subprocess.run([
            'iperf3', '-c', public_ip, '-p', '5201', '-t', '5', '-f', 'm'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("SUCCESS: iperf3 server is working!")
            print(result.stdout)
            return True
        else:
            print("ERROR: iperf3 test failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error testing iperf3: {e}")
        return False

def main():
    """Main function"""
    print("Creating AWS EC2 iperf3 Server...")
    
    try:
        # Initialize EC2 client
        ec2 = boto3.client('ec2', region_name='us-east-1')
        
        # Create security group
        security_group_id = create_security_group(ec2)
        if not security_group_id:
            print("Failed to create security group")
            return
        
        # Create key pair
        key_name = create_key_pair(ec2)
        if not key_name:
            print("Failed to create key pair")
            return
        
        # Create instance
        instance_id, public_ip = create_iperf3_server(ec2, security_group_id, key_name)
        if not instance_id:
            print("Failed to create instance")
            return
        
        print("\nSUCCESS: iperf3 Server Created Successfully!")
        print(f"Instance ID: {instance_id}")
        print(f"Public IP: {public_ip}")
        print(f"Key file: {key_name}.pem")
        
        # Save server info
        server_info = {
            'instance_id': instance_id,
            'public_ip': public_ip,
            'key_name': key_name,
            'security_group_id': security_group_id,
            'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('iperf3_server_info.json', 'w') as f:
            json.dump(server_info, f, indent=2)
        
        print(f"\nServer info saved to: iperf3_server_info.json")
        print(f"\nTo test the server, run:")
        print(f"iperf3 -c {public_ip} -p 5201 -t 10 -f m")
        
        # Test connection
        if test_iperf3_connection(public_ip):
            print("\nSUCCESS: Server is ready for use!")
        else:
            print("\nWARNING: Server created but iperf3 test failed. Check security groups and instance status.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure AWS credentials are configured correctly")

if __name__ == "__main__":
    main()
