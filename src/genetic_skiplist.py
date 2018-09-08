from sorting_algorithms import skipSort, test
from sys import maxsize
from timeit import timeit

def sort_with_ranged_bases(a=-maxsize-1, b=maxsize, N=100, trials=10, start=2, stop=8, increment=1):

    base = start
    while base <= stop:
        print("Running "+str(trials)+" trials for each sorting algorithm on a dataset of N=" +str(N) +
              "\nwith randomized datasets generated between a = "+str(a)+" and b = "+str(b))

        baseTime = timeit(stmt="test(skipSort, N={}, a={}, b={})".format(N, a, b), number=trials,
                          setup="from sorting_algorithms import skipSort, test")



if __name__ == 'main':

