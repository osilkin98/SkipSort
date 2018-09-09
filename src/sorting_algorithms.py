from sys import maxsize
from skiplist import Skiplist
from random import randint


# skipsort algorithm implementation in python
def skipSort(data: list, probability_base=2):
    slist = Skiplist(probability_base)
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


def partition(arr, l, h):
    i = (l - 1)
    x = arr[h]

    for j in range(l, h):
        if arr[j] <= x:
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)


# Function to do Quick sort
# arr[] --> Array to be sorted,
# l  --> Starting index,
# h  --> Ending index
def quickSortIterative(arr, l=0, h=None):
    # Create an auxiliary stack
    h = len(arr) - 1 if h is None else h

    size = h - l + 1
    stack = [0] * (size)

    # initialize top of stack
    top = -1

    # push initial values of l and h to stack
    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition(arr, l, h)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h

# Recursive impleentation
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


def radixSort(alist, base=10):
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


def timSort(data: list):
    data.sort()


if __name__ == '__main__':
    # slist = Skiplist()

    N, trials = 100, 10
    a, b = 0, 50

    print("Running {} trials for each sorting algorithm on a dataset of N={}\n\
with randomized datasets generated between a = {} and b = {}".format(trials, N, a, b))

    import timeit

    skip_time = timeit.timeit("test(skipSort, N={}, a={}, b={})".format(N, a, b),
                              number=trials, setup="from __main__ import test, skipSort")

    # slist.print()