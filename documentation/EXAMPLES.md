# Practical Examples - Network Scanner

Real-world use cases and detailed walkthroughs.

---

## Table of Contents

- [Scenario 1: First Time Network Audit](#scenario-1-first-time-network-audit)
- [Scenario 2: Finding Rogue Devices](#scenario-2-finding-rogue-devices)
- [Scenario 3: Security Vulnerability Scan](#scenario-3-security-vulnerability-scan)
- [Scenario 4: Printer Discovery](#scenario-4-printer-discovery)
- [Scenario 5: IoT Device Inventory](#scenario-5-iot-device-inventory)
- [Scenario 6: Hotspot Device Tracking](#scenario-6-hotspot-device-tracking)
- [Scenario 7: Network Change Monitoring](#scenario-7-network-change-monitoring)
- [Scenario 8: Automated Daily Scans](#scenario-8-automated-daily-scans)
- [Scenario 9: Multi-Location Network Audit](#scenario-9-multi-location-network-audit)
- [Scenario 10: Troubleshooting Network Issues](#scenario-10-troubleshooting-network-issues)

---

## Scenario 1: First Time Network Audit

**Goal:** Create a complete inventory of all devices on your office network.

**Context:** New IT admin needs to document all devices.

### Step-by-Step

**Step 1: Identify Your Network**
```bash
# Check your computer's IP
ipconfig  # Windows
ifconfig  # Linux/Mac
```

**Output:**
```
IPv4 Address. . . . . . . . . . . : 192.168.44.96
Subnet Mask . . . . . . . . . . . : 255.255.255.0
Default Gateway . . . . . . . . . : 192.168.44.1
```

**Your network is:** `192.168.44.0/24`

**Step 2: Run Quick Discovery**
```bash
python scanner.py discover 192.168.44.0/24
```

**Output:**
```
Discovering hosts on 192.168.44.0/24...
Starting ARP scan on 192.168.44.0/24...
✓ Discovered 73 devices

╭──────────────────────── Network Scan Results ────────────────────────╮
│  IP Address      MAC Address        Hostname           Vendor        │
│ ──────────────────────────────────────────────────────────────────── │
│  192.168.44.1    bc-cf-4f-b8-99-3b  gateway            TP-Link       │
│  192.168.44.5    bc-9b-5e-b8-44-81  desktop-admin      Dell Inc.     │
│  ...             ...                ...                ...            │
╰───────────────────────────────────────────────────────────────────────╯

Total devices found: 73
```

**Step 3: Full Scan with Ports**
```bash
python scanner.py scan 192.168.44.0/24 --export-csv network_audit.csv --export-json network_audit.json
```

**Step 4: Analyze Results**

Open `network_audit.csv` in Excel:

1. **Sort by Vendor** - Group similar devices
2. **Filter by Open Ports** - Find active services
3. **Look for:**
   - Unknown devices
   - Unexpected open ports
   - Duplicate IPs
   - Missing hostnames

**Step 5: Document Findings**

Create a report:
- Total devices: 73
- Breakdown by vendor:
  - Dell: 15 desktops
  - HP: 8 laptops
  - Apple: 12 phones/tablets
  - TP-Link: 3 routers/switches
  - Samsung: 5 TVs/monitors
  - Unknown: 30 devices (investigate!)

**Next Actions:**
- Investigate unknown devices
- Update network documentation
- Set baseline for future comparisons

---

## Scenario 2: Finding Rogue Devices

**Goal:** Identify unauthorized devices that shouldn't be on the network.

**Context:** Security concern - want to ensure only authorized devices are connected.

### Workflow

**Step 1: Create Baseline (Day 1)**
```bash
python scanner.py scan 192.168.44.0/24 --export-json baseline_monday.json
```

**Step 2: Regular Scan (Day 7)**
```bash
python scanner.py scan 192.168.44.0/24 --export-json current_monday.json
```

**Step 3: Compare Results**

Create `compare_scans.py`:
```python
#!/usr/bin/env python3
import json
import sys

def load_scan(filename):
    with open(filename) as f:
        data = json.load(f)
    return {d['ip']: d for d in data['devices']}

# Load scans
baseline = load_scan(sys.argv[1])
current = load_scan(sys.argv[2])

# Find differences
baseline_ips = set(baseline.keys())
current_ips = set(current.keys())

new_devices = current_ips - baseline_ips
removed_devices = baseline_ips - current_ips

# Report new devices
if new_devices:
    print(f"\n🚨 NEW DEVICES DETECTED: {len(new_devices)}\n")
    for ip in new_devices:
        device = current[ip]
        print(f"IP: {ip}")
        print(f"  MAC: {device.get('mac', 'Unknown')}")
        print(f"  Hostname: {device.get('hostname', 'Unknown')}")
        print(f"  Vendor: {device.get('vendor', 'Unknown')}")
        print(f"  Open Ports: {device.get('open_ports', [])}")
        print()

# Report removed devices
if removed_devices:
    print(f"\n📤 REMOVED DEVICES: {len(removed_devices)}\n")
    for ip in removed_devices:
        device = baseline[ip]
        print(f"IP: {ip}")
        print(f"  Hostname: {device.get('hostname', 'Unknown')}")
        print()

# Report if no changes
if not new_devices and not removed_devices:
    print("✅ No changes detected")
```

**Step 4: Run Comparison**
```bash
python compare_scans.py baseline_monday.json current_monday.json
```

**Output:**
```
🚨 NEW DEVICES DETECTED: 2

IP: 192.168.44.175
  MAC: aa-bb-cc-dd-ee-ff
  Hostname: Unknown
  Vendor: Unknown
  Open Ports: []

IP: 192.168.44.201
  MAC: 11-22-33-44-55-66
  Hostname: android-xyz
  Vendor: Samsung
  Open Ports: []
```

**Step 5: Investigate**
- Check if these are legitimate devices
- Ask employees if they connected new devices
- Check physical locations
- If unauthorized:
  - Block MAC address on router
  - Investigate security breach
  - Update policies

---

## Scenario 3: Security Vulnerability Scan

**Goal:** Find devices with potentially dangerous open ports.

**Context:** Monthly security audit to find vulnerabilities.

### Security Port Checklist

**High-Risk Ports:**
- 21 (FTP) - Unencrypted file transfer
- 23 (Telnet) - Unencrypted remote access
- 445 (SMB) - File sharing vulnerabilities
- 3389 (RDP) - Remote desktop exposure

**Step 1: Scan for Vulnerable Ports**
```bash
python scanner.py scan 192.168.44.0/24 \
  --ports 21,22,23,25,80,135,139,445,3389,5900 \
  --export-csv security_audit.csv
```

**Step 2: Analyze Results**

Open `security_audit.csv` and filter for specific ports:

**Critical Findings Example:**

| IP | Hostname | Vendor | Open Ports | Risk Level |
|----|----------|--------|-----------|------------|
| 192.168.44.50 | old-server | HP | 21, 23, 80 | 🔴 CRITICAL |
| 192.168.44.75 | legacy-device | Dell | 23, 445 | 🟠 HIGH |
| 192.168.44.100 | workstation-1 | Dell | 3389 | 🟡 MEDIUM |

**Step 3: Create Remediation Plan**

**Port 21 (FTP):**
- Action: Replace with SFTP (port 22)
- Timeline: Immediate
- Owner: Network team

**Port 23 (Telnet):**
- Action: Disable and use SSH instead
- Timeline: This week
- Owner: System admin

**Port 445 (SMB):**
- Action: Ensure latest patches, consider disabling if not needed
- Timeline: Verify this week
- Owner: Security team

**Port 3389 (RDP):**
- Action: Implement VPN requirement, change default port
- Timeline: Next month
- Owner: IT manager

**Step 4: Document and Track**

Create tracking spreadsheet:
```csv
IP,Port,Risk,Action,Status,Owner,Due Date
192.168.44.50,21,Critical,Disable FTP,In Progress,John,2025-11-25
192.168.44.50,23,Critical,Disable Telnet,In Progress,John,2025-11-25
192.168.44.75,23,High,Replace with SSH,Pending,Mary,2025-11-30
```

**Step 5: Re-scan After Fixes**
```bash
python scanner.py scan 192.168.44.0/24 --ports 21,23 --export-csv post_fix.csv
```

Verify vulnerable ports are closed.

---

## Scenario 4: Printer Discovery

**Goal:** Find all network printers for inventory and maintenance.

**Context:** Need to update printer firmware and create printer map.

### Printer Discovery

**Step 1: Scan Printer Ports**
```bash
python scanner.py scan 192.168.44.0/24 --ports 9100,515,631,80,443 --export-csv printers.csv
```

**Port Reference:**
- 9100: Raw printing (HP JetDirect)
- 515: LPD (Line Printer Daemon)
- 631: IPP (Internet Printing Protocol)
- 80/443: Web admin interface

**Step 2: Analyze Results**

**Example Output:**

| IP | Hostname | Vendor | Open Ports |
|----|----------|--------|-----------|
| 192.168.44.14 | printer-hp-1 | Hewlett-Packard | 80, 443, 9100 |
| 192.168.44.27 | printer-canon | Canon | 80, 9100 |
| 192.168.44.35 | printer-epson | Epson | 631, 9100 |
| 192.168.44.52 | mfp-ricoh | Ricoh | 80, 443, 9100 |

**Step 3: Create Printer Map**

Document each printer:

**Printer 1:**
- IP: 192.168.44.14
- Model: HP LaserJet Pro (check via web interface)
- Location: 2nd Floor - Room 201
- Purpose: General office printing
- Users: Marketing team
- Firmware: Check http://192.168.44.14

**Step 4: Access Web Interface**
```bash
# Open in browser
http://192.168.44.14
```

Check:
- Firmware version
- Supply levels
- Configuration
- Security settings

**Step 5: Maintenance Schedule**

Create maintenance plan:
```csv
IP,Model,Location,Last Check,Firmware,Next Update
192.168.44.14,HP LJ Pro,2F-201,2025-11-20,v1.2,2025-12-20
192.168.44.27,Canon MF,1F-105,2025-11-20,v2.1,2025-12-20
```

---

## Scenario 5: IoT Device Inventory

**Goal:** Identify all smart devices (cameras, thermostats, smart TVs, etc.).

**Context:** Security audit requires inventory of all IoT devices.

### IoT Discovery Strategy

**Step 1: Full Network Scan**
```bash
python scanner.py scan 192.168.44.0/24 --export-csv full_network.csv
```

**Step 2: Identify IoT Devices**

Open CSV in Excel and look for:

**Common IoT Vendors:**
- Xiaomi (smart home)
- Hikvision / Dahua (cameras)
- Shenzhen companies (various)
- Tuya (smart plugs)
- TP-Link / D-Link (smart devices)
- Ring / Nest (cameras, doorbells)
- Philips Hue (smart lights)
- Samsung (smart TVs)

**Filter by:**
1. **Vendor column** - search for IoT brands
2. **Unknown hostnames** - often IoT devices don't set proper hostnames
3. **Unusual IPs** - devices often get higher IPs from DHCP

**Example IoT Devices Found:**

| IP | MAC | Hostname | Vendor | Likely Device |
|----|-----|----------|--------|---------------|
| 192.168.44.19 | 4c-4b-f9-... | camera-front | Hikvision | Security Camera |
| 192.168.44.31 | a4-c3-f0-... | Unknown | Xiaomi | Smart Plug |
| 192.168.44.45 | b0-be-76-... | Unknown | TP-Link | Smart Bulb |
| 192.168.44.58 | 18-b4-30-... | ring-doorbell | Amazon | Doorbell Camera |

**Step 3: Port Scan IoT Devices**
```bash
# Scan specific IPs with wide port range
python scanner.py scan 192.168.44.19/32 --ports 1-10000 --export-csv camera_ports.csv
```

**Common IoT Ports:**
- 554: RTSP (camera streaming)
- 8080: HTTP alt (web interface)
- 8081-8089: Various web services
- 1883: MQTT (IoT messaging)
- 5353: mDNS (service discovery)

**Step 4: Security Assessment**

For each IoT device, check:

**Camera (192.168.44.19):**
```bash
# Check web interface
http://192.168.44.19

# Common issues:
# - Default password still set?
# - Firmware outdated?
# - Unnecessary ports open?
# - Accessible from internet?
```

**Action Items:**
1. Change default passwords
2. Update firmware
3. Disable UPnP
4. Create separate IoT VLAN (if possible)
5. Document all devices

**Step 5: Create IoT Inventory**

```csv
IP,Device Type,Model,Vendor,Location,Last Update,Firmware,Password Changed
192.168.44.19,Camera,DS-2CD2142FWD,Hikvision,Front Door,2025-11-20,v5.6.3,Yes
192.168.44.31,Smart Plug,Mi Smart,Xiaomi,Living Room,2025-11-20,v1.4,N/A
192.168.44.45,Smart Bulb,Kasa LB100,TP-Link,Office,2025-11-20,v2.1,N/A
```

---

## Scenario 6: Hotspot Device Tracking

**Goal:** Find devices connected through desktop Wi-Fi hotspots.

**Context:** Office policy allows personal hotspots, need to track what's connected.

### Multi-Network Discovery

**Step 1: Detect All Networks**
```bash
python multi_network_scanner.py detect-networks
```

**Output:**
```
Detected Networks:
  • 192.168.44.0/24      (Main office network)
  • 192.168.137.0/24     (Windows hotspot detected)

Common Hotspot Networks:
  • 192.168.137.0/24 (Windows Mobile Hotspot)
  • 192.168.0.0/24
  • 192.168.1.0/24
  • 172.20.10.0/24 (iPhone Hotspot)
```

**Step 2: Scan All Networks**
```bash
python multi_network_scanner.py scan-all --export-csv all_networks.csv
```

**Output:**
```
╭──────────── Network: 192.168.44.0/24 (70 devices) ─────────────╮
│  IP              MAC              Hostname        Vendor       │
│  192.168.44.1    bc-cf-4f-b8-9b  gateway         TP-Link      │
│  192.168.44.5    bc-9b-5e-b8-81  desktop-john    Dell Inc.    │
│  ...                                                           │
╰─────────────────────────────────────────────────────────────────╯

╭──────────── Network: 192.168.137.0/24 (3 devices) ─────────────╮
│  IP              MAC              Hostname        Vendor       │
│  192.168.137.1   d8-bb-c1-56-93  DESKTOP-JOHN    Intel        │
│  192.168.137.50  a4-c3-f0-5e-2a  android-phone   Samsung      │
│  192.168.137.51  44-61-32-a1-b3  Unknown         Apple        │
╰─────────────────────────────────────────────────────────────────╯

Total devices found: 73
Networks scanned: 2
```

**Step 3: Analyze Hotspot Usage**

Findings:
- John's desktop (192.168.44.5) is running a hotspot
- 2 devices connected to his hotspot:
  - Samsung phone
  - Apple device (iPad?)

**Step 4: Policy Enforcement**

**If hotspots are allowed:**
- Document which employees use hotspots
- Track connected devices
- Ensure no business data on personal devices

**If hotspots are not allowed:**
- Contact John
- Explain policy
- Disable mobile hotspot feature
- Block hotspot detection in Group Policy

**Step 5: Monitor Regularly**
```bash
# Run daily
python multi_network_scanner.py scan-all --export-csv daily_$(date +%Y%m%d).csv
```

**Alert on new hotspot networks:**
```python
# Script to alert on new networks
import json
import sys

baseline_networks = ['192.168.44.0/24']

with open(sys.argv[1]) as f:
    scan = json.load(f)

# Get unique networks
networks = set(d.get('network') for d in scan['devices'] if d.get('network'))

new_networks = networks - set(baseline_networks)

if new_networks:
    print(f"🚨 NEW NETWORKS DETECTED:")
    for net in new_networks:
        print(f"  - {net}")
else:
    print("✅ No new networks")
```

---

## Scenario 7: Network Change Monitoring

**Goal:** Track changes in network over time.

**Context:** Want to know immediately when devices join/leave network.

### Automated Monitoring

**Step 1: Create Baseline**
```bash
# Initial scan
python scanner.py scan 192.168.44.0/24 --export-json baseline.json
```

**Step 2: Create Monitoring Script**

`monitor_network.py`:
```python
#!/usr/bin/env python3
"""
Network Change Monitor
Compares current scan to baseline and alerts on changes
"""

import json
import subprocess
import sys
from datetime import datetime

def load_devices(filename):
    """Load devices from JSON file"""
    with open(filename) as f:
        data = json.load(f)
    return {d['ip']: d for d in data['devices']}

def run_scan(network):
    """Run a new scan and return devices"""
    # Run scanner
    subprocess.run([
        'python', 'scanner.py', 'scan', network,
        '--export-json', 'current_scan.json'
    ], capture_output=True)
    
    return load_devices('current_scan.json')

def compare_and_alert(baseline, current):
    """Compare scans and print alerts"""
    baseline_ips = set(baseline.keys())
    current_ips = set(current.keys())
    
    new = current_ips - baseline_ips
    removed = baseline_ips - current_ips
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if new or removed:
        print(f"\n{'='*60}")
        print(f"NETWORK CHANGES DETECTED - {timestamp}")
        print(f"{'='*60}\n")
        
        if new:
            print(f"🆕 NEW DEVICES ({len(new)}):")
            for ip in new:
                d = current[ip]
                print(f"\n  IP: {ip}")
                print(f"  MAC: {d.get('mac', 'Unknown')}")
                print(f"  Hostname: {d.get('hostname', 'Unknown')}")
                print(f"  Vendor: {d.get('vendor', 'Unknown')}")
        
        if removed:
            print(f"\n📤 REMOVED DEVICES ({len(removed)}):")
            for ip in removed:
                d = baseline[ip]
                print(f"\n  IP: {ip}")
                print(f"  Hostname: {d.get('hostname', 'Unknown')}")
    else:
        print(f"✅ No changes detected - {timestamp}")

if __name__ == '__main__':
    network = sys.argv[1] if len(sys.argv) > 1 else '192.168.44.0/24'
    
    # Load baseline
    baseline = load_devices('baseline.json')
    
    # Run new scan
    print(f"Scanning {network}...")
    current = run_scan(network)
    
    # Compare and alert
    compare_and_alert(baseline, current)
```

**Step 3: Schedule Monitoring**

**Windows Task Scheduler:**
```cmd
# Create task to run every hour
schtasks /create /tn "Network Monitor" /tr "python C:\scanner\monitor_network.py" /sc hourly /ru SYSTEM
```

**Linux Cron:**
```bash
# Add to crontab - run every hour
0 * * * * cd /home/admin/scanner && python3 monitor_network.py >> monitor.log 2>&1
```

**Step 4: Email Alerts (Optional)**

Add to `monitor_network.py`:
```python
def send_email_alert(subject, body):
    """Send email alert"""
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'scanner@company.com'
    msg['To'] = 'admin@company.com'
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your-email@gmail.com', 'your-app-password')
        server.send_message(msg)

# Call in compare_and_alert function when changes detected
if new or removed:
    alert_text = f"New devices: {len(new)}, Removed: {len(removed)}"
    send_email_alert("Network Changes Detected", alert_text)
```

---

## Scenario 8: Automated Daily Scans

**Goal:** Run automatic scans and save results for historical analysis.

**Context:** Compliance requires daily network inventory.

### Automated Scanning Setup

**Step 1: Create Scan Script**

`daily_scan.bat` (Windows):
```batch
@echo off
REM Daily Network Scan Script
SET SCAN_DATE=%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%
SET SCAN_DIR=C:\NetworkScans\

REM Run scan
python C:\scanner\scanner.py scan 192.168.44.0/24 ^
  --export-csv %SCAN_DIR%scan_%SCAN_DATE%.csv ^
  --export-json %SCAN_DIR%scan_%SCAN_DATE%.json

REM Cleanup old scans (keep 30 days)
forfiles /p %SCAN_DIR% /m *.csv /d -30 /c "cmd /c del @path"

echo Scan complete: scan_%SCAN_DATE%.csv
```

`daily_scan.sh` (Linux):
```bash
#!/bin/bash
# Daily Network Scan Script

SCAN_DATE=$(date +%Y%m%d)
SCAN_DIR="/var/scans/"

# Run scan
python3 /opt/scanner/scanner.py scan 192.168.44.0/24 \
  --export-csv ${SCAN_DIR}scan_${SCAN_DATE}.csv \
  --export-json ${SCAN_DIR}scan_${SCAN_DATE}.json

# Cleanup old scans (keep 30 days)
find ${SCAN_DIR} -name "scan_*.csv" -mtime +30 -delete

echo "Scan complete: scan_${SCAN_DATE}.csv"
```

**Step 2: Schedule Script**

**Windows:**
```cmd
schtasks /create ^
  /tn "Daily Network Scan" ^
  /tr "C:\scanner\daily_scan.bat" ^
  /sc daily ^
  /st 02:00 ^
  /ru SYSTEM
```

**Linux:**
```bash
# Add to crontab
sudo crontab -e

# Add line (runs at 2 AM daily)
0 2 * * * /opt/scanner/daily_scan.sh >> /var/log/network_scan.log 2>&1
```

**Step 3: Analysis Script**

`analyze_history.py`:
```python
#!/usr/bin/env python3
"""Analyze historical scans"""

import json
import glob
from collections import defaultdict
from datetime import datetime

def load_scans(directory):
    """Load all scan files"""
    scans = []
    for file in sorted(glob.glob(f"{directory}/scan_*.json")):
        with open(file) as f:
            data = json.load(f)
            scans.append({
                'date': data['scan_time'][:10],
                'devices': {d['ip']: d for d in data['devices']}
            })
    return scans

def analyze_trends(scans):
    """Analyze device count trends"""
    print("Device Count Trends:")
    print("-" * 40)
    for scan in scans:
        print(f"{scan['date']}: {len(scan['devices'])} devices")

def find_frequent_joiners(scans):
    """Find devices that frequently join/leave"""
    device_appearances = defaultdict(list)
    
    all_ips = set()
    for scan in scans:
        all_ips.update(scan['devices'].keys())
    
    for ip in all_ips:
        for scan in scans:
            device_appearances[ip].append(ip in scan['devices'])
    
    # Find devices with <80% uptime
    print("\nFrequent Joiners/Leavers (< 80% uptime):")
    print("-" * 40)
    for ip, appearances in device_appearances.items():
        uptime = sum(appearances) / len(appearances)
        if uptime < 0.8:
            hostname = "Unknown"
            for scan in scans:
                if ip in scan['devices']:
                    hostname = scan['devices'][ip].get('hostname', 'Unknown')
                    break
            print(f"{ip} ({hostname}): {uptime*100:.1f}% uptime")

if __name__ == '__main__':
    scans = load_scans('/var/scans/')
    analyze_trends(scans)
    find_frequent_joiners(scans)
```

---

## Scenario 9: Multi-Location Network Audit

**Goal:** Audit networks across multiple office locations.

**Context:** Company has offices in 3 cities, need unified inventory.

### Multi-Location Strategy

**Location Setup:**
- **HQ Office**: 192.168.10.0/24
- **Branch 1**: 192.168.20.0/24
- **Branch 2**: 192.168.30.0/24

**Step 1: Deploy Scanner**

Install scanner on computer at each location:
```bash
# Install on each site
pip install -r requirements.txt
```

**Step 2: Create Site-Specific Scripts**

`scan_hq.bat`:
```batch
python scanner.py scan 192.168.10.0/24 --export-csv HQ_scan.csv
```

`scan_branch1.bat`:
```batch
python scanner.py scan 192.168.20.0/24 --export-csv Branch1_scan.csv
```

**Step 3: Collect Results**

**Option A: Manual Collection**
- Email CSV files to central IT
- Consolidate in master spreadsheet

**Option B: Automated Collection**
```bash
# Upload to shared folder
python scanner.py scan 192.168.10.0/24 --export-json scan.json
# Copy to shared drive
copy scan.json \\fileserver\NetworkScans\HQ_scan.json
```

**Step 4: Consolidate Data**

`consolidate_sites.py`:
```python
#!/usr/bin/env python3
"""Consolidate multi-site scans"""

import json
import pandas as pd

sites = {
    'HQ': 'HQ_scan.json',
    'Branch1': 'Branch1_scan.json',
    'Branch2': 'Branch2_scan.json'
}

all_devices = []

for site, filename in sites.items():
    with open(filename) as f:
        data = json.load(f)
        for device in data['devices']:
            device['site'] = site
            all_devices.append(device)

# Create consolidated report
df = pd.DataFrame(all_devices)
df.to_csv('consolidated_inventory.csv', index=False)

# Site summary
print("\nDevice Count by Site:")
print(df.groupby('site').size())

print("\nVendor Distribution by Site:")
print(df.groupby(['site', 'vendor']).size().unstack(fill_value=0))
```

**Output:**
```
Device Count by Site:
HQ         73
Branch1    45
Branch2    38

Vendor Distribution by Site:
            Dell  HP  Apple  TP-Link  Samsung
HQ           25   15    12       3        5
Branch1      18   10     8       2        3
Branch2      15    8     7       1        2
```

---

## Scenario 10: Troubleshooting Network Issues

**Goal:** Diagnose connectivity issues using network scanner.

**Context:** Users report intermittent connectivity issues.

### Troubleshooting Workflow

**Issue: "Printer not responding"**

**Step 1: Verify Printer Online**
```bash
# Quick check if printer IP is reachable
python scanner.py discover 192.168.44.14/32
```

**Result:** Printer found? ✅ Continue. Not found? ❌ Printer offline.

**Step 2: Check Printer Ports**
```bash
# Check if printer services are running
python scanner.py scan 192.168.44.14/32 --ports 9100,631,80
```

**Expected:** Ports 9100, 80 open  
**If closed:** Printer service crashed, restart printer.

**Step 3: Check Network Path**
```bash
# Verify no IP conflicts
python scanner.py discover 192.168.44.0/24 | grep "192.168.44.14"
```

**Issue: "Can't access file server"**

**Step 1: Verify Server Online**
```bash
python scanner.py scan 192.168.44.50/32 --ports 445,139
```

**Step 2: Check All SMB Devices**
```bash
# Find all file shares
python scanner.py scan 192.168.44.0/24 --ports 445 --export-csv file_servers.csv
```

**Issue: "Network slow"**

**Step 1: Count Active Devices**
```bash
python scanner.py discover 192.168.44.0/24
```

**Normal:** 70-80 devices  
**Today:** 150 devices ← Problem!

**Step 2: Investigate New Devices**
- Compare to baseline
- Find unauthorized devices
- Check for bandwidth hogs

---

## Summary

These examples demonstrate:
- ✅ Network auditing and documentation
- ✅ Security vulnerability assessment  
- ✅ Device tracking and monitoring
- ✅ Automated scanning and alerting
- ✅ Multi-location management
- ✅ Troubleshooting workflows

**Key Takeaways:**
1. Always create baselines for comparison
2. Export results for analysis
3. Automate regular scans
4. Document findings
5. Take action on discoveries

---

For more information:
- [README.md](README.md) - Complete documentation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command cheat sheet
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Problem solving
