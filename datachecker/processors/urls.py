import re

from urlparse import urlparse

from .regex import match
from ..errors import DataTypeError, FormatError, InvalidError
from ..util import processor


__all__ = (
    'email',
    'url',
)


# Borrowed from Django:
# https://github.com/django/django/blob/1.5.1/django/core/validators.py#L98
EMAIL_RE = r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+" \
    r"(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*" \
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|' \
    r'\\[\001-\011\013\014\016-\177])*"' \
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+' \
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)' \
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)' \
    r'(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$'


@processor
def email(check_dns=False):
    email_match = match(EMAIL_RE, options=re.IGNORECASE)

    if check_dns:
        import dns.resolver

    def email_processor(data):
        try:
            local_part, domain = data.split(u'@', 1)
        except AttributeError:
            raise DataTypeError('string')
        except ValueError:
            raise FormatError(data)

        try:
            domain_ascii = domain.encode('idna')
        except UnicodeError:
            raise FormatError(data)
        data_ascii = '%s@%s' % (local_part, domain_ascii)
        email_match(data_ascii)

        if check_dns:
            try:
                dns.resolver.query(domain_ascii, 'MX')
            except dns.resolver.NXDOMAIN:
                # Domain doesn't exist.
                raise InvalidError(data)
            except dns.resolver.NoAnswer:
                # Domain exists, but no MX records, try for an A.
                try:
                    dns.resolver.query(domain_ascii, 'A')
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    # No A record either; domain not suitable for email.
                    raise InvalidError(data)
                except:
                    # Either a timeout or a DNS server error occurred.
                    # Not indicative of a bad domain. Assume good.
                    pass
            except:
                # Either a timeout or a DNS server error occurred.
                # Not indicative of a bad domain. Assume good.
                pass

        return data
    return email_processor


@processor
def url(schemes=None):
    def url_processor(data):
        try:
            parsed = urlparse(data)
        except AttributeError:
            raise DataTypeError('string')

        if parsed.scheme \
                and (parsed.netloc or parsed.path) \
                and (not schemes or parsed.scheme in schemes):
            return data
        else:
            raise FormatError(data)
    return url_processor

