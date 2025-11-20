# Installation Guide - Network Scanner

Complete installation instructions for Windows, Linux, and macOS.

---

## Table of Contents

- [Windows Installation](#windows-installation)
- [Linux Installation](#linux-installation)
- [macOS Installation](#macos-installation)
- [Verification](#verification)
- [Troubleshooting Installation](#troubleshooting-installation)

---

## Windows Installation

### Prerequisites

- Windows 10 or Windows 11
- Administrator access
- Internet connection

### Step 1: Install Python

1. **Download Python**
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version)
   - Save the installer

2. **Run Python Installer**
   - Double-click the downloaded file
   - ✅ **CRITICAL**: Check "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Python Installation**
   ```cmd
   # Open Command Prompt (Win+R, type "cmd", Enter)
   python --version
   ```
   
   Expected output: `Python 3.x.x`
   
   If you see "python is not recognized":
   - You forgot to check "Add Python to PATH"
   - Reinstall Python and check the box
   - Or manually add Python to PATH (see Troubleshooting)

### Step 2: Download Network Scanner

**Option A: Download from GitHub**
```cmd
cd C:\
mkdir NetworkScanner
cd NetworkScanner
# Download scanner.py and multi_network_scanner.py
# Download requirements.txt
```

**Option B: Download ZIP**
- Download all files
- Extract to `C:\NetworkScanner\`

### Step 3: Install Python Packages

1. **Open Command Prompt**
   - Press Windows key
   - Type "cmd"
   - Press Enter

2. **Navigate to Scanner Folder**
   ```cmd
   cd C:\NetworkScanner
   ```

3. **Install Packages**
   ```cmd
   python -m pip install -r requirements.txt
   ```
   
   Or install manually:
   ```cmd
   python -m pip install scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp
   ```

4. **Wait for Installation**
   - This may take 2-5 minutes
   - You'll see "Successfully installed..." messages

### Step 4: Install Npcap (REQUIRED for Windows)

**⚠️ CRITICAL - Without Npcap, ARP scanning won't work on Windows**

1. **Download Npcap**
   - Go to https://npcap.com/#download
   - Click "Download Npcap Installer"
   - Save the file

2. **Run Npcap Installer**
   - Right-click the installer
   - Select "Run as administrator"
   - Click "I Agree" on license
   - ✅ **IMPORTANT**: Check "Install Npcap in WinPcap API-compatible Mode"
   - Leave other options as default
   - Click "Install"
   - Wait for installation
   - Click "Finish"

3. **Restart Computer** (if prompted)

### Step 5: Test Installation

1. **Open Command Prompt as Administrator**
   - Press Windows key
   - Type "cmd"
   - Right-click "Command Prompt"
   - Select "Run as administrator"

2. **Navigate to Scanner**
   ```cmd
   cd C:\NetworkScanner
   ```

3. **Test Scanner**
   ```cmd
   python scanner.py --help
   ```
   
   You should see the help menu.

4. **Test Imports**
   ```cmd
   python -c "import scapy; print('Scapy OK')"
   python -c "import nmap; print('Nmap OK')"
   python -c "import click; print('Click OK')"
   python -c "from rich.console import Console; print('Rich OK')"
   ```
   
   All should print "OK" without errors.

5. **Run First Scan**
   ```cmd
   # Replace with your network
   python scanner.py discover 192.168.1.0/24
   ```

### Windows Installation Complete! ✅

---

## Linux Installation

### Debian/Ubuntu

**Step 1: Update System**
```bash
sudo apt update
sudo apt upgrade -y
```

**Step 2: Install Python and Dependencies**
```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies for Scapy
sudo apt install tcpdump libpcap-dev -y

# Verify Python
python3 --version
```

**Step 3: Download Scanner**
```bash
cd ~
mkdir network_scanner
cd network_scanner

# Download files (or use git clone)
wget https://your-repo/scanner.py
wget https://your-repo/multi_network_scanner.py
wget https://your-repo/requirements.txt
```

**Step 4: Create Virtual Environment (Recommended)**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**Step 5: Install Python Packages**
```bash
# Install packages
pip install -r requirements.txt

# Or manually
pip install scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp
```

**Step 6: Test Installation**
```bash
# Test as root (required for ARP)
sudo python3 scanner.py --help

# Run first scan
sudo python3 scanner.py discover 192.168.1.0/24
```

### Fedora/RHEL/CentOS

**Step 1: Install Python**
```bash
sudo dnf install python3 python3-pip -y
sudo dnf install tcpdump libpcap-devel -y
```

**Step 2-6: Same as Debian/Ubuntu above**

### Arch Linux

**Step 1: Install Python**
```bash
sudo pacman -S python python-pip tcpdump libpcap
```

**Step 2-6: Same as Debian/Ubuntu above**

---

## macOS Installation

### Prerequisites

- macOS 10.15 (Catalina) or newer
- Administrator access
- Homebrew (recommended)

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
brew install python3
```

**Option B: Download from python.org**
- Go to https://www.python.org/downloads/macos/
- Download macOS installer
- Run installer
- Follow prompts

### Step 3: Install libpcap

```bash
brew install libpcap
```

### Step 4: Download Scanner

```bash
cd ~
mkdir network_scanner
cd network_scanner

# Download files
curl -O https://your-repo/scanner.py
curl -O https://your-repo/multi_network_scanner.py
curl -O https://your-repo/requirements.txt
```

### Step 5: Install Python Packages

```bash
# Install packages
pip3 install -r requirements.txt

# Or manually
pip3 install scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp
```

### Step 6: Test Installation

```bash
# Test as root
sudo python3 scanner.py --help

# Run first scan
sudo python3 scanner.py discover 192.168.1.0/24
```

### macOS-Specific Notes

1. **Security & Privacy**: You may need to allow Terminal in System Preferences > Security & Privacy > Full Disk Access

2. **Firewall**: If macOS Firewall is enabled, you might need to allow Python

3. **Network Permissions**: Some macOS versions require additional permissions for network scanning

---

## Verification

### Test All Components

Create a file `test_installation.py`:

```python
#!/usr/bin/env python3
"""Test Network Scanner Installation"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name} - FAILED: {e}")
        return False

def main():
    print("Testing Network Scanner Installation\n")
    print("=" * 50)
    
    # Test Python version
    version = sys.version_info
    print(f"\nPython Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    else:
        print("✅ Python version OK")
    
    print("\n" + "=" * 50)
    print("Testing Required Packages:\n")
    
    # Test all required packages
    results = []
    results.append(test_import("scapy", "Scapy"))
    results.append(test_import("nmap", "python-nmap"))
    results.append(test_import("netaddr", "netaddr"))
    results.append(test_import("mac_vendor_lookup", "mac-vendor-lookup"))
    results.append(test_import("click", "Click"))
    results.append(test_import("rich", "Rich"))
    results.append(test_import("aiohttp", "aiohttp"))
    
    print("\n" + "=" * 50)
    
    # Summary
    if all(results):
        print("\n✅ All packages installed correctly!")
        print("\nYou can now run:")
        print("  python scanner.py --help")
        return True
    else:
        print("\n❌ Some packages are missing.")
        print("\nInstall missing packages:")
        print("  pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

Run the test:
```bash
python test_installation.py
```

### Expected Output

```
Testing Network Scanner Installation

==================================================

Python Version: 3.11.5
✅ Python version OK

==================================================
Testing Required Packages:

✅ Scapy - OK
✅ python-nmap - OK
✅ netaddr - OK
✅ mac-vendor-lookup - OK
✅ Click - OK
✅ Rich - OK
✅ aiohttp - OK

==================================================

✅ All packages installed correctly!

You can now run:
  python scanner.py --help
```

---

## Troubleshooting Installation

### Python Not Found

**Problem:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
```cmd
# Try these alternatives
python3 --version
py --version
py -3 --version

# Or add Python to PATH manually:
# 1. Search "Environment Variables" in Start Menu
# 2. Click "Environment Variables"
# 3. Under "System variables", select "Path"
# 4. Click "Edit"
# 5. Add: C:\Python313\ and C:\Python313\Scripts\
# 6. Click OK
# 7. Restart Command Prompt
```

**Linux/Mac:**
```bash
# Use python3 instead
python3 --version

# Or create alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

---

### Pip Not Found

**Problem:**
```
'pip' is not recognized
```

**Solution:**
```bash
# Windows
python -m pip --version
py -m pip --version

# Linux/Mac
python3 -m pip --version

# Install pip if missing
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

---

### Scapy Installation Fails

**Problem:**
```
ERROR: Failed building wheel for scapy
```

**Windows Solution:**
```cmd
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Install "Desktop development with C++"

# Then retry:
pip install scapy
```

**Linux Solution:**
```bash
# Install development tools
sudo apt install python3-dev libpcap-dev  # Debian/Ubuntu
sudo dnf install python3-devel libpcap-devel  # Fedora
sudo pacman -S python libpcap  # Arch

# Retry installation
pip install scapy
```

---

### Npcap Installation Issues (Windows)

**Problem:** Scapy can't find Npcap

**Solutions:**

1. **Verify Npcap is installed:**
   - Check: `C:\Windows\System32\Npcap\`
   - Should contain: `wpcap.dll` and `Packet.dll`

2. **Reinstall Npcap:**
   - Uninstall current Npcap
   - Reboot
   - Install again with "WinPcap API-compatible Mode" checked

3. **Check Npcap Service:**
   ```cmd
   # Open Services (services.msc)
   # Find "Npcap Loopback Adapter"
   # Ensure it's running
   ```

4. **Run as Administrator:**
   - Scapy needs admin rights
   - Always use "Run as administrator"

---

### Permission Denied Errors

**Problem:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**

**Windows:**
```cmd
# Run Command Prompt as Administrator
# Right-click CMD > "Run as administrator"
```

**Linux/Mac:**
```bash
# Use sudo
sudo python3 scanner.py discover 192.168.1.0/24

# Or give Python raw socket permissions
sudo setcap cap_net_raw=eip /usr/bin/python3
```

---

### Import Errors After Installation

**Problem:**
```python
ModuleNotFoundError: No module named 'scapy'
```

**But pip shows it's installed:**
```bash
pip list | grep scapy
# Shows: scapy 2.5.0
```

**Cause:** Multiple Python installations

**Solution:**

1. **Find which Python pip is using:**
   ```bash
   # Windows
   where python
   where pip
   
   # Linux/Mac
   which python3
   which pip3
   ```

2. **Install to specific Python:**
   ```bash
   # Use full path
   C:\Python313\python.exe -m pip install scapy
   
   # Or
   /usr/bin/python3 -m pip install scapy
   ```

3. **Use virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

---

### Virtual Environment Issues

**Problem:** Can't activate virtual environment

**Windows Solution:**
```cmd
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate:
venv\Scripts\activate
```

**Linux/Mac Solution:**
```bash
# Make activate script executable
chmod +x venv/bin/activate

# Then activate:
source venv/bin/activate
```

---

### Network Scanner Files Not Found

**Problem:**
```
python: can't open file 'scanner.py': [Errno 2] No such file or directory
```

**Solution:**
```bash
# Check current directory
# Windows
dir

# Linux/Mac
ls -la

# Navigate to correct folder
cd /path/to/network_scanner

# Verify scanner.py exists
# Windows
dir scanner.py

# Linux/Mac
ls -l scanner.py
```

---

## Post-Installation Setup

### Create Desktop Shortcuts (Windows)

1. Right-click Desktop > New > Shortcut
2. Location: `C:\Python313\python.exe C:\NetworkScanner\scanner.py scan 192.168.1.0/24`
3. Name: "Network Scanner"
4. Right-click shortcut > Properties
5. Click "Advanced" > Check "Run as administrator"

### Add to System PATH

**Windows:**
```cmd
# Add NetworkScanner to PATH
setx PATH "%PATH%;C:\NetworkScanner"
```

**Linux/Mac:**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export PATH="$PATH:$HOME/network_scanner"' >> ~/.bashrc
source ~/.bashrc

# Make scripts executable
chmod +x ~/network_scanner/scanner.py
chmod +x ~/network_scanner/multi_network_scanner.py

# Add shebang to scripts
# First line: #!/usr/bin/env python3
```

### Create Aliases

**Bash/Zsh:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias netscan='sudo python3 ~/network_scanner/scanner.py'
alias netmulti='sudo python3 ~/network_scanner/multi_network_scanner.py'

# Reload
source ~/.bashrc
```

**PowerShell:**
```powershell
# Add to PowerShell profile
notepad $PROFILE

# Add:
function netscan { python C:\NetworkScanner\scanner.py $args }
```

---

## Upgrade Instructions

### Upgrade Python Packages

```bash
# Upgrade all packages
pip install --upgrade -r requirements.txt

# Upgrade specific package
pip install --upgrade scapy

# Check versions
pip list | grep scapy
```

### Upgrade Python

**Windows:**
1. Download new Python installer
2. Run installer
3. Check "Upgrade Now"

**Linux:**
```bash
# Ubuntu
sudo apt update
sudo apt upgrade python3

# Fedora
sudo dnf upgrade python3
```

**Mac:**
```bash
brew upgrade python3
```

### Update Network Scanner

```bash
# Download new versions
# Replace old scanner.py and multi_network_scanner.py

# Or use git
git pull origin main
```

---

## Uninstallation

### Remove Python Packages

```bash
pip uninstall scapy python-nmap netaddr mac-vendor-lookup click rich aiohttp -y
```

### Remove Npcap (Windows)

1. Control Panel > Programs and Features
2. Find "Npcap"
3. Right-click > Uninstall

### Remove Python (if needed)

**Windows:**
1. Settings > Apps
2. Find "Python 3.x"
3. Click Uninstall

**Linux:**
```bash
sudo apt remove python3 python3-pip  # Don't do this unless necessary!
```

**Mac:**
```bash
brew uninstall python3
```

---

## Getting Help

If installation still fails:

1. Check Python version: `python --version` (must be 3.8+)
2. Check pip version: `pip --version`
3. Run test script: `python test_installation.py`
4. Check error logs
5. Search error messages online
6. Open GitHub issue with:
   - Operating system and version
   - Python version
   - Full error message
   - Steps you tried

---

**Installation Guide Complete!**

Return to [README.md](README.md) for usage instructions.
