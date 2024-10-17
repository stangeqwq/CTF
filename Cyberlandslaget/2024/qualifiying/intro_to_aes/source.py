from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes # pip install pycryptodome
import os

try:
    # The ciphertext at the bottom corresponds to the flag from disk on authors machine.
    # Your goal is to recover the contents of this flag.
    flag = open("../flag.txt","rb").read()
except FileNotFoundError:
    # Obviously, you dont have the real flag.
    # If you run this script on your machine flag will be set to a dummy/fake flag
    flag = b"flag{dummy_flag}"

# We use a known plaintext downloaded from https://github.com/brunoklein99/deep-learning-notes/blob/master/shakespeare.txt 
shakespeare = open("../shakespeare.txt","rb").read()[0:16*16]
# We build a new variable with 16 blocks of known plaintext + the unknown flag
plaintext = shakespeare + b"\n\n" + flag

# We use a cryptographicly secure random generator to get a 16 byte randomized key.
key = os.urandom(16)
# NB! Each time this command is run one would get a different key. So if you run this command
# on your computer you will get a totally different key. Also, remember that your goal is not to recover the key.

# xor is a function that performs XOR between the bytes in two byte buffers.
# It is equivalent with other libraries, like `from pwntools import xor`
def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

# We encrypt each 16byte block of plaintext using AES. I have created a custom block mode, but it has a severe flaw. Can you find it?
ciphertext = ""
for i in range(0, len(plaintext), 16):
    cipher = AES.new(key, AES.MODE_CBC, iv=bytes(16))
    ct = cipher.encrypt(flag[0:12] + long_to_bytes((i//16)%16,4))
    ciphertext += xor(plaintext[i:i+16], ct).hex()

# ciphertext is given as a hexadecimal string
print(ciphertext)

# 8e7e24751f22bf36361a14f243beb4011469f9764108770874d5e7e0e1656d5e13b1f75a12ee8c972fbc1c31a2ac18b4f4088c5d3a61e2a204ebc1978cadcfa2786bec26f43480a796299a18ac57baf1b8b809af387cdc3f55420a479950351a4bd7da21a3ef6e53ac26c1ee43845f19b21e37775b8bf09b4bf5d220bb888a3d38fc280c972b837a107d98bb5aa1c41f43f6aa73ddd0f73bf16a9f5a41885aff4c4d230c2b22442225dc4a09d5c317d13946f447cd122b207c22c23092a0aa593258e20e978b573c3e6acea22d4ffb3db6d9ddcfc24f1db4fa966240c664631c6de34bb67c2da7b18bd1fd53b45875b06f99c144fa7a866c15dc3ea46b694685d03c07392d0a8a1b063d339724838c64102dd64e7a366d4153d5d9eadb64784e01a6cd266dc4909d30fd1839a7b709befd22

"""
Tip; when you are to work on the ciphertext at your end you can convert it back to bytes in Python using the builtin bytes.fromhex function;

ciphertext = bytes.fromhex("<hex...>")
"""