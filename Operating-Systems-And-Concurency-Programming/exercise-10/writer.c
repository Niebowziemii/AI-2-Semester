#include <stdio.h>
#include <unistd.h>
#include <semaphore.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define LIMIT_READERS 10

int main()
{
    sem_t *writer_named_semaphor;
    sem_t *reader_named_semaphor;
    reader_named_semaphor = sem_open("/reader_semaphor", 0, 0666, 0);   //creating and opening the semaphors
    writer_named_semaphor = sem_open("/writer_semaphor", 0, 0666, 0);
   
    while (1) //writer can only enter empty room all readers must be blocked
    {
        printf("WAIT writer\n");
        sem_wait(writer_named_semaphor);
        for (int i = 0; i < LIMIT_READERS; i++)
        {
            printf("WAIT reader\n");
            sem_wait(reader_named_semaphor);
        }
        printf("CRITICAL OPEN Writer entered\n");
        sleep(1);                                   //WRITING
        printf("CRITICAL CLOSE Writer exited\n");
        for (int i = 0; i < LIMIT_READERS; i++)
        {
            printf("POST reader\n");
            sem_post(reader_named_semaphor);
        }
        printf("POST writer\n");
        sem_post(writer_named_semaphor);
        sleep(10);
    }
}
