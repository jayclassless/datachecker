import re

from urlparse import urlparse

from .regex import match
from ..errors import DataTypeError, DataError
from ..util import processor


__all__ = (
    'email',
    'url',
)


# Borrowed from Django, https://github.com/django/django/blob/master/django/core/validators.py
email_re =  r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*" \
            r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"' \
            r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)' \
            r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$'

@processor
def email(check_dns=False):
    email_match = match(email_re, options=re.IGNORECASE)

    if check_dns:
        import dns.resolver

    def email(data):
        try:
            local_part, domain = data.split(u'@', 1)
        except AttributeError:
            raise DataTypeError('string')
        except ValueError:
            raise DataError(data)

        try:
            domain_ascii = domain.encode('idna')
        except UnicodeError:
            raise DataError(data)
        data_ascii = '%s@%s' % (local_part, domain_ascii)
        email_match(data_ascii)

        if check_dns:
            try:
                answer = dns.resolver.query(domain_ascii, 'MX')
            except dns.resolver.NXDOMAIN:
                # Domain doesn't exist.
                raise DataError(data)
            except dns.resolver.NoAnswer:
                # Domain exists, but no MX records, try for an A.
                try:
                    answer = dns.resolver.query(domain_ascii, 'A')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    # No A record either; domain not suitable for email.
                    raise DataError(data)
                except:
                    # Either a timeout or a DNS server error occurred. Not indicative
                    # of a bad domain. Assume good.
                    pass
            except:
                # Either a timeout or a DNS server error occurred. Not indicative
                # of a bad domain. Assume good.
                pass

        return data
    return email


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

