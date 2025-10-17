# AWS iperf3 Server Setup Guide

## Quick Setup (Manual)

### 1. Create EC2 Instance
1. Go to AWS Console → EC2 → Launch Instance
2. **Select Frankfurt (eu-central-1) region** for best performance in Germany
3. Choose **Amazon Linux 2 AMI** (Free tier eligible)
4. Select **t3.micro** instance type
4. Create or select a key pair
5. Configure security group:
   - SSH (22) from anywhere (0.0.0.0/0)
   - Custom TCP (5201) from anywhere (0.0.0.0/0)
6. Launch instance

### 2. Install iperf3 on the Instance
SSH into your instance and run:

```bash
# Update system
sudo yum update -y

# Install iperf3
sudo yum install -y epel-release
sudo yum install -y iperf3

# Start iperf3 server
sudo iperf3 -s -p 5201 -D

# Make it start on boot
echo "sudo iperf3 -s -p 5201 -D" | sudo tee -a /etc/rc.local
sudo chmod +x /etc/rc.local

# Configure firewall
sudo firewall-cmd --permanent --add-port=5201/tcp
sudo firewall-cmd --reload
```

### 3. Test the Server
From your local machine:
```bash
iperf3 -c YOUR_EC2_PUBLIC_IP -p 5201 -t 10 -f m
```

### 4. Update Your Monitoring App
Once you have the EC2 IP, update the `app.py` file to use your server:

```python
# In the run_speed_test() function, replace the iperf_servers list with:
iperf_servers = [
    {'host': 'YOUR_EC2_PUBLIC_IP', 'port': 5201},
    # Keep fallback servers
    {'host': 'iperf.he.net', 'port': 5201},
    {'host': 'speedtest.serverius.net', 'port': 5002},
]
```

## Automated Setup (Using AWS CLI)

### Prerequisites
1. Install AWS CLI: `pip install awscli`
2. Configure credentials: `aws configure`
3. **Set region to Frankfurt**: `aws configure set region eu-central-1`
4. Install boto3: `pip install boto3`

### Run the Script
```bash
python create_iperf3_server.py
```

### Cleanup
```bash
python cleanup_iperf3_server.py
```

## Cost Considerations
- **t3.micro**: Free tier eligible (750 hours/month)
- **Data transfer**: First 1GB out per month is free
- **Storage**: 30GB EBS storage free for 12 months

## Expected Performance
With your own iperf3 server in Frankfurt, you should see:
- **Download**: 200-300 Mbps (your actual connection speed)
- **Upload**: 200-300 Mbps (your actual connection speed)
- **Latency**: 5-15ms (excellent for Germany)

## Troubleshooting

### If iperf3 test fails:
1. Check security group allows port 5201
2. Verify iperf3 is running: `sudo netstat -tlnp | grep 5201`
3. Check firewall: `sudo firewall-cmd --list-ports`
4. Test from EC2 itself: `iperf3 -c localhost -p 5201`

### If AWS CLI fails:
1. Check credentials: `aws sts get-caller-identity`
2. Configure new credentials: `aws configure`
3. Check region: `aws configure get region`
