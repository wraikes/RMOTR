from functools import reduce

def add(*args):
    # your implementation here
    return sum(args)

def subtract(*args):
    # your implementation here
    return reduce(lambda x, y: x-y, args)

def multiply(*args):
    # your implementation here
    return reduce(lambda x, y: x*y, args)

def divide(*args):
    # your implementation here
    return reduce(lambda x, y: x/y, args)

def plot(*args):
    # OPTIONAL EXTRA CREDIT FUNCTION! 
    # See README for info.
    pass

# add your custom operations here
