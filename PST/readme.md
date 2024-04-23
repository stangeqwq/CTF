# Hack all the things
Dette var en ctf som er i forbindelse med PST-sitt stillingsannonse `Seniorutvikler/utvikler innen avansert digital innhenting`. 
## Tilgang
For å få tilgang til de forskjellige oppgavene, måtte man dekode følgende `01100100 01101101 00111001 01110010 01100100 01000111 01010110 01111001 01001100 01101110 01101000 00110101 01100101 01100111 00111101 00111101`. Ved å bruke konvertere på nettet, altså fra `binary`-to-`ascii` converter, også `base64`-to-`ascii` converter, får man tilgang på nettsiden: `vokter.xyz`. Insipiserer mann nettsiden, får man endepunktet `vokter.xyz/hvithatt`. Her er oppgavene:
## Oppgave 2 (Crypto)
Oppgaveteksten kan ses på `Oppgave_2/crypto.txt`. Teksten består av en crypterttekst og en privatnøkkel. Vi leser av fra privatnøkkel gjennom terminalen:

```zsh
> cat key.pem
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQClV56rd1l1ds/o
LFA2S16+t9F+qBqoph4xBeRXJW2JDy+iroGs7VHqd/PWr5W8rru5omfD9vqq88pA
f0WbZNRCY6p8Qar8uSpT7JkiAMMWtRgAxihHMvBPYhFGc2RHuCQumAbWztv5aQ6x
yGRXXk4/A25p8O2PKTqq3w2RgY/VRpx13UhjswvPZfUy8FmAziBFQNUp96TiJbK0
VDBwwbZNqHpbYQ/YpfuZSH9YSfXT1R9rl0l+CxLePSVvXwEPzrjG3Bqcr3xIiope
nuZcYlrgISj30xN+SsxAYIo00EXeTwcGznalriosguupoq1IKFiuRVFG/RZ7gWmr
5GH4KQhbAgMBAAECggEAMlqv6PptFTf883FjcFWd4ilrNM6PZ+NHeJiZxOySIlas
pDfPKFISS30CltRcntz8MPnD7ktuZdffNatNEJkxh5KA3lzFbTgbKvn4XQGsaGL4
j2vJ4n0h8JsmNbV4ydrLsiD8nDjdh2S2Y/Bqlq0S2V/7JWqJfrsIsfdCU5kIq+Pa
1CQShAgiYDtUmxcL2KeFHkWJAH3KVZ9Wf99J5T+vim8/2R5bRDTJCDr5lfuw4p+C
2kOO7JBz7hCifXgyc6mh4rJHyU1OhIUTb1Cv46eX/BLu72UGusx6rL6nqNwANEjt
PcE9wgWn1XDi1jaksWZz665KWnA/6s2wgBGdKLmrkQKBgQDYQ1KDrx/5z+tYkW2v
OjH4QqGK08DQSPCk//yCNn1VsX6o23LqHkDF5bUSiw7Ss8mAj33iIHIC6srThWrI
Bg1bhiUWgAouftLuKURZ3QRPQvq9zi6HtCMgp1Oc9Fa1OAmp8b0keA19xBL/+v2S
dNgNCmKGy06Uhz9suCJ9T2nROQKBgQDDuRDE4jO9dIXMZ0iTXzTENiZflvA2DB9J
JtHkedbu7dTAMT0C5cKoujuN7rrP08MooT82mTWthzYHfpA+K6Dk1dgWwPziVNyx
C87KeESqsJiFbTzh4cqIUpqwy4DgDazDLwWaoW5RvNZ54tQ3iv9EhRZW4hrO7I3g
m/J2pMkqMwKBgDGFYPy0ek769HpIeuRYIB8oKtOeX5WSTkCKOakbjyGzTjyeW7cO
jGiEjC0d2JwY/ThKI1pHcbQHTcCX2XbKI/7kPdPkJ/Czq9tLadJmENmRjdcuwmri
rfSJPFVBgiVnGpdmupgCQZyd7HffYndJ+DssOJmDLpBGVBiyJXuqVqHJAoGAMply
s2PDepRYTurYwXjYnG1faFEOUvq5T+EgXE//eA+2c+WG32vk8lgLM3tngnk9uBBP
1l6vmOge2LsosVn4I5EBZ4iHGEBWOdNSp9eF8Rbsp3oBRmhoQuwQH+rMq5/9bQyI
B1z6t1j5ndM9iAqASgeaKeYUhjBz0YCfo3qgoy8CgYBHBK3DBN4k215FjZo66JgA
vIlgLDUSFU+WtTiiao0VY55wVPcW/KTJIJ8h36SHdGejmdkOHkv+rFsZi8Sl2ZTP
4Rx4HcRiOoU/udtUnQKax8/RlKYnapukkn8wcmZm6anqRj1u+6uHH0gQopUPMKV5
/Pu5+MltJrax3klgFXVYXg==
-----END PRIVATE KEY-----
> openssl rsa -in key.pem -text -noout

Private-Key: (2048 bit, 2 primes)
modulus:
    00:a5:57:9e:ab:77:59:75:76:cf:e8:2c:50:36:4b:
    5e:be:b7:d1:7e:a8:1a:a8:a6:1e:31:05:e4:57:25:
    6d:89:0f:2f:a2:ae:81:ac:ed:51:ea:77:f3:d6:af:
    95:bc:ae:bb:b9:a2:67:c3:f6:fa:aa:f3:ca:40:7f:
    45:9b:64:d4:42:63:aa:7c:41:aa:fc:b9:2a:53:ec:
    99:22:00:c3:16:b5:18:00:c6:28:47:32:f0:4f:62:
    11:46:73:64:47:b8:24:2e:98:06:d6:ce:db:f9:69:
    0e:b1:c8:64:57:5e:4e:3f:03:6e:69:f0:ed:8f:29:
    3a:aa:df:0d:91:81:8f:d5:46:9c:75:dd:48:63:b3:
    0b:cf:65:f5:32:f0:59:80:ce:20:45:40:d5:29:f7:
    a4:e2:25:b2:b4:54:30:70:c1:b6:4d:a8:7a:5b:61:
    0f:d8:a5:fb:99:48:7f:58:49:f5:d3:d5:1f:6b:97:
    49:7e:0b:12:de:3d:25:6f:5f:01:0f:ce:b8:c6:dc:
    1a:9c:af:7c:48:8a:8a:5e:9e:e6:5c:62:5a:e0:21:
    28:f7:d3:13:7e:4a:cc:40:60:8a:34:d0:45:de:4f:
    07:06:ce:76:a5:ae:2a:2c:82:eb:a9:a2:ad:48:28:
    58:ae:45:51:46:fd:16:7b:81:69:ab:e4:61:f8:29:
    08:5b
publicExponent: 65537 (0x10001)
...osv
```
også får vi hex av alle de forskjellige delene som er nødvendig for å kryptere filen. Siden den er privatnøkkel, vi kan dekryptere. Pythonskriptet er gitt ved `Oppgave_2/decrypt.py`. Flagget er altså: `PST{ItsPrivateForAReason}`

