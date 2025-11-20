# Network Scanner - Quick Reference Card

One-page cheat sheet for common tasks and commands.

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Find your network
ipconfig  # Windows
ifconfig  # Linux/Mac

# 2. Open as Administrator/Root
# Windows: Right-click CMD > "Run as administrator"
# Linux/Mac: sudo -i

# 3. Run scan
python scanner.py discover 192.168.44.0/24
```

---

## 📖 Common Commands

### Basic Discovery

```bash
# Quick device discovery (fastest)
python scanner.py discover 192.168.44.0/24

# Full scan with ports (slower but complete)
python scanner.py scan 192.168.44.0/24

# Scan with CSV export
python scanner.py scan 192.168.44.0/24 --export-csv report.csv
```

### Port Scanning

```bash
# Common ports only (fast)
python scanner.py scan 192.168.44.0/24 --ports 22,80,443,3389

# Port range
python scanner.py scan 192.168.44.0/24 --ports 1-100

# All ports (very slow!)
python scanner.py scan 192.168.44.0/24 --ports 1-65535
```

### Multi-Network Scanning

```bash
# Detect available networks
python multi_network_scanner.py detect-networks

# Scan all networks (including hotspots)
python multi_network_scanner.py scan-all

# Scan all with export
python multi_network_scanner.py scan-all --export-csv all.csv
```

---

## 🎯 Common Use Cases

| Task | Command |
|------|---------|
| **Network Inventory** | `python scanner.py scan 192.168.44.0/24 --export-csv inventory.csv` |
| **Security Audit** | `python scanner.py scan 192.168.44.0/24 --ports 21,22,23,445,3389` |
| **Find Web Servers** | `python scanner.py scan 192.168.44.0/24 --ports 80,443,8080` |
| **Find Printers** | `python scanner.py scan 192.168.44.0/24 --ports 9100,515,631` |
| **Find Hotspot Devices** | `python multi_network_scanner.py scan-all` |
| **Quick Check** | `python scanner.py discover 192.168.44.0/24` |

---

## 🔧 Command Options

### scanner.py scan

| Option | Default | Description |
|--------|---------|-------------|
| `--ports` | 1-1000 | Port range (e.g., 22,80 or 1-100) |
| `--timeout` | 2.0 | Connection timeout in seconds |
| `--max-concurrent` | 100 | Simultaneous connections |
| `--export-csv` | None | Export to CSV file |
| `--export-json` | None | Export to JSON file |
| `--scan-type` | fast | Scan type (fast/full) |

**Examples:**
```bash
python scanner.py scan 192.168.44.0/24 --ports 1-500 --timeout 1.5 --max-concurrent 150
python scanner.py scan 192.168.44.0/24 --export-csv report.csv --export-json report.json
```

---

## 🌐 Network Ranges

| Your IP | Network to Scan | Covers |
|---------|----------------|---------|
| 192.168.1.100 | 192.168.1.0/24 | 192.168.1.1 - 192.168.1.254 |
| 192.168.44.96 | 192.168.44.0/24 | 192.168.44.1 - 192.168.44.254 |
| 10.0.0.50 | 10.0.0.0/24 | 10.0.0.1 - 10.0.0.254 |
| 172.16.1.20 | 172.16.1.0/24 | 172.16.1.1 - 172.16.1.254 |

**Rule:** If your IP is X.X.X.Y, scan X.X.X.0/24

---

## 🔌 Common Ports

| Port | Service | Used By |
|------|---------|---------|
| 21 | FTP | File Transfer |
| 22 | SSH | Remote Access (Linux) |
| 23 | Telnet | Insecure Remote (Legacy) |
| 25 | SMTP | Email |
| 80 | HTTP | Web Server |
| 443 | HTTPS | Secure Web |
| 445 | SMB | Windows File Sharing |
| 3306 | MySQL | Database |
| 3389 | RDP | Remote Desktop (Windows) |
| 8080 | HTTP Alt | Web Server Alternative |
| 9100 | Print | Network Printer |

---

## 🔍 Output Interpretation

```
╭──────────────────────── Network Scan Results ────────────────────────╮
│  IP Address      MAC Address        Hostname        Vendor    Ports  │
│ ──────────────────────────────────────────────────────────────────── │
│  192.168.44.1    bc-cf-4f-b8-99-3b  router          TP-Link   80,443 │
│  192.168.44.5    bc-9b-5e-b8-44-81  desktop-john    Dell      445    │
│  192.168.44.10   cc-8e-71-fa-8d-4c  iphone-12       Apple     None   │
╰───────────────────────────────────────────────────────────────────────╯
```

**What You See:**
- **IP Address**: Device network address
- **MAC Address**: Hardware identifier
- **Hostname**: Device name (if available)
- **Vendor**: Manufacturer from MAC
- **Ports**: Open ports found

---

## ⚡ Performance Tips

### Speed Up Scans

```bash
# Reduce port range
--ports 1-100                    # Instead of 1-1000

# Scan specific ports only
--ports 22,80,443,3389          # Only these 4 ports

# Increase concurrency
--max-concurrent 200            # More simultaneous connections

# Reduce timeout
--timeout 1.0                   # Faster, might miss slow devices

# Use discover for quick check
python scanner.py discover ...  # No port scanning
```

### Typical Scan Times

- **Discovery only**: 5-10 seconds
- **Scan 100 ports**: 30-60 seconds
- **Scan 1000 ports**: 2-5 minutes
- **Scan 65535 ports**: 30-60 minutes

---

## 🚨 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **No devices found** | Wrong network? Check with `ipconfig` or `arp -a` |
| **Permission denied** | Run as Administrator (Windows) or `sudo` (Linux) |
| **Scapy errors** | Windows: Install Npcap from https://npcap.com |
| **Module not found** | `pip install -r requirements.txt` |
| **Scan too slow** | Use `--ports 1-100` or `--max-concurrent 200` |
| **Firewall blocking** | Temporarily disable firewall, test, re-enable |

---

## 📊 Export Formats

### CSV (Excel)
```bash
python scanner.py scan 192.168.44.0/24 --export-csv network.csv
# Open in Excel for analysis
```

### JSON (Automation)
```bash
python scanner.py scan 192.168.44.0/24 --export-json network.json
# Use in scripts or APIs
```

---

## 🔐 Security Best Practices

✅ **Do:**
- Only scan networks you own/administer
- Get permission before scanning work networks
- Run scans during low-traffic times
- Document findings for security reviews

❌ **Don't:**
- Scan networks without authorization
- Use for malicious purposes
- Scan production systems during business hours
- Share results publicly with sensitive info

---

## 📋 Pre-Scan Checklist

Before running a scan:

- [ ] Running as Administrator/root?
- [ ] Correct network range? (Check with `ipconfig`/`ifconfig`)
- [ ] Npcap installed? (Windows only)
- [ ] Firewall allows scanning?
- [ ] Authorization to scan this network?

---

## 🆘 Getting Help

**Error Messages:**
```bash
# Save error to file
python scanner.py scan ... 2>&1 | tee error.log
```

**Check Installation:**
```bash
python --version          # Should be 3.8+
pip list | grep scapy    # Should show version
python scanner.py --help # Should show help
```

**Documentation:**
- README.md - Complete guide
- INSTALLATION.md - Setup instructions
- TROUBLESHOOTING.md - Detailed problem solving
- COMMAND_EXAMPLES.md - Output examples

---

## 💡 Pro Tips

1. **Save Baseline**: Run initial scan and save as baseline
   ```bash
   python scanner.py scan 192.168.44.0/24 --export-json baseline.json
   ```

2. **Schedule Regular Scans**: Use Task Scheduler (Windows) or cron (Linux)

3. **Export for Reports**: CSV works great for management reports

4. **Monitor Changes**: Compare scans over time to find new/removed devices

5. **Custom Shortcuts**: Create batch files or aliases for common scans
   ```bash
   # Windows batch file: quick_scan.bat
   @echo off
   python C:\scanner\scanner.py scan 192.168.44.0/24 --export-csv daily.csv
   ```

6. **Multiple Networks**: Use multi_network_scanner.py to find all devices

---

## 📱 Common Network Ranges

| Network Type | Common Range |
|--------------|--------------|
| Home Router | 192.168.1.0/24 or 192.168.0.0/24 |
| Corporate | 10.0.0.0/8 or 172.16.0.0/12 |
| Windows Hotspot | 192.168.137.0/24 |
| iPhone Hotspot | 172.20.10.0/24 |

---

## 🎓 Understanding CIDR

| CIDR | Range | # of IPs |
|------|-------|----------|
| /24 | X.X.X.0 - X.X.X.255 | 256 |
| /25 | X.X.X.0 - X.X.X.127 | 128 |
| /26 | X.X.X.0 - X.X.X.63 | 64 |
| /28 | X.X.X.0 - X.X.X.15 | 16 |

**Most common:** /24 (covers 256 IPs, usually one subnet)

---

## 🔄 Workflow Example

**Complete Network Audit Workflow:**

```bash
# 1. Detect networks
python multi_network_scanner.py detect-networks

# 2. Quick discovery
python scanner.py discover 192.168.44.0/24

# 3. Full scan with export
python scanner.py scan 192.168.44.0/24 --export-csv audit.csv

# 4. Security scan
python scanner.py scan 192.168.44.0/24 --ports 21,22,23,445,3389 --export-csv security.csv

# 5. Open in Excel for analysis
start audit.csv
```

---

**Print this page for quick reference!** 📄

For complete documentation, see [README.md](README.md)
