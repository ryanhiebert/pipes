def pipe(*args):
    """Returns a pipe-enabled function"""

    def pipemethod(arg, kwarg):
        def ret(self):
            return (arg, kwarg)
        return ret

    if len(args) > 2:
        raise ValueError('Too many arguments')
    elif len(args) == 2:
        # args must be a (int,str) tuple
        if args[0] != None and not isinstance(int, args[0]):
            raise ValueError('First Argument was not an int')
        if args[1] != None and not isinstance(basestring, args[1]):
            raise ValueError('Second Argument was not a str')
        def wrapper(fun):
            fun.__pipe__ = pipemethod(args[0], args[1])
        return wrapper
    elif len(args) == 1:
        if isinstance(int, args[0]):
            def wrapper(fun):
                fun__pipe__ = pipemethod(args[0], None)
            return wrapper
        if isinstance(basestring, args[0]):
            def wrapper(fun):
                fun.__pipe__ = pipemethod(None, args[0])
            return wrapper
        else:
            args[0].__pipe__ = pipemethod(0, None)
            return args[0]
