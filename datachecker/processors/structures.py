import __builtin__

from ..checker import Checker
from ..errors import CheckerError, DataTypeError, DictionaryError, ExtraDataError
from ..util import processor


__all__ = (
    'list',
    'tuple',
    'dict',
)


@processor
def list(*processors, **options):
    coerce = options.get('coerce', False)

    checker = Checker(*processors)

    def list(data):
        if not isinstance(data, __builtin__.list) and not coerce:
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
        if not isinstance(data, __builtin__.tuple) and not coerce:
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


@processor
def dict(structure, **options):
    coerce = options.get('coerce', False)
    ignore_extra = options.get('ignore_extra', False)
    pass_extra = options.get('pass_extra', False)
    capture_all_errors = options.get('capture_all_errors', False)

    procs = {}
    for name, processors in structure.items():
        if not isinstance(processors, (__builtin__.list, __builtin__.tuple)):
            processors = [processors]
        procs[name] = Checker(*processors)

    def dict(data):
        if not isinstance(data, __builtin__.dict) and not coerce:
            raise DataTypeError('dict')
        else:
            try:
                data = __builtin__.dict(data)
            except (TypeError, ValueError):
                raise DataTypeError('dict')

        cleandata = {}
        errors = {}
        seen = set()
        for name, value in data.items():
            try:
                if name in procs:
                    cleandata[name] = procs[name].process(value)
                    seen.add(name)
                elif ignore_extra:
                    pass
                elif pass_extra:
                    cleandata[name] = value
                else:
                    raise ExtraDataError()
            except CheckerError as ex:
                if capture_all_errors:
                    errors[name] = unicode(ex)
                else:
                    raise

        for name in (set(procs.keys()) - seen):
            try:
                cleandata[name] = procs[name].process(None)
            except CheckerError as ex:
                if capture_all_errors:
                    errors[name] = unicode(ex)
                else:
                    raise

        if errors:
            raise DictionaryError(errors)

        return cleandata

    return dict

