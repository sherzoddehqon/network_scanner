#!/usr/bin/env python3
"""
Multi-Network Scanner - Scans multiple networks including hotspots
"""

import asyncio
import socket
import subprocess
import re
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import json

try:
    from scapy.all import ARP, Ether, srp, conf
    conf.verb = 0
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Warning: Scapy not available.")

try:
    from mac_vendor_lookup import MacLookup
    MAC_LOOKUP_AVAILABLE = True
except ImportError:
    MAC_LOOKUP_AVAILABLE = False

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()


@dataclass
class Device:
    """Represents a discovered network device"""
    ip: str
    mac: Optional[str] = None
    hostname: Optional[str] = None
    vendor: Optional[str] = None
    network: Optional[str] = None  # Which network it was found on
    ports: List[int] = field(default_factory=list)
    
    def to_dict(self):
        return {
            'ip': self.ip,
            'mac': self.mac,
            'hostname': self.hostname,
            'vendor': self.vendor,
            'network': self.network,
            'open_ports': self.ports
        }


class MultiNetworkScanner:
    """Scan multiple networks including hotspots"""
    
    def __init__(self):
        self.all_devices: List[Device] = []
        self.mac_lookup = None
        
        if MAC_LOOKUP_AVAILABLE:
            try:
                self.mac_lookup = MacLookup()
                self.mac_lookup.update_vendors()
            except:
                self.mac_lookup = None
    
    def get_local_networks(self) -> List[str]:
        """Detect all local networks on this computer"""
        networks = []
        
        try:
            if subprocess.os.name == 'nt':  # Windows
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                output = result.stdout
                
                # Find all IPv4 addresses and subnet masks
                ip_pattern = r'IPv4 Address[.\s]+:\s+(\d+\.\d+\.\d+\.\d+)'
                subnet_pattern = r'Subnet Mask[.\s]+:\s+(\d+\.\d+\.\d+\.\d+)'
                
                ips = re.findall(ip_pattern, output)
                subnets = re.findall(subnet_pattern, output)
                
                for ip, subnet in zip(ips, subnets):
                    # Convert to network address
                    ip_parts = [int(p) for p in ip.split('.')]
                    subnet_parts = [int(p) for p in subnet.split('.')]
                    
                    network_parts = [ip_parts[i] & subnet_parts[i] for i in range(4)]
                    
                    # Calculate CIDR notation
                    cidr = sum([bin(s).count('1') for s in subnet_parts])
                    
                    network = f"{'.'.join(map(str, network_parts))}/{cidr}"
                    if network not in networks and not network.startswith('169.254'):
                        networks.append(network)
            
        except Exception as e:
            console.print(f"[yellow]Could not auto-detect networks: {e}[/yellow]")
        
        return networks
    
    def scan_network_arp(self, network: str) -> List[Device]:
        """Scan a single network using ARP"""
        if not SCAPY_AVAILABLE:
            console.print("[yellow]Scapy required for scanning[/yellow]")
            return []
        
        try:
            console.print(f"[cyan]Scanning {network}...[/cyan]")
            
            arp = ARP(pdst=network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp
            
            result = srp(packet, timeout=3, verbose=0)[0]
            
            devices = []
            for sent, received in result:
                device = Device(ip=received.psrc, mac=received.hwsrc, network=network)
                
                # Get vendor
                if self.mac_lookup:
                    try:
                        device.vendor = self.mac_lookup.lookup(device.mac)
                    except:
                        device.vendor = "Unknown"
                
                # Get hostname
                try:
                    device.hostname = socket.gethostbyaddr(device.ip)[0]
                except:
                    device.hostname = None
                
                devices.append(device)
            
            console.print(f"[green]✓ Found {len(devices)} devices on {network}[/green]")
            return devices
            
        except PermissionError:
            console.print(f"[red]ERROR: Need administrator privileges for {network}[/red]")
            return []
        except Exception as e:
            console.print(f"[yellow]Could not scan {network}: {e}[/yellow]")
            return []
    
    def scan_all_networks(self, additional_networks: List[str] = None):
        """Scan all detected networks plus any additional ones"""
        # Get local networks
        local_networks = self.get_local_networks()
        
        # Add common hotspot networks
        common_hotspot_networks = [
            '192.168.137.0/24',  # Windows Mobile Hotspot
            '192.168.0.0/24',
            '192.168.1.0/24',
            '172.20.10.0/24',  # iPhone hotspot
        ]
        
        # Combine all networks
        all_networks = list(set(local_networks + common_hotspot_networks))
        
        if additional_networks:
            all_networks.extend(additional_networks)
        
        console.print(Panel.fit(
            f"[bold cyan]Multi-Network Scanner[/bold cyan]\n"
            f"Scanning {len(all_networks)} networks",
            border_style="cyan"
        ))
        
        console.print("\n[cyan]Networks to scan:[/cyan]")
        for net in all_networks:
            console.print(f"  • {net}")
        console.print()
        
        # Scan each network
        for network in all_networks:
            devices = self.scan_network_arp(network)
            self.all_devices.extend(devices)
        
        return self.all_devices
    
    def display_results(self):
        """Display all discovered devices grouped by network"""
        if not self.all_devices:
            console.print("[yellow]No devices found[/yellow]")
            return
        
        # Group by network
        networks = {}
        for device in self.all_devices:
            net = device.network or "Unknown"
            if net not in networks:
                networks[net] = []
            networks[net].append(device)
        
        # Display each network
        for network, devices in networks.items():
            table = Table(
                title=f"Network: {network} ({len(devices)} devices)",
                box=box.ROUNDED
            )
            table.add_column("IP Address", style="cyan", no_wrap=True)
            table.add_column("MAC Address", style="magenta")
            table.add_column("Hostname", style="green")
            table.add_column("Vendor", style="yellow")
            
            for device in devices:
                table.add_row(
                    device.ip,
                    device.mac or "N/A",
                    device.hostname or "Unknown",
                    device.vendor or "Unknown"
                )
            
            console.print("\n")
            console.print(table)
        
        console.print(f"\n[green]Total devices found: {len(self.all_devices)}[/green]")
        console.print(f"[green]Networks scanned: {len(networks)}[/green]")
    
    def export_csv(self, filename: str):
        """Export all results to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Network', 'IP', 'MAC', 'Hostname', 'Vendor'])
            
            for device in self.all_devices:
                writer.writerow([
                    device.network or '',
                    device.ip,
                    device.mac or '',
                    device.hostname or '',
                    device.vendor or ''
                ])
        
        console.print(f"[green]✓ Results exported to {filename}[/green]")
    
    def export_json(self, filename: str):
        """Export all results to JSON"""
        data = {
            'scan_time': datetime.now().isoformat(),
            'total_devices': len(self.all_devices),
            'devices': [device.to_dict() for device in self.all_devices]
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        console.print(f"[green]✓ Results exported to {filename}[/green]")


@click.group()
def cli():
    """Multi-Network Scanner - Find devices across multiple networks"""
    pass


@cli.command()
@click.option('--networks', '-n', multiple=True, help='Additional networks to scan (e.g., 192.168.1.0/24)')
@click.option('--export-csv', help='Export to CSV file')
@click.option('--export-json', help='Export to JSON file')
def scan_all(networks, export_csv, export_json):
    """Scan all local networks and common hotspot ranges
    
    Example: multi_network_scanner.py scan-all
    Example: multi_network_scanner.py scan-all -n 192.168.50.0/24 -n 10.0.0.0/24
    """
    scanner = MultiNetworkScanner()
    
    # Scan all networks
    additional = list(networks) if networks else None
    scanner.scan_all_networks(additional_networks=additional)
    
    # Display results
    scanner.display_results()
    
    # Export if requested
    if export_csv:
        scanner.export_csv(export_csv)
    
    if export_json:
        scanner.export_json(export_json)


@cli.command()
def detect_networks():
    """Detect all network interfaces on this computer"""
    scanner = MultiNetworkScanner()
    networks = scanner.get_local_networks()
    
    console.print("\n[cyan]Detected Networks:[/cyan]")
    for net in networks:
        console.print(f"  • {net}")
    
    console.print("\n[cyan]Common Hotspot Networks:[/cyan]")
    console.print("  • 192.168.137.0/24 (Windows Mobile Hotspot)")
    console.print("  • 192.168.0.0/24")
    console.print("  • 192.168.1.0/24")
    console.print("  • 172.20.10.0/24 (iPhone Hotspot)")


if __name__ == '__main__':
    cli()
