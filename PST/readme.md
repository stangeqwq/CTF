# Hack all the things
Dette var en ctf som er i forbindelse med PST-sitt stillingsannonse `Seniorutvikler/utvikler innen avansert digital innhenting`. 
## Tilgang
For å få tilgang til de forskjellige oppgavene, måtte man dekode følgende `01100100 01101101 00111001 01110010 01100100 01000111 01010110 01111001 01001100 01101110 01101000 00110101 01100101 01100111 00111101 00111101`. Ved å bruke konvertere på nettet, altså fra `binary`-to-`ascii` converter, også `base64`-to-`ascii` converter, får man tilgang på nettsiden: `vokter.xyz`. Insipiserer mann nettsiden, får man endepunktet `vokter.xyz/hvithatt`. Her er oppgavene:
## Oppgave 2 (Crypto)
Oppgaveteksten kan ses på `Oppgave_2/crypto.txt`. Teksten består av en crypterttekst og en privatnøkkel. Vi leser av fra privatnøkkel gjennom terminalen:
```zsh
openssl rsa -in key.pem -text -noout

Private-Key: (2048 bit, 2 primes)
modulus:
...
```
også får vi hex av alle de forskjellige delene som er nødvendig for å kryptere filen. Siden den er privatnøkkel, vi kan dekryptere. Pythonskriptet er gitt ved `Oppgave_2/decrypt.py`. Flagget er altså: `PST{ItsPrivateForAReason}`

