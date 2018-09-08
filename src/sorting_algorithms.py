from sys import maxsize
from skiplist import Skiplist
from random import randint


# skipsort algorithm implementation in python
def skipSort(data: list):
    slist = Skiplist()
    while len(data) != 0:
        slist.insert(data.pop(0))

    head = slist.head.next[0]
    while head is not None:
        data += [head.value] * head.count
        head = head.next[0]




# For testing the algorithm
def bubbleSort(data):
    for passnum in range(len(data) - 1, 0, -1):
        for i in range(passnum):
            if data[i] > data[i + 1]:
                temp = data[i]
                data[i] = data[i + 1]
                data[i + 1] = temp


def quickSort(x):
    if len(x) == 1 or len(x) == 0:
        return x
    else:
        pivot = x[0]
        i = 0
        for j in range(len(x)-1):
            if x[j+1] < pivot:
                x[j+1],x[i+1] = x[i+1], x[j+1]
                i += 1
        x[0],x[i] = x[i],x[0]
        first_part = quickSort(x[:i])
        second_part = quickSort(x[i+1:])
        first_part.append(x[i])
        return first_part + second_part


def radix_sort(alist, base=10):
    if alist == []:
        return

    def key_factory(digit, base):
        def key(alist, index):
            return ((alist[index] // (base ** digit)) % base)

        return key

    largest = max(alist)
    exp = 0
    while base ** exp <= largest:
        alist = counting_sort(alist, base - 1, key_factory(exp, base))
        exp = exp + 1
    return alist


def counting_sort(alist, largest, key):
    c = [0] * (largest + 1)
    for i in range(len(alist)):
        c[key(alist, i)] = c[key(alist, i)] + 1

    # Find the last index for each element
    c[0] = c[0] - 1  # to decrement each element for zero-based indexing
    for i in range(1, largest + 1):
        c[i] = c[i] + c[i - 1]

    result = [None] * len(alist)
    for i in range(len(alist) - 1, -1, -1):
        result[c[key(alist, i)]] = alist[i]
        c[key(alist, i)] = c[key(alist, i)] - 1

    return result


def test(sort, N=100, a=0, b=maxsize):
    data = [randint(a, b) for i in range(N)]
    sort(data)
    data.clear()


def stlSort(data: list):
    data.sort()


if __name__ == '__main__':
    # slist = Skiplist()

    N, trials = 10000, 10
    a, b = 0, 512

    print("Running {} trials for each sorting algorithm on a dataset of N={}\n\
with randomized datasets generated between a = {} and b = {}".format(trials, N, a, b))

    import timeit

    skip_time = timeit.timeit("test(skipSort, N={}, a={}, b={})".format(N, a, b),
                              number=trials, setup="from __main__ import test, skipSort")
    print("Skipsort Time: {}secs".format(skip_time))

    skip_time = timeit.timeit("test(radix_sort, N={}, a={}, b={})".format(N, a, b),
                              number=trials, setup="from __main__ import test, radix_sort")

    print("Radix Time: {}secs".format(skip_time))

    quickTime = timeit.timeit("test(quickSort, N={}, a={}, b={})".format(N, a, b),
                              number=trials, setup="from __main__ import test, quickSort")

    print("Quick Sort Time: {}secs".format(quickTime))

    stltime = timeit.timeit("test(stlSort, N={}, a={}, b={})".format(N, a, b),
                            number=trials, setup="from __main__ import test, stlSort")

    print("Timsort Time: {}secs".format(stltime))

    '''
    bubble_time = timeit.timeit("test(bubbleSort, N={}, a={}, b={})".format(N, a, b),
                                number=trials, setup="from __main__ import test, bubbleSort")

    print("Bubble Time: {}secs".format(bubble_time))
    '''
    # slist.print()