from ..errors import DataRequiredError, ShortCircuitSignal
from ..util import processor


__all__ = (
    'required',
    'optional',
)


@processor
def required():
    def required_processor(data):
        if data is None:
            raise DataRequiredError()
        return data
    return required_processor


@processor
def optional(default=None):
    def optional_processor(data):
        if data is None:
            signal = ShortCircuitSignal()
            signal.data = default
            raise signal
        return data
    return optional_processor

