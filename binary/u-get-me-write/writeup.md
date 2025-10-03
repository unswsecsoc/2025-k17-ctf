- This challenge is a ROP method known as ret2gets. The whole binary is as follows:

```c
#include <stdio.h>
#include <string.h>

void main(void) {

    char *str = "Pleasure to meet you! Please enter your name: ";
    char buf[20];
    printf("Hello! %s\n", str);

    gets(buf);
}

``` 

- gets is known to be the most vulnerable function in C, and is just broken.

- While the binary does not have any gadgets for ret2libc, gets places a pointer in rdi to some writeable section of memory in libc. 

- If we call gets again after this function finishes, our pointer in rdi is set to be that region of memory, notably _IO_stdfile_0_lock, and now we can write to that region of memory.

- We can get the exact same pointer back into rdi for that region of memory and can use a trivial format string to leak memory from the stack or libc or anywhere else.

- Notably %3$p the value pointed to some constant symbol in libc from which we can find the offset to the base of libc, and eventually perform a simple ret2libc.

