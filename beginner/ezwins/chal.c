#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct person {
    char name[32];
    char age;
    void (*func)();
} __attribute__((packed));

void win() {
    system("/bin/sh");
}

void print_greeting(struct person p) {
    printf("Hello, %s. You are %d years old.\n", p.name, p.age);
}

int main(void) {
    struct person c;
    c.func = print_greeting;

    puts("Hello! Let's get to know you a bit better.");
    puts("What's your name?");

    fgets(c.name, sizeof(c.name), stdin);

    puts("How old are you?");
    scanf(" %lld", &c.age);  
    
    int d; while ((d=getchar())!='\n' && d!=EOF);
    
    c.func(c);

    return 0;
}