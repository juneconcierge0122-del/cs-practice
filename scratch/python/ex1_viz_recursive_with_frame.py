import functools
import inspect

def trace(func):
    # signature() is expensive: compute once at decoration time, not per call.
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.currentframe()

        try:

            # NOTE: caller is `fib`, not `wrapper`.
            # This trips up most people learning decorators. The real stack is:
            #   <module> -> wrapper -> fib (original) -> wrapper -> fib -> ...
            # The decorator inserts a frame between every level of recursion.
            # So stepping back one frame from wrapper lands in the original
            # function's body, and co_name is "fib".
            #   (If you put currentframe() inside the original function instead,
            #      f_back would be `wrapper`.)


            caller = frame.f_back
            caller_name = caller.f_code.co_name

            # NOTE: f_lineno can't tell the two recursive calls apart here,
            # because `fib(n-1) + fib(n-2)` sits on one line. On Python 3.11+,
            # frame.f_lasti together with co_positions() gives column offsets,
            # which pinpoints whether it was the left or the right call.


            lineno = caller.f_lineno


            # Walk the whole stack and count how many frames are "us".
            depth, f = 0, caller
            while f is not None:

                # NOTE: the `f_locals.get("func") is func` check is NOT optional.
                # Each call to trace() builds a fresh closure, but the code
                # object is fixed at compile time — every wrapper shares one.
                
                # Matching on f_code alone means decorating fib and some other
                # function would let their depths contaminate each other.
                # Comparing the closure variable `func` confirms it's the same
                # decorated target.


                if f.f_code is wrapper.__code__ and f.f_locals.get("func") is func:
                    depth += 1

                f = f.f_back

        finally:

            # NOTE: deleting frame refs is what the docs recommend. A frame
            # references its own locals, and those locals hold the frame —
            # an easy reference cycle. Today's GC collects it fine, but in a
            # tracer that runs on every single call it's a good habit.

            del frame, caller # avoid `reference cycle`

        bound = sig.bind(*args, **kwargs)  # `args = (3, 'A', 'C')` == sig.bind ==> `args = hanoi(n=3, src='A', dst='C') `

        bound.apply_defaults() # fulfilled all the argument default value

        arg_str = ", ".join(f"{k}={v!r}" for k, v in bound.arguments.items())

        pad = "|  " * depth
        print(f"{pad}┌─ {func.__name__}({arg_str})   <-- call by {caller_name}:{lineno}")
        ret = func(*args, **kwargs)
        print(f"{pad}└─ {ret!r}")

        return ret

    return wrapper


@trace
def fib(n):
    if n <= 1:
        return n 
    return fib(n-1)+fib(n-2)

@trace
def gcd(a,b):
    if b==0:
        return a
    return gcd(b, b%a)



if __name__ == "__main__":
    fib(3)

    print("------------------\n")

    gcd(108, 27)



# PERFORMANCE NOTE:
# This is slower than the `nonlocal depth` counter version — every call walks
# the entire stack, so n levels of recursion costs O(n^2). If all you need is
# indentation, use the counter. The frame version earns its keep by exposing
# call-site info, and by not depending on the decorator tracking its own state:
# even if an exception unwinds the stack mid-flight, the depth is always right.
#
# If you only want the caller, sys._getframe(1) is a bit faster than
# inspect.currentframe().f_back. The one to avoid is inspect.stack() — by
# default it reads source files to build context lines, which is dramatically
# slower. If you must use it, pass inspect.stack(0).
