"""
Example of how the CRC-based state hashing works for a simple class,
using the automated decorator.

Note: the decorators only output text in debug mode.
So running with python3 -O ex_decorated.py gives no output.
"""

import pystate

# Additional module imports for examples of unpicklable objects
import threading # for threading.Lock()

class Foo(pystate.TrackState):
    @pystate.track_init
    def __init__(self, dummy_arg, kw_1=2, kw_2=3):
        self.val = 0
        self.dummy_arg = dummy_arg
        self.blah = 2
        self.unpicklable = threading.Lock()

    @pystate.track_stack_calls
    def recurse_n_times(self, n):
        if n > 0:
            self.recurse_n_times(n - 1)

    @pystate.track_stack_calls
    def complex_args(self, my_int, my_str, my_list, flag=True):
        if flag:
            self.val += my_int
            self.val += len(my_str)
            self.val += len(my_list)

    @pystate.track_stack_calls
    def setter(self):
        self.val = 42

    @pystate.track_stack_calls
    def no_args(self):
        pass

    @pystate.track_stack_calls
    def call_no_args(self):
        self.no_args()

x = Foo(3, kw_1=0)

x.recurse_n_times(5)

x.complex_args(1, "2", [3, 4, 5])
x.complex_args(6, "7", [], False)
x.complex_args(6, "7", [], flag=False)

x.setter()
x.setter()

x.no_args()

x.call_no_args()

print("Final CRC: {}".format(hex(x.get_crc())))
