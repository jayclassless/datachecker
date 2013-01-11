from ..errors import InvalidError
from ..util import processor


__all__ = (
    'constant',
    'choice'
)


@processor
def constant(value):
    def constant(data):
        if data != value:
            raise InvalidError(data)
        return data
    return constant


@processor
def choice(*choices):
    def choice(data):
        if data not in choices:
            raise InvalidError(data)
        return data
    return choice

