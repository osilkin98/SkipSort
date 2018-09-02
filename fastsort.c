//
// Created by oleg on 9/1/18.
//

#include <stddef.h>
#include <stdlib.h>
#include "fastsort.h"
#include "skiplist.h"


int* sortData(int *data) {
    Skiplist slist = skiplistCreate();

    register int i, *iterdata = data;
    /* iterate through the data once and put the # of occurrences
     * for each number within the dataset into the skip list*/
    while((i = *iterdata++) != 0) {
        /* if the value returned is not the key, then it'll be inserted
         * if it is the key then the number has already been incremented*/
        if(skiplistSearch(slist, i, 1) != i) {
            skiplistInsert(slist, i);
        }
    }

    while((slist = slist->next[0]) != NULL) {
        for(i = 0; i < slist -> count; ++i) {
            *data++ = slist -> key;
        }
    }

    skiplistDestroy(slist);
}