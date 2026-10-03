from scapy.al import *
packet = IP(src="10.9.0.5", dst="10.9.0.6") / ICMP(type=8)
send(packet)
