#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#define LIMIT 10

unsigned int thread_number;
pthread_mutex_t mutex;
pthread_cond_t cond_var;

struct args_struct{
    int time;
    int index;
};


void * barrier(void* arguments){
    struct args_struct * args = (struct args_struct*) arguments;
    pthread_mutex_lock(& mutex);
    printf("(barrier) Fan %d entered mutex\n",args->index);
     thread_number++;
    if( thread_number == LIMIT){
        printf("(barrier) broadcasting\n");
        pthread_cond_broadcast(& cond_var);
    }
    else{
        while( thread_number!=LIMIT){
            printf("(barrier) waiting\n");
            pthread_cond_wait(& cond_var,& mutex);
        }
    }
    printf("(barrier) Fan %d exited mutex\n",args->index);
    pthread_mutex_unlock(& mutex);
}

void* depeche_mode_fan (void* arguments){
    struct args_struct * args = (struct args_struct*) arguments;
    printf("(func) Depeche mode fan number %d is going to a concert. He will approach the destination place in %d seconds.\n",  args -> index,args->time );
    sleep( args->time);
    barrier(args);
    printf("(func) Now fan number %d arrived\n",args->index);
}

int main(){
    srand(time(NULL));
    printf("(main) Initializing variables...\n");
    struct args_struct args[10];
    thread_number = 0;
    pthread_mutex_init(&mutex,NULL);
    pthread_cond_init(&cond_var,NULL);
    printf("(main) Creating threads...\n");
    pthread_t threads[LIMIT];
    for(unsigned int i =0;i<LIMIT;i++){
        args[i].index = i;
        args[i].time = (rand() % 10) + 1;
        pthread_create(&threads[i],NULL,depeche_mode_fan,(void*) &args[i]);
    }
    printf("(main) Joining threads...\n");
    for(unsigned int i = 0;i< LIMIT;i++){
        pthread_join(threads[i],NULL);
    }
    printf("(main) Let us go to the concert.\n");
    printf("(main) End of main function.\n");
    return 0;
}
