#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

const char *names[] = {
    "Alice", "Sophia", "Emma", "Olivia", "Isabella",
    "Mia", "Charlotte", "Amelia", "Harper", "Evelyn"
};
#define NAMES_COUNT (sizeof(names) / sizeof(names[0]))

void append_name(const char *var) {
    char *val = getenv(var);
    if (!val) {
        printf("%s not set\n", var);
        return;
    }

    const char *name = names[rand() % NAMES_COUNT];

    size_t newlen = strlen(val) + 1 + strlen(name) + 1;
    char *newval = malloc(newlen);
    if (!newval) {
        perror("malloc");
        exit(1);
    }

    snprintf(newval, newlen, "%s_%s", name, val);
    setenv(var, newval, 1);

    printf("%s\n", getenv(var));
    free(newval);
}

int main() {
    srand(time(NULL));

    append_name("v1");
    append_name("v2");
    append_name("v3");

    return 0;
}