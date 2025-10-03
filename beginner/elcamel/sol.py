from pwn import *

def solve(p, q, c):
    ## Check if c is QR
    return pow(c, q, p) == 1

r = remote("challenge.secso.cc", 7001)

r.recvuntil(b'\n')
r.recvuntil(b'\n')
r.recvuntil(b'\n')

p = int(r.recvuntil(b'\n').strip().decode())
q = int(r.recvuntil(b'\n').strip().decode())

r.sendline(b"0")
r.sendline(b"1")

r.recvuntil(b"How long do you want the coin to be?> ")

for _ in range(50):
    c = int(r.recvline().strip())

    r.recvuntil(b"(H or T)> ")

    if solve(p, q, c):
        r.sendline(b"H")
    else:
        r.sendline(b"T")

    res = r.recvuntil(b"\n\n")
    print(res)

print(r.recv())
