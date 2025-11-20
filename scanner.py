#!/usr/bin/env python3
"""
Network Scanner - Professional network discovery tool
Discovers devices, scans ports, identifies services
"""

import asyncio
import socket
import ipaddress
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

# Third-party imports
try:
    from scapy.all import ARP, Ether, srp, conf
    conf.verb = 0  # Disable Scapy verbosity
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: Scapy not available. ARP scanning disabled.")

try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False
    print("Warning: python-nmap not available. Advanced scanning disabled.")

try:
    from netaddr import EUI
    NETADDR_AVAILABLE = True
except ImportError:
    NETADDR_AVAILABLE = False

try:
    from mac_vendor_lookup import MacLookup
    MAC_LOOKUP_AVAILABLE = True
except ImportError:
    MAC_LOOKUP_AVAILABLE = False

import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich import box

console = Console()


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class Port:
    """Represents a scanned port"""
    number: int
    state: str  # 'open', 'closed', 'filtered'
    service: Optional[str] = None
    version: Optional[str] = None


@dataclass
class Device:
    """Represents a discovered network device"""
    ip: str
    mac: Optional[str] = None
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    device_type: Optional[str] = None
    ports: List[Port] = field(default_factory=list)
    scan_time: datetime = field(default_factory=datetime.now)
    
    def get_open_ports(self) -> List[int]:
        """Return list of open port numbers"""
        return [p.number for p in self.ports if p.state == 'open']
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            'ip': self.ip,
            'mac': self.mac,
            'hostname': self.hostname,
            'vendor': self.vendor,
            'device_type': self.device_type,
            'open_ports': self.get_open_ports(),
            'scan_time': self.scan_time.isoformat()
        }


@dataclass
class ScanConfig:
    """Scan configuration"""
    network: str
    ports: str = "1-1000"
    timeout: float = 2.0
    max_concurrent: int = 100
    service_detection: bool = True
    scan_type: str = "fast"  # fast, full


# ============================================================================
# NETWORK SCANNING ENGINE
# ============================================================================

class NetworkScanner:
    """Core network scanning engine"""
    
    def __init__(self, config: ScanConfig):
        self.config = config
        self.devices: List[Device] = []
        self.mac_lookup = None
        
        if MAC_LOOKUP_AVAILABLE:
            try:
                self.mac_lookup = MacLookup()
                # Update vendor database
                self.mac_lookup.update_vendors()
            except:
                self.mac_lookup = None
    
    def discover_hosts_arp(self) -> List[Device]:
        """
        Discover hosts using ARP scanning (most reliable for local networks)
        Requires: Scapy library and appropriate permissions
        """
        if not SCAPY_AVAILABLE:
            console.print("[yellow]ARP scanning requires Scapy library[/yellow]")
            return []
        
        try:
            console.print(f"[cyan]Starting ARP scan on {self.config.network}...[/cyan]")
            
            # Create ARP request packet
            arp = ARP(pdst=self.config.network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            # Send packet and receive responses
            result = srp(packet, timeout=3, verbose=0)[0]
            
            devices = []
            for sent, received in result:
                device = Device(ip=received.psrc, mac=received.hwsrc)
                
                # Get MAC vendor
                if self.mac_lookup:
                    try:
                        device.vendor = self.mac_lookup.lookup(device.mac)
                    except:
                        device.vendor = "Unknown"
                elif NETADDR_AVAILABLE:
                    try:
                        mac = EUI(device.mac)
                        device.vendor = mac.oui.registration().org
                    except:
                        device.vendor = "Unknown"
                
                # Get hostname
                try:
                    device.hostname = socket.gethostbyaddr(device.ip)[0]
                except:
                    device.hostname = None
                
                devices.append(device)
            
            self.devices = devices
            console.print(f"[green]✓ Discovered {len(devices)} devices[/green]")
            return devices
            
        except PermissionError:
            console.print("[red]ERROR: ARP scanning requires administrator privileges[/red]")
            console.print("[yellow]Run Command Prompt as Administrator[/yellow]")
            return []
        except Exception as e:
            console.print(f"[red]ARP scan failed: {e}[/red]")
            return []
    
    async def scan_port(self, ip: str, port: int) -> Port:
        """Async port scanner"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=self.config.timeout
            )
            writer.close()
            await writer.wait_closed()
            
            # Try to get service name
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            
            return Port(number=port, state='open', service=service)
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return None
    
    async def scan_device_ports(self, device: Device):
        """Scan all ports for a device"""
        # Parse port range
        if '-' in self.config.ports:
            start, end = map(int, self.config.ports.split('-'))
            ports = range(start, end + 1)
        else:
            ports = [int(p) for p in self.config.ports.split(',')]
        
        console.print(f"[cyan]Scanning {device.ip}...[/cyan]")
        
        # Create tasks with concurrency limit
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        async def scan_with_semaphore(port):
            async with semaphore:
                return await self.scan_port(device.ip, port)
        
        tasks = [scan_with_semaphore(port) for port in ports]
        results = await asyncio.gather(*tasks)
        
        # Filter out None results (closed ports)
        device.ports = [r for r in results if r is not None]
        
        if device.ports:
            console.print(f"[green]✓ {device.ip}: Found {len(device.ports)} open ports[/green]")
        else:
            console.print(f"[yellow]○ {device.ip}: No open ports found[/yellow]")
    
    async def scan_all_devices(self):
        """Scan all discovered devices"""
        if not self.devices:
            console.print("[yellow]No devices to scan[/yellow]")
            return
        
        console.print(f"\n[cyan]Starting port scan on {len(self.devices)} devices...[/cyan]\n")
        
        tasks = [self.scan_device_ports(device) for device in self.devices]
        await asyncio.gather(*tasks)
    
    def display_results(self):
        """Display scan results in a nice table"""
        if not self.devices:
            console.print("[yellow]No devices found[/yellow]")
            return
        
        table = Table(title="Network Scan Results", box=box.ROUNDED)
        table.add_column("IP Address", style="cyan", no_wrap=True)
        table.add_column("MAC Address", style="magenta")
        table.add_column("Hostname", style="green")
        table.add_column("Vendor", style="yellow")
        table.add_column("Open Ports", style="red")
        
        for device in self.devices:
            open_ports = ', '.join(map(str, device.get_open_ports())) if device.get_open_ports() else "None"
            table.add_row(
                device.ip,
                device.mac or "N/A",
                device.hostname or "Unknown",
                device.vendor or "Unknown",
                open_ports
            )
        
        console.print("\n")
        console.print(table)
        console.print(f"\n[green]Total devices found: {len(self.devices)}[/green]")
    
    def export_json(self, filename: str):
        """Export results to JSON"""
        data = {
            'scan_time': datetime.now().isoformat(),
            'network': self.config.network,
            'devices': [device.to_dict() for device in self.devices]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        console.print(f"[green]✓ Results exported to {filename}[/green]")
    
    def export_csv(self, filename: str):
        """Export results to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['IP', 'MAC', 'Hostname', 'Vendor', 'Open Ports'])
            
            for device in self.devices:
                open_ports = ','.join(map(str, device.get_open_ports()))
                writer.writerow([
                    device.ip,
                    device.mac or '',
                    device.hostname or '',
                    device.vendor or '',
                    open_ports
                ])
        
        console.print(f"[green]✓ Results exported to {filename}[/green]")


# ============================================================================
# CLI INTERFACE
# ============================================================================

@click.group()
def cli():
    """Professional Network Scanner - Discover devices and scan ports"""
    pass


@cli.command()
@click.argument('network')
@click.option('--ports', default='1-1000', help='Port range to scan (e.g., 1-1000 or 22,80,443)')
@click.option('--timeout', default=2.0, help='Connection timeout in seconds')
@click.option('--max-concurrent', default=100, help='Maximum concurrent connections')
@click.option('--export-json', help='Export results to JSON file')
@click.option('--export-csv', help='Export results to CSV file')
@click.option('--scan-type', type=click.Choice(['fast', 'full']), default='fast', help='Scan type')
def scan(network, ports, timeout, max_concurrent, export_json, export_csv, scan_type):
    """Scan a network for devices and open ports
    
    Example: scanner.py scan 192.168.1.0/24
    """
    console.print(Panel.fit(
        "[bold cyan]Network Scanner v1.0[/bold cyan]\n"
        f"Scanning: {network}",
        border_style="cyan"
    ))
    
    # Create configuration
    config = ScanConfig(
        network=network,
        ports=ports,
        timeout=timeout,
        max_concurrent=max_concurrent,
        scan_type=scan_type
    )
    
    # Create scanner
    scanner = NetworkScanner(config)
    
    # Discover hosts
    devices = scanner.discover_hosts_arp()
    
    if not devices:
        console.print("[yellow]No devices found. Make sure you're running as Administrator.[/yellow]")
        return
    
    # Scan ports
    asyncio.run(scanner.scan_all_devices())
    
    # Display results
    scanner.display_results()
    
    # Export if requested
    if export_json:
        scanner.export_json(export_json)
    
    if export_csv:
        scanner.export_csv(export_csv)


@cli.command()
@click.argument('network')
def discover(network):
    """Quick host discovery without port scanning
    
    Example: scanner.py discover 192.168.1.0/24
    """
    console.print(f"[cyan]Discovering hosts on {network}...[/cyan]\n")
    
    config = ScanConfig(network=network)
    scanner = NetworkScanner(config)
    
    devices = scanner.discover_hosts_arp()
    
    if devices:
        scanner.display_results()
    else:
        console.print("[yellow]No devices found[/yellow]")


if __name__ == '__main__':
    cli()
