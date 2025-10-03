#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

#define FILENAME "/tmp/config"
#define MAX_FILE_SIZE 16 * 1024

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>

void receive_file() {
    FILE *f = fopen(FILENAME, "wb");
    if (!f) {
        perror("fopen");
        exit(1);
    }

    char buf[4096];
    size_t total = 0;
    size_t n;

    while ((n = fread(buf, 1, sizeof(buf), stdin)) > 0) {
        total += n;
        if (total > MAX_FILE_SIZE) {
            fwrite(buf, 1, n - (total - MAX_FILE_SIZE), f);
            break;
        }
        fwrite(buf, 1, n, f);
    }

    fclose(f);
}

char **get_config_envp() {
    FILE *f = fopen(FILENAME, "rb");
    if (!f) {
        perror("fopen");
        exit(1);
    }

    size_t cap = 32;
    size_t count = 0;
    char **envp = malloc(cap * sizeof(char *));
    if (!envp) {
        perror("malloc");
        exit(1);
    }

    char line[4096];
    while (fgets(line, sizeof(line), f)) {
        char *eq = strstr(line, " = ");
        if (!eq) continue;

        char *newline = strchr(line, '\n');
        if (newline) *newline = '\0';

        *eq = '\0';
        char *var = line;
        char *val = eq + 3;

        size_t len = strlen(var) + 1 + strlen(val) + 1;
        char *entry = malloc(len);
        if (!entry) {
            perror("malloc");
            exit(1);
        }
        snprintf(entry, len, "%s=%s", var, val);

        if (count + 1 >= cap) {
            cap *= 2;
            envp = realloc(envp, cap * sizeof(char *));
            if (!envp) {
                perror("realloc");
                exit(1);
            }
        }

        envp[count++] = entry;
    }
    fclose(f);

    envp[count] = NULL;
    return envp;
}

int main() {
    printf("Welcome to our service! Give us some variables and we will ladify them!\n");
    receive_file();
    char **envp = get_config_envp();

    printf("Calculating new values...\n");

    char *argv[] = {"./calc", NULL};
    execve("./calculator", argv, envp);
    perror("execve");
    exit(1);

    return 0;
}