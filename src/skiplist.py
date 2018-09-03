from sys import maxsize
from random import randint


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
        random_height = self.chooseHeight(self.probability_base, self.max_tower_height)

        current_node = self.head

        level = self.height - 1

        # This will start from the tower height index and go until the random_height index (random height-1) is reached
        # If self.height < random_height, this loop won't run, but if random_height > self.height, then we have
        # No searching to do
        while level >= random_height - 1:

            # While the next node in the current node list isn't null and its value is less than or equal to
            # The key that we were given, move current_node to be the next node
            while current_node.next[level] is not None and current_node.next[level].value <= key:
                current_node = current_node.next[level]

            # If this is the key, just increment and return
            if current_node.value == key:
                # Increment and return
                current_node.count += 1
                return

            level -= 1

        # level after this will be equal to random_height - 2, 1 below the proposed height,
        # However the current_node pointer will still be on index random_height -1, right
        # In front of the position it will begin inserting into

        # At this point the current_node pointer would point to the value right before
        # The one at which we need to insert. However since we're not sure if the value
        # Is already in the skiplist or not, we need to traverse deeper into the list to check whether or
        # not that's the case. We will do so by copying the state of current_node into a new variable

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

        # At this point if we haven't found the value we're looking for already, we can give up and start inserting
        # We know that the level will be random_height - 2, while current_node is on random_height - 1
        # We need to insert the new node at random_height -1 and set its height to random_height

        # instantiate the new node to insert
        new_node = self.SNode(key, random_height)

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


# For testing the algorithm
def bubbleSort(data):
    for passnum in range(len(data) - 1, 0, -1):
        for i in range(passnum):
            if data[i] > data[i + 1]:
                temp = data[i]
                data[i] = data[i + 1]
                data[i + 1] = temp


# skipsort algorithm implementation in python
def skipSort(data: list):
    slist = Skiplist()
    while len(data) != 0:
        slist.insert(data.pop(0))

    head = slist.head.next[0]
    while head is not None:
        data += [head.value] * head.count
        head = head.next[0]


def quickSort(x):
    if len(x) == 1 or len(x) == 0:
        return x
    else:
        pivot = x[0]
        i = 0
        for j in range(len(x)-1):
            if x[j+1] < pivot:
                x[j+1],x[i+1] = x[i+1], x[j+1]
                i += 1
        x[0],x[i] = x[i],x[0]
        first_part = quickSort(x[:i])
        second_part = quickSort(x[i+1:])
        first_part.append(x[i])
        return first_part + second_part



def test(sort, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    sort(data)
    data.clear()


def stlSort(data: list):
    data.sort()


if __name__ == '__main__':
    # slist = Skiplist()

    N = 20000
    a, b = 0, 50

    print("Using N={} with randomized datasets generated between a = {} and b = {}".format(N, a, b))

    import timeit

    skip_time = timeit.timeit("test(skipSort, N={}, a={}, b={})".format(N, a, b),
                              number=100, setup="from __main__ import test, skipSort")
    print("Skipsort Time: {}secs".format(skip_time))

    quickTime = timeit.timeit("test(quickSort, N={}, a={}, b={})".format(N, a, b),
                              number=100, setup="from __main__ import test, quickSort")

    print("Quick Sort Time: {}secs".format(quickTime))

    stltime = timeit.timeit("test(stlSort, N={}, a={}, b={})".format(N, a, b),
                            number=100, setup="from __main__ import test, stlSort")

    print("Timsort Time: {}secs".format(stltime))

    '''
    bubble_time = timeit.timeit("test(bubbleSort, N={}, a={}, b={})".format(N, a, b),
                                number=100, setup="from __main__ import test, bubbleSort")

    print("Bubble Time: {}secs".format(bubble_time))
    '''
    # slist.print()