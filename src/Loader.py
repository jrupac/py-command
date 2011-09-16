#!/usr/bin/env python

class Loader():
    def __init__(self, end, every):
        self.end = end / every - 1
        self.every = every
        self.progress = '='
    
    def _clear_line(self):
        ''' Clear one terminal line '''
        print '\x1b[1A',
    
    def __call__(self, i):
        ''' Print loader for the ith time '''
        if not i % self.every:
            return
        self._clear_line()
        print '[' + self.progress * (i/2) + ' ' * (self.end - (i/2)) + ']'

