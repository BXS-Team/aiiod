import functools


def singleton(cls):
    ''' Use class as singleton. '''

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


def ignore_errors(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        try:
            fn(*args, **kw)
        except Exception:
            pass

    return wrapper