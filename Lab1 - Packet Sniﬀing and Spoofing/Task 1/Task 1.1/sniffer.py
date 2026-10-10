from scapy.all import *

def print_pkt(pkt):
    pkt.show()
    
pkt = sniff(iface="br-9e6e3b2d8339", filter="tcp and src host 10.9.0.5 and dst port 23", prn=print_pkt)