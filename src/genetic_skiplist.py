from sorting_algorithms import skipSort
from sys import maxsize
from timeit import timeit
from random import randint


def skipsort_test(base=2, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    skipSort(data, base)
    data.clear()


def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, n=100, trials=10, start=2, stop=8, increment=1):

    base = start
    while base <= stop:
        print("Running "+str(trials)+" trials for skipsort with a probability base of Pb = " +str(base) +
              ", on a dataset of N=" +str(n) + "\nwith randomized datasets generated between a = "+
              str(a)+" and b = "+str(b))

        base_time = timeit(stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b), number=trials,
                           setup="from __main__ import skipsort_test")

        print("Time taken: " + str(base_time) + " secs")

        base += increment


if __name__ == 'main':
    sort_with_ranged_bases()
