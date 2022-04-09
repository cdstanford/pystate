"""
Some basic tests for how decorators work with argument lists.

This file is not part of the relevant source code.
"""

def print_args(f):
    def wrapper(*args, **kwargs):
        print(f"Args: {args}, Kwargs: {kwargs}")
        return f(*args, **kwargs)
    return wrapper

@print_args
def add(a, b):
    return a + b

print("=== First example ===")
print(f"2 + 2 = {add(2, 2)}")
print(f"5 + 7 = {add(5, 7)}")
print(f"2 + 3 = {add(a=2, b=3)}")
print(f"2 + 3 = {add(2, b=3)}")
print(f"2 + 3 = {add(2, 3)}")

def add_defaults(a=None, b=None):
    if a and b:
        return a + b
    else:
        return None

print("=== Second example ===")
print(f"2 + 3 = {add_defaults(a=2, b=3)}")
print(f"2 + 3 = {add_defaults(2, b=3)}")
print(f"2 + 3 = {add_defaults(2, 3)}")
print(f"None + None = {add_defaults(None, None)}")
print(f"default + default = {add_defaults()}")
print(f"2 + default = {add_defaults(2)}")
print(f"None + 3 = {add_defaults(None, 3)}")
