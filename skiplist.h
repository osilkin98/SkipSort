struct skiplist {
    int key;
    int count;
    int height;                /* number of next pointers */
    struct skiplist *next[1];  /* first of many */
};

typedef struct skiplist * Skiplist;

typedef char bool;

/* create an empty skiplist */
Skiplist skiplistCreate(void);

/* destroy a skiplist */
void skiplistDestroy(Skiplist s);

/* return maximum key less than or equal to key */
/* or INT_MIN if there is none */
int skiplistSearch(Skiplist s, int key, bool increment);

/* insert a new key into s */
void skiplistInsert(Skiplist s, int key);

/* delete a key from s */
void skiplistDelete(Skiplist s, int key);

/* print out the contents of s in a tower-like form */
void skiplistPrint(Skiplist s);

/* */
/** Increment the node with value key if found, otherwise insert if not found
 *
 * @param s Skiplist header node to be operated on
 * @param key Value of the key to be inserted or incremented
 * @return The number of steps performed in total
 */
int skiplistSafeInsert(Skiplist s, int key);
