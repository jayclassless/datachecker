from ..errors import DataRequiredError
from ..util import processor


__all__ = (
    'required',
    'optional',
)


@processor
def required():
    def required(data):
        if data is None:
            raise DataRequiredError()
        return data
    return required


@processor
def optional(default=None):
    def optional(data):
        if data is None:
            return default
        return data
    return optional

