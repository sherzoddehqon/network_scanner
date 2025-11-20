# Troubleshooting Guide - Network Scanner

Comprehensive troubleshooting for common issues and errors.

---

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Scanning Issues](#scanning-issues)
- [Performance Issues](#performance-issues)
- [Network Issues](#network-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Advanced Troubleshooting](#advanced-troubleshooting)

---

## Quick Diagnostics

### Run Diagnostic Script

Create `diagnose.py`:

```python
#!/usr/bin/env python3
import sys
import subprocess
import platform

print("=" * 60)
print("NETWORK SCANNER DIAGNOSTIC TOOL")
print("=" * 60)

# System info
print(f"\n📋 System Information:")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Python: {sys.version}")
print(f"Architecture: {platform.machine()}")

# Check Python version
print(f"\n🐍 Python Check:")
if sys.version_info >= (3, 8):
    print("✅ Python version OK (3.8+)")
else:
    print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} - Need 3.8+")

# Check packages
print(f"\n📦 Package Check:")
packages = [
    'scapy', 'nmap', 'netaddr', 'mac_vendor_lookup',
    'click', 'rich', 'aiohttp', 'asyncio'
]

for pkg in packages:
    try:
        __import__(pkg)
        print(f"✅ {pkg}")
    except ImportError:
        print(f"❌ {pkg} - NOT INSTALLED")

# Check network interfaces
print(f"\n🌐 Network Interfaces:")
if platform.system() == 'Windows':
    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
else:
    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
print(result.stdout[:500])  # First 500 chars

# Check permissions
print(f"\n🔒 Permission Check:")
import os
if os.geteuid() == 0 if hasattr(os, 'geteuid') else True:
    print("✅ Running with elevated privileges")
else:
    print("⚠️  Not running as root/admin (ARP scanning may fail)")

print("\n" + "=" * 60)
print("Diagnostic complete!")
```

Run:
```bash
python diagnose.py
```

---

## Installation Issues

### Issue: "pip" not recognized

**Symptoms:**
```
'pip' is not recognized as an internal or external command
```

**Solutions:**

**Solution 1: Use Python Module**
```bash
python -m pip install -r requirements.txt
```

**Solution 2: Check Python Installation**
```bash
# Windows
where python
where pip

# Linux/Mac
which python3
which pip3
```

**Solution 3: Reinstall pip**
```bash
python -m ensurepip --upgrade
```

---

### Issue: Scapy installation fails

**Symptoms:**
```
ERROR: Failed building wheel for scapy
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solutions:**

**Windows:**
1. Install Visual Studio Build Tools:
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++"
   - Restart computer
   - Retry: `pip install scapy`

2. Or use pre-built wheel:
   ```cmd
   pip install scapy --prefer-binary
   ```

**Linux:**
```bash
# Install development tools
sudo apt install build-essential python3-dev libpcap-dev
pip install scapy
```

---

### Issue: "No module named 'scapy'"

**Symptoms:**
- Pip shows scapy is installed
- Python can't import it

**Cause:** Multiple Python installations

**Solution:**

**1. Check Python/Pip Paths:**
```bash
# Windows
where python
where pip

# Linux/Mac
which python3
which pip3
```

**2. Install to Correct Python:**
```bash
# Use explicit path
/usr/bin/python3 -m pip install scapy

# Or
C:\Python313\python.exe -m pip install scapy
```

**3. Use Virtual Environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

### Issue: Npcap installation problems (Windows)

**Symptoms:**
- Scapy installed but "Network is unreachable"
- "Failed to execute arp request"

**Solutions:**

**1. Verify Npcap Installation:**
```cmd
# Check if files exist
dir C:\Windows\System32\Npcap\wpcap.dll
dir C:\Windows\System32\Npcap\Packet.dll
```

**2. Reinstall Npcap:**
- Uninstall current Npcap (Control Panel)
- Reboot
- Download fresh: https://npcap.com/#download
- Install with "WinPcap API-compatible Mode" ✅
- Reboot again

**3. Check Npcap Service:**
```cmd
# Open Services (services.msc)
# Find "Npcap Loopback Adapter"
# Right-click > Start (if stopped)
```

**4. Run Test:**
```python
from scapy.all import *
conf.iface  # Should show network interface
```

---

## Scanning Issues

### Issue: No devices found

**Symptoms:**
```
Discovering hosts on 192.168.44.0/24...
Starting ARP scan on 192.168.44.0/24...
✓ Discovered 0 devices
```

**Diagnosis Checklist:**

1. **Wrong Network Range?**
   ```bash
   # Check your IP
   ipconfig  # Windows
   ifconfig  # Linux/Mac
   
   # If your IP is 192.168.44.96
   # Scan: 192.168.44.0/24
   # NOT: 192.168.1.0/24
   ```

2. **Not Running as Administrator?**
   ```bash
   # Windows: Right-click CMD > "Run as administrator"
   # Linux/Mac: sudo python3 scanner.py
   ```

3. **Firewall Blocking?**
   ```bash
   # Windows - Temporary disable
   netsh advfirewall set allprofiles state off
   # Test scan
   python scanner.py discover 192.168.44.0/24
   # Re-enable
   netsh advfirewall set allprofiles state on
   ```

4. **Other Devices Actually Exist?**
   ```bash
   # Check Windows ARP cache
   arp -a
   
   # Ping router
   ping 192.168.44.1
   ```

5. **Network Isolation?**
   - Some networks have AP isolation (prevents device-to-device communication)
   - Common on public Wi-Fi, guest networks
   - Solution: Connect to main network, not guest

---

### Issue: Permission denied

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied
ERROR: ARP scanning requires administrator privileges
```

**Solutions:**

**Windows:**
```cmd
# Method 1: Run as Administrator
# Right-click Command Prompt
# Select "Run as administrator"

# Method 2: Run specific command
runas /user:Administrator "python scanner.py discover 192.168.44.0/24"
```

**Linux/Mac:**
```bash
# Method 1: Use sudo
sudo python3 scanner.py discover 192.168.44.0/24

# Method 2: Give Python capabilities (permanent)
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Method 3: Add user to group
sudo usermod -a -G wireshark $USER
# Logout and login again
```

---

### Issue: Scan timeout or hangs

**Symptoms:**
- Scan starts but never completes
- Stuck on "Scanning X.X.X.X..."
- Takes extremely long

**Solutions:**

**1. Reduce Timeout:**
```bash
python scanner.py scan 192.168.44.0/24 --timeout 1.0
```

**2. Reduce Port Range:**
```bash
# Instead of 1-1000
python scanner.py scan 192.168.44.0/24 --ports 1-100
```

**3. Reduce Concurrent Connections:**
```bash
python scanner.py scan 192.168.44.0/24 --max-concurrent 50
```

**4. Use Discover Instead:**
```bash
# Skip port scanning
python scanner.py discover 192.168.44.0/24
```

**5. Check Network Connectivity:**
```bash
# Ping a known device
ping 192.168.44.1

# Check if network is congested
```

---

### Issue: Partial results

**Symptoms:**
- Some devices found, but not all
- Inconsistent results between scans

**Causes & Solutions:**

**1. Devices Are Off/Sleeping:**
- Mobile devices often sleep
- Solution: Run scan when devices are active

**2. Network Timing:**
```bash
# Increase timeout
python scanner.py scan 192.168.44.0/24 --timeout 3.0
```

**3. Network Load:**
- Other traffic interfering
- Solution: Run scan during low-traffic times

**4. ARP Cache Issues:**
```bash
# Clear ARP cache first
# Windows
arp -d *
netsh interface ip delete arpcache

# Linux
sudo ip -s -s neigh flush all

# Then scan
python scanner.py discover 192.168.44.0/24
```

---

### Issue: Can't find hotspot devices

**Symptoms:**
- Main network devices found
- Devices on Wi-Fi hotspots not visible

**Explanation:**
Desktop hotspots create separate networks with NAT. You can't see through NAT from outside.

**Solutions:**

**1. Use Multi-Network Scanner:**
```bash
python multi_network_scanner.py scan-all
```

**2. Scan from Hotspot Computer:**
- Log into the computer running the hotspot
- Run scanner on that machine:
  ```bash
  python scanner.py scan 192.168.137.0/24
  ```

**3. Check Hotspot IP Range:**
```bash
# Windows hotspot usually uses:
python scanner.py discover 192.168.137.0/24

# iPhone hotspot:
python scanner.py discover 172.20.10.0/24
```

---

## Performance Issues

### Issue: Scan is too slow

**Problem:** Scanning 73 devices takes 10+ minutes

**Solutions:**

**1. Limit Port Range:**
```bash
# Scan only common ports
python scanner.py scan 192.168.44.0/24 --ports 22,80,443,3389,8080

# Or small range
python scanner.py scan 192.168.44.0/24 --ports 1-100
```

**2. Increase Concurrency:**
```bash
# More simultaneous connections
python scanner.py scan 192.168.44.0/24 --max-concurrent 200
```

**3. Reduce Timeout:**
```bash
# Faster but might miss slow devices
python scanner.py scan 192.168.44.0/24 --timeout 1.0
```

**4. Use Fast Mode:**
```bash
python scanner.py scan 192.168.44.0/24 --scan-type fast
```

**5. Split the Scan:**
```bash
# Scan in chunks
python scanner.py scan 192.168.44.0/26  # First 64 IPs
python scanner.py scan 192.168.44.64/26  # Next 64 IPs
```

**Benchmark:**
- Discovery only: 5-10 seconds
- Scan 100 ports: 30-60 seconds
- Scan 1000 ports: 2-5 minutes
- Scan 65535 ports: 30-60 minutes

---

### Issue: High CPU/Memory usage

**Problem:** Python using 100% CPU or lots of RAM

**Solutions:**

**1. Reduce Concurrent Connections:**
```bash
python scanner.py scan 192.168.44.0/24 --max-concurrent 50
```

**2. Process in Batches:**
```python
# Modify scanner to process fewer devices at once
```

**3. Close Other Programs:**
- Free up system resources

**4. Check for Loops:**
```bash
# If stuck at 100% CPU, might be infinite loop
# Kill with Ctrl+C
```

---

## Network Issues

### Issue: "Network is unreachable"

**Symptoms:**
```
OSError: [Errno 101] Network is unreachable
```

**Solutions:**

**1. Verify Network Connection:**
```bash
# Ping gateway
ping 192.168.44.1

# Check network interfaces
ipconfig  # Windows
ip addr   # Linux
```

**2. Check Network Cable/Wi-Fi:**
- Ensure connected to network
- Check Wi-Fi status

**3. Verify IP Range:**
```bash
# Don't scan networks you're not on
# If your IP is 192.168.44.96
# DON'T scan: 10.0.0.0/24
# DO scan: 192.168.44.0/24
```

---

### Issue: Firewall blocking

**Symptoms:**
- Scan fails with no results
- Connection refused errors
- Timeout errors

**Solutions:**

**1. Check Windows Firewall:**
```cmd
# Check status
netsh advfirewall show allprofiles

# Temporarily disable (as admin)
netsh advfirewall set allprofiles state off
# Test scan
# Re-enable
netsh advfirewall set allprofiles state on
```

**2. Add Firewall Exception:**
```cmd
# Allow Python through firewall
netsh advfirewall firewall add rule name="Python Scanner" dir=in action=allow program="C:\Python313\python.exe"
```

**3. Check Antivirus:**
- Some antivirus blocks network scanning
- Add scanner to exceptions

**4. Check Router Firewall:**
- Router might block ARP or ICMP
- Check router settings

---

### Issue: VPN interference

**Problem:** Scanner doesn't work with VPN connected

**Solutions:**

**1. Scan Before VPN Connection:**
- Disconnect VPN
- Run scan
- Reconnect VPN

**2. Bind to Specific Interface:**
```python
# Modify scanner to use specific interface
conf.iface = "Ethernet"  # or "Wi-Fi"
```

**3. Split-Tunnel VPN:**
- Configure VPN to not route local traffic
- Allows local network access while VPN active

---

## Platform-Specific Issues

### Windows-Specific

#### Issue: WinPcap vs Npcap confusion

**Problem:** Installed WinPcap instead of Npcap

**Solution:**
1. Uninstall WinPcap
2. Install Npcap with compatibility mode
3. Npcap is the modern replacement for WinPcap

#### Issue: Windows Defender blocking

**Symptoms:** Scanner runs but finds nothing

**Solution:**
```cmd
# Add folder to exclusions
# Settings > Update & Security > Windows Security
# Virus & threat protection > Exclusions
# Add folder: C:\NetworkScanner\
```

#### Issue: PowerShell execution policy

**Problem:** Can't run scripts

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Linux-Specific

#### Issue: "Operation not permitted"

**Problem:** Even with sudo, can't scan

**Solution:**
```bash
# Give Python raw socket capabilities
sudo setcap cap_net_raw,cap_net_admin=eip $(which python3)

# Or check if AppArmor/SELinux blocking
sudo aa-status  # AppArmor
sestatus        # SELinux
```

#### Issue: Python 2 vs Python 3

**Problem:** System has both Python 2 and 3

**Solution:**
```bash
# Always use python3 explicitly
python3 scanner.py discover 192.168.44.0/24

# Or create alias
alias python=python3
```

---

### macOS-Specific

#### Issue: SIP (System Integrity Protection) blocking

**Problem:** Can't access network interfaces

**Solution:**
```bash
# Run with sudo
sudo python3 scanner.py discover 192.168.44.0/24

# Or disable SIP (not recommended)
# Reboot to Recovery Mode
# csrutil disable
```

#### Issue: Gatekeeper blocking Python

**Problem:** "Python can't be opened"

**Solution:**
```bash
# Allow Python
# System Preferences > Security & Privacy
# Click "Allow" next to Python

# Or from terminal
xattr -d com.apple.quarantine /path/to/python
```

---

## Advanced Troubleshooting

### Enable Debug Mode

**Add debug output to scanner:**

```python
import logging

# Add at top of scanner.py
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add debug statements
logger.debug(f"Scanning {network}")
logger.debug(f"Found device: {device.ip}")
```

---

### Network Packet Capture

**Verify packets are being sent:**

```bash
# Windows
# Download Wireshark
# Start capture on network interface
# Run scanner
# Filter by "arp"

# Linux
sudo tcpdump -i eth0 arp
# In another terminal
sudo python3 scanner.py discover 192.168.44.0/24
```

---

### Test Individual Components

**Test ARP:**
```python
from scapy.all import *

# Test ARP request
arp = ARP(pdst="192.168.44.1")
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
packet = ether/arp

result = srp(packet, timeout=2, verbose=1)
print(result)
```

**Test Port Scan:**
```python
import socket

def test_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0

print(test_port("192.168.44.1", 80))
```

---

### Check Logs

**Windows Event Viewer:**
- Windows Logs > Application
- Look for Python errors

**Linux System Logs:**
```bash
sudo tail -f /var/log/syslog | grep python
```

**Python Traceback:**
```bash
python scanner.py discover 192.168.44.0/24 2>&1 | tee error.log
```

---

### Clean Reinstall

If all else fails:

**1. Uninstall Everything:**
```bash
pip uninstall scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp -y
```

**2. Clear Pip Cache:**
```bash
pip cache purge
```

**3. Reinstall:**
```bash
pip install --no-cache-dir -r requirements.txt
```

**4. Reboot Computer**

**5. Test:**
```bash
python scanner.py --help
```

---

## Getting Additional Help

### Information to Collect

When asking for help, provide:

1. **System Information:**
   ```bash
   python --version
   pip --version
   # Windows
   ver
   # Linux
   uname -a
   ```

2. **Package Versions:**
   ```bash
   pip list
   ```

3. **Full Error Message:**
   ```bash
   python scanner.py discover 192.168.44.0/24 2>&1 | tee error.log
   ```

4. **Network Configuration:**
   ```bash
   ipconfig  # Windows
   ip addr   # Linux
   ```

5. **Steps to Reproduce:**
   - What command did you run?
   - What did you expect?
   - What happened instead?

### Resources

- **Documentation:** README.md, INSTALLATION.md
- **Examples:** COMMAND_EXAMPLES.md
- **GitHub Issues:** Report bugs and feature requests
- **Stack Overflow:** Search for similar issues
- **Scapy Documentation:** https://scapy.readthedocs.io/

---

## Still Stuck?

If none of these solutions work:

1. Run diagnostic script: `python diagnose.py`
2. Check all error messages carefully
3. Search error online (often someone had same issue)
4. Try alternative scan methods
5. Ask for help with detailed information
6. Consider using alternative tools temporarily

---

**Remember:** Most issues are due to:
- Not running as administrator/root
- Wrong network range
- Npcap not installed (Windows)
- Firewall blocking
- Multiple Python installations

Check these first! ✅

---

Return to [README.md](README.md) for usage instructions.
