from decimal import Decimal

import datachecker as dc


GOOD_IP_TESTS = (
    ('127.0.0.1', True, False),
    ('127.0.0.1', True, True),
    ('1.2.3.4', True, False),
    ('1.2.3.4', True, True),

    ('2001:0db8:0000:0000:0000:ff00:0042:8329', False, True),
    ('2001:0db8:0000:0000:0000:ff00:0042:8329', True, True),
    ('2001:db8:0:0:0:ff00:42:8329', False, True),
    ('2001:db8:0:0:0:ff00:42:8329', True, True),
    ('2001:0db8::ff00:0042:8329', False, True),
    ('2001:0db8::ff00:0042:8329', True, True),
    ('2001:db8::ff00:42:8329', False, True),
    ('2001:db8::ff00:42:8329', True, True),
    ('0000:0000:0000:0000:0000:0000:0000:0001', False, True),
    ('0000:0000:0000:0000:0000:0000:0000:0001', True, True),
    ('0:0:0:0:0:0:0:1', False, True),
    ('0:0:0:0:0:0:0:1', True, True),
    ('::0001', False, True),
    ('::0001', True, True),
    ('::1', False, True),
    ('::1', True, True),

    ('127.0.0.1', False, False),
    ('1.2.3.4', False, False),
    ('2001:0db8:0000:0000:0000:ff00:0042:8329', False, False),
    ('2001:db8:0:0:0:ff00:42:8329', False, False),
    ('2001:0db8::ff00:0042:8329', False, False),
    ('2001:db8::ff00:42:8329', False, False),
    ('0000:0000:0000:0000:0000:0000:0000:0001', False, False),
    ('0:0:0:0:0:0:0:1', False, False),
    ('::0001', False, False),
    ('::1', False, False),
)

def test_ip_good():
    for input, ipv4, ipv6 in GOOD_IP_TESTS:
        yield check_ip_good, input, ipv4, ipv6

def check_ip_good(input, ipv4, ipv6):
    checker = dc.Checker(dc.ip(ipv4=ipv4, ipv6=ipv6))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


BAD_IP_TESTS = (
    ('', True, True),
    ('', True, False),
    ('', False, True),
    ('foo', True, True),
    ('foo', True, False),
    ('foo', False, True),

    ('127.0.0.1', False, True),
    ('1.2.3.4', False, True),

    ('2001:0db8:0000:0000:0000:ff00:0042:8329', True, False),
    ('2001:db8:0:0:0:ff00:42:8329', True, False),
    ('2001:0db8::ff00:0042:8329', True, False),
    ('2001:db8::ff00:42:8329', True, False),
    ('0000:0000:0000:0000:0000:0000:0000:0001', True, False),
    ('0:0:0:0:0:0:0:1', True, False),
    ('::0001', True, False),
    ('::1', True, False),
)
BAD_IP_TESTS2 = (
    (1, True, True),
    (1, True, False),
    (1, False, True),
    (1.23, True, True),
    (1.23, True, False),
    (1.23, False, True),
    (Decimal('1'), True, True),
    (Decimal('1'), True, False),
    (Decimal('1'), False, True),
    (True, True, True),
    (True, True, False),
    (True, False, True),
)

def test_ip_bad():
    for input, ipv4, ipv6 in BAD_IP_TESTS:
        yield check_ip_bad, input, ipv4, ipv6, dc.FormatError
    for input, ipv4, ipv6 in BAD_IP_TESTS2:
        yield check_ip_bad, input, ipv4, ipv6, dc.DataTypeError

def check_ip_bad(input, ipv4, ipv6, expected_exception):
    checker = dc.Checker(dc.ip(ipv4=ipv4, ipv6=ipv6))
    try:
        output = checker.process(input)
    except expected_exception:
        pass
    except Exception as ex:
        raise ex
    else:
        assert False, 'Got output of: %s' % output


GOOD_DOMAIN_TESTS = (
    ('google.com', False),
    ('www.google.com', False),
    ('asdasdasads.asdasdasasd.com', False),
    ('foobar.io', False),

    ('google.com', True),
    ('www.yahoo.com', True),
)


def test_domain_good():
    for input, check_dns in GOOD_DOMAIN_TESTS:
        yield check_domain_good, input, check_dns

def check_domain_good(input, check_dns):
    checker = dc.Checker(dc.domain(check_dns=check_dns))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


BAD_DOMAIN_TESTS = (
    ('', False, dc.FormatError),
    ('foo', False, dc.FormatError),
    ('fooba.r', False, dc.FormatError),
    ('', True, dc.FormatError),
    ('foo', True, dc.FormatError),
    ('fooba.r', True, dc.FormatError),

    ('example-.com', False, dc.FormatError),
    ('-example.com', False, dc.FormatError),
    ('exam-.ple-.com', False, dc.FormatError),
    ('exam-.-ple.com', False, dc.FormatError),
    ('.com', False, dc.FormatError),
    ('example-.com', True, dc.FormatError),
    ('-example.com', True, dc.FormatError),
    ('exam-.ple-.com', True, dc.FormatError),
    ('exam-.-ple.com', True, dc.FormatError),
    ('.com', True, dc.FormatError),

    ('sdkjhldkshfslkdjhdslkjhdlksfhgdslgdf.com', True, dc.InvalidError),
    ('as-d-asd-asd-asdasda-sd-asd-asd.net', True, dc.InvalidError),
)
BAD_DOMAIN_TESTS2 = (
    (1, False),
    (1.23, False),
    (Decimal('1'), False),
    (True, False),
    (1, True),
    (1.23, True),
    (Decimal('1'), True),
    (True, True),
)

def test_domain_bad():
    for input, check_dns, expected_exception in BAD_DOMAIN_TESTS:
        yield check_domain_bad, input, check_dns, expected_exception
    for input, check_dns in BAD_DOMAIN_TESTS2:
        yield check_domain_bad, input, check_dns, dc.DataTypeError

def check_domain_bad(input, check_dns, expected_exception):
    checker = dc.Checker(dc.domain(check_dns=check_dns))
    try:
        output = checker.process(input)
    except expected_exception:
        pass
    else:
        assert False, 'Got output of: %s' % output

