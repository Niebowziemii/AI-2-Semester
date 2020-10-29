#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <semaphore.h>
#include <unistd.h>

#define SUPPLY_LIMIT 100

struct args_struct{
    sem_t empty;
    sem_t full;
    int index_in;
    int index_out;
    pthread_t producer_thread;
    pthread_t consumer_thread;
    char supply_Buffer[SUPPLY_LIMIT];
};

void * consumer_function(void* arguments){
    struct args_struct * args = (struct args_struct *) arguments;
    for(int i=0;i<SUPPLY_LIMIT*2;i++){
        sem_wait(&(args->full));
        int produced = i+50;
        produced = args -> supply_Buffer[args -> index_out];
        printf("Apparently a consumer has just eaten an item: %d from index: %d\n",produced, args -> index_out);
        sleep(1);
        args -> index_out = (args -> index_out+1)%SUPPLY_LIMIT;
        sem_post(& (args -> empty));
    }
}

void * producer_function(void* arguments){
    struct args_struct * args = (struct args_struct *) arguments;
    for(int i=0;i<SUPPLY_LIMIT*2;i++){
        sem_wait(&args->empty);
        int produced = i+50;
        args->supply_Buffer[args->index_in] = produced;
        printf("Okey, let us produce something new... maybe: %d at index: %d\n",produced,args->index_in);
        sleep(1);
        args->index_in = (args->index_in+1)%SUPPLY_LIMIT;
        sem_post(&args->full);
    }
}

int main(){
    srand(time(NULL));

    struct args_struct args;
    args.index_in=0;
    args.index_out=0;
    sem_init(&args.empty,0,SUPPLY_LIMIT);
    sem_init(&args.full,0,0);

    pthread_create(&args.producer_thread, NULL, producer_function, (void*)&args);
    pthread_create(&args.consumer_thread, NULL, consumer_function, (void*)&args);

    pthread_join(args.producer_thread,NULL);
    pthread_join(args.consumer_thread,NULL);

    sem_destroy(&args.empty);
    sem_destroy(&args.full);
    return 0;
}
