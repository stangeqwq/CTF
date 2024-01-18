# 2 Initiell aksess

For å få tilgang til de forskjellige departmentene, måtte man 
1. utnytte en `IDOR` sårbarhet ved `/comment`-endepunktet til `IT-ticket support verktøyet`
2. manipulere `JWT` ved å sende en konstruert `POST`-request til `/update_user`-endepunktet der `admin=True` er satt som ekstra parameter.
3. overbevise `Eva`, KI-modell, at du er `admin` og gi `FLAGG` med tomromfor å unngå `CLASSIFIED`-blokade
4. analysere `drop.pcap`-fila på `Wireshark` og merke `HTTP` request uten `TLS/SSL` beskyttelse der innholdet kan sjekkes å være en `zip`-fil, altså en `information disclosure`-problem

Dette lar oss `ssh` til meste parten av virksomhetens innside, dog med `reduserte privilegier`

Jeg brukte mesteparten av tiden min til `Department of Intelligence` og `Department of Development and Test`.
## 2.1. Department of Intelligence
Det kan være nyttig å lese dokumentasjon om `BITS`-protokollet nedenfra, da finner man ut hvordan å få bitstrømmen ut. Det er nok å finne `11` som viser slutten av `fibonacci-tallene` og finne når `bildet` begynner. 32-bits encryption kan man brute-force med samme algoritmen, siden krypteringsalgoritmen er symmetrisk.

For `bitswin`, kan man tenke at hvert `11111` som en heap, der man tar visse verdier fra, lik på `NIM`-spillet. Da blir spillet et problem å finne `nim-verdier` (et enkelt `grafteori` problem) for hvert heap for deretter å kjøre `sum-of-games` teoremet i `kombinatorisk spillteori`. Det blir `xor` operasjon. Først var jeg ikke sikker på tallrekken, så utviklet jeg en `rekursiv` algoritme som løser nim-verdiene for hver `node` (representert antall `1` i tilleg til `11`) i rettet graf. Tallrekken søkte jeg deretter på databasen for tallrekker [https://oeis.org/] og brukte det videre.

## 2.4. Department of Development and Test
Det bør være løselig med litt dedikasjon og nysgjerrighet på hvordan `MOV-16` fungerer, et `assembly` lignende lavnivå programmeringsspråk.

## Konklusjon og Refleksjon
Det var noen steder jeg kunne ha hentet ut flagget med litt mer prøving. For eksempel i `department of security`, kunne jeg ha prøvd å ha `cd passFTP_shared/src` istedenfor `get passFTP_shared/FLAGG` eller andre `cd passFTP_shared/FLAGG` eller `cd /home/admin` osv.

Jeg merket nok i `department of technology` at `hardcoded secret` var `ciphertext` i `AES-ECB` dekodingen og dermed at jeg må prøve å finne en nøkkel som dekodere det med en kommando. Her bruteførcet jeg `ls;` i begynnelsen men var utålmodig og tenkte på om det var en matematisk løsning. I etterkant innser jeg nå at `sh;` er overkommelig nok.


