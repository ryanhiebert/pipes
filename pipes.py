class Pipe(object):
    """A Pipe-enabled function wrapper"""

    def __init__(self, func, arg=None, kwarg=None):
        self.func = func
        self.arg = self.kwarg = None

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __pipe__(self, pipein, *args, **kwargs):
        if self.arg is not None:
            args = args[:self.arg] + (pipein,) + args[self.arg:]
        elif self.kwarg is not None:
            kwargs[self.kwarg] = pipein
        return self.func(*args, **kwargs)

def pipedecorator(*args):
    """a decorator to make a function a pipeable function"""
    if len(args) > 2:
        raise ValueError('Too many arguments')
    elif len(args) == 2:
        def wrapper(func):
            return Pipe(func, arg=args[0], kwarg=args[1])
        return wrapper
    elif len(args) == 1:
        if isinstance(args[0], int):
            def wrapper(func):
                return Pipe(func, arg=args[0])
            return wrapper
        elif isinstance(args[0], basestring):
            def wrapper(func):
                return Pipe(func, kwarg=args[0])
            return wrapper
        else:
            # This is doing the decorating
            return Pipe(args[0], arg=0)
    else:
        raise ValueError('Not enough argments')
