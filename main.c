#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>
#include "fastsort.h"
#include "skiplist.h"

#define N 50

#define printArray(data) for(int i = 0; i < N; ++i) { printf("%d ", data[i]);}

void printArrayFunc(int *data, int n) {

    for(register size_t i = 0; i < n; ++i) {
        printf("%d ", data[i]);
    }
    printf("\n");
}


int* createRandomArray(int n, int mod) {
    srand((unsigned)time(0));
    int *array = malloc(sizeof(int) * n);

    while(array == NULL) {
        array = malloc(sizeof(int) * n);
    }

    for(register size_t i = 0; i < n; ++i) {
        array[i] = rand() % mod;
    }
    return array;
}

void randomizeArray(int *data, int n, int mod) {
    srand((unsigned)time(0));
    for(register size_t i = 0; i < n; ++i) {
        data[i] = rand() % mod;
    }
}

void copyArray(int *A, int *B, int n) {
    for(register size_t i = 0; i < n; ++i) {
        *B = *A;
    }
}

int* arrayCopy(int const *data, int n) {
    int *copy = malloc(sizeof(int)*n);

    while(copy == 0) {
        copy = malloc(sizeof(int)*n);
    }

    for(register size_t i = 0; i < n; ++i) {
        copy[i] = data[i];
    }

    return copy;
}


void compareSorts(int num_trials, int mod) {
    clock_t qstart, qdiff, sstart, sdiff;

    long bubble_msec_total = 0, skip_msec_total = 0;

    int *unsorted = createRandomArray(N, mod);
    int *unsorted_copy = arrayCopy(unsorted, N);

    for(int trial = 0; trial < num_trials; ++trial) {

        qstart = clock();
        bubbleSort(unsorted, N);

        qdiff = clock() - qstart;
        bubble_msec_total += (qdiff*1000 / CLOCKS_PER_SEC);

        sstart = clock();
        sortData(unsorted_copy, N);
        sdiff = clock() - sstart;

        skip_msec_total += (sdiff * 1000/ CLOCKS_PER_SEC);

        randomizeArray(unsorted, N, mod);
        copyArray(unsorted, unsorted_copy, N);
    }
    free(unsorted);
    free(unsorted_copy);
    printf("SkipSort Time: %ld seconds, %ld milliseconds\n", skip_msec_total/1000, skip_msec_total%1000);
    printf("BubbleSort Time: %ld seconds, %ld milliseconds\n", bubble_msec_total/1000, bubble_msec_total%1000);

    skip_msec_total /= num_trials;
    bubble_msec_total /= num_trials;

    printf("SkipSort Average: %ld seconds, %ld milliseconds\n", skip_msec_total/1000, skip_msec_total%1000);
    printf("BubbleSort Average: %ld seconds, %ld milliseconds\n", bubble_msec_total/1000, bubble_msec_total%1000);



}

#define REPEAT 10000
#define MOD 73

int main(void) {



    int *randomarray = createRandomArray(N, MOD);

    skipSortOptimized(randomarray, MOD);
    free(randomarray);

    return 0;
}