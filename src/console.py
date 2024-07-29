#
#   Author: Mamert Vonn G. Santelices
#   ID:     90026174
#
#   console.py
#
#

import sys

class Console:
    def __init__(self, is_log):
        self._is_log = is_log
        self._prev = ''
        self._end = None
        self._index = 0
    
    def log(self, *args, end=''):
        if self._is_log:
            print(*args, end=end)
    
    def success(self):
        if not self._is_log:
            return
        if self._prev:
            print('\b' * (len(self._prev)), "Successfully")
            self._prev = ''
            return
        print("\tSuccessfully")
    
    def fail(self):
        if not self._is_log:
            return
        if self._prev:
            print('\b' * (len(self._prev)), "Failed")
            self._prev = ''
            return
        print("\tFailed")

    def log_loading(self, *args, end=''):
        if not self._is_log:
            return
        self._index = 1
        self._end = None
        self._prev = '0'
        print(*args, "\t", self._prev, end=end)

    def log_loading_size_of(self, size : int, *args, end=''):
        if not self._is_log:
            return
        self._index = 1
        self._end = size
        self._prev = "0/" + str(size)
        print(*args, "\t", self._prev, end=end)
         
    def increment(self):
        if not self._is_log:
            return
        next = str(self._index) + '' if self._end is None else '/' + str(self._end)
        sys.stdout.write('\b' * len(self._prev) + next)
        sys.stdout.flush()
        self._prev = next
        self._index += 1