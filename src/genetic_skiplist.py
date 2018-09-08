from sorting_algorithms import skipSort
from sys import maxsize
from timeit import timeit
from random import randint
import numpy as np

def skipsort_test(base=2, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    skipSort(data, base)
    data.clear()


def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, n=100, trials=10, start=2, stop=8, increment=1.0):

    data = []
    base = start
    while base <= stop:
        print("Running "+str(trials)+" trials for skipsort with a probability base of Pb = " +str(base) +
              ", on a dataset of N=" +str(n) + "\nwith randomized datasets generated between a = "+
              str(a)+" and b = "+str(b))

        base_time = timeit(stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b), number=trials,
                           setup="from __main__ import skipsort_test")

        # x: base, y: time taken to sort data using probability base b
        data.append([base, base_time])

        print("Time taken: " + str(base_time) + " secs\n")

        base += increment

    return np.array(data)

if __name__ == '__main__':
    data = sort_with_ranged_bases(a=0, b=7, n=65, trials=1000, start=1, stop=4, increment=0.01)