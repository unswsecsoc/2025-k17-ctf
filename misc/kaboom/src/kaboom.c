#define _POSIX_C_SOURCE 200809L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zip/zip.h"

#define MAX_ZIP_SIZE 1994
#define MAX_UNZIPPED_SIZE 20000000

struct zip_action {
    char unzipped[MAX_UNZIPPED_SIZE];
    char *(*fn)(const char *, size_t);
    size_t fn_arg;
};

int unzip_all(struct zip_t *zip, char *buf) {
    int n = zip_entries_total(zip);
    printf("Found %d entries\n", n);

    char *buf_end = buf;
    for (int i = 0; i < n; ++i) {
        if (zip_entry_openbyindex(zip, i) == 0) {
            const char *name = zip_entry_name(zip);
            if (!zip_entry_isdir(zip)) {
                unsigned long long size = zip_entry_size(zip);
                printf("Reading %s (%llu bytes)\n", name, size);

                buf_end += zip_entry_noallocread(zip, buf_end, MAX_UNZIPPED_SIZE);
            } else {
                printf("Skipping directory %s\n", name);
            }

            zip_entry_close(zip);
        } else {
            puts("Failed to open entry");
            return 1;
        }
    }

    return 0;
}

void unzip(struct zip_action *action) {
    char zip_bytes[MAX_ZIP_SIZE] = {0};

    size_t zip_size = fread(zip_bytes, 1, sizeof(zip_bytes), stdin);
    if (!feof(stdin)) {
        puts("Warning: maximum size exceeded");
    }

    struct zip_t *zip = zip_stream_open(zip_bytes, zip_size, 0, 'r');
    if (!zip) {
        puts("Failed to open zip");
        return;
    }

    if (unzip_all(zip, action->unzipped) != 0) {
        puts("Error when unzipping file entries");
        return;
    }
    zip_stream_close(zip);

    char *res = action->fn(action->unzipped, action->fn_arg);
    puts(res);
}

char *checksum(const char *s, size_t dummy) {
    unsigned int res;
    for (const char *c = s; *c; c++) {
        res += *c;
    }

    char *new = malloc(32);
    snprintf(new, 32, "Checksum: 0x%x", res);
    return new;
}

int main(void) {
    struct zip_action *action = malloc(sizeof(struct zip_action));
    
    action->fn = strndup;
    action->fn_arg = 128;
    printf("Select action:\n  [1] Head\n  [2] Checksum\nEnter choice (1): ");
    char input[3];
    if (fgets(input, sizeof(input), stdin) && input[0] == '2') {
        action->fn = checksum;
    }

    printf("\nI'll save you some time, here's the address of system: %p\n", system);

    printf("Enter Zip Bytes:\n");
    unzip(action);

    printf("Done.\n");
    return 0;
}
