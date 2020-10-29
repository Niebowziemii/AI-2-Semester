#include <semaphore.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <sys/types.h>

#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
#define LIMIT_READERS 10
#define LIMIT_WRITERS 5
#define O_CREATE 0100

int main()
{
    printf("unlink old semaphores\n");
    sem_unlink("/reader_semaphor"); //if earlier existed unlink them
    sem_unlink("/writer_semaphor");
    
    sem_t *reader_named_semaphor;
    sem_t *writer_named_semaphor;
    
    reader_named_semaphor = sem_open("/reader_semaphor", O_CREATE, 0666, LIMIT_READERS);//creaton of semaphores
    writer_named_semaphor = sem_open("/writer_semaphor", O_CREATE, 0666, 1);
    
    pid_t readers[LIMIT_READERS]; //list of processes I want to create 
    pid_t writers[LIMIT_WRITERS];
    for (int i = 0; i < LIMIT_READERS; i++)
    {
        if (!(readers[i] = fork()))
        {
            execl("./reader", "reader", (char *)0);//creates parallel processes of readers(10)
            return EXIT_FAILURE;
        }
    }
    
    for (int i = 0; i < LIMIT_WRITERS; i++)
    {
        if (!(writers[i] = fork()))
        {
            execl("./writer", "writer", (char *)0); //creates parallel processes of writers (5)
            return EXIT_FAILURE;
        }
    }
    sleep(20);//execution time of the program
    //to prevent infinite loop I have added sigkill
    for (int i = 0; i < LIMIT_READERS; i++)
    {
        kill(readers[i],SIGKILL);
    }
    for (int i = 0; i < LIMIT_WRITERS; i++)
    {
        kill(writers[i],SIGKILL);
    }
    sem_destroy(writer_named_semaphor);//destroy the semaphors
    sem_destroy(reader_named_semaphor);
    return EXIT_SUCCESS;
}
