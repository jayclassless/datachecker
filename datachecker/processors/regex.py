import re

from ..errors import DataError, DataTypeError
from ..util import processor


__all__ = (
    'match',
    'alpha',
    'numeric',
    'alphanumeric',
)


@processor
def match(regex, options=0):
    pattern = re.compile(regex, options)
    def match(data):
        try:
            if pattern.match(data):
                return data
            else:
                raise DataError(data)
        except TypeError:
            raise DataTypeError('string')
    return match


@processor
def alpha():
    return match(r'^[^\W\d_]*$', options=re.UNICODE)


@processor
def numeric():
    return match(r'^\d*$', options=re.UNICODE)


@processor
def alphanumeric():
    return match(r'^[^\W_]*$', options=re.UNICODE)
