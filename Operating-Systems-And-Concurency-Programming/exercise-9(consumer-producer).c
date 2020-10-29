#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <semaphore.h>
#include <unistd.h>

#define SUPPLY_LIMIT 20

struct args_struct{
    pthread_mutex_t mutex;
    sem_t empty;
    sem_t full;
    int index_in;
    int index_out;
    pthread_t producer_thread[10];
    pthread_t consumer_thread[10];
    char supply_Buffer[SUPPLY_LIMIT];
};

void * consumer_function(void* arguments){
    struct args_struct * args = (struct args_struct *) arguments;
    while(1){
        int produced;
        sem_wait(&(args->full));
        pthread_mutex_lock(&(args->mutex));
        produced = args -> supply_Buffer[args -> index_out];
        printf("Apparently a consumer has just eaten an item: %d from index: %d\n",produced, args -> index_out);
        sleep(1);
        args -> index_out = (args -> index_out+1)%SUPPLY_LIMIT;
        pthread_mutex_unlock(& (args -> mutex));
        sem_post(& (args -> empty));
    }
}

void * producer_function(void* arguments){
    struct args_struct * args = (struct args_struct *) arguments;
    while(1){
        int produced = rand()%50;
        sem_wait(&args->empty);
        pthread_mutex_lock(&args->mutex);
        args->supply_Buffer[args->index_in] = produced;
        printf("Okey, let us produce something new... maybe: %d at index: %d\n",produced,args->index_in);
        sleep(1);
        args->index_in = (args->index_in+1)%SUPPLY_LIMIT;
        pthread_mutex_unlock(&args->mutex);
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

    for(int a=0;a<10;a++){
    pthread_create(&args.producer_thread[a], NULL, producer_function, (void*)&args);
    }
    for(int a=0;a<10;a++){
    pthread_create(&args.consumer_thread[a], NULL, consumer_function, (void*)&args);
    }
    for(int a=0;a<10;a++){
    pthread_join(args.producer_thread[a],NULL);
    }
    for(int a=0;a<10;a++){
    pthread_join(args.consumer_thread[a],NULL);
    }
    pthread_mutex_destroy(&args.mutex);
    sem_destroy(&args.empty);
    sem_destroy(&args.full);
    return 0;
}
