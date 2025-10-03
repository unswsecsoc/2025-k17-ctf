from pwn import *
import hlextend

"""
The INTENDED idea was to showcase a length extension attack on SHA1...
Essentially, because of how all SHA functions work, if we are given hash(m) and len(m),
we can compute hash(m || pad(m) || m2) for any m2 that we want.

In the challenge, we're given all of these values, so we can compute m' = m || pad(m) || m2,
where m is salt||"admin". This was, we can generate a password m' which is not the same as m,
but still has the same salt as a prefix, so it passes the check. We can add this new hash to 
the server using option 3.

The payload below basically just carries out this exploit and length extends admin.
"""

def solve(hash):
    target = b"admin".hex().encode()
    append = b"1"

    sha = hlextend.new("sha1")
    new_pass = sha.extend(append, target, 16, hash).hex()
    new_hash = sha.hexdigest()
    
    return new_pass, new_hash


r = remote("127.0.0.1", 8080)

r.sendline(b"3")
r.sendline(b"admin")
r.sendline(b"1")

r.recvuntil(b"Current password: ")

passw = r.recvuntil(b'\n').strip()
newp, newh = solve(passw.decode())

print(newp)
print(newh)

r.sendline(b"3")
r.sendline(b"admin")
r.sendline(newh.encode())

r.sendline(b"2")
r.sendline(b"admin")
r.sendline(newp.encode())

r.interactive()