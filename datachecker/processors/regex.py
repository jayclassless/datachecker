import re

from ..errors import FormatError, DataTypeError
from ..util import processor


__all__ = (
    'match',
    'alpha',
    'numeric',
    'alphanumeric',
    'replace',
    'collapse_whitespace',
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
    return match(r'^[^\W\d_]+$', options=re.UNICODE)


@processor
def numeric():
    return match(r'^\d+$', options=re.UNICODE)


@processor
def alphanumeric():
    return match(r'^[^\W_]+$', options=re.UNICODE)


@processor
def replace(regex, replacement, options=0):
    mask = re.compile(regex, options)

    def replace_processor(data):
        try:
            return mask.sub(replacement, data)
        except TypeError:
            raise DataTypeError('string')
    return replace_processor


@processor
def collapse_whitespace():
    return replace(r'\s+', u' ', options=re.UNICODE)

