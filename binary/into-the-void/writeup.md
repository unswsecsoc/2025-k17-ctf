- This challenge used a combination of overwriting the GOT, stack pivoting and a SROP. The whole binary is as follows:

```c
#include <stdio.h>
#include <unistd.h>


__attribute__((naked)) void _dl_locate_static_clone() {
    __asm__ volatile (
        ".byte 0x5E\n\t"
        ".byte 0xC3\n\t"
    );
}

int main(void) {

    char buf[8];
    int ret = read(0, buf, 0x1000);   

    return 15;  
}

``` 

- Given that _dl_locate_static_clone is just a pop rsi gadget, and read takes in the buffer as the second argument, we essentially have a write what where primitive. 

- Our goal is setup the SROP payload, overwrite the last byte of read to point to the syscall and pivot to the payload so our ret from our main executes that syscall. 

- We firsly write /bin/sh somewhere in writeable memory, there is a segment of writeable memory write after the GOT (located from 0x404100 to 0x405000). Our rdi from the execve SROP payload will point to that memory. My choice was at 0x404f00.

- We then send over the plt for read along with the bytes for our srop frame, which is located at 0x404a00. This would set up all the registers in that region of memory, preparing the SROP.

- Finally we overwrite the last byte in GOT for read, to point to a syscall rather than the start of read. I believe across all libc version, 16 bytes after the libc read functionality there is a syscall instruction. (I'm also not very sure but I think that the last nibble in the read function across all libc versions is either zero or eight. i.e. the last byte to change from beginning of read to the syscall instruction requires a bit of bruteforce (1/32)).


- We then pivot our stack to 0x404a00, where after returning 15 (i.e setting rax to 15) and performing the leaving instruction, rsp should now point to 0x404a00, and our final ret instruction would simply be the now syscall instruction.
