//
// Created by oleg on 9/1/18.
//

#include <stddef.h>
#include <stdlib.h>
#include "fastsort.h"
#include "skiplist.h"


int* sortData(int *data) {
    Skiplist slist = skiplistCreate();

    for(register int i = 0; i < N; ++i) {
        if(skiplistSearch(slist, data[i], 1) != data[i]) {
            skiplistInsert(slist, data[i]);
        }
    }

    int k = 0, i = 0;
    while((slist = slist->next[0]) != NULL) {

        for(i = k; i < k+slist -> count; ++i) {
            data[i] = slist->key;
        }

        k=i;
    }

    skiplistDestroy(slist);
}