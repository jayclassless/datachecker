import __builtin__

from ..checker import Checker
from ..errors import DataTypeError
from ..util import processor


__all__ = (
    'list',
    'tuple',
)


@processor
def list(*processors, **options):
    coerce = options.get('coerce', False)

    checker = Checker(*processors)

    def list(data):
        if data is None and coerce:
            data = []
        elif not isinstance(data, __builtin__.list) and not coerce:
            raise DataTypeError('list')
        else:
            if not isinstance(data, basestring):
                try:
                    data = __builtin__.list(data)
                except TypeError:
                    data = [data]
            else:
                data = [data]

        cleandata = []
        for element in data:
            cleandata.append(checker.process(element))
        return cleandata

    return list


@processor
def tuple(*processors, **options):
    coerce = options.get('coerce', False)

    checker = Checker(*processors)

    def tuple(data):
        if data is None and coerce:
            data = ()
        elif not isinstance(data, __builtin__.tuple) and not coerce:
            raise DataTypeError('tuple')
        else:
            if not isinstance(data, basestring):
                try:
                    data = __builtin__.tuple(data)
                except TypeError:
                    data = (data,)
            else:
                data = (data,)

        cleandata = []
        for element in data:
            cleandata.append(checker.process(element))
        return __builtin__.tuple(cleandata)

    return tuple

