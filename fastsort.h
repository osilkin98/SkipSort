//
// Created by oleg on 9/1/18.
//

#ifndef CFASTSORT_FASTSORT_H
#define CFASTSORT_FASTSORT_H

/** Sorts the data given using the SkipSort algorithm I devised, with just
 * slightly modified functions provided by James Aspnes in his implementation
 * of a Skiplist.
 *
 * Due to the fact that the implemenation provided had no native support for
 * handling duplicate items, on average, there are two searches performed within
 * the skip list for each data member. This is inefficient and has an asymptotic
 * runtime of O(2nlog(n)) = O(n log (n^2)) ~= O(n log n). Since the constants
 * get dropped, it turns out to be O(n log n), however the optimization problem
 * is exactly that; a problem.
 *
 *
 * @param [in,out] data C Pointer to array of integers
 * @param [in] N Number of data members within the data array
 */
void sortData(int* data, int N);


/** Sorts the data given using the Skipsort algorithm I devised. This version
 * uses an optimized function I wrote using a basic implementation of the
 * SkipList provided by James Aspnes.
 *
 * The function algorithm searches for the data member once to see if it's
 * in the list or not. Upon finding it, the algorithm increments the ocurrance
 * of that data member, and returns the amount of steps performed by the function.
 * If it wasn't found, the function creates it.
 *
 * Since the function anticipates insertion, it calculates the potential tower
 * height ahead of time, and uses the height it received as the 'save' point.
 * If it fails to find the data member, it simply goes back to this save point, and
 * begins inserting the new data member. This point is based on a Geometric
 * distribution and will always be, on average, halfway between the top of the data
 * and the bottom.
 *
 * Since the algorithm uses a probabilistic data structure, which does not take
 * duplicate entries, the algorithm will theoretically have a worst-case runtime
 * of Ө(n log n) for an EVEN distribution of data members represented by M number
 * of bits, when M > log_2(n). Once log_2(n) > M, the number of steps required
 * for each data member will, on average, be a constant M, and as such, the worst
 * case will be Ө(n * M) = Ө(n).
 *
 * The algorithm actually performs better with more serial and uneven distributions
 * of numbers, as it creates a more concentrated skiplist much faster, causing
 * the best-case scenario to be Ω(n), which occurs when more compact datasets are
 * fed into it.
 *
 * Due to the optimization of the method, the asymptotic runtime will be, on average,
 * Ө(n/2 log(n)) = Ө(n log(sqrtr(n))) ~= Ө(n log n).
 *
 * @param [in,out] data C Pointer to array of integers
 * @param [in] N Number of data members within the data array
 */
void skipSortOptimized(int* data, int N);


#endif //CFASTSORT_FASTSORT_H