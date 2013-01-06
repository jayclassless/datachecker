from decimal import Decimal

import datachecker as dc


GOOD_URL_TESTS = (
    ('http://www.google.com', None),
    ('http://www.google.com', ['http', 'ftp']),
    ('mailto:foo@bar.com', None),
    ('mailto:foo@bar.com', ['http', 'mailto']),
    ('file:///foo.ext', None),
    ('file:///foo.ext', ['file', 'http']),
)

def test_url_good():
    for input, schemes in GOOD_URL_TESTS:
        yield check_url_good, input, schemes

def check_url_good(input, schemes):
    checker = dc.Checker(dc.url(schemes=schemes))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


BAD_URL_TESTS = (
    ('http://www.google.com', ['https', 'ftp']),
    ('foo', None),
    ('foo', ['foo', 'http']),
    ('http://', None),
    ('http://', ['http']),
    ('mailto:', None),
    ('mailto:', ['mailto']),
)
BAD_URL_TESTS2 = (
    (1, None),
    (1, ['http']),
    (1.23, None),
    (1.23, ['http']),
    (Decimal('1'), None),
    (Decimal('1'), ['http']),
    (True, None),
    (True, ['http']),
)

def test_url_bad():
    for input, schemes in BAD_URL_TESTS:
        yield check_url_bad, input, schemes, dc.DataError
    for input, schemes in BAD_URL_TESTS2:
        yield check_url_bad, input, schemes, dc.DataTypeError

def check_url_bad(input, schemes, expected_exception):
    checker = dc.Checker(dc.url(schemes=schemes))
    try:
        output = checker.process(input)
    except expected_exception:
        pass
    except Exception as ex:
        raise ex
    else:
        assert False, 'Got output of: %s' % output

