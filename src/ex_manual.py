"""
Example of how the CRC-based state hashing works for a simple class,
implemented manually.

NOTE: this file is just for reference. See ex_decorated.py for
the correct usage of the module.

The output of this file should be similar (but not exactly the same) as
ex_decorated.py, since the objects are turned into bytes a little
differently.

This file is unfinished.
"""

import pystate

class Foo:
    def __init__(self):
        self._stack_crc = pystate.MAX_32
        self.val = 0

    def get_crc(self):
        return self._stack_crc ^ pystate.MAX_32

    def recurse_n_times(self, n):
        self._stack_crc = pystate.crc_push(self._stack_crc, n)
        print("Call {}, CRC {}".format(n, hex(self._stack_crc)))
        if n > 0:
            self.recurse_n_times(n - 1)
        self._stack_crc = pystate.crc_pop(self._stack_crc, n)
        print("Return, CRC {}".format(hex(self._stack_crc)))

    def complex_args(self, my_int, my_str, my_list, flag=True):
        # TODO: manual CRC update code
        if flag:
            self.val += my_int
            self.val += len(my_str)
            self.val += len(my_list)
        print("Return, CRC {}".format(hex(self._stack_crc)))

    def setter(self):
        # TODO: manual CRC update code
        self.val = 42
        print("Return, CRC {}".format(hex(self._stack_crc)))

    def no_args(self):
        # TODO: manual CRC update code
        print("Return, CRC {}".format(hex(self._stack_crc)))

    def call_no_args(self):
        # TODO: manual CRC update code
        self.no_args()
        print("Return, CRC {}".format(hex(self._stack_crc)))

x = Foo()

x.recurse_n_times(5)

x.complex_args(1, "2", [3, 4, 5])
x.complex_args(6, "7", [], False)
x.complex_args(6, "7", [], flag=False)

x.setter()
x.setter()

x.no_args()

x.call_no_args()

print("Final CRC: {}".format(hex(x.get_crc())))
