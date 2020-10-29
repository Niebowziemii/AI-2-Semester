#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>
#include <semaphore.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <time.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define LIMIT_CON 10
#define LIMIT_PROD 10
#define LIMIT_BUFFER 15
#define O_CREATE 0100

int main(int argc, char **argv)
{
    //fprintf(stderr, "początek prod %s\n", argv[1]);
    srand(time(NULL) * getpid());
    sem_t *producer_semaphore;
    sem_t *consumer_semaphore;
    sem_t *regular_semaphore;
    producer_semaphore = sem_open("/producer_semaphore", O_CREATE, 0666, 0);
    consumer_semaphore = sem_open("/consumer_semaphore", O_CREATE, 0666, 0);
    regular_semaphore = sem_open("/regular_semaphore", O_CREATE, 0666, 0);
    if (producer_semaphore == SEM_FAILED || consumer_semaphore == SEM_FAILED || regular_semaphore == SEM_FAILED)
    {
        fprintf(stderr, "ERROR 10\n");
    }
    int *index_in;
    int *index_out;
    int *buffer;
    key_t index_out_key = ftok("./main", 2137);
    if (index_out_key == -1)
    {
        fprintf(stderr, "ERROR 11\n");
    }
    key_t index_in_key = ftok("./main", 88);
    if (index_in_key == -1)
    {
        fprintf(stderr, "ERROR 12\n");
    }
    key_t buffer_key = ftok("./main", 14);
    if (buffer_key == -1)
    {
        fprintf(stderr, "ERROR 13\n");
    }
    int shmid_index_out = shmget(index_out_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_out == -1)
    {
        fprintf(stderr, "ERROR 14\n");
    }
    int shmid_index_in = shmget(index_in_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_in == -1)
    {
        fprintf(stderr, "ERROR 15\n");
    }
    int shmid_buffer = shmget(buffer_key, LIMIT_BUFFER * sizeof(int), 0666 | IPC_CREAT);
    if (shmid_buffer == -1)
    {
        fprintf(stderr, "ERROR 16\n");
    }
    index_out = (int *)shmat(shmid_index_out, (void *)0, 0);
    if (index_out == (void *)-1)
    {
        fprintf(stderr, "ERROR 17\n");
    }
    index_in = (int *)shmat(shmid_index_in, (void *)0, 0);
    if (index_in == (void *)-1)
    {
        fprintf(stderr, "ERROR 18\n");
    }
    buffer = (int *)shmat(shmid_buffer, (void *)0, 0);
    if (buffer == (void *)-1)
    {
        fprintf(stderr, "ERROR 19\n");
    }
    while (1)
    {
        //fprintf(stderr, "pętla prod %s\n", argv[1]);
        sem_wait(producer_semaphore);
        //fprintf(stderr, "WAIT prod prod %s\n", argv[1]);
        sem_wait(regular_semaphore);
        //fprintf(stderr, "WAIT regular prod %s\n", argv[1]);
        int produced_item = rand() % 100;
        buffer[*index_in] = produced_item;
        fprintf(stderr, "Producer of id: %s, has produced item: %d at index: %d.\n", argv[1], produced_item, *index_in);
        int random_number = rand() % 5;
        sleep(random_number);
        //fprintf(stderr, "sleep(%d) %s\n", random_number, argv[1]);
        int bufferp = 0;
        bufferp = *index_in;
        bufferp = (bufferp + 1) % LIMIT_BUFFER;
        *index_in = bufferp;
        //fprintf(stderr, "POST regular prod %s\n", argv[1]);
        sem_post(regular_semaphore);
        //fprintf(stderr, "POST cons prod %s\n", argv[1]);
        sem_post(consumer_semaphore);
    }
    return EXIT_SUCCESS;
}
