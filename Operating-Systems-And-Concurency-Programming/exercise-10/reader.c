#include <semaphore.h>
#include <unistd.h>
#include <stdio.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1

int main()
{
    sem_t *reader_named_semaphor;
    sem_t *writer_named_semaphor;
    reader_named_semaphor = sem_open("/reader_semaphor", 0, 0666, 0); //creating necessary semaphores
    writer_named_semaphor = sem_open("/writer_semaphor", 0, 0666, 0);

    while (1) //we need to be sure that reader is not entering the room while writer is inside
    {
        printf("WAIT writer\n");
        sem_wait(writer_named_semaphor);
        printf("WAIT reader\n");
        sem_wait(reader_named_semaphor);
        printf("POST writer\n");
        sem_post(writer_named_semaphor);
        printf("CRITICAL OPEN Reader entered\n");
        sleep(1); //READING
        printf("CRITICAL CLOSE Reader exited\n");
        printf("POST reader\n");
        sem_post(reader_named_semaphor);
        sleep(10);
    }
    return EXIT_SUCCESS;
}
