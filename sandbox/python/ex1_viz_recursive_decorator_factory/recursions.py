"""
recursions — classic recursive algorithms, each traced.

    python recursions.py            # list the demos
    python recursions.py gcd        # run one
    python recursions.py all        # run everything
    python recursions.py fib --no-color

Every demo is a plain function that decorates its algorithm locally, so the
tracer options can differ per algorithm and the counters start clean.
"""

import functools
import sys

from rtrace import trace, note

DEMOS = {}


def demo(name, blurb):
    """Register a demo under a short name."""
    def deco(fn):
        fn.blurb = blurb
        DEMOS[name] = fn
        return fn
    return deco


def report(fn):
    s = fn.stats()
    print(f"\n  {s['calls']} calls, max depth {s['max_depth']}")


# ---------------------------------------------------------------------------
@demo("gcd", "linear recursion — no branching, one straight line down")
def demo_gcd(color=True):
    @trace(color=color)
    def gcd(a, b):
        if b == 0:
            return a
        return gcd(b, a % b)

    gcd(1071, 462)
    report(gcd)
    print("  Tail recursive: the tree is a stick, so a while loop is equivalent.")


# ---------------------------------------------------------------------------
@demo("fib", "binary recursion — the classic exponential blow-up")
def demo_fib(color=True):
    @trace(color=color)
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(5)
    report(fib)
    print("  Same subtrees recomputed over and over — compare with `memo`.")


# ---------------------------------------------------------------------------
@demo("memo", "the same fib, memoised — cache outside, tracer inside")
def demo_memo(color=True):
    @functools.lru_cache(maxsize=None)
    @trace(color=color)
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)

    fib(10)
    report(fib.__wrapped__)
    print("  lru_cache sits OUTSIDE the tracer, so cache hits never reach it:")
    print("  every line printed is work that genuinely happened.")
    print("  Flip the two decorators to see the hits instead.")


# ---------------------------------------------------------------------------
@demo("hanoi", "binary recursion driven by side effects, not return values")
def demo_hanoi(color=True):
    @trace(show_return=False, color=color)
    def hanoi(n, src, dst, tmp):
        if n == 0:
            return
        hanoi(n - 1, src, tmp, dst)
        note(f"move disc {n}: {src} → {dst}")
        hanoi(n - 1, tmp, dst, src)

    hanoi(3, "A", "C", "B")
    report(hanoi)
    print("  The move order is an in-order walk of this tree. Shift the")
    print("  note() call before or after both branches and it breaks.")


# ---------------------------------------------------------------------------
@demo("msort", "divide and conquer — split on the way down, merge on the way up")
def demo_msort(color=True):
    @trace(color=color)
    def merge_sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = merge_sort(a[:mid])
        right = merge_sort(a[mid:])
        out, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                out.append(left[i]); i += 1
            else:
                out.append(right[j]); j += 1
        return out + left[i:] + right[j:]

    merge_sort([5, 2, 9, 1, 7, 3, 8, 4])
    report(merge_sort)
    print("  Nothing is sorted on the way down. All the ordering shows up")
    print("  in the └─ lines, i.e. on the return trip. Depth is log n.")


# ---------------------------------------------------------------------------
@demo("subsets", "backtracking — watch `path` grow and shrink")
def demo_subsets(color=True):
    @trace(show_return=False, color=color, hide=("nums", "result"))
    def subsets(nums, i, path, result):
        if i == len(nums):
            result.append(path[:])      # copy! see note below
            note(f"emit {path}")
            return
        subsets(nums, i + 1, path, result)          # skip nums[i]
        path.append(nums[i])
        subsets(nums, i + 1, path, result)          # take nums[i]
        path.pop()                                  # undo — this is the
                                                    # "backtracking" step

    out = []
    subsets([1, 2, 3], 0, [], out)
    report(subsets)
    print(f"  got {out}")
    print("  `path` is printed on every line, so the append/pop cycle is")
    print("  visible directly. Drop the [:] copy and every result goes empty.")


# ---------------------------------------------------------------------------
@demo("queens", "backtracking with pruning — dead ends are visible as stubs")
def demo_queens(color=True):
    @trace(show_return=False, color=color, hide=("n", "sols", "d1", "d2"))
    def queens(n, row, cols, d1, d2, board, sols):
        if row == n:
            sols.append(board[:])
            note(f"solution {board}")
            return
        for c in range(n):
            if c in cols or (row - c) in d1 or (row + c) in d2:
                continue
            board.append(c)
            queens(n, row + 1, cols | {c}, d1 | {row - c}, d2 | {row + c},
                   board, sols)
            board.pop()

    sols = []
    queens(4, 0, set(), set(), set(), [], sols)
    report(queens)
    print(f"  {len(sols)} solutions")
    print("  A ┌─ immediately followed by └─ is a pruned branch: every column")
    print("  was rejected, so the loop body never ran.")


# ---------------------------------------------------------------------------
@demo("perms", "permutations — n! leaves, so max_depth keeps it readable")
def demo_perms(color=True):
    @trace(show_return=False, color=color, max_depth=2, hide=("out",))
    def perms(remaining, path, out):
        if not remaining:
            out.append(tuple(path))
            return
        for i, x in enumerate(remaining):
            path.append(x)
            perms(remaining[:i] + remaining[i + 1:], path, out)
            path.pop()

    out = []
    perms([1, 2, 3, 4], [], out)
    report(perms)
    print(f"  {len(out)} permutations")
    print("  max_depth=2 hides everything below level 2 and prints one")
    print("  elision marker per subtree instead.")


# ---------------------------------------------------------------------------
@demo("ackermann", "non-primitive recursion — grows absurdly fast")
def demo_ackermann(color=True):
    @trace(color=color, max_depth=3)
    def ack(m, n):
        if m == 0:
            return n + 1
        if n == 0:
            return ack(m - 1, 1)
        return ack(m - 1, ack(m, n - 1))

    ack(2, 2)
    report(ack)
    print("  ack(3, 3) still finishes; ack(4, 2) will not. The call count")
    print("  is the interesting number here, not the tree shape.")


# ---------------------------------------------------------------------------
def main(argv):
    args = [a for a in argv if not a.startswith("-")]
    color = "--no-color" not in argv

    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        print("\navailable demos:\n")
        for name, fn in DEMOS.items():
            print(f"  {name:<10} {fn.blurb}")
        return

    names = list(DEMOS) if args[0] == "all" else args
    for name in names:
        if name not in DEMOS:
            print(f"unknown demo: {name}")
            continue
        fn = DEMOS[name]
        print(f"\n{'─' * 68}\n{name} — {fn.blurb}\n{'─' * 68}")
        fn(color=color)


if __name__ == "__main__":
    main(sys.argv[1:])
