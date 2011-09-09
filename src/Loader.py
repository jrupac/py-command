class Loader():
    def __init__(self, end, every):
        self.end = end / every - 1
        self.every = every
        self.progress = '='
    
    def __call__(self, i):
        if not i % self.every:
            return
        print '\x1b[1A',
        print '[' + self.progress * (i/2) + ' ' * (self.end - (i/2)) + ']'

