I decided to write up some thoughts on python and pipelines, and see if you can give any feedback. This is a long message, in story format (explaining my thought processes), so be aware. There's not a good tl;dr for this.

I've been thinking about how pipelines could or should be implemented in Python for quite a while. I started with python-pipeline (now known as python-grapevine). Its an interesting idea, and I liked the idea of wrapping these objects in something else to make them use multiple processes. However, I felt limited by them. Also, it relies on operator overload, which means that there would be some conflict somewhere where the operator wasn't OK to use.

Really, I didn't want to have to reimplement every function I needed as a pipe object. Ideally, the functions that _already_ exist in the stdlib could be used as-is, or less desirably lightly-wrapped, and be available in a pipe-like fashion. I didn't feel like I could get that without syntactical extension to the language.

It seems to me that pipes are very much like functions that you call left-to-right instead of inner-to-outer. Consider this admittedly contrived example:

```python
sum(filter(lambda x: x % 5, filter(lambda x: x % 4, range(100))))
```

Personally, I find this annoying to understand. OK, so Pythonistas don't like ``lambda`` very much. Let's do it with generator expressions:

```python
sum(x for x in (x for x in range(100) if x % 4) if x % 5)
```

Wow, I'm not sure which is worse. It's all out of order to the way I'm _thinking_ about this problem. This is closer to what a pipeline should look like:

```
range(100) | filter(lambda x: x % 4) | filter(lambda x: x % 5) | sum()
```

Of course, this syntax doesn't, and won't ever, work in python, because the vertical bar is the bitwise-or operator. However, it does give an idea of what I'm looking for: things written in the same order they happen, and the same way that I'm thinking about them.

OK, now here's some thought on the different ways and possibilities for implementing this.

I figure that there is precedence for having an implicit first argument, specifically the ``.`` operator, which uses descriptors to pass in an implicit first argument (self) to the function or method. This implicit first argument is technically implemented using the descriptor protocol, yet I believe this is precedent for having similar behavior for these pipes.

At this point, I came up with 2 possibilities for the "pipeline operator". The first was borrowed from F#, which I believe got it from OCAML: ``|>``.

The second possibility attempted to play on the similarity between the ``.`` operator: ``..``

So the possibilities, as examples were:

```
range(100) |> filter(lambda x: x % 4) |> sum()
```

or

```
range(100) .. filter(lambda x: x % 4) .. sum()
```

I realized at this point that I'd need to deal with modules and classes of functions as well, so to help I'd consider a foo module/class that would contain these otherwise builtin functions, and rewrite the examples:

```
foo.range(100) |> foo.filter(lambda x: x % 4) |> foo.sum()
```

or

```
foo.range(100) .. foo.filter(lambda x: x % 4) .. foo.sum()
```

OK, I'm seeing that the ``..`` is perhaps a bit confusing, especially considering that ``...`` is the literal for the Ellipsis. That means that ``......`` could be an ambiguous combination of the Ellipsis literal, and these two operators. I'm not totally convinced that ``..`` is a terrible idea, but it seems like ``|>`` is probably better, so I'll continue with it for now.

At this point, it also becomes apparent that the operator isn't really limited to the ``|>``, because it must have the ``()`` or be an error. So, the operator is now ``|> ()``. At this point, the pipeline operator passes the result on the left in as the first operator in the () function call.

But now I have a problem again. Many of the stdlib functions that take iterators (the primary group for using pipelines) have the iterator not as the _first_ argument, but as the _last_.

For that, I came up with this sorta-solution: the pipeline protocol. The pipeline protocol defines a method on a callable, ``__pipe__(input, *args, **kwargs)``. The pipe operator ``|> ()`` would attempt to make the call using this magic method first, which would allow overriding which argument got the pipeline input, and then fall back to using the ``__call__`` method if ``__pipe__`` was not defined.

The main problem that I've found with this setup is that there is still some ambiguity regarding which call to add the extra argument to. For example, which call gets the pipeline input here, or is it an error:

```
foo.range(100) |> bar.baz().spam().eggs
```

If we defined it to be the first call after the ``|>``, then the above would be equivalent to

```
bar.baz(foo.range(100)).spam().eggs
```

If we defined it be be the last call (but before the next ``|>``), then it would be equivalent to

```
bar.baz().spam(foo.range(100)).eggs
```

If we said that the call had to be on the very last thing, right before any more ``|>``, if desired, then that syntax would throw an error. (I've never thought that an implicit call, even in this situation, would be a good idea)

This is the way it was left for quite a while, with this quandary only partially realized.

Then, recently, I came up with this idea:

```
foo.range(100) |> bar.baz().spam(*).eggs
```

Which, because of the explicit ``*`` mark, would unambiguously translate to:

```
bar.baz().spam(foo.range(100)).eggs
```

After all, explicit is better than implicit. Following that, I came up with several new options for the operator: ``|> (*)``, ``*> (*)``, ``|* (*)``. This also has the benefit of not needing a new ``__pipe__`` method, and just relying on plain old calling. An example, using the ``|* (*)`` syntax:

```
foo.range(100) |* bar.baz().spam(*).eggs
```

However, there is the potential for confusion (not ambiguity, but confusion), since the ``*`` already has meaning in the context of function calls. In function definitions the lone ``*`` means "gobble all the rest of the positional arguments", similar to how ``*args`` means "put all the rest of the positional arguments into the ``args`` variable.

Another possibility instead of ``*`` that I just came up with might be ``@``. The only other place this is used is in decorators, and decorators require it to be at the beginning of a line, and right before a def or class block. We could perhaps even also use it as the pipe operator, so that it could be ``@ (@)``. Example:

```
foo.range(100) @ bar.baz().spam(@).eggs
```

I'm not sure I like that. I think I like the ``|* (*)`` form better. I'm not sure, however whether I like this explicit form better, or the pipe protocol (using ``__pipe__``) better.
