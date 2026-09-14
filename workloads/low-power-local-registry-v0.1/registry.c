#define _POSIX_C_SOURCE 200809L
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX_RECORDS 64
#define MAX_KEY 32
#define MAX_VALUE 96
#define MAX_LINE 256
#define DEFAULT_PORT 8087

typedef struct {
    char key[MAX_KEY];
    char value[MAX_VALUE];
} record_t;

static record_t records[MAX_RECORDS];
static size_t record_count = 0;
static const char *state_path = NULL;
static volatile sig_atomic_t running = 1;

static void on_signal(int sig) {
    (void)sig;
    running = 0;
}

static int find_record(const char *key) {
    for (size_t i = 0; i < record_count; ++i) {
        if (strcmp(records[i].key, key) == 0) return (int)i;
    }
    return -1;
}

static bool valid_token(const char *s, size_t max_len) {
    size_t n = strlen(s);
    if (n == 0 || n >= max_len) return false;
    for (size_t i = 0; i < n; ++i) {
        unsigned char c = (unsigned char)s[i];
        if (c <= 0x20 || c == 0x7f || c == '\t') return false;
    }
    return true;
}

static int fsync_parent_dir(const char *path) {
    char *copy = strdup(path);
    if (!copy) return -1;
    char *slash = strrchr(copy, '/');
    const char *dir = ".";
    if (slash) {
        if (slash == copy) slash[1] = '\0';
        else *slash = '\0';
        dir = copy;
    }
    int dfd = open(dir, O_RDONLY | O_DIRECTORY);
    free(copy);
    if (dfd < 0) return -1;
    int rc = fsync(dfd);
    close(dfd);
    return rc;
}

static int persist_state(void) {
    size_t n = strlen(state_path) + 5;
    char *tmp = malloc(n);
    if (!tmp) return -1;
    snprintf(tmp, n, "%s.tmp", state_path);

    int fd = open(tmp, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) {
        free(tmp);
        return -1;
    }
    FILE *fp = fdopen(fd, "w");
    if (!fp) {
        close(fd);
        unlink(tmp);
        free(tmp);
        return -1;
    }

    for (size_t i = 0; i < record_count; ++i) {
        if (fprintf(fp, "%s\t%s\n", records[i].key, records[i].value) < 0) {
            fclose(fp);
            unlink(tmp);
            free(tmp);
            return -1;
        }
    }
    if (fflush(fp) != 0 || fsync(fd) != 0) {
        fclose(fp);
        unlink(tmp);
        free(tmp);
        return -1;
    }
    if (fclose(fp) != 0) {
        unlink(tmp);
        free(tmp);
        return -1;
    }
    if (rename(tmp, state_path) != 0) {
        unlink(tmp);
        free(tmp);
        return -1;
    }
    int rc = fsync_parent_dir(state_path);
    free(tmp);
    return rc;
}

static int load_state(void) {
    FILE *fp = fopen(state_path, "r");
    if (!fp) {
        if (errno == ENOENT) return 0;
        return -1;
    }
    char line[MAX_LINE];
    while (fgets(line, sizeof(line), fp)) {
        char *nl = strchr(line, '\n');
        if (nl) *nl = '\0';
        char *tab = strchr(line, '\t');
        if (!tab) continue;
        *tab = '\0';
        const char *key = line;
        const char *value = tab + 1;
        if (!valid_token(key, MAX_KEY) || !valid_token(value, MAX_VALUE)) continue;
        if (record_count >= MAX_RECORDS) break;
        snprintf(records[record_count].key, MAX_KEY, "%s", key);
        snprintf(records[record_count].value, MAX_VALUE, "%s", value);
        ++record_count;
    }
    fclose(fp);
    return 0;
}

static int put_record(const char *key, const char *value) {
    if (!valid_token(key, MAX_KEY) || !valid_token(value, MAX_VALUE)) return -2;
    int idx = find_record(key);
    if (idx < 0) {
        if (record_count >= MAX_RECORDS) return -3;
        idx = (int)record_count++;
        snprintf(records[idx].key, MAX_KEY, "%s", key);
    }
    snprintf(records[idx].value, MAX_VALUE, "%s", value);
    return persist_state();
}

static void write_all(int fd, const char *s) {
    size_t left = strlen(s);
    while (left > 0) {
        ssize_t n = send(fd, s, left, 0);
        if (n < 0) {
            if (errno == EINTR) continue;
            return;
        }
        s += (size_t)n;
        left -= (size_t)n;
    }
}

static void handle_client(int fd) {
    char line[MAX_LINE];
    size_t used = 0;
    while (used + 1 < sizeof(line)) {
        ssize_t n = recv(fd, line + used, 1, 0);
        if (n <= 0) return;
        if (line[used] == '\n') {
            line[used] = '\0';
            break;
        }
        ++used;
    }
    if (used == 0 && line[0] != '\0') return;

    char *save = NULL;
    char *cmd = strtok_r(line, " \r\t", &save);
    if (!cmd) {
        write_all(fd, "ERR empty\n");
        return;
    }

    if (strcmp(cmd, "PING") == 0) {
        write_all(fd, "PONG\n");
        return;
    }
    if (strcmp(cmd, "COUNT") == 0) {
        char out[64];
        snprintf(out, sizeof(out), "COUNT %zu\n", record_count);
        write_all(fd, out);
        return;
    }
    if (strcmp(cmd, "GET") == 0) {
        char *key = strtok_r(NULL, " \r\t", &save);
        if (!key || !valid_token(key, MAX_KEY)) {
            write_all(fd, "ERR key\n");
            return;
        }
        int idx = find_record(key);
        if (idx < 0) {
            write_all(fd, "NOT_FOUND\n");
            return;
        }
        char out[MAX_VALUE + 16];
        snprintf(out, sizeof(out), "VALUE %s\n", records[idx].value);
        write_all(fd, out);
        return;
    }
    if (strcmp(cmd, "PUT") == 0) {
        char *key = strtok_r(NULL, " \r\t", &save);
        char *value = strtok_r(NULL, " \r\t", &save);
        if (!key || !value) {
            write_all(fd, "ERR args\n");
            return;
        }
        int rc = put_record(key, value);
        if (rc == 0) write_all(fd, "OK\n");
        else if (rc == -2) write_all(fd, "ERR token\n");
        else if (rc == -3) write_all(fd, "ERR full\n");
        else write_all(fd, "ERR persist\n");
        return;
    }

    write_all(fd, "ERR command\n");
}

int main(int argc, char **argv) {
    if (argc < 2 || argc > 3) {
        fprintf(stderr, "usage: %s STATE_FILE [PORT]\n", argv[0]);
        return 2;
    }
    state_path = argv[1];
    int port = DEFAULT_PORT;
    if (argc == 3) {
        char *end = NULL;
        long parsed = strtol(argv[2], &end, 10);
        if (!end || *end != '\0' || parsed < 1 || parsed > 65535) {
            fprintf(stderr, "invalid port\n");
            return 2;
        }
        port = (int)parsed;
    }

    if (load_state() != 0) {
        perror("load_state");
        return 1;
    }

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);
    signal(SIGPIPE, SIG_IGN);

    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd < 0) {
        perror("socket");
        return 1;
    }
    int one = 1;
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons((uint16_t)port);

    if (bind(sfd, (struct sockaddr *)&addr, sizeof(addr)) != 0) {
        perror("bind");
        close(sfd);
        return 1;
    }
    if (listen(sfd, 16) != 0) {
        perror("listen");
        close(sfd);
        return 1;
    }

    printf("axm-registry-v0.1 listening on %d with %zu record(s)\n", port, record_count);
    fflush(stdout);

    while (running) {
        int cfd = accept(sfd, NULL, NULL);
        if (cfd < 0) {
            if (errno == EINTR) continue;
            perror("accept");
            break;
        }
        handle_client(cfd);
        close(cfd);
    }

    close(sfd);
    return 0;
}
