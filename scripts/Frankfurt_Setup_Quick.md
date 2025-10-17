# Quick Frankfurt iperf3 Server Setup

## 🚀 Manual Setup (5 minutes)

### Step 1: Create EC2 Instance
1. **Go to AWS Console**: https://console.aws.amazon.com/ec2/
2. **Select Frankfurt region** (eu-central-1) - top right corner
3. **Click "Launch Instance"**
4. **Name**: `iperf3-server`
5. **AMI**: Amazon Linux 2 (Free tier eligible)
6. **Instance type**: t3.micro (Free tier eligible)
7. **Key pair**: Create new or select existing
8. **Security group**: Create new with these rules:
   - SSH (22) from Anywhere (0.0.0.0/0)
   - Custom TCP (5201) from Anywhere (0.0.0.0/0)
9. **Launch instance**

### Step 2: Install iperf3
1. **SSH into your instance**:
   ```bash
   ssh -i your-key.pem ec2-user@YOUR_PUBLIC_IP
   ```

2. **Install and start iperf3**:
   ```bash
   sudo yum update -y
   sudo yum install -y epel-release iperf3
   sudo iperf3 -s -p 5201 -D
   sudo firewall-cmd --permanent --add-port=5201/tcp
   sudo firewall-cmd --reload
   ```

3. **Make it start on boot**:
   ```bash
   echo "sudo iperf3 -s -p 5201 -D" | sudo tee -a /etc/rc.local
   sudo chmod +x /etc/rc.local
   ```

### Step 3: Test Your Server
From your local machine:
```bash
python test_iperf3_server.py YOUR_PUBLIC_IP
```

### Step 4: Update Monitoring App
```bash
python update_aws_server.py YOUR_PUBLIC_IP
```

## Expected Results
- **Latency**: 5-15ms (excellent for Germany)
- **Download**: 200-300 Mbps (your actual speed)
- **Upload**: 200-300 Mbps (your actual speed)

## Cost
- **Free tier**: 750 hours/month
- **Data transfer**: 1GB out free/month
- **Total cost**: ~$0 if within free tier

## Cleanup
When done testing:
```bash
python cleanup_iperf3_server.py
```
Or manually terminate the instance in AWS Console.
