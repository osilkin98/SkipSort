from sys import maxsize
from typing import List, Any, Union


class Skiplist(object):

    class SNode(object):

        def __init__(self, key, height, prev_node=None):
            """

            :param int key: Number to store inside the current node
            :param int height: This is the height of the node which we will create
            :param SNode prev_node: Previous Node object that instantiated
            """
            self.value = key  # Set the key
            self.count = 1  # Set the current count
            self.height = height    # Set the maximum height, this value should be determined outside

            # If we don't have a previous node, then this is the first Node to be inserted
            if prev_node is None:

                # Height of all entry towers, filled with null pointers
                self.next = [None] * self.height

            else:

                self.next = [None] * self.height

                traversal_node = prev_node

                for level in range(self.height - 1, -1, -1):

                    # Positions the traversal node to be the node just before the current one in value
                    while traversal_node.next[level] is not None and traversal_node.next[level].value < self.value:
                        traversal_node = traversal_node.next[level]

                    # Now the traversal_node is in a position where it's right before the current
                    # node in terms of key value, and we can just do a linked list insertion
                    self.next[level] = traversal_node.next[level]
                    traversal_node.next[level] = self


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


