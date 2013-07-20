import re
import socket

from .regex import match
from ..errors import FormatError, DataTypeError, InvalidError
from ..util import processor


__all__ = (
    'ip',
    'domain',
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


# Adapted from Django:
# https://github.com/django/django/blob/1.5.1/django/core/validators.py#L98
DOMAIN_RE = r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+' \
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)' \
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)' \
    r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$'


@processor
def domain(check_dns=False):
    domain_match = match(DOMAIN_RE, options=re.IGNORECASE)

    if check_dns:
        import dns.resolver

    def domain_processor(data):
        try:
            domain_ascii = data.encode('idna')
        except AttributeError:
            raise DataTypeError('string')
        except UnicodeError:
            raise FormatError(data)

        domain_match(domain_ascii)

        if check_dns:
            try:
                dns.resolver.query(domain_ascii, 'A')
            except dns.resolver.NXDOMAIN:
                raise InvalidError(data)
            except:
                pass

        return data
    return domain_processor

