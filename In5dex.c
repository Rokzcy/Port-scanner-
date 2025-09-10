#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <semaphore.h>

#define MAX_THREADS 100   // Limit concurrent threads
#define TIMEOUT 1         // Timeout seconds

typedef struct {
    char target_host[256];
    int port;
} thread_args;

sem_t semaphore;

void* scan_port(void* args) {
    thread_args* targs = (thread_args*)args;
    int sock;
    struct sockaddr_in target_addr;

    sem_wait(&semaphore);  // Limit concurrent threads

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock >= 0) {
        target_addr.sin_family = AF_INET;
        target_addr.sin_port = htons(targs->port);
        target_addr.sin_addr.s_addr = inet_addr(targs->target_host);

        struct timeval tv;
        tv.tv_sec = TIMEOUT;
        tv.tv_usec = 0;
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);
        setsockopt(sock, SOL_SOCKET, SO_SNDTIMEO, (const char*)&tv, sizeof tv);

        if (connect(sock, (struct sockaddr*)&target_addr, sizeof(target_addr)) == 0) {
            printf("[+] Port %d OPEN\n", targs->port);
        }
        close(sock);
    }

    free(targs);
    sem_post(&semaphore);
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <target_ip>\n", argv[0]);
        return 1;
    }

    char* target_host = argv[1];

    sem_init(&semaphore, 0, MAX_THREADS);
    pthread_t threads[65535];

    printf("[*] Scanning %s on ports 1-65535...\n\n", target_host);

    int tcount = 0;
    for (int port = 1; port <= 65535; port++) {
        thread_args* args = malloc(sizeof(thread_args));
        strcpy(args->target_host, target_host);
        args->port = port;

        pthread_create(&threads[tcount++], NULL, scan_port, args);
    }

    for (int i = 0; i < tcount; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("\n[*] Scan complete.\n");
    return 0;
}
