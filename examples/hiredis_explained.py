# python -m pip install hiredis

"""
However, there’s also a C library, Hiredis, that contains 
a fast parser that can offer significant speedups for some 
Redis commands such as LRANGE. You can think of Hiredis as 
an optional accelerator that it doesn’t hurt to 
have around in niche cases.

The nice thing is that you don’t really need to call hiredis 
yourself. Just pip install it, and this will let redis-py 
see that it’s available and use its HiredisParser 
instead of PythonParser.

...

# redis/utils.py
try:
    import hiredis
    HIREDIS_AVAILABLE = True
except ImportError:
    HIREDIS_AVAILABLE = False


# redis/connection.py
if HIREDIS_AVAILABLE:
    DefaultParser = HiredisParser
else:
    DefaultParser = PythonParser

"""

