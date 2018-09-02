//
// Created by oleg on 9/1/18.
//

#include <stddef.h>
#include <stdlib.h>
#include "fastsort.h"
#include "skiplist.h"


/* sorts the data */
void sortData(int *data, int N) {

    Skiplist slist = skiplistCreate();

    /* Go through the entire dataset */
    for(register int i = 0; i < N; ++i) {

        /* if the data member is already inside the skiplist, it'll be incremented
         * automatically. Otherwise, a separate insertion routine is called */
        if(skiplistSearch(slist, data[i], 1) != data[i]) {
            /* I don't like this separation between the search function
             * and the insertion function*/
            skiplistInsert(slist, data[i]);
        }
    }

    /* k is the running index of the entire data loop, which goes from 0 to N-1
     * i is the index which we use to actually access the data array and we use
     * i to loop from k to k + d, where d is the duplicate count of a single member
     */
    int k = 0, i = 0;
    /* here we set the pointer from the head to the first element pointer
     * and we proceed to check whether or not slist is NULL. If slist is NULL,
     * we have arrived at the end of the list, and the entire data array is re-populated
     * */
    while((slist = slist->next[0]) != NULL) {

        for(i = k; i < k+slist -> count; ++i) {
            data[i] = slist->key;
        }

        k=i;
    }
    /* destroy the skiplist */
    skiplistDestroy(slist);
}

int skipSortOptimized(int *data, int N) {
    Skiplist slist = skiplistCreate();

    register int i;

    int total_steps = 0;
    /* go through the dataset */
    for(i = 0; i < N; ++i) {
        /* insert/increment the data member at data[i] within the skiplist*/
        total_steps += skiplistSafeInsert(slist, data[i]);

    }

    /* try and put k on the register */
    register int k = 0;
    while((slist = slist->next[0]) != NULL) {

        /* put the value from the skiplist back into the data array, list->count times*/
        for(i = k; i < k+slist->count; ++i){
            data[i] = slist->key;
        }
        k = i;
    }

    /* Destroy the skiplist */
    skiplistDestroy(slist);

    /* N total steps performed during the last while loop */
    return total_steps + N;
}