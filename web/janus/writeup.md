# Writeup for `janus`

|      author     | category | value |
|-----------------|----------|-------|
| Ixbixbam        | web      |  308  |

Someone hacked my space image viewer, but it's 100% secure now! Note: Attacking nasa's API is out of scope for this challenge

## Solution

<details>
<summary>Click here to reveal the solution!</summary>

### Walkthrough

The system contains a hidden web service on port 5001 that we need to access using Server Side Request Forgery. The server has an endpoint where it accesses nasa's API from an url provided as a parameter.

However, you can't directly access the local website by accessing `https://janus.secso.cc/api?url=localhost:5001` because the server checks that the IP address resolves to nasa's API.

The intended way to bypass this is by using a DNS rebinding attack, where we change the DNS record from one of Nasa's IP addresses to the local machine on 127.0.0.1.

This can be done using online tools like rebindr with the payload `https:/janus.secso.cc/api?url=03af733c.7f000001.rbndr.us:5001`, but it can also be done more consistently when controlling the DNS records yourself.

See [solve.py](solve.py) for the solve script that manually rebinds the DNS record.

Note that the response will be Bad Gateway if we try to access port 5001 on Nasa's website, and Bad Request if the server detects that the IP address doesn't resolve to one of Nasa's.

An interesting unintended solve is to abuse the parsing differences in urllib and urllib3. `https://janus.secso.cc/api?url=https://your_own_website.redirecting.tolocalhost5001\@images-api.nasa.gov`.

### Flag(s)

- `K17{DNS___more_l1ke_d0main_name_shuffl3}`

</details>
