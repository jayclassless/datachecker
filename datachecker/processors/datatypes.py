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

        check_bounds(data, min=min, max=max)

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

        check_bounds(data, min=min, max=max)

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

        check_bounds(data, min=min, max=max)

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



