## phished
Description:
```
We fired Billy last week after he failed a phishing test for the 6th time. We wiped his machine, but now we really need one of the files that was on it. Maybe he uploaded it somewhere? Do you think you can get it back from this packet capture?
```

## overview
- The PCAP shows a fake CAPTCHA malware site that tricks the user into running a program that then runs an encoded powershell script.
- This powershell script encrypts local files with a hardcoded AES key and exfiltrates them using DNS requests.

## community writeup
https://jia.je/ctf-writeups/2025-09-19-k17-ctf-2025/phished.html

## flag
<details>
    <summary>Click to reveal</summary>

    K17{inf0_stealer?n@h_1t's_a_fr33_backup!}
</details>