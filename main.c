#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "fastsort.h"
#include "skiplist.h"

#define N 20

#define printArray(data) for(int i = 0; i < N; ++i) { printf("%d ", data[i]);}

void printArrayFunc(int *data, int n) {

    for(register size_t i = 0; i < n; ++i) {
        printf("%d ", data[i]);
    }
    printf("\n");
}


int main(void) {

    /*
    int *data = malloc(sizeof(int) * N);

    for(int i = 0; i < N; ++i) {
        data[i] = rand() % 17;
        //printf("%d ", data[i]);
    }
    */


    /**sortData(data);**/

    /*
    printf("printArray macro: ");
    printArray(data)

    sortData(data, N);

    printArray(data);

    free(data);*/

    return 0;
}