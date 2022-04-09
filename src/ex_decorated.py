"""
Example of how the CRC-based state hashing works for a simple class,
using an automated decorator.

The output of this file should be the same as ex_manual.py.
"""

import crc32

class Foo(crc32.TrackState):
    @crc32.track_init
    def __init__(self):
        pass

    @crc32.track_stack_calls
    def recurse_n_times(self, n):
        if n > 0:
            self.recurse_n_times(n - 1)

x = Foo()
x.recurse_n_times(5)
x.get_crc()
