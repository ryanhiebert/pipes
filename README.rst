pipes
=====

Implementing iterator pipelines in python

Pipeline Protocol
=================
The pipeline protocol defines a new special property:

def __pipe__():
    """
    returns a tuple of (int, str) relating the arg for the pipeline.
    None is acceptable as exactly one of the tuples.
    If neither is there, should throw a NotImplemented Exception.
    If both are present, either should be appropriate to use, and
    should reference the same variable. Implementations will prefer to use
    the position, falling back to using the kwarg if there aren't enough
    positional args to make the difference.
    """

Pipeline Protocol (New Idea)
============================
The Pipeline Protocol defines a new special property:

def __pipe__(pipein, \*args, \*\*kwargs):
    """
    the method that will be called when the pipeline operator is used.
    The pipeline input will be the first argument, unless there is an
    implicit self argument. When used in a pipeline, the pipein
    argument will be passed in implicitly, similarly to a method call.
    """

For the sake of an example, we will demonstrate what this does with
the bitwise or operator, which will NOT be recommended for use as the
pipeline operator.

Here's an example pipeline:

range(10) | foo.bar().spam(3)

translates to:

foo.bar().spam.__pipe__(range(10), spam(3))

The pipe must end with a function call, else it is a syntax error.

Pipeline Decorator
==================
The pipeline decorator (@pipe) adds a __pipe__() method to a function.
It can be called in one of four ways:

@pipe
def fun():
    """The default decorator assumes arg 0 is the pipeline input"""

@pipe(1)
def fun():
    """You can also manually specify arg for pipeline input"""

@pipe('foo')
def fun():
    """Specify the kwarg for pipeline input using a str"""

@pipe(1, 'foo')
def fun():
    """Specify both the arg and kwarg. They must match, and the arg is first"""

Pipe class
==========
Until there is a pipeline operator native, an abused class will need to help.

calling methods of a Pipe instance look in the containing scope for functions,
and call the __pipe__() special method to determine how to pipeline the data.

The Pipe class also has a fallback to allow use of builtin python functions.
When a function doesn't have any __pipe__() method defined, Pipe assumes that 
the first argument is the pipeline.

The Pipe class also defines a 'r' attribute which reverses the assumption, 
and appending the pipeline to the argument list.

Additionally, because a we must return a Pipe in order to allow chaining, there
must be a final .sink() in order to retrieve the final output of the pipeline.

Proposed Pipeline operator
==========================
There is one place of precedent to having an inferred argument to a function 
call: with the '.' operator. Because of this, a new '..' operator seems like it
may be a reasonable choice. The : may also work, but has conflict with blocks.

The | and ^ are in use other places, so are not appropriate candidates for 
pipeline operator, despite their precident for use as a pipeline operator in 
some shells.
