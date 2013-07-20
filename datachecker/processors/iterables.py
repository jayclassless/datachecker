from ..errors import DataTypeError
from ..util import processor, check_bounds


__all__ = (
    'length',
)


# pylint: disable=W0622
@processor
def length(min=None, max=None, exact=None):
    def length_processor(data):
        try:
            data_length = len(data)
        except TypeError:
            raise DataTypeError('iterable')

        check_bounds(data_length, min=min, max=max, exact=exact)

        return data
    return length_processor

