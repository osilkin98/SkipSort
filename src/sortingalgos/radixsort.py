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

from itertools import chain

def radixsort(lst):
    is_sorted = lambda l: all([a < b for a, b in zip(l[:-1], l[1:])])
    shift = 1
    zeroes = []
    ones = []
    while not is_sorted(lst.lst):
        orig = lst.lst[:]
        while len(orig) != 0:
            # take an item out of the list
            item = orig.pop(0)
            # put it in the right bucket
            if (item.i & shift) == 0:
                zeroes.append(item)
            else:
                ones.append(item)
            # copy the items back into the main list
            for j, item in enumerate(chain(zeroes, orig, ones)):
                lst[j] = item
            # for a more simple graph, comment out the line below
            lst.log()
            #
            if is_sorted(lst):
                return
        lst.log()
        shift = shift << 1
        zeroes[:] = []
        ones[:] = []
