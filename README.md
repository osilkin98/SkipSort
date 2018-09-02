# SkipSort

### What is this?

This is an implementation of a near `O(n)` non-comparison based sorting algorithm for large-ish datasets that
I came up with. 

### How Does it Work?

#### Linear-Time Sorting
The basic idea is that in order to sort the dataset `X`, you just go through it once and hash the number
by its value into its correct spot using some kind of hash function which only requires `O(1)` time. 

Since all you'd need for such an algorithm is to traverse the set of data just once, you'd be able to
obtain a sorted set in just `O(n)` steps. 

#### Sorting by Hashing
A Hash-based sorting function would look something like this:
```cpp
list<int> sort(list<int> unsortedData, int hashFunction*(int)) {
    // create the same length list as unsortedData
    list<int> sortedData(unsortedData.length); 
    
    // sort the unsortedData list
    for(int i = 0; i < unsortedData.length; i++) {
        sortedData[i] = hashFunction(unsortedData[i]);
    }
    
    // return the sortedData
    return sortedData;
   
}
```
While this looks great in theory, in practice it requires far more resources than is reasonable. 
The time it takes to hash the values may be `O(1)`, but to be able to hash all possible values of integers
into the same datastructure, using `D` bits to take into a account for duplicates, would require 
`O(D^(2^(bits)))` of space complexity. For example, to use a hash table for sorting `32-bit` integers 
and using `8-bit` values to count duplicates, you would need `O(8^(2^32)) = O(8^4294967296)` which 
is an ***ASTRONOMICAL*** amount of space that we can't even begin to comprehend; just for sorting integers.

Even if we *were* somehow able to store that much memory, even in disk memory, the amount of time that would
take to traverse a sparse hash table like that would be directly proportional to the amount of space
we consume. 

#### A More Feasible Approach
Methods to bypass this limitation would include using a hash-table which would only instantiate 'bucket'
values (an entry in the hash table representing the specific value and number of times it has appeared) 
only when it needs them, and then creating a link between the new bucket and the already existing
buckets, so that we can just jump to them. This approach is definitely more feasible, 
but when you think about it, it's just an ordered linked list, which would give us a time complexity
of `O(n^2)`, which is about as good as bubble sort.

Amends can be made to this approach however. We could use a technique of 'Folding', where we determine
the average difference between numbers in the set, and make something like `2^(4-i)` steps when entering
the data instead of `1`. This helps but not by quite the amount that we'd need. 


#### A Quick Way to Access Data With Step Reductions?
What we need in this case, is a data-structure which would allow us to have a very quick access and
insertion time, but at the same time maintain order. 

If you're reading this and by now your mind isn't screaming *"Skip List!"* I don't know what to tell you.
A skip list has `O(log n)` lookup time, which isn't exactly *optimal*, but when you think about the 
problem at hand, if the data that we're dealing with can contain duplicate entries, AND we want to be
able to sort larger sets of data with very minimal overhead, a skip-list that contains the numeric
value, as well as a counter for the number of times we've seen a number, makes perfect sense.

For example, if we're dealing with lots of `8-bit` integers, the amount that we'll have will likely
be all over the place. And if we're using `8-bit` integers, it might be due to the fact that we need 
lots of them, otherwise space consumption would become a major hassle. If we're dealing with many
of these `byte` values, over `256` to be exact, then we're going to going to probabilistically see
the same values over and over again, and the amount that the skip-list needs to hold would be limited
to just `256`. On average, we would need `log(256) = 8` steps in order to access one of these values, 
and so if `n > 256`, then the amount of steps needed to access all of these in one pass would be 
`Ө(n*log(256))`, or `Ө(n*8) ~= Ө(n)`. 

## The Algorithm 

#### Psuedo-Code

The psuedo-code to this algorithm is actually not far off from what I wrote in the first example
of a hash-based approach to sorting. It goes like this:
```cpp
list<int> SkipSort(list<int> unsorted) {

    // Use a skiplist for the insertion and return process
    Skiplist<int> skip;
    
    // iterate through the entire dataset
    for(int i = 0; i < unsorted.length; i++) {
        
        // if the value isn't already in the skip list
        if(!skip.contains(unsorted[i])) {
            // add it
            skip.insert(unsorted[i]);
        } else {
            // count the number of times the number appears
            skip.incrementCount(unsorted[i]);
        }
    }
    
    // new array into which we will insert sorted values
    list<int> sorted;
    
    // go through each value in the skip list
    for(int j = 0; j < skip.length; j++) {
              
        for(int k = 0; k < skip[i].count; k++) {
            sorted.add(skip[j].value);
        }
  
    } // in total this process will take unsorted.length steps
    
    
    return sorted
    
}
```
#### Algorithm Complexity

##### Time Complexity

| Best | Average | Worst |
|:----:|:-------:|:-----:|
|`Ө(n)`|`Ө(n)`| `Ө(n log n)`|

##### Space Complexity

`Ө(n log n)`

#### Ө(n) Runtime? What's the catch?
This answer is actually very interesting. Because at the surface level, it seems like the *only* way 
for this algorithm to utilize its efficiency is to be using a large amount of data, but that's not
exactly true. In order to need `log(n)` to exceed the number of `bits` the datatype uses, you need to 
be using a uniform distribution of data. 

This may *sound* like a drawback, but it's actually not. This means that the algorithm will actually
perform the absolute worst ***WHEN*** you have a uniform distribution. 

In other words, the algorithm will only perform poorly if you purposefully try and sort an out-of-order
set of every `byte` value. 

To put matters into perspective, if you were to try and sort all `4,294,967,296` possible integer values,
you would **AT MOST** require `32` steps for each value, which isn't bad at all. Bubble sort would require
`2^64 = 18,446,744,073,709,551,616`, whereas this would only require `O(n) = O(2^32 + 1) = 4,294,967,293`
steps for `n = 2^32 + 1`, in the average case. Or in the worst case it would require 
`O(n log n)` which in this case would only be `O(2^32 * 32) = O(137,438,953,472)`
## Where do we go From Here?
There is still room for further optimization and fine-tuning to this algorithm, namely in the 
searching and inserting space. I've considered using a trie data-structure to reduce it down to 
`O(log log n)` lookup, allowing it to become `O(n)` far quicker, however there is no defined order
to a trie, which makes the process of actually retrieving the data in an ordered and linear fashion, 
rather difficult. 

It's possible to use a hash-table to pre-check whether or not numbers are within the actual skip
list before looking them. This however might be a problem, as the performance of this decreases
very quickly with more and more values, so I can't see it being useful considering it would only
be desirable when we're performing `32` steps just to check whether or not an item is within the skiplist.

It is possible to combine other data structures with the skip list to reduce access times, and so I will
look into that as well. 