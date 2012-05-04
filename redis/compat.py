import sys

__all__ = ['basestring', 'bytes', 'imap', 'izip', 'long', 'unicode',
           'unichr', 'BytesIO', 'iterd', 'xrange']

MAJOR_VERSION = sys.version_info[0]

if MAJOR_VERSION >= 3:
    basestring = str
    bytes = bytes
    imap = map
    izip = zip
    long = int
    unichr = chr
    unicode = str
    xrange = range
    from io import BytesIO

    iterd = lambda d: d.items()
else:
    from itertools import imap, izip

    basestring = basestring
    try:
        bytes = bytes
    except NameError:
        bytes = str
    long = long
    unichr = unichr
    unicode = unicode
    unicode = unicode
    xrange = range

    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    BytesIO = StringIO

    iterd = lambda d: d.iteritems()
