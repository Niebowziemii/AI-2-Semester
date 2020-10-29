#include <stdlib.h>
#include <pthread.h>

#define SMALL_SIZE 20
#define LARGE_SIZE 1000

struct Small_Queue_Struct
{
    int front, rear, count;
    pthread_mutex_t mutex;
    int buffer[SMALL_SIZE];
};

struct Large_Queue_Struct
{
    int front_l, rear_l, count_l;
    pthread_mutex_t mutex_l;
    int buffer_l[LARGE_SIZE];
};

void initQueueSmall(struct Small_Queue_Struct *q)
{
    q->front = 0;
    q->rear = -1;
    q->count = 0;
    pthread_mutex_init(&(q->mutex), NULL);
}
void initQueueLarge(struct Large_Queue_Struct *q)
{
    q->front_l = 0;
    q->rear_l = -1;
    q->count_l = 0;
    pthread_mutex_init(&q->mutex_l, NULL);
}
int isFullSmall(struct Small_Queue_Struct *q)
{
    if (q->count == SMALL_SIZE)
    {
        return -1;
    }
    return 0;
}
int isFullLarge(struct Large_Queue_Struct *q)
{
    if (q->count_l == LARGE_SIZE)
    {
        return -1;
    }
    return 0;
}
int isEmptySmall(struct Small_Queue_Struct *q)
{
    if (q->count == 0)
    {
        return -1;
    }
    return 0;
}
int isEmptyLarge(struct Large_Queue_Struct *q)
{
    if (q->count_l == 0)
    {
        return -1;
    }
    return 0;
}
void pushSmall(struct Small_Queue_Struct *q, int item)
{
    pthread_mutex_lock(&(q->mutex));
    if (isFullSmall(q))
    {
        fprintf(stderr, "Queue Overflow \n");
        return;
    }
    q->rear = (q->rear + 1) % SMALL_SIZE;
    q->buffer[q->rear] = item;
    q->count++;
    pthread_mutex_unlock(&(q->mutex));
}
void pushLarge(struct Large_Queue_Struct *q, int item)
{
    pthread_mutex_lock(&(q->mutex_l));
    if (isFullLarge(q))
    {
        fprintf(stderr, "Queue Overflow \n");
        return;
    }
    q->rear_l = (q->rear_l + 1) % LARGE_SIZE;
    q->buffer_l[q->rear_l] = item;
    q->count_l++;
    pthread_mutex_unlock(&(q->mutex_l));
}
int popSmall(struct Small_Queue_Struct *q)
{
    pthread_mutex_lock(&(q->mutex));
    if (isEmptySmall(q))
    {
        fprintf(stderr, "Queue Underflow\n");
        return -1;
    }
    int item = q->buffer[q->front];
    q->front = (q->front + 1) % SMALL_SIZE;
    q->count--;
    pthread_mutex_unlock(&(q->mutex));
    return item;
}
int popLarge(struct Large_Queue_Struct *q)
{
    pthread_mutex_lock(&(q->mutex_l));
    if (isEmptyLarge(q))
    {
        fprintf(stderr, "Queue Underflow\n");
        return -1;
    }
    int item = q->buffer_l[q->front_l];
    q->front_l = (q->front_l + 1) % LARGE_SIZE;
    q->count_l--;
    pthread_mutex_unlock(&(q->mutex_l));
    return item;
}
