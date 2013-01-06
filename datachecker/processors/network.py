import socket

from ..errors import DataError, DataTypeError
from ..util import processor


__all__ = (
    'ip',
)



@processor
def ip(ipv4=True, ipv6=socket.has_ipv6):

    if ipv6 and not socket.has_ipv6:
        raise ValueError('IPv6 is not supported by this platform')

    def ip(data):
        if ipv4:
            try:
                socket.inet_pton(socket.AF_INET, data)
            except TypeError:
                raise DataTypeError('string')
            except socket.error:
                if not ipv6:
                    raise DataError(data)
            else:
                return data

        if ipv6:
            try:
                socket.inet_pton(socket.AF_INET6, data)
            except TypeError:
                raise DataTypeError('string')
            except socket.error:
                raise DataError(data)
            else:
                return data

        return data
    return ip

