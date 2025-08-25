import time
from itertools import chain

def current_timestamp():
    return int(time.time() * 1000)  # Get epoch time in milliseconds

def chain_errors(errors):
    return list(chain.from_iterable(errors))