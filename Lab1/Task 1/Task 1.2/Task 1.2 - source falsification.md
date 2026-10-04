![[Pasted image 20261004125100.png]]

So, the code is:

```python
from scapy.all import *
	packet = IP(src="10.9.0.5", dst="10.9.0.6") 
	/ ICMP(type=8, code=0, id=1234, seq=1) 
	/ Raw(load=b"Task 1: Spoofing ICMP Packet")
send(packet, verbose=False)
```

After executing the script on the attacker, an ICMP request is sent to 10.9.0.6 with a false source IP `10.9.0.5`. In Wireshark, we can see the request inside packet 4 and the reply on packet 7. Host B replies to that false IP, keeping the ICMP ID as 1234 and sequence number 1. 

![[Pasted image 20261004125335.png]]

