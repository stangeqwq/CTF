# 2 Initiell aksess

For å få tilgang til de forskjellige departmentene, måtte man 
1. utnytte en `IDOR` sårbarhet ved `/comment`-endepunktet til `IT-ticket support verktøyet`
2. manipulere `JWT` ved å sende en konstruert `POST`-request til `/update_user`-endepunktet der `admin=True` er satt som ekstra parameter.
3. overbevise `Eva`, KI-modell, at du er `admin` og gi `FLAGG` med tomromfor å unngå `CLASSIFIED`-blokade
4. analysere `drop.pcap`-fila på `Wireshark` og merke `HTTP` request uten `TLS/SSL` beskyttelse der innholdet kan sjekkes å være en `zip`-fil, altså en `information disclosure`-problem

Dette lar oss `ssh` til meste parten av virksomhetens innside, dog med `reduserte privilegier`

Jeg brukte mesteparten av tiden min til `Department of Intelligence` og `Department of Development and Test`
## Department of Intelligence

## Department of Development and Test




