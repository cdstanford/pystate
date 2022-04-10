"""
Example of how the CRC-based state hashing works for a simple class,
using an automated decorator.

The output of this file should be similar (but not exactly the same) as
ex_manual.py, since the objects are turned into bytes a little
differently.

Note: the decorators only output in debug mode.
Running with python3 -O ex_decorated.py gives no output.
"""

import crc32

class Foo(crc32.TrackState):
    @crc32.track_init
    def __init__(self):
        self.val = 0

    @crc32.track_stack_calls
    def recurse_n_times(self, n):
        if n > 0:
            self.recurse_n_times(n - 1)

    @crc32.track_stack_calls
    def complex_args(self, my_int, my_str, my_list, flag=True):
        if flag:
            self.val += my_int
            self.val += len(my_str)
            self.val += len(my_list)

    @crc32.track_stack_calls
    def setter(self):
        self.val = 42

    @crc32.track_stack_calls
    def no_args(self):
        pass

    @crc32.track_stack_calls
    def call_no_args(self):
        self.no_args()

x = Foo()

x.recurse_n_times(5)

x.complex_args(1, "2", [3, 4, 5])
x.complex_args(6, "7", [], False)
x.complex_args(6, "7", [], flag=False)

x.setter()
x.setter()

x.no_args()

x.call_no_args()

x.get_crc()
