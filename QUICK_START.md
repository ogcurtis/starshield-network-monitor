# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### 1. Setup (One-time)
```bash
# Clone the repository
git clone https://github.com/ogcurtis/starshield-network-monitor.git
cd starshield-network-monitor

# Run setup (Windows)
setup.bat
```

### 2. Start Monitoring
```bash
# Start the monitor
start.bat
```

### 3. Access Dashboard
Open your browser and go to: **http://localhost:8080**

## ✅ What You'll See

- **Real-time Status**: Online/Offline indicator
- **Latency**: Current ping to gateway (27ms typical)
- **Bandwidth**: RX/TX data usage
- **Interface Selection**: Dropdown to choose network interface
- **Performance History**: Last 100 measurements
- **Speed Testing**: Fast.com integration

## 🎯 Key Features

- ✅ **Interface Detection**: Automatically finds "Ethernet 4" (Starshield)
- ✅ **Real-time Monitoring**: Updates every 5 seconds
- ✅ **Performance Tracking**: Best/worst latency and bandwidth
- ✅ **Downtime Tracking**: Counts outages and last down time
- ✅ **Speed Testing**: Automated Fast.com tests every 10 minutes
- ✅ **Mobile Friendly**: Works on phones and tablets

## 📊 Current Status Example

```json
{
  "status": "online",
  "selected_interface": "Ethernet 4",
  "latency": 27.17,
  "uptime": 151,
  "worst_latency": 1056.0,
  "bandwidth": {"rx": 21499913, "tx": 22621413}
}
```

## 🔧 Troubleshooting

**Can't find .bat files?**
- Use: `.\start.bat` or `.\setup.bat`

**Port 8080 in use?**
- Edit `app.py` and change port 8080 to another port

**Interface not found?**
- Check the dropdown in the web interface
- Ensure your network interface is active

## 📱 Mobile Access

Access from your phone:
- Find your computer's IP address
- Go to: `http://[your-ip]:8080`
- Example: `http://192.168.10.3:8080`

---

**Need help?** Check the full [README.md](README.md) for detailed documentation.
