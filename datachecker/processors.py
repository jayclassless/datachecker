import __builtin__
import re

from decimal import Decimal, InvalidOperation

from .errors import *
from .util import processor


__all__ = (
    'integer',
    'float',
    'decimal',
    'string',
    'boolean',

    'length',

    'constant',
    'choice',

    'lower',
    'upper',
    'strip',

    'match',
    'alpha',
    'numeric',
    'alphanumeric',
)


def _check_bounds(data, min, max):
    if min is not None and min > data:
        raise BoundsError('below', min)
    if max is not None and max < data:
        raise BoundsError('above', max)


@processor
def integer(coerce=False, min=None, max=None):
    def integer(data):
        if data is None and coerce:
            data = 0
        elif not isinstance(data, (int, long)) and not coerce:
            raise DataTypeError('integer')
        else:
            try:
                data = int(data)
            except (ValueError, TypeError):
                if isinstance(data, basestring):
                    # int() won't convert floats that are strings, so try float()ing them first
                    try:
                        data = int(__builtin__.float(data))
                    except (ValueError, TypeError):
                        raise DataTypeError('integer')
                else:
                    raise DataTypeError('integer')

        _check_bounds(data, min, max)

        return data

    return integer


@processor
def float(coerce=False, min=None, max=None):
    def float(data):
        if data is None and coerce:
            data = 0.0
        elif not isinstance(data, __builtin__.float) and not coerce:
            raise DataTypeError('float')
        else:
            try:
                data = __builtin__.float(data)
            except (ValueError, TypeError):
                raise DataTypeError('float')

        _check_bounds(data, min, max)

        return data

    return float


@processor
def decimal(coerce=False, min=None, max=None):
    def decimal(data):
        if data is None and coerce:
            data = Decimal('0.0')
        elif not isinstance(data, Decimal) and not coerce:
            raise DataTypeError('decimal')
        else:
            try:
                data = Decimal(unicode(data))
            except (ValueError, TypeError, InvalidOperation):
                raise DataTypeError('decimal')

        _check_bounds(data, min, max)

        return data

    return decimal


@processor
def string(coerce=False):
    def string(data):
        if data is None and coerce:
            data = unicode('')
        elif not isinstance(data, basestring) and not coerce:
            raise DataTypeError('string')
        elif isinstance(data, (dict, list, tuple)):
            raise DataTypeError('string')
        else:
            data = unicode(data)

        return data

    return string


@processor
def boolean(coerce=False):
    def boolean(data):
        if data is None and coerce:
            data = False
        elif not isinstance(data, bool) and not coerce:
            raise DataTypeError('boolean')
        else:
            data = unicode(data).strip().lower()
            if data in ('true', 'yes', 'y', '1', 'on'):
                return True
            elif data in ('false', 'no', 'n', '0', 'off'):
                return False
            else:
                raise DataTypeError('boolean')

    return boolean


@processor
def length(min=None, max=None, exact=None):
    def length(data):
        try:
            l = len(data)
        except TypeError:
            raise DataTypeError('iterable')

        if exact is not None and l != exact:
            raise BoundsError('not', exact)
        else:
            _check_bounds(l, min, max)

        return data

    return length


@processor
def constant(value):
    def constant(data):
        if data != value:
            raise DataError(data)
        return data
    return constant


@processor
def choice(*choices):
    def choice(data):
        if data not in choices:
            raise DataError(data)
        return data
    return choice


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

