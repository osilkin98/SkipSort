# from sorting_algorithms import skipSort, test
from sys import maxsize
from timeit import timeit

def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, n=100, trials=10, start=2, stop=8, increment=1):

    base = start
    while base <= stop:
        print("Running "+str(trials)+" trials for skipsort with a probability base of Pb = " +str(base) +
              ", on a dataset of N=" +str(n) + "\nwith randomized datasets generated between a = "+
              str(a)+" and b = "+str(b))

        base_time = timeit(stmt="test(skipSort, N={}, a={}, b={})".format(n, a, b), number=trials,
                          setup="from sorting_algorithms import skipSort, test")

        print("Time taken: " + str(base_time) + " secs")

        base += increment

if __name__ == 'main':

