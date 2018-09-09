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

    # To know how much decimal places we need to round the value to in the future
    increment_precision = str(increment)[::-1].find('.')

    data = []
    base = start
    lengths_length, total_time = len(lengths), 0
    while base < stop + increment:

        # Basic array
        length_times = [base] + [0] * lengths_length

        if not quiet:
            print("{}Testing Base {}{}\n".format(Fore.LIGHTRED_EX, Fore.RESET, base))

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

        base = round(base + increment, increment_precision)

    if not quiet:
        print("{}TOTAL TIME TAKEN:{} {:.5f}secs".format(Fore.LIGHTRED_EX, Fore.RESET, total_time))

    return np.array(data)


def sort_with_ranged_bases_multithreaded(a=-maxsize-1, b=maxsize, lengths=None, trials=10,
                                         start=2.0, stop=8.0, increment=1.0, quiet=False):

    increment_precision = str(increment)[::-1].find('.')

    data = []
    base = start
    total_time, lengths_length = 0, len(lengths)
    while base < stop + increment:

        # Basic array
        length_times = [base] + [0] * lengths_length

        if not quiet:
            print("{}Testing Base {}{}\n".format(Fore.LIGHTRED_EX, Fore.RESET, base))


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

        base = round(base + increment, increment_precision)

    if not quiet:
        print("{}TOTAL TIME TAKEN:{} {:.5f}secs".format(Fore.LIGHTRED_EX, Fore.RESET, total_time))

    return np.array(data)


def elements_vs_time(a=-maxsize-1, b=maxsize, base=1.5, trials=100,
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


def sparsity_vs_time(min_value=0, start_value=50, stop_value=1000, increment=10, num_elements=500,
                     trials=100, probability_base=2, fpath=None, quiet=False, overwrite=True, multithread=False):
    """ This function plots the Sparsity of the sorted dataset against the time it took to sort it.

        The Sparsity of a dataset is defined as the range of possible values over the size of the dataset, or
    `S = |B - A|/N`, where `B` and `A` are the highest and lowest values in the dataset, respectively, and `N`
    is the total number of values in the dataset.

        When `S < 1`, the runtime of the skipsort algorithm is `O(n)`, since there are more spaces for values than
    there are possible values, the Skiplist would be filled up completely, and so the number of steps it would take
    to access a value would at most be `O(M)`, where `M = log(|B - A|)`, which is how many bits it takes to represent
    the biggest value in the range, assuming the Probability Base is 2.

        If `S > 1`, then the number of possible values in the set is greater than the maximum number it can hold,
    meaning that it's possible that the entire time you might be having to insert a number in the worst case scenario,
    causing the runtime to be `O(n log n)`. In reality, this is probably not going to be the case, however it will
    definitely become harder to come across duplicates.

        The more sparse a dataset is, the worse this algorithm will perform. If the sparsity is low, since it will just
    be a constant insertion/lookup operation for each n, whereas a dense dataset will cause the space usage to
    become constant.

    :param int | float min_value: The Minumum Value for the Dataset
    :param int | float start_value: The Value from which we will start generating datasets from
    :param int | float stop_value: The Highest Value we will go to before halting data creation
    :param int | float increment: How Much we will increase by value each iteration. This is the variable in this case.
    :param int num_elements: Total number of elements to use for our dataset. This number stays constant
    :param int trials: Number of trials to average a single datapoint over, default is 100.
    :param float probability_base: Base to use when computing probability. I.E. `1/b^n >= p` where `b`
     denotes the base. This value is 2 by default, however it can be scaled accordingly. Generally, the base
     doesn't matter as long as it's greater than 2, however anything below 1.4 is a bad idea and will generally
     result in diminished performance.
    :param str fpath: File Path of where the data file should be saved to
    :param bool quiet: Flag to indicate whether or not to suppress logging messages. Off by default.
    :return: 2-D Numpy Array, of the form [[sparsity, time]_1, ... , [sparsity, time]_N].
    :rtype: numpy.ndarray
    """


            current_value += increment
            index += 1

        return np.array(data)

def create_sorting_data_graph(a=0, b=maxsize, n: list=None, trials=100, start=1.4,
                              stop=2.0, inc=0.05, fpath=None, quiet=False):

    n = n if n is not None else [1000]

    fpath = fpath if fpath is not None else \
        "{}/data/datafileValues{}-{}Trials{}Interval{}-{}Inc{}.txt".format(os.getcwd(),
                                                                           b, a,
                                                                           trials,
                                                                           str(stop).replace('.', ''),
                                                                           str(start).replace('.', ''),
                                                                           str(inc).replace('.', ''))

    if os.path.exists(fpath):
        data = np.loadtxt(fpath)

    else:
        if trials < 100:

            data = sort_with_ranged_bases(a=a, b=b, lengths=n, trials=trials,
                                          start=start, stop=stop, increment=inc, quiet=quiet)
        else:
            if not quiet:
                print("Trials ({}) > 100, enabling multithreading".format(trials))

            data = sort_with_ranged_bases_multithreaded(a=a, b=b, lengths=n, trials=trials,
                                                        start=start, stop=stop, increment=inc, quiet=quiet)
        # If the filepath doesn't exist
        if not os.path.exists("{}/data".format(os.getcwd())):
            # Make the directories
            os.makedirs("{}/data".format(os.getcwd()))

        # This is where the plots will be saved
        if not os.path.exists("{}/plots".format(os.getcwd())):
            os.makedirs("{}/plots".format(os.getcwd()))

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
            "For "+str(trials)+" Randomized Sets of Values Between "+str(a)+" and "+str(b) +\
            "\nUsing " + str(int((stop-start)/inc)*trials) + " Total Samples (increment=" +\
            str(round(inc, str(inc)[::-1].find('.'))) + ", trials/sample=" + str(trials)+ ")"


    plot = sorting_time_data.plot(title=title)

    plot.set_xlabel("Probability Bases (Pb)")
    plot.set_ylabel("Time Taken (Secs)")

    # Save the figure as to avoid overwriting other plots
    plt.savefig("{}/plots/plot{}.png".format(os.getcwd(), len(os.listdir(os.getcwd() + "/plots"))))


    # Display the plot objects
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



if __name__ == '__main__':

    N = list(map(lambda x: 250*x, range(2, 7)))
    create_sorting_data_graph(a=0, b=99999, n=N, trials=300, start=1.25, stop=2, inc=0.01)