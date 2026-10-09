import sys
import re
import socket
from scapy.all import ARP, Ether, srp

class NetworkScanner:
    def __init__(self):
        # Focus scanning on common administrative or web service ports
        self.target_ports = [21, 22, 23, 80, 443, 445, 3389, 8080]

    def scan_network(self, ip_range):
        """Discovers active IP and MAC addresses using ARP requests."""
        print(f"\n📡 Scanning target range: {ip_range}...")
        print("=" * 60)
        
        # 1. Craft an ARP Broadcast Request Packet
        # Broadcast asks "Who has this IP?" to every device on the subnet
        arp_request = ARP(pdst=ip_range)
        broadcast_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        
        # Combine them into a single ethernet transmission
        packet = broadcast_frame / arp_request

        # 2. Send the packet and listen for replies
        # srp() sends and receives packets at layer 2 (Ethernet)
        answered_list = srp(packet, timeout=2, verbose=False)[0]

        discovered_hosts = []
        for element in answered_list:
            host_info = {
                "ip": element[1].psrc,
                "mac": element[1].hwsrc
            }
            discovered_hosts.append(host_info)
            
        return discovered_hosts

    def check_ports(self, ip):
        """Performs a TCP handshake scan on essential target ports."""
        open_ports = []
        
        for port in self.target_ports:
            # Set up a clean TCP socket block
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # Fast timeout to keep the scan speedy
            
            # Attempt connection (0 means success)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            s.close()
            
        return open_ports

    def run(self, target_range):
        """Coordinates discovery and deeper port testing."""
        # Simple regex validation for IP formatting (e.g., 192.168.1.1/24)
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/\d{1,2})?$', target_range):
            print("[-] Invalid target range format. Example: 192.168.1.1/24")
            return

        hosts = self.scan_network(target_range)
        
        if not hosts:
            print("[-] No active hosts found or permission denied.")
            return

        print(f"{'IP Address':<17}{'MAC Address':<20}{'Open Ports'}")
        print("-" * 60)
        
        for host in hosts:
            # For every live device found, look for open doors
            ports = self.check_ports(host['ip'])
            port_str = ", ".join(map(str, ports)) if ports else "None detected"
            
            print(f"{host['ip']:<17}{host['mac']:<20}{port_str}")
            
        print("=" * 60)
        print(f"Scan complete. Discovered {len(hosts)} active device(s).\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scanner.py <target_ip_or_range>")
        print("Example: python scanner.py 192.168.1.1/24")
        print("Note: Must be run as Administrator on Windows.")
    else:
        scanner = NetworkScanner()
        scanner.run(sys.argv[1])