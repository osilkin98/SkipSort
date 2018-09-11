from sys import maxsize
from skiplist import Skiplist
from random import randint


# skipsort algorithm implementation in python
def skipsort(data: list, probability_base=2):
    slist = Skiplist(probability_base)
    while len(data) != 0:
        slist.insert(data.pop(0))

    head = slist.head.next[0]
    while head is not None:
        data += [head.value] * head.count
        head = head.next[0]


# For testing the algorithm
def bubblesort(data):
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
def quicksort(arr, l=0, h=None):
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
def quicksort_recursive(x):
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
        first_part = quicksort_recursive(x[:i])
        second_part = quicksort_recursive(x[i + 1:])
        first_part.append(x[i])
        return first_part + second_part


def merge(a, left, mid, right):
    """
    Merge fuction
    """
    # Copy array
    copy_list = []
    i, j = left, mid + 1
    ind = left

    while ind < right + 1:

        # if left array finish merging, copy from right side
        if i > mid:
            copy_list.append(a[j])
            j += 1
        # if right array finish merging, copy from left side
        elif j > right:
            copy_list.append(a[i])
            i += 1
        # Check if right array value is less than left one
        elif a[j] < a[i]:
            copy_list.append(a[j])
            j += 1
        else:
            copy_list.append(a[i])
            i += 1
        ind += 1

    ind = 0
    for x in (range(left, right + 1)):
        a[x] = copy_list[ind]
        ind += 1

# This is an iterative implementation of timsort_merge sort
def mergesort(list_, left=0, right=None):
    """
    Iterative version of the Merge Sort Algorithm
    """
    right = len(list_) - 1 if right is None else right
    factor = 2
    temp_mid = 0
    # Main loop to iterate over the array by 2^n.
    while 1:
        index = 0
        left = 0
        right = len(list_) - (len(list_) % factor) - 1
        mid = int(factor / 2) - 1

        # Auxiliary array to timsort_merge subdivisions
        while index < right:
            temp_left = index
            temp_right = temp_left + factor - 1
            mid2 = int((temp_right + temp_left) / 2)
            merge(list_, temp_left, mid2, temp_right)
            index = (index + factor)

        # Chek if there is something to timsort_merge from the remaining
        # Sub-array created by the factor
        if len(list_) % factor and temp_mid != 0:
            # timsort_merge sub array to later be merged to the final array
            merge(list_, right + 1, temp_mid, len(list_) - 1)
            # Update the pivot
            mid = right
        # Increase the factor
        factor = factor * 2
        temp_mid = right

        # Final timsort_merge, timsort_merge subarrays created by the subdivision
        # of the factor to the main array.
        if factor > len(list_):
            mid = right
            right = len(list_) - 1
            merge(list_, 0, mid, right)
            break


def radixsort(alist, base=10):
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


def timsort_c(data: list):
    data.sort()


# based off of this code https://gist.github.com/nandajavarma/a3a6b62f34e74ec4c31674934327bbd3
# Brandon Skerritt
# https://skerritt.tech

def binary_search(the_array, item, start, end):
    if start == end:
        if the_array[start] > item:
            return start
        else:
            return start + 1
    if start > end:
        return start

    mid = round((start + end) / 2)

    if the_array[mid] < item:
        return binary_search(the_array, item, mid + 1, end)

    elif the_array[mid] > item:
        return binary_search(the_array, item, start, mid - 1)

    else:
        return mid


"""
Insertion sort that timsort uses if the array size is small or if
the size of the "run" is small
"""


def insertion_sort(the_array):
    l = len(the_array)
    for index in range(1, l):
        value = the_array[index]
        pos = binary_search(the_array, value, 0, index - 1)
        the_array = the_array[:pos] + [value] + the_array[pos:index] + the_array[index + 1:]
    return the_array


def timsort_merge(left, right):
    """Takes two sorted lists and returns a single sorted list by comparing the
    elements one at a time.
    [1, 2, 3, 4, 5, 6]
    """
    if not left:
        return right
    if not right:
        return left
    if left[0] < right[0]:
        return [left[0]] + timsort_merge(left[1:], right)
    return [right[0]] + timsort_merge(left, right[1:])


def timsort(the_array):
    runs, sorted_runs = [], []
    length = len(the_array)
    new_run = [the_array[0]]

    # for every i in the range of 1 to length of array
    for i in range(1, length):
        # if i is at the end of the list
        if i == length - 1:
            new_run.append(the_array[i])
            runs.append(new_run)
            break
        # if the i'th element of the array is less than the one before it
        if the_array[i] < the_array[i - 1]:
            # if new_run is set to None (NULL)
            if not new_run:
                runs.append([the_array[i]])
                new_run.append(the_array[i])
            else:
                runs.append(new_run)
                new_run = []
        # else if its equal to or more than
        else:
            new_run.append(the_array[i])

    # for every item in runs, append it using insertion sort
    for item in runs:
        sorted_runs.append(insertion_sort(item))

    # for every run in sorted_runs, timsort_merge them
    sorted_array = []
    for run in sorted_runs:
        sorted_array = timsort_merge(sorted_array, run)


if __name__ == '__main__':
    # slist = Skiplist()
    from graphing_sorts import create_random_dataset_standard
    dataset = create_random_dataset_standard(b=10, set_length=10, num_sets=1)[0]
    print(dataset)
    timsort(dataset)

    # slist.print()