![Pasted image 20261004125757](../../Pics/Pasted%20image%2020261004125757.png)

```python
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
```

The python script increments the TTL for each iteration until destination is reached

```bash
root@archlinux:/volumes# ip route get 8.8.8.8  
8.8.8.8 via 192.168.3.1 dev enp5s0 src 192.168.3.7 uid 0    
   cache
```

So on Wireshark I select the interface `enp5s0`;

![Pasted image 20261004141857](../../Pics/Pasted%20image%2020261004141857.png)

while on attaker shell:
```bash
root@archlinux:/volumes# python3 /volumes/traceroute.py  
1 192.168.3.1 (ICMP type 11, code 0)  
2 10.1.37.2 (ICMP type 11, code 0)  
3 10.1.37.1 (ICMP type 11, code 0)  
4 10.253.0.1 (ICMP type 11, code 0)  
5 213.187.0.113 (ICMP type 11, code 0)  
6 213.187.0.30 (ICMP type 11, code 0)  
7 185.1.114.26 (ICMP type 11, code 0)  
8 192.178.96.161 (ICMP type 11, code 0)  
9 142.250.211.29 (ICMP type 11, code 0)  
10 8.8.8.8 (ICMP type 0, code 0)  
Destination reached.
```

We can observe that from 1 to 9, the intermediate routers replied with ICMP time exceeded/ With TTL 10, destination replied with Echo Reply, so there are 10 hops with 9 intermediate routers. This is an experimental measurement that can change during time.

