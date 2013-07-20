import __builtin__

from decimal import Decimal, InvalidOperation

from ..errors import DataTypeError
from ..util import processor, check_bounds


__all__ = (
    'integer',
    'float',
    'decimal',
    'string',
    'boolean',
)


# pylint: disable=W0622
@processor
def integer(coerce=False, min=None, max=None):
    def integer_processor(data):
        if not isinstance(data, (int, long)) and not coerce:
            raise DataTypeError('integer')
        else:
            try:
                data = int(data)
            except (ValueError, TypeError):
                if isinstance(data, basestring):
                    # int() won't convert floats that are strings,
                    # so try float()ing them first
                    try:
                        data = int(__builtin__.float(data))
                    except (ValueError, TypeError):
                        raise DataTypeError('integer')
                else:
                    raise DataTypeError('integer')

        check_bounds(data, min=min, max=max)

        return data

    return integer_processor


# pylint: disable=W0622
@processor
def float(coerce=False, min=None, max=None):
    def float_processor(data):
        if not isinstance(data, __builtin__.float) and not coerce:
            raise DataTypeError('float')
        else:
            try:
                data = __builtin__.float(data)
            except (ValueError, TypeError):
                raise DataTypeError('float')

        check_bounds(data, min=min, max=max)

        return data

    return float_processor


# pylint: disable=W0622
@processor
def decimal(coerce=False, min=None, max=None):
    def decimal_processor(data):
        if not isinstance(data, Decimal) and not coerce:
            raise DataTypeError('decimal')
        else:
            try:
                data = Decimal(unicode(data))
            except (ValueError, TypeError, InvalidOperation):
                raise DataTypeError('decimal')

        check_bounds(data, min=min, max=max)

        return data

    return decimal_processor


# pylint: disable=W0622
@processor
def string(coerce=False):
    def string_processor(data):
        if not isinstance(data, basestring) and not coerce:
            raise DataTypeError('string')
        elif isinstance(data, (dict, list, tuple, type(None))):
            raise DataTypeError('string')
        else:
            data = unicode(data)

        return data

    return string_processor


# pylint: disable=W0622
@processor
def boolean(coerce=False):
    def boolean_processor(data):
        if not isinstance(data, bool) and not coerce:
            raise DataTypeError('boolean')
        else:
            data = unicode(data).strip().lower()
            if data in ('true', 'yes', 'y', '1', 'on'):
                return True
            elif data in ('false', 'no', 'n', '0', 'off'):
                return False
            else:
                raise DataTypeError('boolean')

    return boolean_processor

