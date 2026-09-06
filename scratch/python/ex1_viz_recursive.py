import functools

def trace(func):
    depth = 0 # current depth in Recursion

    @functools.wraps(func) # `functools`: a module; `functools.wraps`: a function in `functools`
    def wrapper(*args, **kwargs):
        nonlocal depth
        pad = "| " * depth
        arg_str = ", ".join(
                [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )

        print(f"{pad}┌─{func.__name__}({arg_str})")

        depth += 1
        try:
            ret = func(*args, **kwargs)
        finally:
            depth -= 1

        print(f"{pad}└─{ret!r}")
        return ret

    return wrapper



#### [repr(a) for a in args] --> `args`: tuple
# fib(3) --> args=(3,) => [repr(a) for a in args] --> ['3']
#    cf. str("abc") --> abc; repr("abc") --> 'abc'
#          It may mislead that `f(abc)` has the input `abc` rather than
#                              the input `'abc'` with f('abc')  [a string].
#
#############################################################################

#### {v!r} <-- the same --> {repr(v)}
# !r --> repr
# !s --> str  (default)
# !a --> ascii
#
#  *** f"{v!r}" <-- the same --> f"{repr(v)}" 
#
#############################################################################

# ---- Example of Recursion ---- #

@trace
def fib(n):
    if n <=1:
        return n

    return fib(n-1) + fib(n-2)


@trace
def gcd(a, b):
    if b==0:
        return a

    return gcd(b, b%a)



if __name__ == "__main__":

    print("Function: fib")
    fib(3)
    print('\n ******   ****** \n')
    fib(4)

    print('==================================\n')

    print("Function: gcd")

    gcd(48, 18)
    print('\n ******   ****** \n')
    gcd(36, 24)

    print('==================================\n')

