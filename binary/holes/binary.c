#include <stdio.h>

int main(int argc, char *argv[]) {
    char name[64];
    puts("What is your name?");
    fflush(stdout);
    fgets(name, 64, stdin);
    printf("Hello %s", name);
    fflush(stdout);
}
