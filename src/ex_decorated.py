"""
Example of how the CRC-based state hashing works for a simple class,
using an automated decorator.

The output of this file should be the same as ex_manual.py.

Note: the decorators only output in debug mode.
Running with python3 -O ex_decorated.py gives no output.
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
