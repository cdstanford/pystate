"""
Example of how the CRC-based state hashing works for a simple class,
using an automated decorator.

The output of this file should be the same as ex_manual.py.
"""

import crc32

class Foo(crc32.TrackState):
    def __init__(self):
        super().__init__()

    def recurse_n_times(self, n):
        self._stack_crc = crc32.crc_push(self._stack_crc, n)
        print(f"Call {n}, CRC {hex(self._stack_crc)}")
        if n > 0:
            self.recurse_n_times(n - 1)
        self._stack_crc = crc32.crc_pop(self._stack_crc, n)
        print(f"Return {n}, CRC {hex(self._stack_crc)}")

x = Foo()
x.recurse_n_times(5)
x.get_crc()
