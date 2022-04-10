"""
Example of how the CRC-based state hashing works for a simple class,
implemented manually.

The output of this file should be similar (but not exactly the same) as
ex_decorated.py, since the objects are turned into bytes a little
differently.
"""

import crc32

class Foo:
    def __init__(self):
        self._stack_crc = crc32.MAX_32
        self.val = 0

    def get_crc(self):
        return self._stack_crc ^ crc32.MAX_32

    def recurse_n_times(self, n):
        self._stack_crc = crc32.crc_push(self._stack_crc, n)
        print(f"Call {n}, CRC {hex(self._stack_crc)}")
        if n > 0:
            self.recurse_n_times(n - 1)
        self._stack_crc = crc32.crc_pop(self._stack_crc, n)
        print(f"Return, CRC {hex(self._stack_crc)}")

    # Other types of methods to handle -- TODO
    def no_args(self):
        # TODO: manual CRC update code
        print("Hello from no_args")
        print(f"Return, CRC {hex(self._stack_crc)}")

    def setter(self):
        # TODO: manual CRC update code
        self.val = 42
        print(f"Return, CRC {hex(self._stack_crc)}")

    def complex_args(self, my_int, my_str, my_list, flag=True):
        # TODO: manual CRC update code
        if flag:
            self.val += my_int
            self.val += len(my_str)
            self.val += len(my_list)
        print(f"Return, CRC {hex(self._stack_crc)}")

x = Foo()

x.recurse_n_times(5)

x.complex_args(1, "2", [3, 4, 5])
x.complex_args(6, "7", [], False)
x.complex_args(6, "7", [], flag=False)

# TODO
# x.no_args()
# x.setter()

x.get_crc()
