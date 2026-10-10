from scapy.all import *
packet = IP(src="10.9.0.5", dst="10.9.0.6") / ICMP(type=8, code=0, id=1234, seq=1) / Raw(load=b"Task 1: Spoofing ICMP Packet")
send(packet, verbose=False)
