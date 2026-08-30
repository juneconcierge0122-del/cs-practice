"""
Decorator Factory — a hands-on tutorial script.

Run it top to bottom:      python decorator_factory_tutorial.py
Run just one section:      python decorator_factory_tutorial.py 4

Each section prints what it does, so read the code and the output side by side.
"""

import functools
import sys
import time


def section(n, title):
    """Print a section header."""
    print(f"\n{'=' * 62}\n[{n}] {title}\n{'=' * 62}")


# ---------------------------------------------------------------------------
# 1. @ is just syntax sugar
# ---------------------------------------------------------------------------
# The rule is one line long:
#
#     @X
#     def f(): ...
#
# means exactly:
#
#     def f(): ...
#     f = X(f)
#
# That's it. Everything else in this file follows from that rule.
# So whatever sits after @ must be something that TAKES a function and
# RETURNS a function.

def demo_1():
    section(1, "@ is just syntax sugar")

    def shout(func):
        def wrapper():
            return func().upper() + "!"
        return wrapper

    # -- with the @ syntax --
    @shout
    def greet_a():
        return "hello"

    # -- doing it by hand: identical --
    def greet_b():
        return "hello"
    greet_b = shout(greet_b)

    print("  @shout        ->", greet_a())
    print("  shout(greet)  ->", greet_b())
    print("\n  Both are the same thing. @ saved us one line.")


# ---------------------------------------------------------------------------
# 2. A plain decorator: two layers
# ---------------------------------------------------------------------------
# Layer 1 takes the function being decorated.
# Layer 2 takes the arguments of the actual call.

def demo_2():
    section(2, "A plain decorator has two layers")

    def announce(func):                       # layer 1: the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):         # layer 2: the call
            print(f"  calling {func.__name__}{args}")
            return func(*args, **kwargs)
        return wrapper

    @announce
    def add(a, b):
        return a + b

    print("  result:", add(2, 3))
    print("\n  `announce` IS the decorator. Used bare, with no parentheses.")


# ---------------------------------------------------------------------------
# 3. The problem: how do we pass options to a decorator?
# ---------------------------------------------------------------------------
# Say we want to choose the label:  @announce(label="CALL")
#
# Now the thing after @ is not a name — it's a CALL. Python evaluates it
# first, then uses whatever comes back as the decorator. So we need a
# function that RETURNS a decorator. That is a decorator factory.
#
# Three layers now:
#
#     def factory(options):        <- layer 1: decorator's own options
#         def decorator(func):     <- layer 2: the function
#             def wrapper(*a):     <- layer 3: the call
#                 ...

def demo_3():
    section(3, "Adding options requires a third layer")

    def announce(label="calling"):             # layer 1: options
        def decorator(func):                   # layer 2: the function
            @functools.wraps(func)
            def wrapper(*args, **kwargs):      # layer 3: the call
                print(f"  [{label}] {func.__name__}{args}")
                return func(*args, **kwargs)
            return wrapper
        return decorator
    # NOTE: the ONLY new thing versus section 2 is that the old two-layer
    # decorator got wrapped in one more function that supplies `label`.

    @announce()                                # default label
    def add(a, b):
        return a + b

    @announce(label="MATH")                    # custom label
    def mul(a, b):
        return a * b

    print("  ", add(2, 3))
    print("  ", mul(2, 3))


# ---------------------------------------------------------------------------
# 4. Watch the layers fire, one at a time
# ---------------------------------------------------------------------------
# The three layers run at three DIFFERENT moments. This is the single most
# useful thing to internalise, so this section makes each one announce itself.

def demo_4():
    section(4, "When does each layer actually run?")

    def noisy(tag):
        print(f"  layer 1 runs NOW  -- factory called with tag={tag!r}")

        def decorator(func):
            print(f"  layer 2 runs NOW  -- decorating {func.__name__}")

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"  layer 3 runs NOW  -- {func.__name__} was called")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    print("  -- about to define greet --")

    @noisy(tag="demo")
    def greet():
        return "hi"

    print("  -- greet is now defined; nothing called it yet --")
    print("  -- calling greet() twice --")
    greet()
    greet()

    print("\n  Layers 1 and 2 ran ONCE, at import/definition time.")
    print("  Layer 3 runs on EVERY call.")
    print("  => Put expensive setup in layer 1 or 2, never in layer 3.")


# ---------------------------------------------------------------------------
# 5. Two pairs of parentheses
# ---------------------------------------------------------------------------

def demo_5():
    section(5, "Two pairs of parentheses, unpacked")

    def repeat(times):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return [func(*args, **kwargs) for _ in range(times)]
            return wrapper
        return decorator

    # -- with @ --
    @repeat(3)
    def roll_a():
        return "x"

    # -- by hand: note the TWO calls --
    def roll_b():
        return "x"
    roll_b = repeat(3)(roll_b)
    #        ^^^^^^^^^ ^^^^^^^
    #        |         |
    #        |         second pair: apply the decorator to the function
    #        first pair: call the factory, get a decorator back

    print("  @repeat(3)          ->", roll_a())
    print("  repeat(3)(roll_b)   ->", roll_b())

    # You can even hold the intermediate decorator in a variable:
    triple = repeat(3)
    print("  repeat(3) returned  ->", triple.__name__, type(triple).__name__)


# ---------------------------------------------------------------------------
# 6. The classic trap: forgetting the parentheses
# ---------------------------------------------------------------------------

def demo_6():
    section(6, "The trap: @factory instead of @factory()")

    def repeat(times=2):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return [func(*args, **kwargs) for _ in range(times)]
            return wrapper
        return decorator

    @repeat            # <-- BUG: no parentheses
    def roll():
        return "x"

    # `roll` got bound to the `times` parameter, the factory returned
    # `decorator`, and that is what the name `roll` now points at.
    print("  roll is actually:", roll.__name__)

    try:
        roll()
    except TypeError as e:
        print("  calling roll() raises:", type(e).__name__, "-", e)

    print("\n  The error message points nowhere near the real mistake.")
    print("  Rule of thumb: if the decorator takes options, the () is")
    print("  mandatory even when you want all the defaults -> @repeat()")


# ---------------------------------------------------------------------------
# 7. Supporting both @deco and @deco(...)
# ---------------------------------------------------------------------------
# The standard fix. `functools.lru_cache` uses exactly this shape, which is
# why both @lru_cache and @lru_cache(maxsize=None) work.

def demo_7():
    section(7, "Making both forms work")

    def repeat(func=None, *, times=2):
        # NOTE: the bare `*` forces `times` to be keyword-only. That matters:
        # it guarantees anything landing in the `func` slot is the decorated
        # function, so the `func is None` test below is reliable.
        def decorator(f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return [f(*args, **kwargs) for _ in range(times)]
            return wrapper

        if func is None:
            return decorator      # called as @repeat() or @repeat(times=3)
        return decorator(func)    # called as @repeat

    @repeat
    def a():
        return "a"

    @repeat()
    def b():
        return "b"

    @repeat(times=4)
    def c():
        return "c"

    print("  @repeat            ->", a())
    print("  @repeat()          ->", b())
    print("  @repeat(times=4)   ->", c())


# ---------------------------------------------------------------------------
# 8. Something you would actually ship: @retry
# ---------------------------------------------------------------------------

def retry(attempts=3, delay=0.05, exceptions=(Exception,)):
    """Retry the call up to `attempts` times, sleeping `delay` in between."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last = None
            for i in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last = e
                    print(f"    attempt {i}/{attempts} failed: {e}")
                    if i < attempts:
                        time.sleep(delay)
            raise last
        return wrapper
    return decorator


def demo_8():
    section(8, "A realistic factory: @retry")

    state = {"n": 0}

    @retry(attempts=4, delay=0.01, exceptions=(ValueError,))
    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("not ready")
        return f"succeeded on call {state['n']}"

    print("  ", flaky())

    print("\n  Options live in layer 1, so they are read once at decoration")
    print("  time and captured by the closure -- no re-parsing per call.")


# ---------------------------------------------------------------------------
# 9. Where each variable lives
# ---------------------------------------------------------------------------

def demo_9():
    section(9, "Closure scoping across three layers")

    def tag(prefix):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # `wrapper` can see BOTH `prefix` (layer 1) and `func`
                # (layer 2), because it is nested inside both.
                return f"{prefix}:{func(*args, **kwargs)}"
            return wrapper
        return decorator

    @tag("v1")
    def hello():
        return "hello"

    print("  ", hello())
    print("   closure cells on wrapper:",
          [c.cell_contents if not callable(c.cell_contents)
           else c.cell_contents.__name__
           for c in hello.__closure__])
    print("\n  Each decorated function gets its OWN closure, so two functions")
    print("  decorated with different options never interfere.")


# ---------------------------------------------------------------------------
# Exercises
# ---------------------------------------------------------------------------
EXERCISES = """
Exercises — try these before looking anything up:

  1. Write @clamp(lo, hi) that clamps the return value into [lo, hi].

  2. Turn the `trace` decorator from your recursion work into a factory
     taking (indent="|  ", show_return=True, max_depth=None), where
     max_depth suppresses printing below a given level.

  3. Write @typed(int, int) that checks positional argument types and
     raises TypeError on mismatch. Then extend it to read the annotations
     off the function itself instead, so no arguments are needed --
     and note how that turns it back into a two-layer decorator.

  4. Take the dual-mode `repeat` from section 7 and break it on purpose:
     remove the bare `*` and call it as @repeat(3). Explain the failure.

  5. Stack two factories on one function and predict the order in which
     layer 2 and layer 3 fire for each. Then verify with prints.
"""


DEMOS = [demo_1, demo_2, demo_3, demo_4, demo_5,
         demo_6, demo_7, demo_8, demo_9]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        DEMOS[int(sys.argv[1]) - 1]()
    else:
        for d in DEMOS:
            d()
        print(EXERCISES)
