
def pipe(*args):
    """Returns a pipe-enabled function"""
    if len(args) > 2:
        raise ValueError('Too many arguments')
    elif len(args) == 2:
        # args must be a (int,str) tuple
        if args[0] != None and not isinstance(int, args[0]):
            raise ValueError('First Argument was not an int')
        if args[1] != None and not isinstance(basestring, args[1]):
            raise ValueError('Second Argument was not a str')
    elif len(args) == 1:
        if isinstance(int, args[0]):
            ### USE AS INT
        if isinstance(basestring, args[0]):
            ### USE AS STR
        else:
            ### WRAP THE FUNCTION WITH DEFAULT 0
