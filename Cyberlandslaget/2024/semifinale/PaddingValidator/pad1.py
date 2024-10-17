from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

secret = b"flag{this_is_just_a_test_flag}"
print(pad(secret,16).hex())

def decrypt(key,ct):
    iv = ct[0:16]
    ct = ct[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 16)

def encrypt(key,pt):
    iv = b'\xad\x26\xc7\x35\x27\x67\x6c\xd2\x44\x12\xc8\x0d\xa1\x02\x1d\xb1'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print(iv.hex())
    return iv + cipher.encrypt(pad(pt, 16))

def Challenge(): 
    key = b'0123456789aaaaaa'
    ct = encrypt(key, secret)
    print(f"Welcome to Paddy's Padding Validator. You can validate if your decrypted message's padding is correct, or not.")
    print(ct.hex()[:2*16])
    print(f"ct={ct.hex()}")
    while True:
        ct = bytes.fromhex(input("encrypted secret (hex)> "))
        try:
            print(decrypt(key, ct))
            print("ok decryption")
        except:
            test1 = decrypt(key, ct)
            print(test1)
            print("error")

if __name__ == "__main__":
    #try:
        Challenge()
'''
    except Exception:
        #test1 = decrypt(key, ct)
        #print(test1)
        print("error")
        exit(0)
'''