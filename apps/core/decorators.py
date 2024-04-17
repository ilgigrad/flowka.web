def timeit(method):
    """
    This decorator is very helpful
    if you need to improve the response time of one of then our views
    or if you just want to know how long it takes to run.
    """
   def timed(*args, **kw):
       ts = time.time()
       result = method(*args, **kw)
       te = time.time()
       print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te - ts))
       return result

   return timed


# The way to use this decorator is:
#@timeit
#def my_view(request):
#    ...
