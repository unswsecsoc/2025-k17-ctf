#include <stdio.h>
#include <string.h>

void main(void) {

    char *str = "Pleasure to meet you! Please enter your name: ";
    char buf[20];
    printf("Hello! %s\n", str);

    gets(buf);
}