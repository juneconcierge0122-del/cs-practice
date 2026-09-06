"""
rtrace — a recursion tracer built as a decorator factory.

    from rtrace import trace, note

    @trace(show_return=True)
    def fib(n):
        ...

Options live in layer 1 (the factory), so they are resolved once at
decoration time and captured by the closure. Nothing is re-parsed per call.
"""

import functools
import inspect

__all__ = ["trace", "note", "ANSI", "NO_COLOR"]


# --- palette ---------------------------------------------------------------
# Two dicts with the same keys, so turning colour off is a swap, not an if.

ANSI = {
    "line": "\033[90m",    # tree glyphs
    "name": "\033[36m",    # function name
    "args": "\033[37m",    # argument list
    "ret":  "\033[32m",    # return value
    "note": "\033[33m",    # note() output
    "dim":  "\033[90m",    # elision marker
    "off":  "\033[0m",
}

NO_COLOR = {k: "" for k in ANSI}


# --- shared state for note() -----------------------------------------------
# A stack of (pad, palette) for every tracer frame currently executing.
# note() reads the top so its output lines up with the surrounding branch.

_active = []


def note(msg):
    """Print a message aligned with the innermost traced call."""
    if not _active:
        print(msg)
        return
    pad, pal = _active[-1]
    print(f"{pal['line']}{pad}{pal['off']}{pal['note']}• {msg}{pal['off']}")


# --- the factory -----------------------------------------------------------

def trace(func=None, *, indent="│  ", show_return=True, max_depth=None,
          color=True, max_arg_len=48, hide=()):
    """
    Trace a recursive function as an indented call tree.

    indent       string repeated once per level
    show_return  print the `└─ value` line (turn off for side-effect recursion)
    max_depth    stop printing below this depth; prints one elision marker
    color        ANSI colour on/off
    max_arg_len  truncate any single argument repr longer than this
    hide         parameter names to leave out of the printed argument list
                 (accumulators like `result`, `sols` are noise in the tree)

    Usable bare (@trace) or called (@trace(...)). The keyword-only `*` is
    what makes the `func is None` test below reliable.
    """
    pal = ANSI if color else NO_COLOR
    hide = frozenset(hide)

    def decorator(f):
        sig = inspect.signature(f)
        depth = 0
        calls = 0
        peak = 0
        elided = False          # only print the "..." marker once per subtree

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            nonlocal depth, calls, peak, elided
            calls += 1
            peak = max(peak, depth + 1)
            pad = indent * depth

            quiet = max_depth is not None and depth >= max_depth
            if quiet:
                if not elided:
                    print(f"{pal['dim']}{pad}⋯ (deeper calls hidden){pal['off']}")
                    elided = True
            else:
                elided = False
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                parts = []
                for k, v in bound.arguments.items():
                    if k in hide:
                        continue
                    r = repr(v)
                    if len(r) > max_arg_len:
                        r = r[:max_arg_len - 1] + "…"
                    parts.append(f"{k}={r}")
                arg_str = ", ".join(parts)
                print(f"{pal['line']}{pad}┌─{pal['off']} "
                      f"{pal['name']}{f.__name__}{pal['off']}"
                      f"{pal['args']}({arg_str}){pal['off']}")

            _active.append((pad + indent, pal))
            depth += 1
            try:
                ret = f(*args, **kwargs)
            finally:
                # try/finally so an exception unwinding the stack cannot
                # leave depth stranded — every later line would be misindented.
                depth -= 1
                _active.pop()

            if not quiet:
                if show_return:
                    r = repr(ret)
                    if len(r) > max_arg_len:
                        r = r[:max_arg_len - 1] + "…"
                    print(f"{pal['line']}{pad}└─{pal['off']} "
                          f"{pal['ret']}{r}{pal['off']}")
                else:
                    print(f"{pal['line']}{pad}└─{pal['off']}")
            return ret

        def stats():
            return {"calls": calls, "max_depth": peak}

        def reset():
            nonlocal calls, peak
            calls = peak = 0

        wrapper.stats = stats
        wrapper.reset = reset
        return wrapper

    if func is None:
        return decorator
    return decorator(func)
