import re

from ..errors import FormatError, DataTypeError
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
    def match_processor(data):
        try:
            if pattern.match(data):
                return data
            else:
                raise FormatError(data)
        except TypeError:
            raise DataTypeError('string')
    return match_processor


@processor
def alpha():
    return match(r'^[^\W\d_]*$', options=re.UNICODE)


@processor
def numeric():
    return match(r'^\d*$', options=re.UNICODE)


@processor
def alphanumeric():
    return match(r'^[^\W_]*$', options=re.UNICODE)

