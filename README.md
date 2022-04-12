# pystate

Demonstration of call-sensitive CRC32-based state tracking for Python objects.

## About

The state tracking is *call-sensitive* in the sense that it incorporates the current call stack of all methods in the class, not just the instance attributes of the object. It is thus a more fine-grained approximation of the true state of the program than just hashing the values of the instance attributes.

Local variables and line-specific state are currently unsupported.

We use CRC32 because it can be updated conveniently when state changes. Note that since it's a 32-bit hash, it is not an exact representation. It's also not cryptographically secure and doesn't necessarily behave pseudorandomly.

## Dependencies

This code works with both Python 3 (>= 3.9.9) and Python 2 (>= 2.7.18).

It requires `pickle` and `unittest`, both of which are part of the standard library and should not need to be installed separately.

## How to use

An example is in `src/ex_decorated.py`. To use pystate:

1. `import pystate`

2. Create your Python class, and have it inherit from `pystate.TrackState`

3. Wrap `__init__` with the decorator `@pystate.track_init`

4. Wrap all other methods that you wish to track the state for with `@pystate.track_stack_calls`.

Then you can call `.get_crc()` at any point, which returns the current CRC value of the state.

If you want to track whether the CRC is newly seen, you can also call `.is_new()` which checks whether the current CRC does not equal any the state on any previous invocation of `.is_new()`.
