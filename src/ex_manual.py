"""
Example of how the CRC-based state hashing works for a simple class,
implemented manually.

The output of this file should be the same as ex_decorated.py.
"""

import crc32

class Foo:
    def __init__(self):
        self._stack_crc = crc32.MAX_32

    def get_crc(self):
        return self._stack_crc ^ crc32.MAX_32

    def recurse_n_times(self, n):
        self._stack_crc = crc32.crc_push(self._stack_crc, n)
        print(f"Call {n}, CRC {hex(self._stack_crc)}")
        if n > 0:
            self.recurse_n_times(n - 1)
        self._stack_crc = crc32.crc_pop(self._stack_crc, n)
        print(f"Return {n}, CRC {hex(self._stack_crc)}")

    # Other types of methods to handle -- TODO
    def no_args(self):
        print("Hello from no_args")

    def setter(self):
        self.val = 42

    def complex_args(self, my_int, my_str, my_list, flag=True):
        if flag:
            self.val += my_int
            self.val += my_str.len()
            self.val += my_list.len()

x = Foo()
x.recurse_n_times(5)
x.get_crc()
