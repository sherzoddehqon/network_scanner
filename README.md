# Network Scanner - Professional Network Discovery Tool

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A production-ready network scanner similar to Spiceworks that discovers devices, scans ports, identifies services, and provides comprehensive network inventory across multiple subnets including Wi-Fi hotspots.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Common Use Cases](#common-use-cases)
- [Export Formats](#export-formats)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Advanced Usage](#advanced-usage)
- [Contributing](#contributing)

---

## 🎯 Overview

**Network Scanner** is a Python-based network discovery and auditing tool designed for IT professionals and network administrators. It provides comprehensive device identification, port scanning, and service detection capabilities similar to commercial tools like Spiceworks, but as a free, open-source, customizable solution.

### Key Capabilities

- **🔍 Host Discovery**: ARP-based scanning for reliable local network device detection
- **🔌 Port Scanning**: Concurrent asyncio-based port scanning (100x faster than sequential)
- **🏷️ Device Identification**: MAC vendor lookup, hostname resolution, device type classification
- **🌐 Multi-Network Support**: Scan multiple subnets including Wi-Fi hotspots simultaneously
- **📊 Professional Output**: Beautiful console tables with color-coded results
- **💾 Export Options**: CSV (Excel-ready) and JSON formats for reporting and automation
- **⚡ High Performance**: Scans 1000 ports in ~3 seconds vs 51 minutes sequentially

### Comparison to Spiceworks

| Feature | This Scanner | Spiceworks |
|---------|-------------|------------|
| Device Discovery | ✅ ARP-based | ✅ Multiple methods |
| Port Scanning | ✅ Ports 1-65535 | ✅ Common ports |
| Multi-Network | ✅ Yes | ⚠️ Limited |
| Hotspot Discovery | ✅ Yes | ❌ No |
| Export CSV/JSON | ✅ Yes | ✅ Yes |
| Price | ✅ Free | ✅ Free |
| Customizable | ✅ Yes | ❌ No |
| Cross-Platform | ✅ Yes | ⚠️ Windows only |

---

## ✨ Features

### Core Features

- **ARP Host Discovery**: Most reliable method for local network device detection
- **Concurrent Port Scanning**: Uses Python asyncio for dramatic performance improvements
- **MAC Vendor Lookup**: Automatically identifies device manufacturers
- **Hostname Resolution**: Retrieves device hostnames when available
- **Service Detection**: Identifies common services on open ports
- **Multi-Network Scanning**: Discovers devices across multiple subnets
- **Hotspot Detection**: Finds devices connected through desktop Wi-Fi hotspots
- **Real-Time Progress**: Live scanning progress with device counts
- **Professional Output**: Rich console tables with color-coded results

### Export & Reporting

- **CSV Export**: Excel-ready format for inventory management
- **JSON Export**: Machine-readable format for automation
- **Network Grouping**: Results organized by subnet
- **Historical Tracking**: Compare scans over time (with database support)

### Performance

- **Asyncio Concurrency**: 100x performance improvement for port scanning
- **Configurable Timeout**: Adjust scan speed vs reliability
- **Rate Limiting**: Prevent network congestion
- **Graceful Degradation**: Works even without elevated privileges (limited features)

---

## 💻 System Requirements

### Supported Operating Systems

- ✅ **Windows** 10/11 (Primary testing platform)
- ✅ **Linux** (Ubuntu 20.04+, Debian, Fedora, etc.)
- ✅ **macOS** 10.15+ (Catalina and newer)

### Software Requirements

| Component | Version | Required | Notes |
|-----------|---------|----------|-------|
| Python | 3.8+ | ✅ Yes | Python 3.10+ recommended |
| pip | Latest | ✅ Yes | Usually included with Python |
| Npcap | Latest | ⚠️ Windows only | Required for ARP scanning on Windows |
| Admin/Root | - | ⚠️ For ARP | Some features work without |

### Hardware Requirements

- **RAM**: 512 MB minimum, 1 GB recommended
- **Storage**: 100 MB for application and dependencies
- **Network**: Ethernet or Wi-Fi adapter
- **CPU**: Any modern processor (asyncio benefits from multi-core)

---

## 📥 Installation

### Step 1: Install Python

**Windows:**
1. Download Python from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify: Open Command Prompt and run `python --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**macOS:**
```bash
# Using Homebrew
brew install python3
```

### Step 2: Install Required Packages

Download all project files to a folder, then:

```bash
# Navigate to project folder
cd /path/to/network_scanner

# Install dependencies
pip install -r requirements.txt
```

Or install manually:
```bash
pip install scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp
```

### Step 3: Install Npcap (Windows Only)

**⚠️ CRITICAL FOR WINDOWS USERS:**

1. Download Npcap: https://npcap.com/#download
2. Run installer as Administrator
3. ✅ **IMPORTANT**: Check "Install Npcap in WinPcap API-compatible Mode"
4. Complete installation
5. Restart computer if prompted

**Why Npcap?** Windows requires Npcap for ARP packet capture. Without it, ARP-based scanning won't work.

### Step 4: Verify Installation

Test that everything works:

```bash
# Test imports
python -c "import scapy, nmap, click, rich; print('✅ All packages installed!')"

# Check scanner
python scanner.py --help
```

**📖 For detailed platform-specific instructions, see [INSTALLATION.md](INSTALLATION.md)**

---

## 🚀 Quick Start

### Your First Scan (3 Steps)

**Step 1: Find Your Network**

```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Look for your **IPv4 Address** (e.g., `192.168.44.96`).  
If your IP is `192.168.44.96`, your network is `192.168.44.0/24`

**Step 2: Open Administrator/Root Prompt**

**Windows:**
- Search "cmd"
- Right-click "Command Prompt"
- Select "Run as administrator"

**Linux/Mac:**
```bash
sudo -i
```

**Step 3: Run Your First Scan**

```bash
# Quick discovery (5-10 seconds)
python scanner.py discover 192.168.44.0/24

# Full scan with ports (2-5 minutes)
python scanner.py scan 192.168.44.0/24
```

### Understanding the Output

```
╭──────────────────────── Network Scan Results ────────────────────────╮
│  IP Address      MAC Address        Hostname           Vendor        │
│ ──────────────────────────────────────────────────────────────────── │
│  192.168.44.1    bc-cf-4f-b8-99-3b  router.local       TP-Link       │
│  192.168.44.5    bc-9b-5e-b8-44-81  desktop-john       Dell Inc.     │
│  192.168.44.96   d8-bb-c1-56-e0-93  YOUR-COMPUTER      Intel Corp    │
╰───────────────────────────────────────────────────────────────────────╯

Total devices found: 73
```

**What You're Seeing:**
- **IP Address**: Device network address
- **MAC Address**: Hardware identifier
- **Hostname**: Device name (if available)
- **Vendor**: Manufacturer from MAC address
- **Open Ports**: Services running (in `scan` command)

---

## 📖 Command Reference

### Scanner.py Commands

#### 1. `discover` - Quick Host Discovery

**Purpose:** Find all devices without port scanning (fastest)

**Syntax:**
```bash
python scanner.py discover <network>
```

**Examples:**
```bash
# Discover devices on your network
python scanner.py discover 192.168.44.0/24

# Scan a different subnet
python scanner.py discover 10.0.0.0/24
```

**Output:** Device list with IP, MAC, hostname, vendor  
**Time:** 5-10 seconds  
**Export:** ❌ Not available (use `scan` for export)

---

#### 2. `scan` - Full Network Scan

**Purpose:** Complete discovery with port scanning and export options

**Syntax:**
```bash
python scanner.py scan <network> [OPTIONS]
```

**Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--ports` | 1-1000 | Port range to scan |
| `--timeout` | 2.0 | Connection timeout (seconds) |
| `--max-concurrent` | 100 | Concurrent connections |
| `--export-csv` | None | Export to CSV file |
| `--export-json` | None | Export to JSON file |
| `--scan-type` | fast | Scan type (fast/full) |

**Examples:**

```bash
# Basic full scan
python scanner.py scan 192.168.44.0/24

# Scan specific ports
python scanner.py scan 192.168.44.0/24 --ports 22,80,443,3389

# Scan port range
python scanner.py scan 192.168.44.0/24 --ports 1-100

# Export to CSV
python scanner.py scan 192.168.44.0/24 --export-csv network.csv

# Export to JSON
python scanner.py scan 192.168.44.0/24 --export-json network.json

# Fast scan with both exports
python scanner.py scan 192.168.44.0/24 --ports 1-100 --export-csv network.csv --export-json network.json

# Increase scan speed (more concurrent connections)
python scanner.py scan 192.168.44.0/24 --max-concurrent 200

# Scan all ports (slow - 65535 ports!)
python scanner.py scan 192.168.44.0/24 --ports 1-65535
```

**Output:** Device list + open ports  
**Time:** 2-5 minutes (depends on devices and port range)  
**Export:** ✅ CSV and JSON available

---

### Multi-Network Scanner Commands

#### 3. `detect-networks` - Show Available Networks

**Purpose:** Detect all network interfaces on your computer

**Syntax:**
```bash
python multi_network_scanner.py detect-networks
```

**Examples:**
```bash
python multi_network_scanner.py detect-networks
```

**Output:**
```
Detected Networks:
  • 192.168.44.0/24
  • 192.168.137.0/24

Common Hotspot Networks:
  • 192.168.137.0/24 (Windows Mobile Hotspot)
  • 192.168.0.0/24
  • 192.168.1.0/24
  • 172.20.10.0/24 (iPhone Hotspot)
```

**Time:** <1 second  
**Use Case:** Run this first to know which networks exist

---

#### 4. `scan-all` - Multi-Network Discovery

**Purpose:** Automatically scan all networks including hotspots

**Syntax:**
```bash
python multi_network_scanner.py scan-all [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `-n, --networks` | Add additional networks to scan |
| `--export-csv` | Export to CSV file |
| `--export-json` | Export to JSON file |

**Examples:**

```bash
# Scan all detected networks
python multi_network_scanner.py scan-all

# Add custom networks
python multi_network_scanner.py scan-all -n 192.168.50.0/24 -n 10.0.0.0/24

# Scan all and export
python multi_network_scanner.py scan-all --export-csv all_networks.csv

# Complete scan with multiple networks and export
python multi_network_scanner.py scan-all -n 172.16.0.0/24 --export-csv complete.csv --export-json complete.json
```

**Output:** Grouped device lists by network  
**Time:** 1-3 minutes  
**Export:** ✅ CSV and JSON available

**Perfect For:**
- Finding devices on Wi-Fi hotspots
- Complete network inventory
- Multi-subnet environments

---

## 💼 Common Use Cases

### 1. Network Inventory / Asset Discovery

**Goal:** Create a complete list of all devices on your network

```bash
# Quick inventory
python scanner.py scan 192.168.44.0/24 --export-csv inventory.csv

# Open inventory.csv in Excel for analysis
```

**What You Get:**
- Complete device list
- Hardware manufacturers
- IP/MAC address mapping
- Hostname identification

**Frequency:** Run weekly or monthly

---

### 2. Security Auditing

**Goal:** Find devices with open/vulnerable ports

```bash
# Scan common vulnerable ports
python scanner.py scan 192.168.44.0/24 --ports 21,22,23,80,443,445,3389,8080

# Export for security review
python scanner.py scan 192.168.44.0/24 --ports 1-65535 --export-csv security_audit.csv
```

**Look For:**
- Port 23 (Telnet) - Unencrypted, should be disabled
- Port 445 (SMB) - File sharing vulnerabilities
- Port 3389 (RDP) - Remote desktop exposure
- Unexpected open ports

**Frequency:** Run monthly or after changes

---

### 3. Finding Unauthorized Devices

**Goal:** Detect new/unknown devices on your network

```bash
# Day 1: Baseline scan
python scanner.py scan 192.168.44.0/24 --export-json baseline.json

# Day 7: Compare scan
python scanner.py scan 192.168.44.0/24 --export-json current.json

# Compare the two JSON files to find new devices
```

**Look For:**
- Unknown MAC addresses
- Unfamiliar hostnames
- Unexpected vendors
- Devices in unusual IP ranges

**Frequency:** Run daily in sensitive environments

---

### 4. Monitoring Wi-Fi Hotspot Connections

**Goal:** See devices connected to desktop hotspots

```bash
# Scan all networks including hotspots
python multi_network_scanner.py scan-all --export-csv hotspot_devices.csv
```

**What You'll Find:**
- Devices on main network (192.168.44.0/24)
- Devices on hotspots (192.168.137.0/24)
- Complete cross-network inventory

**Frequency:** As needed

---

### 5. Troubleshooting Network Issues

**Goal:** Verify device connectivity and services

```bash
# Check if specific device is online
python scanner.py discover 192.168.44.0/24 | grep "192.168.44.100"

# Verify web server is running
python scanner.py scan 192.168.44.0/24 --ports 80,443

# Check printer connectivity
python scanner.py scan 192.168.44.0/24 --ports 9100,515,631
```

**Common Port Checks:**
- 80, 443 = Web servers
- 22 = SSH servers
- 3389 = Remote Desktop
- 9100 = Printers
- 445 = File shares

---

### 6. IoT Device Discovery

**Goal:** Find all smart home/IoT devices

```bash
# Full scan to find IoT devices
python scanner.py scan 192.168.44.0/24 --export-csv iot_devices.csv

# Filter in Excel for:
# - Unknown/generic hostnames
# - Unusual vendors (Xiaomi, Tuya, Shenzhen companies)
# - Open ports 8080, 8000, 1883 (MQTT)
```

**Common IoT Vendors:**
- Xiaomi (smart home)
- TP-Link (smart plugs)
- Tuya (various smart devices)
- Shenzhen companies (cameras, sensors)

---

## 📊 Export Formats

### CSV Export (Excel-Ready)

**Best For:** Human analysis, reports, spreadsheets

**Format:**
```csv
Network,IP,MAC,Hostname,Vendor,Open Ports
192.168.44.0/24,192.168.44.1,bc-cf-4f-b8-99-3b,router.local,TP-Link,"80,443"
192.168.44.0/24,192.168.44.5,bc-9b-5e-b8-44-81,desktop-john,Dell Inc.,"445,3389"
```

**Usage in Excel:**
```bash
# Export
python scanner.py scan 192.168.44.0/24 --export-csv network.csv

# Open in Excel
# - Sort by Vendor
# - Filter by Open Ports
# - Create pivot tables
# - Generate charts
```

**Tips:**
- Use Excel filters to find specific vendors
- Sort by open ports to prioritize security issues
- Use conditional formatting to highlight concerns
- Create dashboards for management

---

### JSON Export (Machine-Readable)

**Best For:** Automation, APIs, scripting, databases

**Format:**
```json
{
  "scan_time": "2025-11-20T14:30:00.123456",
  "network": "192.168.44.0/24",
  "total_devices": 73,
  "devices": [
    {
      "ip": "192.168.44.1",
      "mac": "bc-cf-4f-b8-99-3b",
      "hostname": "router.local",
      "vendor": "TP-Link",
      "network": "192.168.44.0/24",
      "open_ports": [80, 443, 8080, 22],
      "scan_time": "2025-11-20T14:30:15.789012"
    }
  ]
}
```

**Usage Examples:**

**Python Processing:**
```python
import json

# Load scan results
with open('network.json', 'r') as f:
    data = json.load(f)

# Find devices with open ports
vulnerable = [d for d in data['devices'] if d['open_ports']]
print(f"Found {len(vulnerable)} devices with open ports")

# Find specific vendor
dell_devices = [d for d in data['devices'] if 'Dell' in d.get('vendor', '')]
```

**PowerShell Processing:**
```powershell
# Load JSON
$data = Get-Content network.json | ConvertFrom-Json

# Find devices
$devices = $data.devices | Where-Object { $_.open_ports.Count -gt 0 }
```

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ "Permission denied" or "Need administrator privileges"

**Problem:** ARP scanning requires elevated privileges

**Solution:**

**Windows:**
```bash
# Right-click Command Prompt
# Select "Run as administrator"
```

**Linux/Mac:**
```bash
sudo python scanner.py scan 192.168.44.0/24
```

---

#### ❌ "Scapy not available" or "ARP scanning disabled"

**Problem:** Scapy library not installed or Npcap missing (Windows)

**Solution:**

**Check Scapy:**
```bash
pip list | grep scapy
# If not found:
pip install scapy
```

**Windows - Install Npcap:**
1. Download: https://npcap.com/#download
2. Install with "WinPcap API-compatible Mode" checked
3. Restart computer

---

#### ❌ "No devices found"

**Problem:** Wrong network, firewall blocking, or permissions

**Solutions:**

**1. Verify correct network:**
```bash
# Check your IP
ipconfig  # Windows
ifconfig  # Linux/Mac

# If your IP is 192.168.44.96, scan 192.168.44.0/24
```

**2. Check with ARP:**
```bash
arp -a
# This shows devices Windows has talked to
```

**3. Temporarily disable firewall:**
```bash
# Windows (run as admin)
netsh advfirewall set allprofiles state off
# Test scan
python scanner.py discover 192.168.44.0/24
# Re-enable firewall
netsh advfirewall set allprofiles state on
```

**4. Try different scan:**
```bash
# If ARP fails, try ICMP
python scanner.py scan 192.168.44.0/24
```

---

#### ❌ "'pip' is not recognized"

**Problem:** Python not in PATH or pip not installed

**Solution:**
```bash
# Use full Python command
python -m pip install -r requirements.txt

# Or
py -m pip install -r requirements.txt
```

---

#### ❌ Scan is too slow

**Problem:** Scanning too many ports or devices

**Solutions:**

```bash
# 1. Reduce port range
python scanner.py scan 192.168.44.0/24 --ports 1-100

# 2. Scan only common ports
python scanner.py scan 192.168.44.0/24 --ports 22,80,443,445,3389

# 3. Increase concurrent connections
python scanner.py scan 192.168.44.0/24 --max-concurrent 200

# 4. Use discover for quick scan
python scanner.py discover 192.168.44.0/24
```

---

#### ❌ "Module not found" errors

**Problem:** Required packages not installed

**Solution:**
```bash
# Install all requirements
pip install -r requirements.txt

# Or install manually
pip install scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp

# Verify installation
pip list
```

---

### Getting Help

**Still having issues?**

1. Check [INSTALLATION.md](INSTALLATION.md) for detailed setup
2. Review [COMMAND_EXAMPLES.md](COMMAND_EXAMPLES.md) for output examples
3. Enable debug mode:
   ```bash
   python scanner.py scan 192.168.44.0/24 --verbose
   ```
4. Check firewall and antivirus logs
5. Open an issue on GitHub with:
   - Operating system and version
   - Python version (`python --version`)
   - Error message (full output)
   - Command you ran

---

## ❓ FAQ

### General Questions

**Q: Is this tool free?**  
A: Yes, completely free and open-source.

**Q: Can I use this in a corporate environment?**  
A: Yes, but always follow your company's security policies and get approval before scanning networks.

**Q: Does this work on Wi-Fi networks?**  
A: Yes, works on both wired and wireless networks.

**Q: Can it scan remote networks over the internet?**  
A: No, this is designed for local network scanning only.

---

### Technical Questions

**Q: Why do I need administrator/root privileges?**  
A: ARP scanning requires raw packet access, which needs elevated privileges. Some features work without admin but are limited.

**Q: How fast is the scanning?**  
A: Device discovery: 5-10 seconds. Port scanning: 2-5 minutes for 73 devices on ports 1-1000.

**Q: Can I automate this?**  
A: Yes! Use Windows Task Scheduler or cron (Linux/Mac) to run scans automatically.

**Q: What's the difference between `discover` and `scan`?**  
A: `discover` only finds devices (fast). `scan` also checks ports (slower but more info).

**Q: Why can't I see devices on hotspots?**  
A: Hotspots create separate networks with NAT. Use `multi_network_scanner.py scan-all` to find them.

---

### Security Questions

**Q: Is this tool safe to use?**  
A: Yes, it's passive scanning. However, always get permission before scanning networks you don't own.

**Q: Will this trigger security alerts?**  
A: Possibly. Port scanning can trigger IDS/IPS systems. Only scan networks you're authorized to scan.

**Q: Can this harm devices?**  
A: No, it only makes connection attempts. It doesn't exploit vulnerabilities or send malicious traffic.

**Q: What data is collected?**  
A: Only network data (IP, MAC, ports). Nothing is sent to external servers.

---

### Comparison Questions

**Q: How is this different from Nmap?**  
A: Nmap is more powerful but complex. This tool is simpler, Python-based, and designed for quick network inventory.

**Q: Can I replace Spiceworks with this?**  
A: For basic network discovery and inventory, yes. Spiceworks has more features (ticketing, monitoring, etc.).

**Q: Why use this instead of built-in tools?**  
A: Combines multiple tools (ARP, port scanning, reporting) in one place with easy export options.

---

## 🚀 Advanced Usage

### Automated Scheduled Scans

**Windows Task Scheduler:**

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily, weekly)
4. Action: Start a program
   - Program: `C:\Python313\python.exe`
   - Arguments: `C:\path\to\scanner.py scan 192.168.44.0/24 --export-csv C:\scans\daily.csv`
5. Run with highest privileges

**Linux Cron:**
```bash
# Edit crontab
crontab -e

# Add daily scan at 2 AM
0 2 * * * cd /path/to/scanner && python scanner.py scan 192.168.44.0/24 --export-csv /var/scans/daily_$(date +\%Y\%m\%d).csv
```

---

### Custom Port Profiles

Create shortcuts for common scan types:

**Web Server Scan:**
```bash
python scanner.py scan 192.168.44.0/24 --ports 80,443,8080,8443
```

**Database Scan:**
```bash
python scanner.py scan 192.168.44.0/24 --ports 1433,3306,5432,27017
```

**Windows Services:**
```bash
python scanner.py scan 192.168.44.0/24 --ports 135,139,445,3389
```

**Security Audit:**
```bash
python scanner.py scan 192.168.44.0/24 --ports 21,22,23,25,80,443,445,3389,8080
```

---

### Comparing Scans Over Time

```bash
# Day 1
python scanner.py scan 192.168.44.0/24 --export-json scan_day1.json

# Day 7
python scanner.py scan 192.168.44.0/24 --export-json scan_day7.json

# Compare with Python
python compare_scans.py scan_day1.json scan_day7.json
```

**Create compare_scans.py:**
```python
import json
import sys

with open(sys.argv[1]) as f:
    scan1 = json.load(f)
with open(sys.argv[2]) as f:
    scan2 = json.load(f)

ips1 = {d['ip'] for d in scan1['devices']}
ips2 = {d['ip'] for d in scan2['devices']}

new = ips2 - ips1
removed = ips1 - ips2

print(f"New devices: {new}")
print(f"Removed devices: {removed}")
```

---

### Integration with Other Tools

**Export to Database:**
```python
import json
import sqlite3

# Load scan
with open('scan.json') as f:
    data = json.load(f)

# Insert into database
conn = sqlite3.connect('network.db')
cursor = conn.cursor()

for device in data['devices']:
    cursor.execute(
        'INSERT INTO devices VALUES (?, ?, ?, ?)',
        (device['ip'], device['mac'], device['hostname'], device['vendor'])
    )

conn.commit()
```

**Send Email Alerts:**
```python
import smtplib
import json

with open('scan.json') as f:
    data = json.load(f)

if len(data['devices']) > 100:
    # Send alert email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # ... email code ...
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

**Ideas for contributions:**
- Additional export formats (HTML, XML)
- GUI interface
- Historical database tracking
- Alert system for changes
- SNMP support
- WMI queries for Windows
- Better OS detection

---

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🙏 Acknowledgments

Built with:
- **Scapy** - Packet manipulation
- **python-nmap** - Nmap integration
- **Rich** - Beautiful terminal output
- **Click** - CLI framework
- **netaddr** - Network address manipulation
- **mac-vendor-lookup** - MAC address database

---

## 📞 Support

- **Documentation**: See all .md files in this folder
- **Examples**: [COMMAND_EXAMPLES.md](COMMAND_EXAMPLES.md)
- **Installation Help**: [INSTALLATION.md](INSTALLATION.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Created with ❤️ for network administrators and IT professionals**

**Version 1.0.0** | Last Updated: November 2025
