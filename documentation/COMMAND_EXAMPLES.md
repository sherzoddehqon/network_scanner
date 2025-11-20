# Network Scanner - Command Output Examples

This document shows example outputs for each command to help you understand what to expect.

---

## Command 1: `scanner.py discover 192.168.44.0/24`

**Purpose:** Quick host discovery without port scanning

**Example Output:**

```
D:\network_scanner>py scanner.py discover 192.168.44.0/24

Discovering hosts on 192.168.44.0/24...

Starting ARP scan on 192.168.44.0/24...
✓ Discovered 41 devices


╭──────────────────────── Network Scan Results ────────────────────────╮
│                                                                       │
│  IP Address      MAC Address        Hostname           Vendor        │
│ ──────────────────────────────────────────────────────────────────── │
│  192.168.44.1    bc-cf-4f-b8-99-3b  router.local       TP-Link       │
│  192.168.44.5    bc-9b-5e-b8-44-81  desktop-john       Dell Inc.     │
│  192.168.44.6    80-7c-62-c9-bf-90  laptop-mary        HP Inc.       │
│  192.168.44.9    bc-9b-5e-b8-44-79  Unknown            ASUSTek       │
│  192.168.44.10   cc-8e-71-fa-8d-4c  iphone-12          Apple, Inc.   │
│  192.168.44.12   34-60-f9-13-92-cd  samsung-tv         Samsung       │
│  192.168.44.14   e4-5a-d4-51-d0-c0  printer-hp         Hewlett-Pack  │
│  192.168.44.15   e4-5a-d4-50-ec-80  Unknown            Xiaomi        │
│  192.168.44.17   00-15-5d-2c-77-5c  vm-server          Microsoft     │
│  192.168.44.19   4c-4b-f9-53-ff-fe  camera-front       Hikvision     │
│  ...             ...                ...                ...           │
│  192.168.44.96   d8-bb-c1-56-e0-93  YOUR-COMPUTER      Intel Corp    │
│                                                                       │
╰───────────────────────────────────────────────────────────────────────╯

Total devices found: 41
```

**Key Information Displayed:**
- ✅ IP Address of each device
- ✅ MAC Address (hardware address)
- ✅ Hostname (if available)
- ✅ Vendor/Manufacturer from MAC address
- ❌ NO Port information (use 'scan' command for ports)

**Time:** ~5-10 seconds

---

## Command 2: `scanner.py scan 192.168.44.0/24`

**Purpose:** Full network scan with host discovery AND port scanning

**Example Output:**

```
D:\network_scanner>py scanner.py scan 192.168.44.0/24

╭───────────────────────────────────────╮
│  Network Scanner v1.0                 │
│  Scanning: 192.168.44.0/24            │
╰───────────────────────────────────────╯

Starting ARP scan on 192.168.44.0/24...
✓ Discovered 73 devices

Starting port scan on 73 devices...

Scanning 192.168.44.1...
✓ 192.168.44.1: Found 4 open ports

Scanning 192.168.44.5...
✓ 192.168.44.5: Found 2 open ports

Scanning 192.168.44.6...
○ 192.168.44.6: No open ports found

Scanning 192.168.44.10...
○ 192.168.44.10: No open ports found

Scanning 192.168.44.12...
✓ 192.168.44.12: Found 1 open ports

Scanning 192.168.44.14...
✓ 192.168.44.14: Found 3 open ports

...

Scanning 192.168.44.96...
✓ 192.168.44.96: Found 8 open ports


╭────────────────────────── Network Scan Results ──────────────────────────╮
│                                                                           │
│  IP Address    MAC Address      Hostname        Vendor       Open Ports  │
│ ───────────────────────────────────────────────────────────────────────  │
│  192.168.44.1  bc-cf-4f-b8-9b  router.local    TP-Link      80, 443,    │
│                                                              8080, 22     │
│  192.168.44.5  bc-9b-5e-b8-81  desktop-john    Dell Inc.    445, 3389    │
│  192.168.44.6  80-7c-62-c9-90  laptop-mary     HP Inc.      None         │
│  192.168.44.10 cc-8e-71-fa-4c  iphone-12       Apple, Inc.  None         │
│  192.168.44.12 34-60-f9-13-cd  samsung-tv      Samsung      8080         │
│  192.168.44.14 e4-5a-d4-51-c0  printer-hp      HP           80, 443, 9100│
│  192.168.44.96 d8-bb-c1-56-93  YOUR-COMPUTER   Intel Corp   80, 135, 139,│
│                                                              445, 3389,   │
│                                                              5040, 5357,  │
│                                                              8080         │
│  ...           ...              ...             ...          ...          │
│                                                                           │
╰───────────────────────────────────────────────────────────────────────────╯

Total devices found: 73
```

**Additional Information:**
- ✅ Everything from 'discover' command
- ✅ Open ports on each device (1-1000 by default)
- ✅ Service names (http, https, ssh, rdp, etc.)

**Time:** ~2-5 minutes for 73 devices (depends on network and port range)

**Common Open Ports You'll See:**
- 22 = SSH (remote access)
- 80 = HTTP (web server)
- 443 = HTTPS (secure web)
- 445 = SMB (file sharing)
- 3389 = RDP (Remote Desktop)
- 8080 = Alternative HTTP
- 9100 = Printer

---

## Command 3: `multi_network_scanner.py detect-networks`

**Purpose:** Detect all network interfaces on your computer

**Example Output:**

```
D:\network_scanner>py multi_network_scanner.py detect-networks


Detected Networks:
  • 192.168.44.0/24
  • 192.168.137.0/24

Common Hotspot Networks:
  • 192.168.137.0/24 (Windows Mobile Hotspot)
  • 192.168.0.0/24
  • 192.168.1.0/24
  • 172.20.10.0/24 (iPhone Hotspot)
```

**What This Shows:**
- ✅ All networks your computer is connected to
- ✅ Ethernet networks
- ✅ WiFi networks
- ✅ Virtual adapters (VM, VPN, Hotspot)
- ℹ️ Common hotspot ranges to check

**Time:** Instant (<1 second)

**Use Case:** Run this FIRST to know which networks to scan

---

## Command 4: `multi_network_scanner.py scan-all`

**Purpose:** Scan ALL networks including hotspots automatically

**Example Output:**

```
D:\network_scanner>py multi_network_scanner.py scan-all

╭────────────────────────────────────────╮
│  Multi-Network Scanner                 │
│  Scanning 6 networks                   │
╰────────────────────────────────────────╯

Networks to scan:
  • 192.168.44.0/24
  • 192.168.137.0/24
  • 192.168.0.0/24
  • 192.168.1.0/24
  • 172.20.10.0/24


Scanning 192.168.44.0/24...
✓ Found 73 devices on 192.168.44.0/24

Scanning 192.168.137.0/24...
✓ Found 3 devices on 192.168.137.0/24

Scanning 192.168.0.0/24...
Could not scan 192.168.0.0/24: Network unreachable

Scanning 192.168.1.0/24...
Could not scan 192.168.1.0/24: Network unreachable

Scanning 172.20.10.0/24...
✓ Found 0 devices on 172.20.10.0/24


╭──────────── Network: 192.168.44.0/24 (73 devices) ─────────────╮
│                                                                 │
│  IP Address    MAC Address      Hostname        Vendor         │
│ ────────────────────────────────────────────────────────────   │
│  192.168.44.1  bc-cf-4f-b8-9b  router.local    TP-Link        │
│  192.168.44.5  bc-9b-5e-b8-81  desktop-john    Dell Inc.      │
│  192.168.44.6  80-7c-62-c9-90  laptop-mary     HP Inc.        │
│  ...           ...              ...             ...            │
│  192.168.44.96 d8-bb-c1-56-93  YOUR-COMPUTER   Intel Corp     │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯


╭──────────── Network: 192.168.137.0/24 (3 devices) ─────────────╮
│                                                                 │
│  IP Address      MAC Address      Hostname        Vendor       │
│ ──────────────────────────────────────────────────────────     │
│  192.168.137.1   d8-bb-c1-56-93  hotspot-host    Intel Corp   │
│  192.168.137.50  a4-c3-f0-5e-2a  android-phone   Samsung       │
│  192.168.137.51  b8-27-eb-a1-3c  raspberry-pi    Raspberry Pi  │
│                                                                 │
╰─────────────────────────────────────────────────────────────────╯


Total devices found: 76
Networks scanned: 2
```

**What This Shows:**
- ✅ Scans ALL possible networks automatically
- ✅ Groups results by network
- ✅ Shows devices on hotspot networks (192.168.137.0/24)
- ✅ Shows devices on main network (192.168.44.0/24)
- ✅ Identifies unreachable networks
- ✅ Total device count across all networks

**Time:** ~1-3 minutes (scans multiple networks)

**Perfect For:**
- Finding devices connected to desktop hotspots
- Complete network inventory across all subnets
- Discovering hidden devices

---

## Export Examples

### CSV Export:
```
D:\network_scanner>py scanner.py scan 192.168.44.0/24 --export-csv network_inventory.csv

[... scanning output ...]

✓ Results exported to network_inventory.csv
```

**CSV File Content (network_inventory.csv):**
```csv
IP,MAC,Hostname,Vendor,Open Ports
192.168.44.1,bc-cf-4f-b8-99-3b,router.local,TP-Link,"80,443,8080,22"
192.168.44.5,bc-9b-5e-b8-44-81,desktop-john,Dell Inc.,"445,3389"
192.168.44.6,80-7c-62-c9-bf-90,laptop-mary,HP Inc.,""
192.168.44.10,cc-8e-71-fa-8d-4c,iphone-12,Apple Inc.,""
```

**Open in Excel for:**
- Sorting by vendor
- Filtering devices with open ports
- Creating reports
- Network documentation

### JSON Export:
```
D:\network_scanner>py scanner.py scan 192.168.44.0/24 --export-json network_data.json

[... scanning output ...]

✓ Results exported to network_data.json
```

**JSON File Content (network_data.json):**
```json
{
  "scan_time": "2025-11-20T14:30:00.123456",
  "network": "192.168.44.0/24",
  "devices": [
    {
      "ip": "192.168.44.1",
      "mac": "bc-cf-4f-b8-99-3b",
      "hostname": "router.local",
      "vendor": "TP-Link",
      "device_type": null,
      "open_ports": [80, 443, 8080, 22],
      "scan_time": "2025-11-20T14:30:15.789012"
    },
    {
      "ip": "192.168.44.5",
      "mac": "bc-9b-5e-b8-44-81",
      "hostname": "desktop-john",
      "vendor": "Dell Inc.",
      "device_type": null,
      "open_ports": [445, 3389],
      "scan_time": "2025-11-20T14:30:18.234567"
    }
  ]
}
```

**Use JSON for:**
- Automation scripts
- Integration with other tools
- Parsing with Python/PowerShell
- Database imports
- API consumption

---

## Quick Command Reference

| Command | Purpose | Time | Export |
|---------|---------|------|--------|
| `scanner.py discover <network>` | Quick device discovery | 5-10s | ❌ No |
| `scanner.py scan <network>` | Full scan + ports | 2-5min | ✅ Yes |
| `multi_network_scanner.py detect-networks` | Show available networks | <1s | ❌ No |
| `multi_network_scanner.py scan-all` | Scan all networks | 1-3min | ✅ Yes |

---

## Color Guide

When you see the scanner output:
- 🔵 **Cyan** = Information, progress messages
- 🟢 **Green** = Success, devices found, checkmarks ✓
- 🟡 **Yellow** = Warnings, devices with no open ports ○
- 🔴 **Red** = Errors, permission issues
- 🟣 **Magenta** = MAC addresses
- **White** = Standard output

---

## Next Steps

After running scans:
1. Review the device list
2. Export to CSV/JSON for documentation
3. Identify unknown devices
4. Check for unauthorized open ports
5. Schedule regular scans to monitor changes
