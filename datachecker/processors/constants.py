from ..errors import InvalidError
from ..util import processor


__all__ = (
    'constant',
    'choice'
)


@processor
def constant(value):
    def constant_processor(data):
        if data != value:
            raise InvalidError(data)
        return data
    return constant_processor


@processor
def choice(*choices):
    def choice_processor(data):
        if data not in choices:
            raise InvalidError(data)
        return data
    return choice_processor

