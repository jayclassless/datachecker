import socket

from ..errors import FormatError, DataTypeError
from ..util import processor


__all__ = (
    'ip',
)


# pylint: disable=C0103
@processor
def ip(ipv4=True, ipv6=socket.has_ipv6):

    if ipv6 and not socket.has_ipv6:
        raise ValueError('IPv6 is not supported by this platform')

    def ip_processor(data):
        if ipv4:
            try:
                socket.inet_pton(socket.AF_INET, data)
            except TypeError:
                raise DataTypeError('string')
            except socket.error:
                if not ipv6:
                    raise FormatError(data)
            else:
                return data

        if ipv6:
            try:
                socket.inet_pton(socket.AF_INET6, data)
            except TypeError:
                raise DataTypeError('string')
            except socket.error:
                raise FormatError(data)
            else:
                return data

        return data
    return ip_processor

