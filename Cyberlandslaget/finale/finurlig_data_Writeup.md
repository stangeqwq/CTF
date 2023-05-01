# FINURLIG DATA
En gøy forensics oppgave der man måtte kombinere forståelse av et filsystem, og scripting--bruteforce.

## Oppgave av PHST
Påsken varer visst helt til finalen, og P(H)ST har bidratt noen ekstraoppgaver til de ivrigste av kyllingagentene. Dette har de å melde:


"Et beslag PHST har tatt fra Sydpolare eggstremistiske aktører inneholder noe finurlig data vi ikke helt klarer å finne ut av. Kan du klekke ut en løsning?"

## Løsning
Gitt av filene er `.secret` som inneholder massevis av txt-filer med b64 enkodet passorder. Vi lager et skript som skal håndtere å gå igjennom passordene. 
```python3
import os
import pyzipper
import base64

# Define the path to the .secret directory
secret_path = ".secret"

# Walk through all subdirectories of .secret and find .txt files
for root, dirs, files in os.walk(secret_path):
    for file in files:
        if file.endswith(".txt"):
            # Read the contents of the file
            with open(os.path.join(root, file), "r") as f:
                contents = f.read().strip()

            # Decode the contents from base64
            password = base64.b64decode(contents).decode()

            # Attempt to open the password-protected zip file
            with pyzipper.AESZipFile("temmelegg_hemmelegg.zip", "r") as myzip:
                try:
                    myzip.extractall(pwd=password.encode())
                    print("🟢Password found: ", password)
                    exit(0)
                except Exception as e:
                    print(e)
                    print("🔴Nope: ", password)

# If the password wasn't found, print a message
print("🔴Unable to find password.")
```

`pyzipper` var blitt brukt siden `zipfile` fører til `incompatible compression`. Dette gir oss i konsole:
 ```zsh
🔴Nope:  VeldigFoelsomtPassord126
Bad password for file 'flag.txt'
🔴Nope:  SvaertNyttigPassord438
Bad password for file 'flag.txt'
🔴Nope:  LittLignendePassord945
🟢Password found:  VeldigTrygtPassord123
stange@ericjoshua filsystem %
```

Flagget blir dermed `flag{En_skal_ikke_skue_paaskekyllingen_på_fjaera}`
            
