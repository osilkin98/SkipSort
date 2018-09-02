#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include <stdio.h>

#include "skiplist.h"

#define MAX_HEIGHT (32)

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

/* create a skiplist node with the given key and height */
/* does not fill in next pointers */
static Skiplist
skiplistCreateNode(int key, int height)
{
    Skiplist s;

    assert(height > 0);
    assert(height <= MAX_HEIGHT);

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
    Skiplist s;
    int i;

    /* s is a dummy head element */
    s = skiplistCreateNode(INT_MIN, MAX_HEIGHT);

    /* this tracks the maximum height of any node */
    s->height = 1;

    for(i = 0; i < MAX_HEIGHT; i++) {
        s->next[i] = 0;
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