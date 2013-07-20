from .errors import BoundsError


__all__ = (
    'processor',
    'is_processor_generator',
    'check_bounds',
)


def processor(func):
    setattr(func, '_processor_generator', True)
    return func

def is_processor_generator(func):
    return getattr(func, '_processor_generator', False)

# pylint: disable=W0622
def check_bounds(data, min=None, max=None, exact=None):
    if exact is not None and data != exact:
        raise BoundsError('not', exact)
    else:
        if min is not None and min > data:
            raise BoundsError('below', min)
        if max is not None and max < data:
            raise BoundsError('above', max)

