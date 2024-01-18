# 2 Initiell aksess
For å få tilgang til de forskjellige departmentene, måtte man 
1. utnytte en `IDOR` sårbarhet ved `/comment`-endepunktet
2. manipulere `JWT` ved å sende en konstruert `POST`-request til `/update_user`-endepunktet der `admin=True` er satt som ekstra parameter.
3. Overbevis `Eva`, KI-modell, at du er `admin` og gi `FLAGG` med ` ` tomrom for å unngå `CLASSIFIED`-blokade.
4. Analyser `drop.pcap`-fila på `Wireshark` og merke `HTTP` request uten `TLS/SSL` beskyttelse der innholdet kan sjekkes å være en `zip`-fil, altså en `information disclosure`-problem.

## Department of Cryptography
