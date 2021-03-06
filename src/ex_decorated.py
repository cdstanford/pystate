"""
Example of how the CRC-based state hashing works for a simple class,
using the automated decorator.
"""

import pystate
# Additional module import for threading.Lock(), an
# example of an unpicklable object
import threading

class Foo(pystate.TrackState):
    # Note: replace with @pystate.track_init to disable debug print info
    @pystate.track_init_print_stack_calls
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

    @pystate.track_stack_calls
    def return_val(self):
        return self.val

    # Note: @pystate.track_stack_calls can't be used on class methods.
    @staticmethod
    def sum(a, b):
        return a + b

x = Foo(3, kw_1=0)

x.recurse_n_times(5)

print("* Should be 0: {}".format(x.return_val()))

x.complex_args(1, "2", [3, 4, 5])
x.complex_args(6, "7", [], False)
x.complex_args(6, "7", [], flag=False)

print("* Should be 5: {}".format(x.return_val()))

x.setter()
x.setter()

print("* Should be 42: {}".format(x.return_val()))

x.no_args()

x.call_no_args()

print("* Should be 5: {}".format(Foo.sum(2, 3)))

print("Final CRC: {}".format(hex(x.get_crc())))
