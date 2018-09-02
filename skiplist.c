#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <time.h>

#include "skiplist.h"

#define MAX_HEIGHT (32)
#define BASE_LEVEL 0

/*
 * Most of skiplist.c and skiplist.h was not written by me but was taken from
 * http://www.cs.yale.edu/homes/aspnes/classes/223/examples/trees/skiplist
 *
 * I've made modifications, to the code, mostly in the form of comments
 * Both of these files lack in terms of documentation, so I've set out to fix that where needed
 * */

/* choose a height according to a geometric distribution */
static int
chooseHeight(void)
{
    int i;

    for(i = 1; i < MAX_HEIGHT && rand() % 2 == 0; i++);

    return i;
}

/*** DEFINITION OF SKIPLIST STRUCT ***/
/*
struct skiplist {
    int key;
    int count;
    int height;                // number of next pointers
    struct skiplist *next[1];  // first of many
}; */

/* create a skiplist node with the given key and height */
/* does not fill in next pointers */
static Skiplist
skiplistCreateNode(int key, int height)
{

    Skiplist s;

    assert(height > 0);
    assert(height <= MAX_HEIGHT);

    /* we allocate space for the amount of space needed for one skiplist node object,
     * that being the key, height and count integers 3*(4Bytes), plus the array of struct skiplist pointers,
     * with one already insantiated. We also allocate space for the remaining uninstantiated pointers,
     * represented as (height - 1) skiplist pointers. */
    size_t memory_usage = sizeof(struct skiplist) + sizeof(struct skiplist *) * (height - 1);

    printf("Using %lu bits of memory to create a new skiplist node\n", memory_usage);

    s = malloc(memory_usage);

    assert(s);

    printf("Initialized a new skiplist node at %p\n\n", s);

    s->key = key;
    s->count = 1;
    s->height = height;

    return s;
}

/* create an empty skiplist */
Skiplist
skiplistCreate(void)
{
    srand((unsigned)time(0));

    Skiplist s;
    int i;

    /* s is a dummy head element */
    s = skiplistCreateNode(INT_MIN, MAX_HEIGHT);

    /* this tracks the maximum height of any node.
     *
     * Although we allocated enough space for 32 pointers,
     * we set the height to 1 because we want to keep track of the
     * maximum current tower height, not the capacity. */
    s->height = 1;

    /* NULL out all the pointers that were allocated with malloc*/
    for(i = 0; i < MAX_HEIGHT; i++) {
        s->next[i] = NULL;
    }
    return s;
}

/* free a skiplist */
void
skiplistDestroy(Skiplist s)
{
    Skiplist next;

    while(s) {
        next = s->next[0];
        free(s);
        s = next;
    }
}



/**
 *
 * @param s Skiplist object to print out
 */
void skiplistPrint(Skiplist s) {

    register int level;
    Skiplist iter;

    for(level = s -> height -1; level >= 0; --level) {
        iter = s;
        printf("%d: ", level);
        while(iter -> next[level]) {
            iter = iter -> next[level];
            printf("%d ", iter -> key);
        }
        printf("\n");
    }
}

/* return maximum key less than or equal to key */
/* or INT_MIN if there is none */
int
skiplistSearch(Skiplist s, int key, bool increment)
{
    register int level;

    /* start at the top level */
    for(level = s->height - 1; level >= 0; level--) {
        /* while the next node is non-null, and the node's key
         * is less than the key we're searching for */
        while(s->next[level] && s->next[level]->key <= key) {
            s = s->next[level];
        }
    }

    if(key == s->key && increment) {
        s->count++;
    }

    return s->key;
}

/* insert a new key into s */
void
skiplistInsert(Skiplist s, int key)
{
    register int level;
    Skiplist elt;

    /* creates a new skiplist struct object with a randomized height
     * determined by the function chooseHeight() at function call */
    elt = skiplistCreateNode(key, chooseHeight());

    /* ensure that the node was created successfully */
    assert(elt);

    if(elt->height > s->height) {
        s->height = elt->height;
    }

    /* search through levels taller than elt */
    for(level = s->height - 1; level >= elt->height; level--) {
        while(s->next[level] && s->next[level]->key < key) {
            s = s->next[level];
        }
    }

    /* now level is elt->height - 1, we can start inserting */
    for(; level >= 0; level--) {
        /* finds the node with a value immediately less than that of the key we're entering */
        while(s->next[level] && s->next[level]->key < key) {
            s = s->next[level];
        }

        /* s is last entry on this level < new element */
        /* do list insert */
        elt->next[level] = s->next[level];
        s->next[level] = elt;
    }
}

/* delete a key from s */
void
skiplistDelete(Skiplist s, int key)
{
    int level;
    Skiplist target;

    /* first we have to find leftmost instance of key */
    target = s;

    for(level = s->height - 1; level >= 0; level--) {
        while(target->next[level] && target->next[level]->key < key) {
            target = target->next[level];
        }
    }

    /* take one extra step at bottom */
    target = target->next[0];

    if(target == 0 || target->key != key) {
        return;
    }

    /* now we found target, splice it out */
    for(level = s->height - 1; level >= 0; level--) {
        while(s->next[level] && s->next[level]->key < key) {
            s = s->next[level];
        }

        if(s->next[level] == target) {
            s->next[level] = target->next[level];
        }
    }

    free(target);
}

int skiplistSafeInsert(Skiplist s, int key) {

    Skiplist toInsert;
    int steps = 0, insertionHeight = chooseHeight(), level;

    /* Check to see if the fist value is null, IE empty list */
    if(!s->next[BASE_LEVEL]) {
        /* create the node which we will insert */
        toInsert = skiplistCreateNode(key, insertionHeight);
        s->height=insertionHeight;

        steps += 1;

        for(; insertionHeight >= 0; --insertionHeight) {
            toInsert->next[insertionHeight] = s->next[insertionHeight];
            s->next[insertionHeight] = toInsert;
            steps += 1;
        }
        return steps;
    }

    /* Now we know that we need to either SEARCH and either INCREMENT or INSERT
     * for this, we'll create a randomized insertion height at which we will
     * theoretically insert the element in. We will conduct a search exactly
     * like when searching through for the insertion point in the insert function,
     * except we will use the <= operator instead of < in the case that we DO
     * find the key value, we can just simply increment it and return the number of
     * steps performed
     * */

    for(level = s->height -1; level >= insertionHeight; --level) {
        while(s->next[level] && /* the next element is non-NULL*/
              s->next[level]->key <= key) /* and its key is less than OR EQUAL to ours*/
        {

        }
    }

}