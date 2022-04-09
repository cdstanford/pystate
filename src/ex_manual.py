"""
Example of how the CRC-based state hashing works for a simple class,
implemented manually.
"""

import crc32

class Foo:
    def __init__(self):
        self._crc = crc32.MAX_32

    def recurse_n_times(self, n):
        self._crc = crc32.crc_push(self._crc, n)
        print(f"Call {n}, CRC {hex(self._crc)}")
        if n > 0:
            self.recurse_n_times(n - 1)
        self._crc = crc32.crc_pop(self._crc, n)
        print(f"Return {n}, CRC {hex(self._crc)}")

    def get_crc(self):
        return self._crc ^ crc32.MAX_32

x = Foo()
x.recurse_n_times(5)
x.get_crc()
