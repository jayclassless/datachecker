from urlparse import urlparse

from ..errors import DataTypeError, DataError
from ..util import processor


__all__ = (
    'url',
)


@processor
def url(schemes=None):
    def url(data):
        try:
            parsed = urlparse(data)
        except AttributeError:
            raise DataTypeError('string')

        if parsed.scheme and (parsed.netloc or parsed.path) and (not schemes or parsed.scheme in schemes):
            return data
        else:
            raise DataError(data)
    return url

