- This challenge used a format string to leak the stack and libc. Followed by a simple ret2libc call. 

- We were allowed to place a "hole" or write what where in anywhere in the program.

- We could enter our name and it would print it out, but through a format string vulnerability. We could obtain a stack leak and a libc leak, and this would give the addresses to system, binsh, and pop rdi gadget. 

- In our fun fact buffer (which was placed at the top of the stack), we can insert a pop rdi; binsh; system payload. This would allow us to pop a shell, if that gets executed.

- Our next goal was to write what where, through our stack leak, we can identify where we return back to main after finishing our hole function. Rather than returning to main and carrying on execution, we can place the address to a return call instead.

- Therefore now rather than returning back to main, we return to the payload in our fun fact region and pop a shell.