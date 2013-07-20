import __builtin__

from ..checker import Checker
from ..errors import CheckerError, DataTypeError, DictionaryError, \
    ExtraDataError
from ..util import processor


__all__ = (
    'list',
    'tuple',
    'dict',
)


# pylint: disable=W0622
@processor
def list(*processors, **options):
    coerce_ = options.get('coerce', False)

    checker = Checker(*processors)

    def list_processor(data):
        if not isinstance(data, __builtin__.list) and not coerce_:
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

    return list_processor


# pylint: disable=W0622
@processor
def tuple(*processors, **options):
    coerce_ = options.get('coerce', False)

    checker = Checker(*processors)

    def tuple_processor(data):
        if not isinstance(data, __builtin__.tuple) and not coerce_:
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

    return tuple_processor


# pylint: disable=R0912,W0622
@processor
def dict(structure, **options):
    coerce_ = options.get('coerce', False)
    ignore_extra = options.get('ignore_extra', False)
    ignore_missing = options.get('ignore_missing', False)
    pass_extra = options.get('pass_extra', False)
    capture_all_errors = options.get('capture_all_errors', False)

    procs = {}
    for name, processors in structure.items():
        if not isinstance(processors, (__builtin__.list, __builtin__.tuple)):
            processors = [processors]
        # pylint: disable=W0142
        procs[name] = Checker(*processors)

    def dict_processor(data):
        if not isinstance(data, __builtin__.dict) and not coerce_:
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
                    ex.field = name
                    raise ex

        if not ignore_missing:
            for name in (set(procs.keys()) - seen):
                try:
                    cleandata[name] = procs[name].process(None)
                except CheckerError as ex:
                    if capture_all_errors:
                        errors[name] = unicode(ex)
                    else:
                        ex.field = name
                        raise ex

        if errors:
            raise DictionaryError(errors)

        return cleandata

    return dict_processor

