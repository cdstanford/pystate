# → [FP4](https://github.com/eniac/FP4)

# pystate

Pystate is a call-sensitive [CRC32](https://en.wikipedia.org/wiki/Cyclic_redundancy_check)-based state tracker for Python objects.
It is used in the [FP4](https://github.com/eniac/FP4) project for fuzzing programmable networks; specifically, to track and respond to changes in control-plane state.

## About

The state tracking is *call-sensitive* in the sense that it incorporates the current call stack of all methods in the class, not just the instance attributes of the object. It is thus a more fine-grained approximation of the true state of the program than just hashing the values of the instance attributes.
On the other hand, it introduces far less overhead than tracking the actual state (which may require $O(n)$ or worse snapshots per update), as state updates can be processed in $O(1)$ with CRC32.

## Dependencies

This code works with both Python 3 (version 3.9.9) and Python 2 (version 2.7.18).

It requires `pickle` and `unittest`, both of which are part of the standard library and should not need to be installed separately.

## How to use

An example is in `src/ex_decorated.py`. To use pystate:

1. `import pystate`

2. Create your Python class, and have it inherit from `pystate.TrackState`

3. Wrap `__init__` with the decorator `@pystate.track_init`

4. Wrap all other methods that you wish to track the state for with `@pystate.track_stack_calls`.

Then you can call `.get_crc()` at any point, which returns the current CRC value of the state.

If you want to track whether the CRC is newly seen, you can also call `.is_new()` which checks whether the current CRC does not equal any the state on any previous invocation of `.is_new()`.

## Issues

If you have any issues using pystate, bug reports, or feedback, please file an issue on this github repository! The author will try to assist.

## Technical notes and limitations

Since CRC32 is a 32-bit hash, it is not an exact representation. It's also not cryptographically secure and doesn't necessarily behave pseudorandomly, so is not appropriate for applications where strong unpredictability is needed.

The current implementation heavily relies on `pickle` and lifts some limitations from `pickle`. Unpicklable attributes can be explicitly excluded from the state by prefixing with `_`, but unpicklable function arguments are not currently supported.

The maintained CRC code is a hash of the following bytes, in order:
1. All function calls on the stack (pickled triple of the function name, arguments, and keyword arguments)
2. All attributes in the object not prefixed with `_`, and which are picklable

Other forms of state are not currently supported (e.g., local variables, line-specific control flow state, or external storage).
