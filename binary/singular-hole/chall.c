#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>


void hole() {
    char *addr;
    unsigned char value;

    puts("Now let's get to business. Where would you like to place your hole?");
    printf(">> ");

    scanf(" %p", &addr);
    puts("What would you like to write there?");

    int c; while ((c=getchar())!='\n' && c!=EOF);
    
    scanf("%hhu", &value);  

    *addr = value;  

    puts("The hole is now in place. Good luck!");

    return;
}


int main(void) {

    puts("Welcome to the singular hole - (not the void though, thats somewhere else)!\"");

    char name[16];
    char fact[96];
    puts("");

    puts("In honour of yellowsubmarine's brain, which is");
    puts("completely full of holes, we're giving you the");
    puts("opportunity to exploit the one true singular hole.");
    puts("");

    puts("Please state your name:");
    printf(">> ");
    fgets(name, sizeof(name), stdin);

    printf("Well hello ");
    printf(name);
    puts("");

    puts("Please state a fun fact about yourself:");
    printf(">> ");
    fgets(fact, sizeof(fact), stdin);

    printf("Interesting, I didn't know that!\n");
    hole();

    return 0;
}


