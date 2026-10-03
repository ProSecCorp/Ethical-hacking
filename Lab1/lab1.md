# Task 1

## Task 1.1A 

**Question**: in the above program, for each captured packet, the callback function `print_pkt()` will be
invoked; this function will print out some of the information about the packet. Run the program with the
root privilege and demonstrate that you can indeed capture packets. After that, run the program again, but
without using the root privilege; describe and explain your observations.

```bash
@archlinux:/volumes# python3 sniffer.py    
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 60172  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x3b80  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ ICMP ]###    
       type      = echo-request  
       code      = 0  
       chksum    = 0xeb9e  
       id        = 0xe074  
       seq       = 0x1  
###[ Raw ]###    
          load      = '\xfdG\xbej\x00\x00\x00\x00\xaae\x07\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\  
x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'  
  
###[ Ethernet ]###    
 dst       = fe:8a:7c:ed:67:32  
 src       = 3a:c6:54:54:05:12  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 8140  
    flags     =    
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x46c1  
    src       = 10.9.0.6  
    dst       = 10.9.0.5  
    \options   \  
###[ ICMP ]###    
       type      = echo-reply  
       code      = 0  
       chksum    = 0xf39e  
       id        = 0xe074  
       seq       = 0x1  
###[ Raw ]###    
          load      = '\xfdG\xbej\x00\x00\x00\x00\xaae\x07\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\  
x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 61081  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x37f3  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ ICMP ]###    
       type      = echo-request  
       code      = 0  
       chksum    = 0x72a  
       id        = 0xe074  
       seq       = 0x2  
###[ Raw ]###    
          load      = '\xfeG\xbej\x00\x00\x00\x00\x8d\xd9\x07\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x  
1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'  
  
###[ Ethernet ]###    
 dst       = fe:8a:7c:ed:67:32  
 src       = 3a:c6:54:54:05:12  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 8688  
    flags     =    
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x449d  
    src       = 10.9.0.6  
    dst       = 10.9.0.5  
    \options   \  
###[ ICMP ]###    
       type      = echo-reply  
       code      = 0  
       chksum    = 0xf2a  
       id        = 0xe074  
       seq       = 0x2  
###[ Raw ]###    
          load      = '\xfeG\xbej\x00\x00\x00\x00\x8d\xd9\x07\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x  
1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 61719  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x3575  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ ICMP ]###    
       type      = echo-request  
       code      = 0  
       chksum    = 0x46c7  
       id        = 0xe074  
       seq       = 0x3  
###[ Raw ]###    
          load      = '\xffG\xbej\x00\x00\x00\x00L;\x08\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b  
\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'  
  
###[ Ethernet ]###    
 dst       = fe:8a:7c:ed:67:32  
 src       = 3a:c6:54:54:05:12  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x0  
    len       = 84  
    id        = 9019  
    flags     =    
    frag      = 0  
    ttl       = 64  
    proto     = icmp  
    chksum    = 0x4352  
    src       = 10.9.0.6  
    dst       = 10.9.0.5  
    \options   \  
###[ ICMP ]###    
       type      = echo-reply  
       code      = 0  
       chksum    = 0x4ec7  
       id        = 0xe074  
       seq       = 0x3  
###[ Raw ]###    
          load      = '\xffG\xbej\x00\x00\x00\x00L;\x08\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b  
\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
```

**Osservazioni:** con privilegi root lo sniffer cattura tre richieste ICMP da Host A
(`10.9.0.5`) a Host B (`10.9.0.6`) e le tre risposte in direzione opposta. Ogni coppia
echo-request/echo-reply mantiene lo stesso identificatore ICMP (`0xe074`), numero di
sequenza e payload; la sequenza aumenta da 1 a 3. Questo conferma la cattura di entrambe
le direzioni del ping. L'esecuzione senza privilegi riportata fallisce: l'apertura del
socket di cattura richiede privilegi adeguati, normalmente root o la capability
`CAP_NET_RAW`. Il messaggio esatto dell'errore non è incluso nei risultati.

--- 

## Task 1.1B
impostando `filter="tcp and src host 10.9.0.5 and dst port 23"` e generando connessione con telnet `telnet 10.9.0.6 23`

```bash
python3 sniffer.py    
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 60  
    id        = 33998  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c1  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813716  
       ack       = 0  
       dataofs   = 10  
       reserved  = 0  
       flags     = S  
       window    = 64240  
       chksum    = 0x144b  
       urgptr    = 0  
       options   = [('MSS', 1460), ('SAckOK', b''), ('Timestamp', (2475475214, 0)), ('NOP', None), ('WScale', 10)]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 33999  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c8  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813717  
       ack       = 934428652  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475214, 3252853322))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34000  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c7  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813717  
       ack       = 934428664  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475246, 3252853354))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 64  
    id        = 34001  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1ba  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813717  
       ack       = 934428664  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x144f  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475246, 3252853354))]  
###[ Raw ]###    
          load      = "\xff\xfb\x18\xff\xfb \xff\xfc#\xff\xfb'"  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 86  
    id        = 34002  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1a3  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813729  
       ack       = 934428682  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x1465  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475246, 3252853354))]  
###[ Raw ]###    
          load      = "\xff\xfa \x0038400,38400\xff\xf0\xff\xfa'\x00\xff\xf0\xff\xfa\x18\x00xterm\xff\xf0"  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 76  
    id        = 34003  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1ac  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813763  
       ack       = 934428697  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x145b  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475247, 3252853355))]  
###[ Raw ]###    
          load      = '\xff\xfd\x03\xff\xfc\x01\xff\xfb\x1f\xff\xfa\x1f\x00|\x00\x19\xff\xf0\xff\xfd\x05\xff\xfb!'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 55  
    id        = 34004  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c0  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813787  
       ack       = 934428700  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x1446  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475247, 3252853355))]  
###[ Raw ]###    
          load      = '\xff\xfd\x01'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34005  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c2  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813790  
       ack       = 934428720  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475288, 3252853355))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34006  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1c1  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813790  
       ack       = 934428740  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475475288, 3252853396))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 54  
    id        = 34007  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1be  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813790  
       ack       = 934428740  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x1445  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475483304, 3252853396))]  
###[ Raw ]###    
          load      = '\r\x00'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34008  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1bf  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813792  
       ack       = 934428742  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475483304, 3252861412))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34009  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1be  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813792  
       ack       = 934428752  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475483304, 3252861412))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 54  
    id        = 34010  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1bb  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813792  
       ack       = 934428752  
       dataofs   = 8  
       reserved  = 0  
       flags     = PA  
       window    = 63  
       chksum    = 0x1445  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475484401, 3252861412))]  
###[ Raw ]###    
          load      = '\r\x00'  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34011  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1bc  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813794  
       ack       = 934428754  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475484401, 3252862509))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34012  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1bb  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813794  
       ack       = 934428773  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475486349, 3252864457))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34013  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1ba  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813794  
       ack       = 934428793  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475486351, 3252864459))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34014  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1b9  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813794  
       ack       = 934428830  
       dataofs   = 8  
       reserved  = 0  
       flags     = A  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475535401, 3252913509))]  
  
###[ Ethernet ]###    
 dst       = 3a:c6:54:54:05:12  
 src       = fe:8a:7c:ed:67:32  
 type      = IPv4  
###[ IP ]###    
    version   = 4  
    ihl       = 5  
    tos       = 0x10  
    len       = 52  
    id        = 34015  
    flags     = DF  
    frag      = 0  
    ttl       = 64  
    proto     = tcp  
    chksum    = 0xa1b8  
    src       = 10.9.0.5  
    dst       = 10.9.0.6  
    \options   \  
###[ TCP ]###    
       sport     = 59502  
       dport     = telnet  
       seq       = 3250813794  
       ack       = 934428831  
       dataofs   = 8  
       reserved  = 0  
       flags     = FA  
       window    = 63  
       chksum    = 0x1443  
       urgptr    = 0  
       options   = [('NOP', None), ('NOP', None), ('Timestamp', (2475535401, 3252913509))]
```

**Osservazioni:** tutti i pacchetti riportati sono TCP da `10.9.0.5:59502` a
`10.9.0.6:23`; Scapy visualizza la porta 23 con il nome `telnet`. Il filtro seleziona
quindi la direzione richiesta: le risposte di Host B non compaiono perché non rispettano
le condizioni su sorgente e porta di destinazione. Si osservano un SYN iniziale (`S`),
ACK (`A`), segmenti con dati (`PA`) e un FIN/ACK finale (`FA`). I payload includono la
negoziazione Telnet, con informazioni sul terminale come `xterm`. La cattura ICMP del
Task 1.1A documenta invece il risultato del filtro `icmp`.


---
# Task 1.2
