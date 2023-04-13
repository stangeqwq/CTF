# Encryption Event
En gøy CTF-oppgave der man måtte forstå og lære om `VBScript` for a decryptere en epost som var kryptert av en dårlig implementert `ransomware`-aktig script på nett.

## Oppgave av Vealending
Threat actors these days have no shame. They steal code, and barely know how to use it.
Not only that, but they are so old fashioned that they are heavily reliant on VBScript for important things like crypto.


Unfortunately, they were still skilled enough to manage to encrypt our client's important file.
I refuse to believe they did a good job. Are you able to retrieve the contents of the file?


(WARNING - Place the files in a separate, empty folder. It will crawl subdirectories and encrypt the files if you accidentally run it.)

## Løsning
Vi prøver selvfølgelig å forstå hva det fordømte VBS-programmet prøver å gjøre. Her kan `chatGPT` være nyttig. Vi kutter ut deler av `vbs` programmet der det er nødvendig.
```html
<job>
  <script language="VBScript" src="aes.vbs"/>
  <script language="VBScript">

    Set fso = CreateObject("Scripting.FileSystemObject")
    set shell = CreateObject("Wscript.Shell")
    Set stream = CreateObject("ADODB.Stream")

    For Each folder In fso.GetFolder(".").SubFolders
      For Each file in fso.GetFolder(folder).Files

      Set src = fso.OpenTextFile(file, 1)
      Set dst = fso.OpenTextFile(file & ".enc", 8, -1)

      Do Until src.AtEndOfStream
        rax = shell.Run("powershell.exe -windowstyle hidden -e JABzAGUAZQBkACAAPQAgAEcAZQB0AC0AUgBhAG4AZABvAG0AIAA7ACAALgBcAGcAZQBuAGUAcgBhAHQAZQAuAGUAeABlACAAJABzAGUAZQBkACAAfAAgAE8AdQB0AC0ARgBpAGwAZQAgAC0ARQBuAGMAbwBkAGkAbgBnACAAYQBzAGMAaQBpACAALQBOAG8ATgBlAHcAbABpAG4AZQAgAGEAZQBzAF8AYQBuAGQAXwBoAG0AYQBjAC4AdAB4AHQA", 0, True)
        bin = FileToBytes("aes_and_hmac.txt")
        fso.DeleteFile("aes_and_hmac.txt")
        aesKey = B64Encode(TrimBytes(bin, 0, 32))
        macKey = B64Encode(TrimBytes(bin, 32, 32))
        dst.WriteLine (Encrypt(src.ReadLine(), aesKey, macKey) & ":" & aesKey)  
      Loop

      src.Close()
      dst.Close()
      fso.DeleteFile(file)
    
      Next
    Next

  </script>
</job>
```
```vbs
Function Encrypt(plaintext, aesKey, macKey)
    aes.GenerateIV()
    aesKeyBytes = B64Decode(aesKey)
    macKeyBytes = B64Decode(macKey)
    Set aesEnc = aes.CreateEncryptor_2((aesKeyBytes), aes.IV)
    plainBytes = utf8.GetBytes_4(plaintext)
    cipherBytes = aesEnc.TransformFinalBlock((plainBytes), 0, LenB(plainBytes))
    macBytes = ComputeMAC(ConcatBytes(aes.IV, cipherBytes), macKeyBytes)
    Encrypt = B64Encode(macBytes) & ":" & B64Encode(aes.IV) & ":" & B64Encode(cipherBytes)
End Function
```
Her kan vi forstå at hver linje i den krypterte eposten gir oss informasjon om `macBytes`, `aes.IV`, `cipherBytes`, og `aesKey`. For å dekryptere må vi reversere prosessen og da må vi finne ut `macKey`.
Ta det som en svart boks og med hjelp av `chatGPT` og litt redigering får vi skriptet som også er løsningen:
```python
from Crypto.Cipher import AES
import base64
import hmac
import hashlib

with open('Documents/important_email.eml.enc', 'r') as f:
    for line in f:
        encrypted_text = line
# split the encrypted text into its components
        mac_bytes, aes_iv, cipher_bytes, aes_key = encrypted_text.split(":")

# base64 decode the components
        mac_bytes = base64.b64decode(mac_bytes)
        aes_iv = base64.b64decode(aes_iv)
        cipher_bytes = base64.b64decode(cipher_bytes)
        aes_key = base64.b64decode(aes_key)

# compute the mac key from the aes key and aes iv
        mac_key = hmac.new(aes_key, msg=aes_iv, digestmod=hashlib.sha256).digest()

# decrypt the cipher bytes using aes-128-cbc mode
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
        plaintext = cipher.decrypt(cipher_bytes)

# remove the padding from the plaintext
        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]

# decode the plaintext to a string
        plaintext = plaintext.decode("utf-8")

# print the decrypted plaintext
        print(plaintext)
```
```console
sage decrypt.py
MIME-Version: 1.0
Date: Mon, 13 Mar 2023 21:58:30 +0100
From: Vealending <Vealending@protonmail.com>
Subject: Implementing backups?
Thread-Topic: Implementing backups?
Message-ID:
 <GF36kOxJsYZeZoYV3yITgynFqi0JQt9enmIW_120nFFMPRfaMWE62Mx-MCcrHdqRATuYhMhiecUBdzha1xkVvKrMZwKvbEyoDcSTqywc5Qc=@protonmail.com>
To: Cyberlandslaget <kontakt@cyberlandslaget.no>
Content-Type: multipart/related;
	boundary="_1F214529-CDDB-4D6F-A725-24FAF58B7989_"

--_1F214529-CDDB-4D6F-A725-24FAF58B7989_
Content-Transfer-Encoding: quoted-printable
Content-Type: text/html; charset="utf-8"

<html><head>
<meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8"></=
head><body><div style=3D"font-family: Arial, sans-serif; font-size: 14px;">=
</div><span style=3D"font-size:15px;font-family:&quot;Segoe UI&quot;, &quot=
;Segoe UI Web (West European)&quot;, &quot;Segoe UI&quot;, -apple-system, B=
```
```console
Content-Type: image/png; name="image.png"
Content-ID: <7b01aaef@protonmail.com>
Content-Transfer-Encoding: base64
Content-Disposition: inline; filename="image.png"

iVBORw0KGgoAAAANSUhEUgAAAfIAAAMRCAYAAAAX3jTVAAAAAXNSR0IArs4c6QAAAARnQU1BAACx
jwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAP+lSURBVHhe7J0FgBxF1sffZt3i7u4KgQDBPYe7
Hi6Hc3DIcdghBx+Hu7sf7sElBEIgHuLE3bPZrO989audN3SGWd9sssv7Qad7qqurqnu76l+vrONC
```
Ved å kjøre cyberchef file-detection på teksten får vi.
```console
File type:   Portable Network Graphics image (under Base64)
Extension:   B64
MIME type:   application/octet-stream
```
Vi må altså ta ut det relevante b64-encodet bildet og omgjøre til noe som er mer brukelig. Jeg brukte python for dette. 

```python
import base64

with open("image.b64", "r") as f:
    encoded_data = f.read()

decoded_data = base64.b64decode(encoded_data)

with open("image.png", "wb") as f:
    f.write(decoded_data)
```
Flagget finner altså da
![intro](https://github.com/stangeqwq/CTF/blob/main/images/encryptionevent.png)


