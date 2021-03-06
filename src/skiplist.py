from sys import maxsize
import random
from math import ceil


class Skiplist(object):

    class SNode(object):

        def __init__(self, key, height):
            """

            :param int key: Number to store inside the current node
            :param int height: This is the height of the node which we will create
            """
            self.value = key  # Set the key
            self.count = 1  # Set the current count
            self.height = height    # Set the maximum height, this value should be determined outside

            # If we don't have a previous node, then this is the first Node to be inserted
            self.next = [None] * self.height


    ''' Skiplist diagram:
    4 NIL ---------------------------------------------------------------> NIL
    
    3 NIL -------------------------------> 10 ---------------------------> NIL
    
    2 NIL ----------> 5 -----------------> 10 -------------------> 23 ---> NIL
    
    1 NIL ----------> 5 ----------> 7 ---> 10 -----------> 23 ---> 25 ---> NIL
                      
    0 NIL ---> 3 ---> 5 ---> 6 ---> 7 ---> 10 ---> 17 ---> 23 ---> 25 ---> NIL
    
    '''

    def __init__(self, probability_base=2, max_tower_height=None):
        """ Skiplist Constructor

        :param int | float probability_base: Number Base to use when calculating
         the probability of an inserted data member has of scaling in height. In short, this is the parameter
         that determines the base of the logarithm for its insertion and lookup times.
         It is denoted by `b`.
        :param int max_tower_height: The max. number of towers this Skiplist can create. If None is provided,
         the default value used will be `int(math.ceil( b^5 ))` where `b` is the probability base specified
         in the first parameter.
        """
        random.seed()

        self.probability_base = probability_base
        self.max_tower_height = max_tower_height if max_tower_height is not None else int(ceil(probability_base ** 5))

        self.head = self.SNode(-maxsize - 1, self.max_tower_height)

        # This is the actual height value
        self.height = 1

        self.total = 0

        self.prehash = dict()

    def search(self, key):
        """ Search within the Skiplist for the given key, and return the closest value less than or equal
         to the key which was specified to search for.

        :param int key: Value to search for within the Skiplist
        :return: Closest value less than or equal to the `key` parameter
        :rtype: int
        """
        if key in self.prehash:
            return key

        search_node = self.head.next[self.height - 1]

        for level in range(self.height - 1, -1, -1):

            while search_node.next[level] is not None and search_node.next[level].value < key:
                search_node = search_node.next[level]

        return search_node.value

    @staticmethod
    def chooseHeight(probability_base=2, max_height=32):
        """ Choose a height according to a geometric distribution

        :param float probability_base: The Probability base used in the computation `rand() <= 1/(b^n)`. 2 By Default.
        :param int max_height: The Maximum Height to calculate up to. 32 By Default
        :return: The Calculated Height h such that 1 <= h <= max_height
        :rtype: int
        """
        level = 1
        while level < max_height and random.random() <= (1/(probability_base ** level)):
            level += 1

        return level

    ''' Skiplist diagram:
    4 NIL ---------------------------------------------------------------> NIL

    3 NIL -------------------------------> 10 ---------------------------> NIL

    2 NIL ----------> 5 -----------------> 10 -------------------> 23 ---> NIL

    1 NIL ----------> 5 ----------> 7 ---> 10 -----------> 23 ---> 25 ---> NIL

    0 NIL ---> 3 ---> 5 ---> 6 ---> 7 ---> 10 ---> 17 ---> 23 ---> 25 ---> NIL
    '''

    def insert(self, key):
        """ Inserts the given key into the skiplist, if it already isn't in it. If the key already
         exists, increment its value.

        :param int key: Key to insert into the skiplist
        :returns: Nothing
        :rtype: None
        """
        if key in self.prehash:

            # Increment the count and return
            self.prehash[key].count += 1
            return

        random_height = self.chooseHeight(self.probability_base, self.max_tower_height)

        current_node = self.head

        level = self.height - 1

        # This will start from the tower height index and go until the random_height index (random height-1) is reached
        # If self.height < random_height, this loop won't run, but if random_height > self.height, then we have
        # No searching to do
        while level >= random_height - 1:

            # While the next node in the current node list isn't null and its value is less than or equal to
            # The key that we were given, move current_node to be the next node
            while current_node.next[level] is not None and current_node.next[level].value < key:
                current_node = current_node.next[level]

            level -= 1

        # level after this will be equal to random_height - 2, 1 below the proposed height,
        # However the current_node pointer will still be on index random_height -1, right
        # In front of the position it will begin inserting into

        # At this point the current_node pointer would point to the value right before
        # The one at which we need to insert. However since we're not sure if the value
        # Is already in the skiplist or not, we need to traverse deeper into the list to check whether or
        # not that's the case. We will do so by copying the state of current_node into a new variable
        '''
        lower_search = current_node

        # This starts the search below the random height index, since we already know the
        # Value we're looking for wasn't there
        while level >= 0:

            # Try to find the value
            while lower_search.next[level] is not None and lower_search.next[level].value <= key:
                lower_search = lower_search.next[level]

            if lower_search.value == key:

                # Increment and return
                lower_search.count += 1
                return

            level -= 1
        '''

        # At this point if we haven't found the value we're looking for already, we can give up and start inserting
        # We know that the level will be random_height - 2, while current_node is on random_height - 1
        # We need to insert the new node at random_height -1 and set its height to random_height

        # instantiate the new node to insert
        new_node = self.SNode(key, random_height)

        # Add the node to the hash table for quicker lookup
        self.prehash[new_node.value] = new_node

        self.height = new_node.height if new_node.height > self.height else self.height

        for level in range(new_node.height - 1, -1, -1):

            # Put the current node to before the insertion point, IE where the value is immediately before the key
            while current_node.next[level] is not None and current_node.next[level].value < new_node.value:
                current_node = current_node.next[level]

            # Perform list insertion
            new_node.next[level] = current_node.next[level]
            current_node.next[level] = new_node

        # Increment the total amount of elements we have
        self.total += 1

    # Method to print the linkedlist
    def print(self):
        """ Basic method to print the linkedlist

        :return:
        """
        iterate = self.head.next[0]

        s = ""
        while iterate is not None:
            s += str(iterate.value) + ", "
            iterate = iterate.next[0]

        print(s)

