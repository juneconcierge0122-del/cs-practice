/******************************************************************************
 * Session Notes: std::next_permutation + Timing in C++
 *
 * Problem: Split digits 1-9 into three 3-digit numbers x, y, z (each digit
 *          used exactly once) such that y == 2x and z == 3x.
 *
 * Build:  g++ -std=c++11 -O2 -Wall permutation_timing.cpp -o perm
 * Run:    ./perm
 *****************************************************************************/

#include <iostream>
#include <algorithm>   // NOTE 1: next_permutation lives here, NOT in <iostream>.
                       // Some compilers pull it in transitively, so omitting
                       // this header may compile "by luck" on one machine and
                       // fail on another. Always include it explicitly.
#include <chrono>      // NOTE 2: modern, type-safe timing (C++11 and later)
#include <ctime>       // NOTE 3: legacy C timing, shown here for comparison

using namespace std;

/*----------------------------------------------------------------------------
 * NOTE 4: next_permutation semantics
 *
 * next_permutation(first, last) rearranges the range into the NEXT
 * lexicographically greater permutation and returns true. When the range is
 * already the largest permutation (descending order), it wraps around to the
 * smallest (ascending) and returns false -- which is what terminates the loop.
 *
 * ex: 123 < 132 < 213 < 231 < 312 < 321
 * 
 * return value:  "Is there a next one?":
 *     If there's a larger permutation → rewrite successful, return true.
 *     If it's already the largest one (i.e., completely descending, 321)
 *        → there's no next one, it will loop back to the smallest 123 and return false.
 *     This false is the termination condition for your loop.
 *     Because it will loop back to the starting point,
 *     starting from the smallest permutation, it will traverse all n! permutations without repetition.
 *
 * Consequence: to enumerate ALL n! permutations you must start from the
 * SORTED (ascending) sequence. Starting from {3,1,2} would only visit the
 * permutations lexicographically after it, silently missing the rest.
 *
 * A do-while (not while) is the right shape: it processes the initial
 * permutation before advancing, so all 9! = 362880 arrangements are visited.
 *--------------------------------------------------------------------------*/

/* Approach A: brute force over every permutation of the 9 digits. */
int solveByPermutation(int results[][3])
{
    int d[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};   // must be sorted -- see NOTE 4
    int count = 0;

    do {
        int x = d[0] * 100 + d[1] * 10 + d[2];
        int y = d[3] * 100 + d[4] * 10 + d[5];
        int z = d[6] * 100 + d[7] * 10 + d[8];

        if (y == x * 2 && z == x * 3) {
            /* NOTE 5: collect results instead of printing them here.
             * Terminal I/O is orders of magnitude slower than the arithmetic
             * being measured, so a cout inside the hot loop would dominate
             * the timing and tell you nothing about the algorithm. */
            results[count][0] = x;
            results[count][1] = y;
            results[count][2] = z;
            count++;
        }
    } while (next_permutation(d, d + 9));

    return count;
}

/* Approach B: bound the search space using the constraints themselves.
 *
 * NOTE 6: z = 3x must stay below 1000, so x <= 333. Digits are 1-9 with no
 * zeros, so x >= 123. That is ~200 candidates instead of 362880 -- roughly a
 * 1700x reduction in work, from the same problem statement.
 *
 * Trade-off: the permutation version is more obviously correct and adapts
 * immediately if the constraints change. This version encodes an assumption
 * (z = 3x) into its loop bounds, so it must be revisited if that changes.
 * Reach for it when the input size makes brute force impractical.
 */
int solveByBoundedSearch(int results[][3])
{
    int count = 0;

    for (int x = 123; x <= 333; x++) {
        int y = 2 * x;
        int z = 3 * x;

        int digits[9] = {x / 100, x / 10 % 10, x % 10,
                         y / 100, y / 10 % 10, y % 10,
                         z / 100, z / 10 % 10, z % 10};

        bool seen[10] = {false};   // index 0 unused; zero-init via {false}
        bool valid = true;

        for (int i = 0; i < 9; i++) {
            /* reject a 0 digit, or any digit already used */
            if (digits[i] == 0 || seen[digits[i]]) {
                valid = false;
                break;
            }
            seen[digits[i]] = true;
        }

        if (valid) {
            results[count][0] = x;
            results[count][1] = y;
            results[count][2] = z;
            count++;
        }
    }

    return count;
}

int main()
{
    int results[16][3];
    int count;

    /*========================================================================
     * TIMING METHOD 1: std::chrono::steady_clock  (preferred)
     *
     * NOTE 7: steady_clock is MONOTONIC -- it never jumps backwards when NTP
     * or the user adjusts the system clock. That is exactly what you want for
     * measuring an interval. system_clock is the wrong tool here: it tracks
     * wall-calendar time and can be adjusted mid-measurement, producing
     * negative or absurd durations. high_resolution_clock is often just an
     * alias for one of the two, so its guarantees are implementation-defined.
     *
     * NOTE 8: pick a unit with enough resolution. This loop runs in tens of
     * milliseconds at most, so duration_cast<milliseconds> would often print
     * 0 or 1. Microseconds give usable numbers here.
     *=======================================================================*/
    auto t0 = chrono::steady_clock::now();
    count = solveByPermutation(results);
    auto t1 = chrono::steady_clock::now();

    long long us = chrono::duration_cast<chrono::microseconds>(t1 - t0).count();

    /* Printing happens AFTER the clock is stopped -- see NOTE 5. */
    cout << "--- Solutions found: " << count << " ---" << endl;
    for (int i = 0; i < count; i++) {
        cout << results[i][0] << " "     // NOTE 9: without the separators,
             << results[i][1] << " "     // "192384576" runs together and is
             << results[i][2] << endl;   // unreadable.
    }

    cout << endl;
    cout << "[chrono] permutation search: " << us << " us"
         << " (" << us / 1000.0 << " ms)" << endl;

    /*========================================================================
     * TIMING METHOD 2: clock() from <ctime>  (legacy, still usable)
     *
     * NOTE 10: the (double) cast is mandatory. clock_t is an integral type,
     * so (end - start) / CLOCKS_PER_SEC is INTEGER DIVISION and collapses to
     * 0 for anything under a second. Cast before dividing, not after.
     *
     * NOTE 11: CLOCKS_PER_SEC is 1000000 on Linux, but that is only the unit
     * of the returned value -- it is NOT a resolution guarantee. The
     * underlying counter typically updates on a 1-10 ms tick, so fast code
     * yields 0 or coarse jumps.
     *
     * NOTE 12: clock() and steady_clock measure DIFFERENT THINGS.
     *
     *   clock()       -> CPU time: how long the process actually held a CPU
     *   steady_clock  -> wall time: how much real time elapsed
     *
     * Single-threaded and compute-bound, the two roughly agree. They diverge
     * sharply otherwise:
     *   - blocked on disk / sleeping -> clock() barely moves, wall time grows
     *   - multi-threaded             -> clock() sums across cores and can
     *                                   exceed wall time several times over
     *=======================================================================*/
    clock_t c0 = clock();
    count = solveByBoundedSearch(results);
    clock_t c1 = clock();

    double ms = (double)(c1 - c0) / CLOCKS_PER_SEC * 1000.0;   // see NOTE 10

    cout << "[clock ] bounded search:     " << ms << " ms"
         << "  (" << count << " solutions, same answers)" << endl;

    /*========================================================================
     * NOTE 13: caveats when comparing implementations
     *
     * - Compile both with the SAME flags. -O2 vs no optimization can differ
     *   by several times over, which swamps the difference you are studying.
     *
     * - A single measurement is noisy. CPU scheduling, cache state and
     *   frequency scaling all perturb it. Run the workload 10+ times and take
     *   the MINIMUM (least perturbed run) or the median; the mean is skewed
     *   upward by occasional outliers.
     *
     * - Beware dead-code elimination: if a result is computed and never used,
     *   -O2 may delete the whole loop and report a suspiciously perfect zero.
     *   Consuming the result (as this file does by printing it) prevents that.
     *
     * - Big-O beats micro-optimization. The 1700x win here came from shrinking
     *   the search space, not from tuning the inner loop.
     *=======================================================================*/

    return 0;
}
