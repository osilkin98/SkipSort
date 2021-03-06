from sorting_algorithms import skipsort, quicksort_recursive, radixsort, \
    quicksort, python_stl_sort, mergesort, timsort
from sortingalgos.radixsort import radixsort as radixsort_other
from sortingalgos.bitonicsort import bitonicsort  # This can only be used if the length is a power of 2
from sortingalgos.heapsort import heapsort
from sortingalgos.smoothsort import smoothsort
from sortingalgos.combsort import combsort
from sys import maxsize
from timeit import timeit
import random
from random import randint
import numpy as np
from time import time
import matplotlib.pyplot as plt
import pandas as pd
import os
import threading
import colorama.ansi
from colorama import Fore
from matplotlib import rc

# This increments the value of the color given as a code
def increment_color(color_code: str):
    return colorama.ansi.CSI + str((int(color_code.rstrip('m').lstrip(colorama.ansi.CSI).rstrip('m')) + 1) % 108) + 'm'


def sort_test_with_data(sort, data):
    """ This is a function to test a given sorting algorithm against the dataset provided.

    :param function sort: Sorting function to sort the data with
    :param list data: List containing prepared unsorted datasets to be sorted. This SHOULD be

    :return: Nothing
    """
    for unsorted_list in data:
        sort(unsorted_list)


def create_random_dataset(set_length=100, num_sets=10, random_func=np.random.normal, force_int=True,
                          **kwargs):
    """ Creates random datasets provided the information in

    :param int set_length: Number of elements within each dataset:
    :param int num_sets: Amount of datasets to generate
    :param function random_func: Random function to use when generating values, Normal Gaussian distribution
     is used by default.
    :param kwargs: Parameters to Provide for random function, must specify 'function', as well as its
     necessary paramters. If none is provided, the standard python library will be used.
    :return: A List of the datasets as tuples , though these should be copied to avoid having already sorted data.
    :rtype: list
    """
    if force_int:
        return [tuple([int(random_func(**kwargs)) for num in range(set_length)]) for dataset in range(num_sets)]
    else:
        return [tuple([random_func(**kwargs) for num in range(set_length)]) for dataset in range(num_sets)]


def create_random_dataset_standard(a=0, b=maxsize, set_length=100, num_sets=10):
    """

    :param int | float a: Lowest possible value for the datasets
    :param int | float b: Highest possible value for the datasets
    :param int set_length: Number of elements within each dataset
    :param int num_sets: Amount of datasets to generate
    :return: A List of the datasets as tuples , though these should be copied to avoid having already sorted data.
    :rtype: list
    """
    if type(a) is int and type(b) is int:
        sets = [tuple([randint(a, b) for k in range(set_length)]) for i in range(num_sets)]

    else:
        sets = [tuple([random.random() * (b - a) + a for k in range(set_length)]) for i in range(num_sets)]

    return sets


# This is for testing any other function since skipsort may have a base specified as well
def sort_test(sort, N=100, a=0, b=maxsize):
    """

    :param function sort: Sorting function to run on the data
    :param int N: Number of elements in dataset to be created
    :param int | float a: Smallest Possible Value
    :param int | float b: Large Possible Value
    :return: Nothing
    """
    # If we're dealing with ints
    if type(a) == int and type(b) == int:
        # Populate the array
        data = [randint(a, b) for i in range(N)]
    else:
        # Populate the array in a float way
        data = [random.random() * (b - a) + a for i in range(N)]

    sort(data)


# This is a wrapper for the standard test function exclusive to skipsort
def skipsort_test(base=2, N=100, a=0, b=maxsize):
    """ Tests Skipsort once with the given parameters

    :param float base: Probability Base
    :param int N: Number of elements to sort
    :param int | float a: Smallest possible value
    :param int | float b: Largest possible value
    :return: Nothing
    """
    data = [randint(a, b) for i in range(N)]
    skipsort(data, base)
    data.clear()


# To be used with multithreading
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


def elements_vs_time(a=-maxsize-1, b=maxsize, trials=100, sorts=(skipsort, quicksort_recursive, python_stl_sort),
                     start=10, stop=1000, increment=10, coefficient=5.0, type='linear',
                     quiet=False, random_func=np.random.normal, **random_params):
    """ Measures the time it takes for the given sorting algorithms to sort data as N increases.
    Returns a 2-D numpy array in the form: [[N, time1, ... ]_1, [N, time1, ... ]_2, ..., [N, time1, ...]_n]

    :param int | float a: Minimum Possible Value
    :param int | float b: Maximum Possible Value
    :param int trials: Number of Trials for each data member
    :param list | tuple sorts: List of Sorting function that have the format `sort(data)`
    :param int start: First N to Start with
    :param int stop: Last N to Finish with
     random data. The parameters if any must be provided. If None is provided,
     the default python random function will be used.
    :param int increment: Increment to Increase by
    :param float coefficient: This is the number that will be exponentiated if 'geometric' is selected
    :param str type: Method of incrementing, either linear or geometric, however linear works better.
    :param bool quiet: Flag to indicate whether or not to suppress output. Off by default.
    :param function random_func: Random function to use for making datasets, uses the numpy.random.normal by default
    :param dict random_params: Parameters to pass into the random function when generating datasets.
    :return: 2-D Numpy Array in the form [ [N, time1, time2, ...]_1, ... [N, time1, time2, ...]_n ],
     as well as a 1-D Numpy Array containing all the randomly generated numbers
    :rtype: numpy.ndarray, numpy.ndarray
    """

    # Initialize the arrays for data and the numbers we'll use
    data = []

    # We'll save the numbers we've used in a dictionary so calling them back will be faster
    # The keys will be the numbers and the values will be the number count
    numbers_used = []

    # Save the number of sorts so we don't keep calling len() each time
    num_sorts, index = len(sorts), 0

    # We can't start with 0 elements, that just doesn't work
    n = start if start > 0 else start + increment

    # While n is less than or equal to the maximum number of elements we want to stop at
    while n <= stop:

        index_string = "{}[index = {}]:{} ".format(Fore.RED, index, Fore.RESET)

        if not quiet:
            # This value will only be set if the quiet flag was called
            print(index_string + "Computing average sorting time for N={}{}{} using {}{}{} samples\n".format(
                Fore.CYAN, n, Fore.RESET, Fore.BLUE, trials, Fore.RESET))
        elif index % 10 == 0:
            print(index_string + "[{}{}{}/{}{}{}]".format(Fore.LIGHTGREEN_EX, n, Fore.RESET,
                                                          Fore.CYAN, stop, Fore.RESET))
        # Create an empty list with the first element being the number of elements that get sorted
        # And each index corresponds to the given functions sorting time
        sorting_times = [n] + [0] * num_sorts

        # This is sort of the main dataset that will be used for sorting, the values within
        # Should be copied into a new list each time, prior to sorting
        unsorted_dataset = create_random_dataset(set_length=n, num_sets=trials,
                                                 random_func=random_func, **random_params)

        # unsorted_dataset = create_random_dataset_standard(a=a, b=b, set_length=n, num_sets=trials)

        for i, sort in enumerate(sorts):

            # Creates a copy of the unsorted data, each time the loop runs, this is reset
            unsorted_dataset_copy = [list(unsorted[:]) for unsorted in unsorted_dataset]

            # The number of trials is reflected in the number of datasets provided in unsorted_dataset
            sorting_time = timeit(
                stmt="sort_test_with_data(sort={}, data={})".format(sort.__name__, unsorted_dataset_copy),
                number=1,
                setup="from __main__ import sort_test_with_data; from {} import {}".format(
                    sort.__module__, sort.__name__))

            # time taken to sort data with number of elements N
            sorting_times[i+1] = sorting_time
            if not quiet:
                print("\tTime to sort N={}{}{} randomly generated values \
between {}{}{} and {}{}{} using {}{}{}: {}{:.3f}{} secs\n".format(
                    Fore.CYAN, n, Fore.RESET,
                    Fore.LIGHTRED_EX, a, Fore.RESET,
                    Fore.LIGHTGREEN_EX, b, Fore.RESET,
                    Fore.LIGHTMAGENTA_EX, sort.__name__, Fore.RESET,
                    Fore.CYAN, sorting_time, Fore.RESET))

        # Add the data
        data.append(sorting_times)

        # Append the flattened numbers into the numbers_used list
        numbers_used += [number for unordered_list in unsorted_dataset for number in unordered_list]

        n += increment if type.lower() == 'linear' else int(increment * (coefficient ** index))
        index += 1
    """
    # Transforms the dictionary we made into a 2-D array where the sub-lists are the number frequency pairs
    # That we kept track of in the numbers_used dict
    numbers_used_array = [[number, frequency] for number, frequency in numbers_used.items()]
    """

    return np.array(data), np.array(numbers_used)


def elements_vs_time_bases(a=-maxsize-1, b=maxsize, bases=(2, 4, 6, 8, 10, 20), trials=100, start=10,
                           stop=1000, increment=10, ratio=5, mode='linear', quiet=False):
    """ Measures the time it takes for the given sorting algorithms to sort data as N increases.
    Returns a 2-D numpy array in the form: [[N, time1, ... ]_1, [N, time1, ... ]_2, ..., [N, time1, ...]_n]

    :param int | float a: Maximum Value
    :param int | float b: Minimum Value
    :param list | tuple bases: List of number bases to be used when collecting the data
    :param int trials: Number of Trials for each data member
    :param int start: First N to Start with
    :param int stop: Last N to Finish with
    :param float ratio: Ratio `r` to use in the equation `a_i = a_1 *(r^i) if the incrementation
     mode is selected as 'geometric'
    :param int increment: Increment to Increase by
    :param str mode: Method of incrementing, either linear or geometric, however linear works better.
    :return: 2-D Numpy Array in the form [ [N, time1, time2, ...]_1, ... [N, time1, time2, ...]_n ]
    :rtype: numpy.ndarray
    """

    data = []
    num_bases, index = len(bases), 0
    n = start if start > 0 else start + increment
    a_1 = increment
    while n <= stop:

        if not quiet:
            # This value will only be set if the quiet flag was called
            index_string = "{}[index = {}]:{} ".format(Fore.RED, index, Fore.RESET)
            print(index_string + "Computing average sorting time for N={}{}{} using {}{}{} samples\n".format(
                Fore.CYAN, n, Fore.RESET, Fore.BLUE, trials, Fore.RESET))

        sorting_times = [n] + [0] * num_bases

        for i, base in enumerate(bases):
            sorting_time = timeit(
                stmt="skipsort_test(base={}, N={}, a={}, b={})".format(base, n, a, b), number=trials,
                setup="from __main__ import skipsort_test")

            # time taken to sort data with number of elements N
            sorting_times[i+1] = sorting_time
            if not quiet:
                print("\tTime to sort N={}{}{} randomly generated values \
between {}{}{} and {}{}{} using Base = {}{}{}: {}{:.3f}{} secs\n".format(
                    Fore.CYAN, n, Fore.RESET,
                    Fore.LIGHTRED_EX, a, Fore.RESET,
                    Fore.LIGHTGREEN_EX, b, Fore.RESET,
                    Fore.LIGHTMAGENTA_EX, base, Fore.RESET,
                    Fore.CYAN, sorting_time, Fore.RESET))

        data.append(sorting_times)

        n = index * increment if mode.lower() == 'linear' else int(a_1 * (ratio ** index))
        index += 1

    return np.array(data)


def sparsity_vs_time(min_value=0, start_value=50, stop_value=1000, increment=10, num_elements=500, sorts=None,
                     trials=100, quiet=False, multithread=False):
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
    :param list | tuple sorts: List of Sorting Function Objects to use on the data
    :param int trials: Number of trials to average a single datapoint over, default is 100.
    :param float probability_base: Base to use when computing probability. I.E. `1/b^n >= p` where `b`
     denotes the base. This value is 2 by default, however it can be scaled accordingly. Generally, the base
     doesn't matter as long as it's greater than 2, however anything below 1.4 is a bad idea and will generally
     result in diminished performance.
    :param str fpath: File Path of where the data file should be saved to
    :param bool quiet: Flag to indicate whether or not to suppress logging messages. Off by default.
    :param bool multithread: Flag to indicate whether or not this function should be parallelized
    :return: 2-D Numpy Array, of the form [[sparsity, time]_1, ... , [sparsity, time]_N].
    :rtype: numpy.ndarray
    """

    from math import fabs

    list_length = int((stop_value - start_value)/increment) + 1  # +1 because we're doing <= for the while loop

    data = [0] * list_length

    print("List length: {}".format(list_length))

    # Swap these if necessary
    if start_value > stop_value:
        tmp = start_value
        start_value = stop_value
        stop_value = tmp

    # Swap these, if the previous were also swapped, this should receive them correctly and swap with lower of 2
    if min_value > start_value:
        tmp = min_value
        min_value = start_value
        start_value = tmp

    if not multithread:

        current_value = start_value
        index, sparsity = 0, 0
        while current_value <= stop_value:

            if not quiet:
                # This value will only be set if the quiet flag was called
                index_string = "{}[index = {}]:{} ".format(Fore.RED, index, Fore.RESET)
                print(index_string+"Computing average sorting time for [{}, {}] using {} samples\n".format(min_value,
                                                                                              current_value,
                                                                                              trials))

            # compute sparsity
            sparsity = fabs(current_value - min_value) / num_elements

            data[index] = [sparsity] + [0.0] * len(sorts)

            for j, sort in enumerate(sorts):
                # Compute the average sorting time with M trials
                sorting_time = timeit(
                    stmt="sort_test({}, N={}, a={}, b={})".format(sort.__name__,num_elements,
                                                                  min_value,current_value), number=trials,
                    setup="from __main__ import sort_test; from sorting_algorithms import {}".format(sort.__name__))

                data[index][j+1] = sorting_time

                if not quiet:
                    print("\tTime to sort N={}{}{} randomly generated values \
between {}{}{} and {}{}{} using {}{}{}: {}{:.3f}{} secs\n".format(
                        Fore.CYAN, num_elements, Fore.RESET,
                        Fore.LIGHTRED_EX, min_value, Fore.RESET,
                        Fore.LIGHTGREEN_EX, current_value, Fore.RESET,
                        Fore.LIGHTMAGENTA_EX, sort.__name__, Fore.RESET,
                        Fore.CYAN, sorting_time, Fore.RESET))

            if not quiet:

                print(index_string+"Sparsity: {}{}{} Possibilities/N\n".format(Fore.LIGHTGREEN_EX if sparsity <= 1 else
                                                                  Fore.LIGHTRED_EX, sparsity, Fore.RESET))

            # increment the values
            current_value += increment
            index += 1

        # Return it
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


def create_sparsity_vs_time_graph(minimum=0, start=500, end=1000, increment=5, num_elements=500,
                                  trials=100, base=2, sorts=(skipsort, quicksort_recursive, python_stl_sort)):

    # Returns a dataset of [[sparsity, time1, ... ]_1, [sparsity, time1, ... ]_2, ..., [sparsity, time1, ... ]_N]
    data = sparsity_vs_time(min_value=minimum, start_value=start, stop_value=end, sorts=sorts,
                            increment=increment, num_elements=num_elements, trials=trials)

    # This is to graph the time as sparsity gets larger
    time_over_sparsity = pd.DataFrame(data=data[:, 1:], index=data[:, 0],
                                      columns=list(map(lambda x: x.__name__, sorts)))

    plot = time_over_sparsity.plot(title="Time Taken to SkipSort An Array of N={}, {} Times\n\
As The Value Range Increases From {} to {}".format(num_elements, trials, (start-minimum), (end-minimum)))

    plot.set_xlabel("Sparsity (range/N)")
    plot.set_ylabel("Time (secs)")

    # Save the figure as to avoid overwriting other plots
    plt.savefig("{}/plots/plot{}.png".format(os.getcwd(), len(os.listdir(os.getcwd() + "/plots"))))

    plt.show()


def create_elements_vs_time_graph(a=0, b=256, start=10, end=5000, increment=5, coefficient=5.0, trials=10,
                                  sorts=(skipsort, quicksort, python_stl_sort), fpath=None, mode='linear',
                                  random_func=np.random.normal, overwrite=True, **random_params):

    fpath = fpath if fpath is not None else\
        "{}/data/TimeOverElements{}-{}_i{}a{}{}.txt".format(os.getcwd(), end, start, increment,
                                                            str(coefficient).replace('.', ''), mode)

    # We want this to be a json serializable object
    numbers_fpath = fpath + '.json' if fpath.find('.txt') == -1 else \
                    fpath.replace('.txt', 'numbers.txt')

    if os.path.exists(fpath) and not overwrite:
        data = np.loadtxt(fpath)
        numbers_frequency = np.loadtxt(numbers_fpath)

        # try and load the number frequency

    else:
        data, numbers_frequency = elements_vs_time(a=a, b=b, start=start, stop=end,
                                                   increment=increment, trials=trials,
                                                   sorts=sorts, type=mode, quiet=False, coefficient=coefficient,
                                                   random_func=random_func, **random_params)

        # Try to save the data as a text file
        np.savetxt(fname=fpath, X=data)
        np.savetxt(fname=numbers_fpath, X=numbers_frequency)

    rc('font', **{'family': 'serif', 'serif': ['Times']})

    time_over_n = pd.DataFrame(data=data[:, 1:], index=data[:, 0], columns=list(map(
        lambda x: x.__name__.replace('_', '\_'), sorts)))

    rc('text', usetex=True)

    time_plot = time_over_n.plot(title="Time Taken by Algorithms to Sort Arrays of Varying Length\n\
    Using ({} incrementation)".format(start, mode))

    time_plot.set_xlabel("Number of Elements (N)")
    time_plot.set_ylabel("Time (secs)")

    entry_number = len(os.listdir(os.getcwd() + '/plots'))

    # Save the figure as to avoid overwriting other plots
    plt.savefig("{}/plots/plot{}.png".format(os.getcwd(), entry_number))

    plt.show()

    numbers_hist = pd.DataFrame(data=numbers_frequency)

    plt.figure()

    numbers_hist.hist(bins=100)
    # plt.rc('text', usetex=True)

    plt.title(r'Numbers Generated with The {} Function: $\alpha={}$, $\theta={}$'.format(
        random_func.__name__, random_params['shape'], random_params['scale']))

    plt.xlabel("Values Generated")

    plt.ylabel("Frequency")

    plt.savefig("{}/plots/plot{}hist.png".format(os.getcwd(), entry_number))

    plt.show()


def create_elements_and_bases_vs_time_graph(a=0, b=256, start=10, end=5000, increment=5, coefficient=5, trials=10,
                                  bases=(2, 4, 10, 20), fpath=None, mode='linear'):

    fpath = fpath if fpath is not None else\
        "{}/data/TimeOverElements{}-{}_i{}a{}{}.txt".format(os.getcwd(), end, start, increment,
                                                            str(coefficient).replace('.', ''), mode)

    if os.path.exists(fpath):
        data = np.loadtxt(fpath)

    else:
        data = elements_vs_time_bases(a=a, b=b, start=start, stop=end, increment=increment,
                                      trials=trials, bases=bases)

    # Try to save the data as a text file
    np.savetxt(fname=fpath, X=data)

    time_over_n = pd.DataFrame(data=data[:, 1:], index=data[:, 0], columns=bases)

    plot = time_over_n.plot(title="Time Taken to Sort An Array as N Increases from {} to {}\n\
With a Value Range of {} ({} incrementation)".format(start, end, b-a, mode))

    plot.set_xlabel("Number of Elements (N)")
    plot.set_ylabel("Time (secs)")

    # Save the figure as to avoid overwriting other plots
    plt.savefig("{}/plots/plot{}.png".format(os.getcwd(), len(os.listdir(os.getcwd() + "/plots"))))

    plt.show()


if __name__ == '__main__':
    random_parameters = {'scale': 2.64, 'shape': 100}

    create_elements_vs_time_graph(end=1000000, start=1000, increment=1.14, trials=10, mode='Geometric', overwrite=True,
                                  sorts=(skipsort, mergesort, combsort,
                                         radixsort, python_stl_sort, heapsort, smoothsort),
                                  random_func=np.random.gamma, **random_parameters)

    # create_elements_vs_time_graph(a=0, b=1000000, start=100, end=1000000, bases=(2, 10),
    #                               increment=1, coefficient=10, trials=1, mode='Geometric')