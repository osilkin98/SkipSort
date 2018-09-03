from sys import maxsize
from random import randint
from typing import List, Any, Union


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

    def __init__(self, probability_base=2, max_tower_height=32):
        """ Skiplist Constructor

        :param int probability_base: Number Base to use when calculating the probability of an inserted data member
         has of scaling in height. In short, this is the parameter that determines the base of the logarithm for
         its insertion and lookup times.
        :param int max_tower_height: The max. number of towers this skiplist can create
        """

        self.probability_base = probability_base
        self.max_tower_height = max_tower_height

        self.head = self.SNode(-maxsize - 1, max_tower_height)

        # This is the actual height value
        self.height = 1

        self.total = 0

    def search(self, key):
        """ Search within the Skiplist for the given key, and return the closest value less than or equal
         to the key which was specified to search for.

        :param int key: Value to search for within the Skiplist
        :return: Closest value less than or equal to the `key` parameter
        :rtype: int
        """
        search_node = self.head.next[self.height - 1]

        for level in range(self.height - 1, -1, -1):

            while search_node.next[level] is not None and search_node.next[level].value <= key:
                search_node = search_node.next[level]

        return search_node.value

    @staticmethod
    def chooseHeight(probability_base=2, max_height=32):
        """ Choose a height according to a geometric distribution

        :param int probability_base: The Probability base used in the computation `rand() <= 1/(b^n)`. 2 By Default.
        :param int max_height: The Maximum Height to calculate up to. 32 By Default
        :return: The Calculated Height h such that 1 <= h <= max_height
        :rtype: int
        """
        level = 1
        while level < max_height and randint(1, probability_base) == 0:
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
        random_height = randint()