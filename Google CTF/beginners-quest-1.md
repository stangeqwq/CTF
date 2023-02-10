# CCTV
A simple programming CTF challenge that requires some understanding of JavaScript, if not doing a little OSINT helps.

## The Challenge
You arrive at your destination. The weather isn’t great, so you figure there’s no reason to stay outside and you make your way to one of the buildings. No one bothered you so far, so you decide to play it bold - you make yourself a cup of coffee in the social area like you totally belong here and proceed to find an empty room with a desk and a chair. You pull out our laptop, hook it up to the ethernet socket in the wall, and quickly find an internal CCTV panel - that’s a way better way to look around unnoticed. Only problem is… it wants a password.

## The Solution
Inspecting the source page, we can see a code snippet that checks the password.
```JS
const checkPassword = () => {
  const v = document.getElementById("password").value;
  const p = Array.from(v).map((a) => 0xcafe + a.charCodeAt(0));

  if (
    p[0] === 52037 &&
    p[6] === 52081 &&
    p[5] === 52063 &&
    p[1] === 52077 &&
    p[9] === 52077 &&
    p[10] === 52080 &&
    p[4] === 52046 &&
    p[3] === 52066 &&
    p[8] === 52085 &&
    p[7] === 52081 &&
    p[2] === 52077 &&
    p[11] === 52066
  ) {
    window.location.replace(v + ".html");
  } else {
    alert("Wrong password!");
  }
};
```
The input on the password field is stored in `v` by `document.getElementId("password").value`. Afterwards, a simple cipher is placed on each character's unicode value, 16 bits, `2^16 = 0-65535` possible values.
The hex value `0xCAFE` is added to each of the characters. We can enumerate each value of the password by subtracting `0xCAFE` from their values (this is the password that's being checked against). I just used terminal with `python3` command.
```console
>>> 52037 - 0xCAFE
71
```
Completing the array with the appropriate indices as given by the page source, we obtain the final list and printing it out.
```console
>>> array = [71, 111, 111, 100, 80, 97, 115, 115, 119, 111, 114, 100]
>>> for i in array: print(chr(i), end='')
GoodPassword
```

This gives us the flag `CTF{IJustHopeThisIsNotOnShodan}`.
