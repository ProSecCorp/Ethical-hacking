## Task 1.1

```shell
docker exec victim-10.9.0.5 sysctl \
  net.ipv4.tcp_syncookies \
  net.ipv4.tcp_max_syn_backlog \
  net.ipv4.tcp_synack_retries
  
  net.ipv4.tcp_syncookies = 0  
  net.ipv4.tcp_max_syn_backlog = 2048  
  net.ipv4.tcp_synack_retries = 5
```


We execute the attack `docker exec -it seed-attacker bash -lc \'cd /volumes && timeout 70s python3 synflood_draft.py'`. 
On a second terminal, we execute the command: `docker exec victim-10.9.0.5 sh -c  "ss -Hant | awk '$1 == "SYN-RECV" && $4 ~ /:23$/ {n++} END {print n+0}'"` which returns `129`.
This is the number of incomplete connections.
We can also see that by trying to Telnet `10.9.0.5` it succeeds. So the attack didn't work in this case.

We can try reduce the queue size to 80
```bash
docker exec victim-10.9.0.5 \
  sysctl -w net.ipv4.tcp_max_syn_backlog=80
docker exec victim-10.9.0.5 ip tcp_metrics flush
```

Reducing the backlog to 80 was enough to saturate all the available spots.
Now, during the attack execution, we can see that the number of incomplete connections now is `61` and the Telnet connections now fails (stays on `Trying 10.9.0.5...`).

Note that running at least four instances of `synflood_draft.py` also does the trick.
## Task 1.2

Now I try to execute the C code.  The number of incomplete connections is now `129`, but the Telnet connection now fails until the attack finishes.

**Observations:**
With the original `tcp_max_syn_backlog` value of 2048, the Python attack produced 129 observed `SYN-RECV` connections, but the legitimate Telnet connection succeeded. After reducing the backlog to 80, approximately 61 incomplete connections were observed and Telnet remained at `Trying 10.9.0.5...`. This is consistent with the lab’s description of reserving about one quarter of the queue for previously proven clients.

After restoring the original backlog, the C attack again produced 129 observed incomplete connections, but Telnet failed while the attack ran. The `SYN-RECV` count is only an instantaneous occupancy measurement. Incomplete connections eventually expire and free slots; the likely difference is that the C program sends replacement SYN packets faster than the Python/Scapy program, leaving fewer opportunities for the legitimate connection. In fact, with only one instance Telnet eventually succeeds before timeout. When the attack stops, Telnet succeeds again.

## Task 1.3
Enable SYN cookies mechanism
```bash
docker exec victim-10.9.0.5 \
  sysctl -w net.ipv4.tcp_syncookies=1
```

With SYN cookies disabled, the C SYN flood prevented the legitimate Telnet connection. After enabling `net.ipv4.tcp_syncookies=1`, Telnet consistently connected during the same attack. The server could therefore continue handling legitimate connection attempts despite the flood. An increase in `SyncookiesSent` confirms that the kernel used SYN cookies.
Also, by checking `SyncookiesSent` and `TCPReqQFullDoCookies` with the command

```bash
docker exec victim-10.9.0.5 nstat -az |
  grep -E 'TcpExt(SyncookiesSent|TCPReqQFullDoCookies)'
```

we can see that they increased, confirming that the cookies worked.
