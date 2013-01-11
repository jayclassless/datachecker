from ..errors import DataTypeError
from ..util import processor, check_bounds


__all__ = (
    'length',
)


@processor
def length(min=None, max=None, exact=None):
    def length(data):
        try:
            l = len(data)
        except TypeError:
            raise DataTypeError('iterable')

        check_bounds(l, min=min, max=max, exact=exact)

        return data
    return length

