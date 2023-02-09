# Task 11 Challenge - Write-up
A very cool and 1337-like CTF file-upload web vulnerability where several CL-tools where used. Take note that the attack machine for TryHackMe was used to complete this challenge.

## The task
It's challenge time!

Head over to jewel.uploadvulns.thm.

Take what you've learned in this room and use it to get a shell on this machine. As per usual, your flag is in /var/www/. Bear in mind that this challenge will be an accumulation of everything you've learnt so far, so there may be multiple filters to bypass. The attached wordlist might help. Also remember that not all webservers have a PHP backend...

## The Solution
### Enumeration
In CTFs like this one, it is imperative to gather as much information as possible on the target. As we were first introduced in the room to enumerate via `gobuster`, we will do exactly that.
```console
root@ip-10-10-241-182:~# gobuster dir -u jewel.uploadvulns.thm -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -t 64
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://jewel.uploadvulns.thm
[+] Threads:        64
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2023/02/09 20:58:12 Starting gobuster
===============================================================
/content (Status: 301)
/modules (Status: 301)
/admin (Status: 200)
/assets (Status: 301)
/Content (Status: 301)
/Assets (Status: 301)
/Modules (Status: 301)
/Admin (Status: 200)
Progress: 9029 / 220561 (4.09%)
```
We look at the website and see how it responds to each of these directories. It seems only `http://jewel.uploadvulns.thm/admin` is interesting. 
----insert image maybe??

Looking at the page source is another method of enumeration. The following lines are interesting. They indicate some sort of script for filtering file-uploads.
```html
    <script src="assets/js/jquery-3.5.1.min.js"></script>
		<script src="assets/js/jquery.colour-2.2.0.min.js"></script>
		<script src="assets/js/upload.js"></script>
		<script src="assets/js/backgrounds.js"></script>
	</head>
	<body>
		<div id="one" class="background"></div>
		<div id="two" class="background" style="display:none;"></div>
```
