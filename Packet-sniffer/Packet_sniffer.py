from scapy.all import sniff,IP,TCP,UDP,ICMP
from collections import defaultdict
import datetime
import logging
import argparse
import sys
import signal

#Configure logging
logging.basicConfig(
    filename='network_traffic.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PacketSniffer:
    def __init__(self):
        self.packet_counts = defaultdict(int)
        self.protocol_counts = defaultdict(int)
        self.src_ip_counts = defaultdict(int)
        self.dst_ip_counts = defaultdict(int)
        self.start_time = datetime.datetime.now()
        self.packets_captured = 0

    def handle_packet(self,packet):
        """Process each captured packet"""
        self.packets_captured += 1

        if IP in packet:
            #Extract IP layer information
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            protocol = packet[IP].proto 

            #update statistics 
            self.src_ip_counts[ip_src] += 1
            self.dst_ip_counts[ip_dst] += 1
            
            #determine protocol and update counts
            if TCP in packets:
                proto_name = "TCP"
                sport = packet[TCP].sport
                dport = packet[TCP].dport
                #check for common services
                service = self.get_service_name(dport)
                self.packet_counts[f"{proto_name} : {services}"] += 1
            elif UDP in packet:
                proto_name = "UDP"
                sport = packet[UDP].sport
                dport = packet[UDP].dport
                service = self.get_service_name(dport)
                self.packet_counts[f"{proto_name} : {services}"] += 1
            elif ICMP in packet:
                proto_name = "ICMP"
                sport = dport = "N/A"
                self.packet_counts[f"{proto_name}"] += 1
            else:
                proto_name = "other"
                sport = dport = "N/A"
                self.packet_counts["other"] += 1

            #log packet information
            log_message = (
                f"protocol: {proto_name} | "
                f"source: {ip_src} -> {sport} | "
                f"destination: {ip_dst} -> {dport} | "
                f"Length : {len(packet)} bytes"
            )
            logging.info(log_message)
            print(f"[+] {log_message}")


    def get_service_name(self,port):
        """Return common servies names for well-known ports"""
        common_ports = {
            80:'HTTP',
            443:'HTTPS',
            22:'SSH',
            21:'FTP',
            53:'DNS',
            3306:'MySQL',
            27017:'MongoDB'
        }
        return common_ports.get(port,str(port))

    def print_statistics(self):
        """Print capture statistics"""
        duration = datetime.datetime.now() - self.start_time
        print("\n" + "="*50)
        print("Packet capture statistics")
        print("="*50)
        print(f"Duration: {duration}")
        print(f"Total packets captured: {self.packets_captured}")
        print("\nProtocol Distribution: ")
        for proto,count in self.protocol_counts.items():
            print(f"{proto}: {count} packets")

        print("\nTop 5 Source IP Addresses:")
        for ip, count in sorted(self.src_ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"{ip}: {count} packets")
        
        print("\nTop 5 Destination IP Addresses:")
        for ip, count in sorted(self.dst_ip_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"{ip}: {count} packets")

    def start_capture(self,interface=None,packet_counts=None):
        """Start packet capture"""
        def signal_hnadler(sig,frame):
            print("\n[!] Stopping packet capture...")
            self.print_statistics()
            sys.exit()
        
        signal.signal(signal.SIGINT,signal_hnadler)

        print(f"[*] Starting packet capture on interface {interface or 'any'}")
        print("[*] Press Ctrl+C to stop capturing and view statistics")
        
        #start packet capture
        sniff(iface=interface,prn=self.handle_packet,store=0,count=packet_counts)
        self.print_statistics()

def main():
    parser = argparse.ArgumentParser(description="Network packet sniffer")
    parser.add_argument("-i", "--interface", help="Network interface to capture packets")
    parser.add_argument("-c", "--count", type=int, help="Number of packets to capture")
    args = parser.parse_args()

    try:
        sniffer = PacketSniffer()
        sniffer.start_capture(
            interface=args.interface,
            packet_counts=args.count
        )
    except PermissionError:
        print("[!] Error: This script requires administrative privileges!")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[!] Packet capture stopped by user")
        sniffer.print_statistics()
    except Exception as e:
        print(f"[!] An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
