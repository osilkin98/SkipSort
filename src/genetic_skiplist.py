from sorting_algorithms import skipSort
from sys import maxsize
from timeit import timeit
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


# This is a wrapper for the standard test function exclusive to skipsort
def skipsort_test(base=2, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    skipSort(data, base)
    data.clear()


def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, lengths=None, trials=10, start=2.0, stop=8.0, increment=1.0):

    data = []
    base = start
    while base <= stop + increment:

        # Basic array
        length_times = [base]

        for n in lengths:
            print("Running " + str(trials) + " trials for skipsort with a probability base of Pb = " + str(base) +
                  ", on a dataset of N=" + str(n) + "\nwith randomized datasets generated between a = " +
                  str(a) + " and b = " + str(b))

            base_time = timeit(stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b), number=trials,
                               setup="from __main__ import skipsort_test")

            length_times.append(base_time)

            print("Time taken: " + str(base_time) + " secs\n")

        # x: base, [Y]: times taken to sort data using probability base b with variable data sizes
        data.append(length_times)

        base += increment

    return np.array(data)


def sort_with_ranged_data(a=-maxsize-1, b=maxsize, base=1.5, trials=100,
                          start=0, stop=1000, increment=10, type='linear'):

    data = []
    n = start if start > 0 else start + increment
    while n <= stop:
        print("Running "+str(trials)+" trials for skipsort with a probability base of Pb = " +str(base) +
              ", on a dataset of N=" + str(n) + "\nwith randomized datasets generated between a = "+
              str(a)+" and b = "+str(b) + ", with " + type + " incrementation")

        num_time = timeit("skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b),
                          number=trials, setup="from __main__ import skipsort_test")

        # x: number of elements, # y: time taken to sort data with number of elements x and probability base Pb
        data.append([n, num_time])

        print("Time taken: "+str(num_time)+" secs\n")

        n = n + increment if type.lower() == 'linear' else n * increment

    return np.array(data)


if __name__ == '__main__':
    a, b = 0, 2 ** 31
    n = [500, 750, 1000, 1250, 1500]

    trials = 100
    start, stop = 1, 8
    inc = 0.1

    fpath = "{}/data/datafileTrials{}Interval{}-{}Inc{}.txt".format(os.getcwd(),
                                                                           trials,
                                                                           str(stop).replace('.', ''),
                                                                           str(start).replace('.', ''),
                                                                           str(inc).replace('.', ''))

    if os.path.exists(fpath):
        data = np.loadtxt(fpath)

    else:
        data = sort_with_ranged_bases(a=a, b=b, lengths=n, trials=trials, start=start, stop=stop, increment=inc)

    # If the filepath doesn't exist
    if not os.path.exists("{}/data".format(os.getcwd())):
        # Make the directories
        os.makedirs("{}/data".format(os.getcwd()))
    try:
        # Try to save the data as a text file
        np.savetxt(fname="{}/data/datafileTrials{}Interval{}-{}Inc{}.txt".format(os.getcwd(),
                                                                           trials,
                                                                           str(stop).replace('.', ''),
                                                                           str(start).replace('.', ''),
                                                                           str(inc).replace('.', '')),
                   X=data)
    # If it failed to write the data to a text file, print it to stdout
    except Exception as e:
        print(e)
        for X in data:
            print(X)

    sorting_time_data = pd.DataFrame(data=data[:, 1:], index=data[:, 0], columns=["N="+str(i) for i in n])

    title = "Time Taken to Sort Data of Variable Probability Bases and Data Length,\n"+\
            "Running "+str(trials)+" Trials, and Generating Values on ["+str(a)+", "+str(b)+"]"

    plt.figure()

    plot = sorting_time_data.plot(
        title=title, x="Probability Bases", y="Seconds"
    )

    plt.show()



    '''
    a, b, n = 0, 2 ** 31, 1000
    trials = 100
    start, stop = 0, 10000
    inc = 5
    mode='Geometric'
    base=1.5

    data = sort_with_ranged_data(a=a, b=b, trials=trials, base=base, start=start, stop=stop, increment=inc, type=mode)

    sort_time_series = pd.Series(data=data[:, 1], index=data[:, 0])

    plot = sort_time_series.plot(
        title="Time Taken to Sort Random Datasets of Variable Length, \nWith Values Generated On [{}, {}]\
        \nUsing {} Increments With Probability Base Pb = {}".format(a, b, mode, base))

    plot.set_xlabel("Probability Bases")
    plot.set_ylabel("Time Taken (seconds)")

    plt.show()

    '''