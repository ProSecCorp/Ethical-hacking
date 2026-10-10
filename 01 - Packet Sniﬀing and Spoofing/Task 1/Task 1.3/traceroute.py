from scapy.all import *

destination = "8.8.8.8"

for ttl in range (1, 30):
    probe = ( IP(dst=destination, ttl=ttl) / ICMP(type=8, id=4321, seq=ttl)
    )

    reply = sr1(probe, verbose=False, timeout=2)

    if reply is None:
        print(f"{ttl:2} *")
        continue
    if not reply.haslayer(ICMP):
        print(f"{ttl:2} {reply[IP].src} (Non-ICMP response)")
        continue
    
    icmp = reply[ICMP]
    print(f"{ttl:2} {reply[IP].src} (ICMP type {icmp.type}, code {icmp.code})")
    
    if icmp.type == 0 and reply[IP].src == destination:
        print("Destination reached.")
        break
    if icmp.type == 3:
        print("Destination unreachable.")
        break
else:
    print("Destination not reached in 30 hops.")