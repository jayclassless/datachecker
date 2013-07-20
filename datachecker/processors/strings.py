import re

from ..errors import DataTypeError
from ..util import processor


__all__ = (
    'lower',
    'upper',
    'strip',
    'title',
    'swapcase',
    'capitalize',
)


@processor
def lower():
    def lower_processor(data):
        try:
            return data.lower()
        except AttributeError:
            raise DataTypeError('string')
    return lower_processor


@processor
def upper():
    def upper_processor(data):
        try:
            return data.upper()
        except AttributeError:
            raise DataTypeError('string')
    return upper_processor


@processor
def strip(left=True, right=True, chars=None):
    def strip_processor(data):
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
    return strip_processor


@processor
def title():
    mask = re.compile(r"[A-Za-z]+('[A-Za-z]+)?", flags=re.UNICODE)

    def title_processor(data):
        try:
            return mask.sub(
                lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),
                data
            )
        except TypeError:
            raise DataTypeError('string')

    return title_processor


@processor
def swapcase():
    def swapcase_processor(data):
        try:
            return data.swapcase()
        except AttributeError:
            raise DataTypeError('string')
    return swapcase_processor


@processor
def capitalize():
    def capitalize_processor(data):
        try:
            return data.capitalize()
        except AttributeError:
            raise DataTypeError('string')
    return capitalize_processor

