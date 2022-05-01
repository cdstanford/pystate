"""
WARNING: this file is probably not what you want.
See ex_decorated.py for the correct usage of the module.

Example of how the CRC-based state hashing could be *implemented manually*
for a simple class.

The output of this file should be similar (but not exactly the same) as
ex_decorated.py, since the objects are turned into bytes a little
differently.
"""

import pystate

class Foo:
    def __init__(self):
        self._stack_crc = pystate.MAX_32
        self.val = 0

    def get_crc(self):
        full_crc = pystate.crc_push(self._stack_crc, self.val)
        return full_crc ^ pystate.MAX_32

    def recurse_n_times(self, n):
        self._stack_crc = pystate.crc_push(self._stack_crc, n)
        print("Call recurse_n_times {}, CRC {}".format(n, hex(self.get_crc())))
        if n > 0:
            self.recurse_n_times(n - 1)
        self._stack_crc = pystate.crc_pop(self._stack_crc, n)
        print("Return, CRC {}".format(hex(self.get_crc())))

    def complex_args(self, my_int, my_str, my_list, flag=True):
        # 201 is an arbitrary value (identifier for the method)
        # Likewise for the remaining methods in this file
        self._stack_crc = pystate.crc_push(self._stack_crc, 201)
        print("Call complex_args, CRC {}".format(hex(self.get_crc())))
        if flag:
            self.val += my_int
            self.val += len(my_str)
            self.val += len(my_list)
        self._stack_crc = pystate.crc_pop(self._stack_crc, 201)
        print("Return, CRC {}".format(hex(self.get_crc())))

    def setter(self):
        self._stack_crc = pystate.crc_push(self._stack_crc, 202)
        print("Call setter, CRC {}".format(hex(self.get_crc())))
        self.val = 42
        self._stack_crc = pystate.crc_pop(self._stack_crc, 202)
        print("Return, CRC {}".format(hex(self.get_crc())))

    def no_args(self):
        self._stack_crc = pystate.crc_push(self._stack_crc, 203)
        print("Call no_args, CRC {}".format(hex(self.get_crc())))
        self._stack_crc = pystate.crc_pop(self._stack_crc, 203)
        print("Return, CRC {}".format(hex(self.get_crc())))

    def call_no_args(self):
        self._stack_crc = pystate.crc_push(self._stack_crc, 204)
        print("Call call_no_args, CRC {}".format(hex(self.get_crc())))
        self.no_args()
        self._stack_crc = pystate.crc_pop(self._stack_crc, 204)
        print("Return, CRC {}".format(hex(self.get_crc())))

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
