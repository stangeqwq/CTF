# New Caesar
A cool cryptography challenge with a particular emphasis on code-understanding and programming with python

## The Challenge by MADSTACKS
We found a brand new type of encryption, can you break the secret code? (Wrap with picoCTF{}) apbopjbobpnjpjnmnnnmnlnbamnpnononpnaaaamnlnkapndnkncamnpapncnbannaapncndnlnpna `new_caesar.py`

## The Solution
Looking into `new_caesar.py` gives us an insight to how this "new cryptographic" system works.

```python
LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

flag = "redacted"
key = "redacted"
assert all([k in ALPHABET for k in key])
assert len(key) == 1

b16 = b16_encode(flag)
enc = ""
for i, c in enumerate(b16):
	enc += shift(c, key[i % len(key)])
print(enc)
```

Firstly, the flag is encrypted via the `b16_encode()` function. Some understanding is needed in how characters are represented via bits. The main idea is that each character is represented by 8 bits.
So, each character in the flag plain text given, `plain`, is split into 4 bits, values ranging from 0-15. This means that for each character two characters are represented of which is a part of the `ALPHABET` string.
`ALPHABET` is equal to `abcdefghijklmnop`. 

Afterwards, each of the characters are placed under the `shift(c, k)` function wherein `c` is the character to be shifted and `k` is the corresponding shift using modular arithmetic (this, we see by the `- LOWERCASE_OFFSET` expression).

Great! The only piece left to be understood is the `key`. The assert keyword dramatically simplifies the `key`. It must be `in ALPHABET` in addition to only being a character.

There are several ways to now decrypt this cipher. My approach was to simply brute force the key which only has 16 possible values where I undo the shifts and the encodings. I edited `new_caesar.py` via `vim` and renamed it to be `new_caesar_edited.py`.

```python
import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_encode(plain):
	enc = ""
	for c in plain:
		binary = "{0:08b}".format(ord(c))
		enc += ALPHABET[int(binary[:4], 2)]
		enc += ALPHABET[int(binary[4:], 2)]
	return enc
def b16_decode(enc):
	plain = ""
	flag = ""
	for i in range(0, len(enc), 2): #analyze 4 bit pairs 01 - 23 - 45 - etc then place them together, essentially undoing the encoding.
		bitpair1 = ord(enc[i]) - LOWERCASE_OFFSET
		bitpair2 = ord(enc[i + 1]) - LOWERCASE_OFFSET
		flag += chr((bitpair1 << 4) + bitpair2)
	return flag

def shift(c, k):
	t1 = ord(c) - LOWERCASE_OFFSET
	t2 = ord(k) - LOWERCASE_OFFSET
	return ALPHABET[(t1 + t2) % len(ALPHABET)]

def unshift(c, k):
        t1 = ord(c) - LOWERCASE_OFFSET
        t2 = ord(k) - LOWERCASE_OFFSET
        return ALPHABET[(t1 - t2) % len(ALPHABET)] # using a clock analogy for modular arithmetic, we essentially rotate back to our original shift.

flag = "apbopjbobpnjpjnmnnnmnlnbamnpnononpnaaaamnlnkapndnkncamnpapncnbannaapncndnlnpna"
for letter in ALPHABET:
	key = letter
	assert all([k in ALPHABET for k in key])
	assert len(key) == 1
	#b16 = b16_encode(flag) the flag is already encoded b16 before the shift, undoing it would entail to unshift first before decoding
	enc = ""
	for i, c in enumerate(flag):
        	enc += unshift(c, key[i % len(key)])
	print(b16_decode(enc))
```
As you can see, I tried to test for every possible key. The output gives us:

```console
(base) stange@ericjoshua Downloads % python3 new_caesar_edited.py
ùÙùÜÝÜÛÑ
        ßÞÞßÐ
             ÛÚÓÚÒ
ÐÒÓÛßÐ            ßÒÑ
ÈèËÌËÊÀûÎÍÍÎÏÿûÊÉþÂÉÁûÎþÁÀüÏþÁÂÊÎÏ
íü×üý·×º»º¹¿ê½¼¼½¾îê¹¸í±¸°ê½í°¿ë¾í°±¹½¾
ÜëÆëì¦Æ©ª©¨®Ù¬««¬­ÝÙ¨§Ü §¯Ù¬Ü¯®Ú­Ü¯ ¨¬­
ËÚµÚÛµÈÌÈËÈËÉË
ºÉ¤ÉÊ¤·»·º·º¸º
©¸¸¹svwvu{¦yxxyzª¦ut©}t|¦y©|{§z©|}uyz
§§¨befedjhgghidclckhkjikldhi
qQqTUTSYWVVWXSR[RZWZYXZ[SWX
v`@`CDCBHsFEEFGwsBAvJAIsFvIHtGvIJBFG
et_tu?_23217b54456fb10e908b5e87c6e89156
TcNcd.N!"! &Q$##$%UQ /T(/'Q$T'&R%T'( $%
CR=RS=@D@C@CAC
2A,AB
?202 ,?3?
!01ûþÿþýóñððñò.ýü!õüô.ñ!ôó/ò!ôõýñò
/
/ ê
íîíìâàïïàáìëäëãàãâáãäìàá
```
Only `et_tu?_23217b54456fb10e908b5e87c6e89156` seems plausible. We submit `picoCTF{et_tu?_23217b54456fb10e908b5e87c6e89156}`, and it is in fact the flag.
