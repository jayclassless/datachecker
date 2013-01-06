from ..errors import DataTypeError
from ..util import processor


__all__ = (
    'lower',
    'upper',
    'strip',
)


@processor
def lower():
    def lower(data):
        try:
            return data.lower()
        except AttributeError:
            raise DataTypeError('string')
    return lower


@processor
def upper():
    def upper(data):
        try:
            return data.upper()
        except AttributeError:
            raise DataTypeError('string')
    return upper


@processor
def strip(left=True, right=True, chars=None):
    def strip(data):
        try:
            if left and right:
                return data.strip(chars)
            elif left:
                return data.lstrip(chars)
            elif right:
                return data.rstrip(chars)
            else:
                return data
        except AttributeError:
            raise DataTypeError('string')
    return strip

