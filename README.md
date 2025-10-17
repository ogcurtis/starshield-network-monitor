# Starshield Network Monitor

A comprehensive Python-based network monitoring solution designed specifically for monitoring Starshield network interfaces. This tool provides real-time monitoring of latency, uptime, bandwidth, and performance metrics with a clean web interface.

## Features

### Core Monitoring
- **Real-time Network Status**: Monitor interface up/down status
- **Latency Tracking**: Ping gateway and DNS servers for latency measurement
- **Bandwidth Monitoring**: Track RX/TX bytes with visual indicators
- **Uptime Tracking**: Count successful monitoring checks
- **Interface Selection**: Dropdown to choose which network interface to monitor

### Advanced Metrics
- **Last Down Time**: Track when the interface was last offline
- **Worst Case Latency**: Record highest latency encountered
- **Best/Worst Bandwidth**: Track performance extremes
- **Downtime Counting**: Count total number of outages
- **Performance History**: Store last 100 performance measurements

### Speed Testing
- **Fast.com Integration**: Automated speed testing every 10 minutes
- **Manual Speed Tests**: On-demand speed testing via web interface
- **Ping-based Fallback**: Alternative speed testing when Fast.com is unavailable

### Web Interface
- **Responsive Dashboard**: Clean, modern Bootstrap-based interface
- **Real-time Updates**: Auto-refresh every 5 seconds
- **Visual Indicators**: Color-coded status and progress bars
- **Performance Charts**: Historical data visualization
- **Mobile Friendly**: Works on desktop and mobile devices

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (tested on Windows 11)
- Network interface to monitor (e.g., "Ethernet 4")

### Installation

1. **Clone or Download** this repository to your desired location
2. **Run Setup**:
   ```batch
   setup.bat
   ```
   This will:
   - Create a Python virtual environment
   - Install all required dependencies
   - Set up the monitoring environment

3. **Start Monitoring**:
   ```batch
   start.bat
   ```
   This will:
   - Activate the virtual environment
   - Start the Flask web server
   - Begin monitoring your network interface

4. **Access Dashboard**:
   Open your web browser and navigate to:
   - `http://localhost:8080` (local access)
   - `http://[your-ip]:8080` (network access)

## Configuration

### Default Settings
- **Target Interface**: Ethernet 4
- **Gateway**: 100.64.0.1
- **DNS Server**: 198.54.100.65
- **Monitoring Interval**: 5 seconds
- **Speed Test Interval**: 10 minutes
- **Web Port**: 8080

### Customizing Settings
Edit `app.py` to modify:
- Default interface name
- Gateway and DNS addresses
- Monitoring intervals
- Web server port

## Usage

### Web Interface

1. **Interface Selection**: Use the dropdown to select which network interface to monitor
2. **Real-time Monitoring**: Watch live updates of network status, latency, and bandwidth
3. **Speed Testing**: Click "Run Speed Test" to perform on-demand Fast.com testing
4. **Performance History**: View recent performance data in the history section
5. **Reset Metrics**: Use "Reset Metrics" to clear performance records

### API Endpoints

- `GET /` - Main dashboard
- `GET /api/status` - Current monitoring data (JSON)
- `GET /api/interfaces` - Available network interfaces (JSON)
- `POST /api/select-interface` - Change monitored interface
- `GET /api/run-speed-test` - Run manual speed test
- `GET /api/reset-metrics` - Reset performance metrics

### Example API Usage

```bash
# Get current status
curl http://localhost:8080/api/status

# Get available interfaces
curl http://localhost:8080/api/interfaces

# Select interface
curl -X POST http://localhost:8080/api/select-interface \
  -H "Content-Type: application/json" \
  -d '{"interface_name": "Ethernet 4"}'

# Run speed test
curl http://localhost:8080/api/run-speed-test
```

## File Structure

```
Starshield Web Server/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── dashboard.html     # Web interface template
├── setup.bat             # Setup script
├── start.bat             # Start script
├── README.md             # This file
└── .venv/                # Python virtual environment (created by setup)
```

## Dependencies

- **Flask 2.3.3**: Web framework
- **psutil 5.9.6**: System and network monitoring
- **requests 2.31.0**: HTTP requests for speed testing
- **ping3 4.0.4**: Ping functionality

## Troubleshooting

### Common Issues

1. **"Virtual environment not found"**
   - Solution: Run `setup.bat` first to create the virtual environment

2. **"Interface not found"**
   - Solution: Check interface name in dropdown, ensure interface is active

3. **"Permission denied" for ping**
   - Solution: Run as administrator or check Windows firewall settings

4. **Speed test fails**
   - Solution: Check internet connection, Fast.com may be temporarily unavailable

5. **Port 8080 already in use**
   - Solution: Change port in `app.py` or stop other services using port 8080

### Debug Mode

To run in debug mode for troubleshooting:
```batch
call .\.venv\Scripts\activate.bat
python app.py
```
Then edit `app.py` and change `debug=False` to `debug=True` in the last line.

### Logs

The application prints monitoring information to the console:
- Status updates every 5 seconds
- Speed test results
- Error messages
- Interface changes

## Network Interface Detection

The monitor automatically detects available network interfaces and filters out:
- Loopback interfaces (lo*)
- Docker interfaces (docker*, veth*)
- Virtual interfaces

Only interfaces with IPv4 addresses are shown in the selection dropdown.

## Performance Considerations

- **Memory Usage**: ~50-100MB (Python + Flask)
- **CPU Usage**: <1% on modern systems
- **Network Usage**: Minimal (ping packets + speed tests)
- **Storage**: Performance history stored in memory (resets on restart)

## Security Notes

- The web interface is accessible to anyone on your network
- No authentication is implemented
- Consider firewall rules for production use
- Monitor runs with standard user permissions

## Customization

### Adding New Metrics
Edit `app.py` to add new monitoring functions and update the dashboard template.

### Changing Update Intervals
Modify the `time.sleep(5)` value in the `run_monitor()` function.

### Styling Changes
Edit `templates/dashboard.html` to modify the web interface appearance.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Ensure all dependencies are properly installed
4. Verify network interface names and permissions

## License

This project is provided as-is for monitoring Starshield network interfaces. Feel free to modify and distribute according to your needs.

---

**Starshield Network Monitor** - Keep your connection monitored! 🛰️