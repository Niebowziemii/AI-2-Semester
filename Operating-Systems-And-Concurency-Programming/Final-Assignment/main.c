#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <semaphore.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define LIMIT_CON 10
#define LIMIT_PROD 10
#define LIMIT_BUFFER 15
#define O_CREATE 0100

int main(int argc, char **argv)
{
    //fprintf(stderr, "unlink old semaphores\n");
    sem_unlink("/producer_semaphore");
    sem_unlink("/consumer_semaphore");
    sem_unlink("/regular_semaphore");
    sem_t *producer_semaphore;
    sem_t *consumer_semaphore;
    sem_t *regular_semaphore;
    producer_semaphore = sem_open("/producer_semaphore", O_CREATE, 0666, LIMIT_PROD);
    consumer_semaphore = sem_open("/consumer_semaphore", O_CREATE, 0666, 0);
    regular_semaphore = sem_open("/regular_semaphore", O_CREATE, 0666, 1);
    if (producer_semaphore == SEM_FAILED || consumer_semaphore == SEM_FAILED || regular_semaphore == SEM_FAILED)
    {
        fprintf(stderr, "ERROR 00\n");
    }
    int *index_in;
    int *index_out;
    int *buffer;

    key_t index_out_key = ftok("./main", 2137);
    if (index_out_key == -1)
    {
        fprintf(stderr, "ERROR 01, %d\n", index_out_key);
    }
    key_t index_in_key = ftok("./main", 88);
    if (index_in_key == -1)
    {
        fprintf(stderr, "ERROR 02\n");
    }
    key_t buffer_key = ftok("./main", 14);
    if (buffer_key == -1)
    {
        fprintf(stderr, "ERROR 03\n");
    }
    int shmid_index_out = shmget(index_out_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_out == -1)
    {
        fprintf(stderr, "ERROR 04\n");
    }
    int shmid_index_in = shmget(index_in_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_in == -1)
    {
        fprintf(stderr, "ERROR 05\n");
    }
    int shmid_buffer = shmget(buffer_key, LIMIT_BUFFER * sizeof(int), 0666 | IPC_CREAT);
    if (shmid_buffer == -1)
    {
        fprintf(stderr, "ERROR 06\n");
    }
    index_out = (int *)shmat(shmid_index_out, (void *)0, 0);
    if (index_out == (void *)-1)
    {
        fprintf(stderr, "ERROR 07\n");
    }
    index_in = (int *)shmat(shmid_index_in, (void *)0, 0);
    if (index_in == (void *)-1)
    {
        fprintf(stderr, "ERROR 08\n");
    }
    buffer = (int *)shmat(shmid_buffer, (void *)0, 0);
    if (buffer == (void *)-1)
    {
        fprintf(stderr, "ERROR 09\n");
    }
    *index_in = 0;
    *index_out = 0;
    pid_t producers[LIMIT_PROD];
    pid_t consumers[LIMIT_CON];
    char *id = malloc(sizeof(char));
    //fprintf(stderr, "main przed forkiem\n");
    for (int i = 0; i < LIMIT_PROD; i++)
    {
        id[0] = i + 48;
        if (!(producers[i] = fork()))
        {
            execl("./prod", "prod", id, (char *)0);
            return EXIT_FAILURE;
        }
    }
    for (int i = 0; i < LIMIT_CON; i++)
    {
        id[0] = i + 48;
        if (!(consumers[i] = fork()))
        {
            execl("./cons", "cons", id, (char *)0);
            return EXIT_FAILURE;
        }
    }
    sleep(60);
    printf("Execution time of the program is 60 seconds\n");
    for (int i = 0; i < LIMIT_CON; i++)
    {
        kill(consumers[i], SIGKILL);
    }
    for (int i = 0; i < LIMIT_PROD; i++)
    {
        kill(producers[i], SIGKILL);
    }
    sem_destroy(producer_semaphore);
    sem_destroy(consumer_semaphore);
    sem_destroy(regular_semaphore);
    free(id);
    return EXIT_SUCCESS;
}
