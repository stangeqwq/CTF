# Intro To ROP

## Task 3 - First ROP
We inspect the files that are in the `~\first_rop` directory. Running a `checksec` on `three_locks` gives us a pretty vulnerable binary.
```console
buzz@intro2rop:~/first_rop$ checksec three_locks
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/home/buzz/first_rop/three_locks'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
With (`NX enabled`)[https://en.wikipedia.org/wiki/NX_bit], the binary does not allow us to both write or execute on memory, `stack`. This feature is the thus called `write XOR execute`. 
Because of this, `ROP` is needed wherein we use operands within the binary itself to execute. Which operands are useful, can we understand through looking at the `three_locks.c` source code.
```C

```



```console
buzz@intro2rop:~/first_rop$ python3 exploit.py
[+] Starting local process './three_locks': pid 12219
[!] cyclic_find() expected a 4-byte subsequence, you gave b'kaa'
    Unless you specified cyclic(..., n=3), you probably just want the first 4 bytes.
    Truncating the data at 4 bytes.  Specify cyclic_find(..., n=3) to override this.
[*] Switching to interactive mode
We need to unlock 3 locks to print the flag!
Lock 1 unlocked!
Lock 2 unlocked!
Lock 3 is a gimmie. If you get the other 2, this should work.
Here is you flag (hopefully):
flag{F1r5t_ROP_c0mpl3t3}
```
