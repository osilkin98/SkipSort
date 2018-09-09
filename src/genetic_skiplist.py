from sorting_algorithms import skipSort
from sys import maxsize
from timeit import timeit
from random import randint
import numpy as np
from time import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import threading
import colorama.ansi
from colorama import Fore


# This increments the value of the color given as a code
def increment_color(color_code: str):
    return colorama.ansi.CSI + str((int(color_code.rstrip('m').lstrip(colorama.ansi.CSI).rstrip('m')) + 1) % 108) + 'm'


# This is a wrapper for the standard test function exclusive to skipsort
def skipsort_test(base=2, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    skipSort(data, base)
    data.clear()


def sort_and_add(times_list: list, index, base, n, a, b, trials, quiet=False):

    if not quiet:
        print("{}Trials{} = {}\n{}Pb{} = {}\n{}N{} = {}\n{}Interval{} = [{}{}{}, {}{}{}]\n\n".format(
            Fore.CYAN, Fore.RESET, trials,             # For the trials
            Fore.LIGHTMAGENTA_EX, Fore.RESET, base,    # For the Probability Base
            Fore.BLUE, Fore.RESET, n,                  # For the Total Count
            Fore.LIGHTBLUE_EX, Fore.RESET,             # For the interval display
            Fore.GREEN, a, Fore.RESET,                 # For the lower bound
            Fore.RED, b, Fore.RESET))                  # For the upper bound

    times_list[index] = timeit(stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b),
                               number=trials, setup="from __main__ import skipsort_test")

    if not quiet:
        print("{}[SORTING DONE]{} Time taken for Thread {}: {}{:.5f}{} secs".format(Fore.RED, Fore.RESET,
                                                                                    index-1, Fore.GREEN,
                                                                                    times_list[index],
                                                                                    Fore.RESET))


# Single threaded function to test sorting with varied bases
def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, lengths: list=None, trials=10,
                           start=2.0, stop=8.0, increment=1.0, quiet=False):

    data = []
    base = start
    lengths_length, total_time = len(lengths), 0
    while base <= stop + increment:

        # Basic array
        length_times = [base] + [0] * lengths_length

        if not quiet:
            print("{}Testing Base {}{}\n".format(Fore.LIGHTRED_EX, Fore.RESET, str(base).rstrip('0')))

            current_color = Fore.LIGHTRED_EX

        for i, n in enumerate(lengths):
            base_time = timeit(stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b), number=trials,
                               setup="from __main__ import skipsort_test")
            # Add to list
            length_times[i+1] = base_time

            if not quiet:
                # Add to total time
                total_time += base_time

                print("{}[N={}]{} Time taken: {}{:.5f}{} secs\n".format(current_color,
                                                                        n, Fore.RESET, Fore.GREEN,
                                                                        base_time, Fore.RESET))

            current_color = increment_color(current_color)

        # x: base, [Y]: times taken to sort data using probability base b with variable data sizes
        data.append(length_times)

        base += increment

    if not quiet:
        print("{}TOTAL TIME TAKEN:{} {:.5f}secs".format(Fore.LIGHTRED_EX, Fore.RESET, total_time))

    return np.array(data)


def sort_with_ranged_bases_multithreaded(a=-maxsize-1, b=maxsize, lengths=None, trials=10,
                                         start=2.0, stop=8.0, increment=1.0, quiet=False):

    data = []
    base = start
    total_time, lengths_length = 0, len(lengths)
    while base <= stop + increment:

        # Basic array
        length_times = [base] + [0] * lengths_length

        t = time()

        threads = []

        for i, n in enumerate(lengths):
            my_thread = threading.Thread(target=sort_and_add,
                                         kwargs={'times_list': length_times,
                                                 'index': i+1,
                                                 'base': base,
                                                 'n': n,
                                                 'a': a,
                                                 'b': b,
                                                 'trials': trials,
                                                 'quiet': quiet})
            if not quiet:
                print("{}Starting Thread{} for N={}{}{}\n".format(Fore.LIGHTGREEN_EX, Fore.RESET,
                                                                  Fore.CYAN, n, Fore.RESET))

            my_thread.start()

            if not quiet:
                print(Fore.GREEN+"Thread " + str(i) + " for " + str(n) + " started" + Fore.RESET)

            threads.append(my_thread)

        if not quiet:
            print(Fore.RED+"\nRunning join for all threads\n"+Fore.RESET)

        for i in range(len(threads) - 1, -1, -1):
            if not quiet:
                print("Waiting for {}Thread {}{}".format(Fore.YELLOW, i, Fore.RESET))

            threads[i].join()

        if not quiet:
            # Compute the amount of time taken for all the threads to get sorted
            t = time() - t

            # Add it up to the total amount of time
            total_time += t

            # Print it to stdout
            print("{}Time taken in total: {:.5f}{} secs".format(Fore.GREEN, t, Fore.RESET))

        '''
        for i, n in enumerate(lengths):
            threads.append(threading.Thread(target=sort_and_add(length_times, i+1, base, n, a, b, trials)))
        '''

        # x: base, [Y]: times taken to sort data using probability base b with variable data sizes
        data.append(length_times)

        base += increment

    if not quiet:
        print("{}TOTAL TIME TAKEN:{} {:.5f}secs".format(Fore.LIGHTRED_EX, Fore.RESET, total_time))

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
    start, stop = 1, 4
    inc = 0.1

    fpath = "{}/data/datafileTrials{}Interval{}-{}Inc{}.txt".format(os.getcwd(),
                                                                           trials,
                                                                           str(stop).replace('.', ''),
                                                                           str(start).replace('.', ''),
                                                                           str(inc).replace('.', ''))

    if os.path.exists(fpath):
        data = np.loadtxt(fpath)

    else:
        data = sort_with_ranged_bases(a=a, b=b, lengths=n, trials=trials,
                                      start=start, stop=stop, increment=inc)

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
            "For "+str(trials)+" Randomized Sets of Values Between "+str(a)+" and "+str(b)

    plt.figure()

    plot = sorting_time_data.plot(title=title)

    plot.set_xlabel("Probability Bases (Pb)")
    plot.set_ylabel("Time Taken (Secs)")

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