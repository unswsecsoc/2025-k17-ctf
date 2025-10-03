# Writeup for `pwnable document format`

|      author     | category | value |
|-----------------|----------|-------|
| Ixbixbam        | web      |  493  |

We patched the XSS by modifying the library, surely it's secure now?

## Solution

<details>
<summary>Click here to reveal the solution!</summary>

### Walkthrough

The website loads arbitrary PDFs from the URL using an outdated version of PDF.js which is vulnerable to both CVE-2024-4367 (a full XSS) and CVE-2018-5158 (an XSS inside the sandboxed worker script). CVE-2024-4367 works by injecting javascript into a string passed from the worker into the main page where it is evaluated. 

We need to leak the user's cookie, which requires an XSS in the main page. To obtain this, we can manually send the same messages to the main page from the worker that CVE-2024-4367 would have sent. We can use CVE-2018-5158 to do this.

To get the flag you can run [server.py] on the internet and visit the page https://pdf-web.k17.kctf.cloud/viewer?url=SERVER/exploit.pdf .

Another nice writeup: https://jia.je/ctf-writeups/2025-09-19-k17-ctf-2025/pwnable-document-format.html

### Flag(s)

- `K17{needs_m0r3_threat_1ntel}`

</details>
