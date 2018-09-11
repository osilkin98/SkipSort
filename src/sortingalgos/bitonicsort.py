"""Copyright (c) 2010 Aldo Cortesi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import math
ASCENDING = True
DESCENDING = False

def compare(lst, i, j, dir):
    if dir == (lst[i] > lst[j]):
        lst[i], lst[j] = lst[j], lst[i]
        lst.log()


def merge(lst, lo, n, dir):
    if n > 1: 
        k = n/2
        for i in range(lo, lo+k):
            compare(lst, i, i+k, dir)
        merge(lst, lo, k, dir)
        merge(lst, lo+k, k, dir)


def _bitonicsort(lst, lo, n, dir):
    if n > 1:
        k = n/2
        _bitonicsort(lst, lo, k, ASCENDING)
        _bitonicsort(lst, lo+k, k, DESCENDING)
        merge(lst, lo, n, dir)


def bitonicsort(lst):
    # Length of list must be 2**x, where x is an integer.
    assert math.modf(math.log(len(lst), 2))[0] == 0
    _bitonicsort(lst, 0, len(lst), ASCENDING)

