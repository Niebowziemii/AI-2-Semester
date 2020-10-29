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
    //fprintf(stderr,"początek cons %s\n",argv[1]);
    srand(time(NULL)*getpid());
    sem_t *producer_semaphore;
    sem_t *consumer_semaphore;
    sem_t *regular_semaphore;
    producer_semaphore = sem_open("/producer_semaphore", O_CREATE, 0666, 0);
    consumer_semaphore = sem_open("/consumer_semaphore", O_CREATE, 0666, 0);
    regular_semaphore = sem_open("/regular_semaphore", O_CREATE, 0666, 0);
    if (producer_semaphore == SEM_FAILED || consumer_semaphore == SEM_FAILED || regular_semaphore == SEM_FAILED)
    {
        fprintf(stderr,"ERROR 20\n");
    }
    int *index_in;
    int *index_out;
    int *buffer;
    key_t index_out_key = ftok("./main", 2137);
    if (index_out_key == -1)
    {
        fprintf(stderr,"ERROR 21\n");
    }
    key_t index_in_key = ftok("./main", 88);
    if (index_in_key == -1)
    {
        fprintf(stderr,"ERROR 22\n");
    }
    key_t buffer_key = ftok("./main", 14);
    if (buffer_key == -1)
    {
        fprintf(stderr,"ERROR 23\n");
    }
    int shmid_index_out = shmget(index_out_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_out == -1)
    {
        fprintf(stderr,"ERROR 24\n");
    }
    int shmid_index_in = shmget(index_in_key, sizeof(int), 0666 | IPC_CREAT);
    if (shmid_index_in == -1)
    {
        fprintf(stderr,"ERROR 25\n");
    }
    int shmid_buffer = shmget(buffer_key, LIMIT_BUFFER * sizeof(int), 0666 | IPC_CREAT);
    if (shmid_buffer == -1)
    {
        fprintf(stderr,"ERROR 26\n");
    }
    index_out = (int *)shmat(shmid_index_out, (void *)0, 0);
    if (index_out == (void *)-1)
    {
        fprintf(stderr,"ERROR 27\n");
    }
    index_in = (int *)shmat(shmid_index_in, (void *)0, 0);
    if (index_in == (void *)-1)
    {
        fprintf(stderr,"ERROR 28\n");
    }
    buffer = (int *)shmat(shmid_buffer, (void *)0, 0);
    if (buffer == (void *)-1)
    {
        fprintf(stderr,"ERROR 29\n");
    }
    //fprintf(stderr,"pętla cons %s\n",argv[1]);
    while (1)
    {
        sem_wait(consumer_semaphore);
        //fprintf(stderr,"WAIT cons cons %s\n",argv[1]);
        sem_wait(regular_semaphore);
        //fprintf(stderr,"WAIT regular cons %s\n",argv[1]);
        int producedc;
        producedc = buffer[*index_out];
        fprintf(stderr,"Consumer of index: %s has consumed an item: %d with index: %d\n", argv[1], producedc, *index_out);
        int random_numberc = rand()%5;
        sleep(random_numberc);
        //fprintf(stderr,"sleep(%d) %s\n",random_numberc, argv[1]);
        int bufferc = 0;
        bufferc = *index_out;
        bufferc = (bufferc + 1) % LIMIT_BUFFER;
        *index_out = bufferc;
        //fprintf(stderr,"POST regular cons %s\n",argv[1]);
        sem_post(regular_semaphore);
        //fprintf(stderr,"POST prod cons %s\n",argv[1]);
        sem_post(producer_semaphore);
    }
    return EXIT_SUCCESS;
}
