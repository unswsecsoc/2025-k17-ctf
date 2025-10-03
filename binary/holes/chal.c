#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int index1;
    int byte1;
    int index2;
    int byte2;

    puts("You may edit two bytes in the provided binary before running it.");

    printf("Enter the index of the first byte you'd like to change: ");
    fflush(stdout);
    scanf("%d", &index1);
    printf("Enter the hex value of the byte you want to change this to: 0x");
    fflush(stdout);
    scanf("%x", &byte1);

    printf("Enter the index of the second byte you'd like to change: ");
    fflush(stdout);
    scanf("%d", &index2);
    printf("Enter the hex value of the byte you want to change this to: 0x");
    fflush(stdout);
    scanf("%x", &byte2);

    system("/usr/bin/cp ./binary /tmp/binary");
    system("chmod +x /tmp/binary");
    FILE *f = fopen("/tmp/binary", "r+");
    if (f == NULL) {
        perror("fopen");
        exit(1);
    }

    fseek(f, index1, SEEK_SET);
    fputc(byte1, f);

    rewind(f);

    fseek(f, index2, SEEK_SET);
    fputc(byte2, f);

    fclose(f);

    printf("Patched the binary.\n");
    fflush(stdout);

    char *const b_argv[] = {"/tmp/binary", NULL};
    char *const b_envp[] = {NULL};
    execve("/tmp/binary", b_argv, b_envp);
    perror("execve failed");
}