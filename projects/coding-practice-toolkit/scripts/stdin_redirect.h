/* Debug-only stdin redirection helper. */
#ifndef LIG_PRACTICE_STDIN_REDIRECT_H
#define LIG_PRACTICE_STDIN_REDIRECT_H
#include <stdio.h>
#include <stdlib.h>
static void lig_practice_redirect_stdin(void) __attribute__((constructor));
static void lig_practice_redirect_stdin(void) {
    const char *path = getenv("LIG_INPUT_FILE");
    if (path && *path && !freopen(path, "rb", stdin)) {
        fprintf(stderr, "Cannot open debug input: %s\n", path);
        exit(2);
    }
}
#endif
