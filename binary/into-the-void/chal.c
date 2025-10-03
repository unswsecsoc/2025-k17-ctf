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