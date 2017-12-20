
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <jansson.h>
#include <CUnit/Basic.h>

/**
 *
 */
int main(int argc, char *argv[]) {

    json_t *json;
    json_error_t error;

    json = json_load_file("file.json", 0, &error);
    if (!json) {
        fprintf(stderr, "error: on line %d.%d: %s\n", error.line, error.column, error.text);
        return 1;
    }

    const char *string = json_string_value(json);

    printf("string = %s/n", string);

    if (argc > 1) {
        printf("Setting 'string' to %s\n", argv[1]);
    }

    if (argc > 2) {
        printf("Setting 'string' to %s\n", argv[2]);
    }

    size_t flags = 0;
    int rc = json_dump_file(json, "file.json", flags);
    if (rc != 0) {
        fprintf(stderr, "error saving json file\n");
        return 1;
    }
}

