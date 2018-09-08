from sorting_algorithms import skipSort
from sys import maxsize
from timeit import timeit
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# This is a wrapper for the standard test function exclusive to skipsort
def skipsort_test(base=2, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    skipSort(data, base)
    data.clear()


def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, n=100, trials=10, start=2.0, stop=8.0, increment=1.0):

    data = []
    base = start
    while base <= stop + increment:
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

    a, b, n = 0, maxsize, 10000
    trials = 10
    start, stop = 0.1, 8.0
    inc = 0.1

    data = sort_with_ranged_bases(a=a, b=b, n=n, trials=trials, start=start, stop=stop, increment=inc)

    sort_time_series = pd.Series(data=data[:, 1], index=data[:, 0])

    plot = sort_time_series.plot(
        title="Time Taken to Sort {} Members Generated on [{}, {}], {} times".format(n, a, b, trials))

    plot.set_xlabel("Probability Bases")
    plot.set_ylabel("Time Taken (seconds)")

    plt.show()