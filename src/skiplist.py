

class Skiplist(object):

    def __init__(self, probability_base = 2, max_tower_height = 32):
        """ Skiplist Constructor

        :param int probability_base: Number Base to use when calculating the probability of an inserted data member
         has of scaling in height. In short, this is the parameter that determines the base of the logarithm for
         its insertion and lookup times.
        :param int max_tower_height: The max. number of towers this skiplist can create
        """

        self.probability_base = probability_base
        self.max_tower_height = max_tower_height