typedef struct skiplist * Skiplist;


/* create an empty skiplist */
Skiplist skiplistCreate(void);

/* destroy a skiplist */
void skiplistDestroy(Skiplist s);

/* return maximum key less than or equal to key */
/* or INT_MIN if there is none */
int skiplistSearch(Skiplist s, int key);

/* insert a new key into s */
void skiplistInsert(Skiplist s, int key);

/* delete a key from s */
void skiplistDelete(Skiplist s, int key);