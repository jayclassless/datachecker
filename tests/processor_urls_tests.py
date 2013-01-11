# -*- coding: utf-8 -*-

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
        yield check_url_bad, input, schemes, dc.FormatError
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



GOOD_EMAIL_TESTS = (
    ('person@example.com', False),
    ('person@exam-ple.com', False),
    ('person@exam--ple.com', False),

    ('foo@gmail.com', True),
    ('foo@yahoo.com', True),
    ('foo@example.com', True),

    # http://idn.icann.org/E-mail_test
    (u'mailtest@مثال.إختبار', False),
    (u'mailtest@例子.测试', False),
    (u'mailtest@例子.測試', False),
    (u'mailtest@παράδειγμα.δοκιμή', False),
    (u'mailtest@उदाहरण.परीक्षा', False),
    (u'mailtest@例え.テスト', False),
    (u'mailtest@실례.테스트', False),
    (u'mailtest@مثال.آزمایشی', False),
    (u'mailtest@пример.испытание', False),
    (u'mailtest@உதாரணம்.பரிட்சை', False),
    (u'mailtest@בײַשפּיל.טעסט', False),
    (u'mailtest@xn--mgbh0fb.xn--kgbechtv', False),
    (u'mailtest@xn--fsqu00a.xn--0zwm56d', False),
    (u'mailtest@xn--fsqu00a.xn--g6w251d', False),
    (u'mailtest@xn--hxajbheg2az3al.xn--jxalpdlp', False),
    (u'mailtest@xn--p1b6ci4b4b3a.xn--11b5bs3a9aj6g', False),
    (u'mailtest@xn--r8jz45g.xn--zckzah', False),
    (u'mailtest@xn--9n2bp8q.xn--9t4b11yi5a', False),
    (u'mailtest@xn--mgbh0fb.xn--hgbk6aj7f53bba', False),
    (u'mailtest@xn--e1afmkfd.xn--80akhbyknj4f', False),
    (u'mailtest@xn--zkc6cc5bi7f6e.xn--hlcj6aya9esc7a', False),
    (u'mailtest@xn--fdbk5d8ap9b8a8d.xn--deba0ad', False),
)

def test_email_good():
    for input, check_dns in GOOD_EMAIL_TESTS:
        yield check_email_good, input, check_dns

def check_email_good(input, check_dns):
    checker = dc.Checker(dc.email(check_dns=check_dns))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


BAD_EMAIL_TESTS = (
    ('', False, dc.FormatError),
    ('foo', False, dc.FormatError),
    ('foo@bar', False, dc.FormatError),
    ('', True, dc.FormatError),
    ('foo', True, dc.FormatError),
    ('foo@bar', True, dc.FormatError),

    ('person@example-.com', False, dc.FormatError),
    ('person@-example.com', False, dc.FormatError),
    ('person@exam-.ple-.com', False, dc.FormatError),
    ('person@exam-.-ple.com', False, dc.FormatError),
    ('person@.com', False, dc.FormatError),
    ('person@example-.com', True, dc.FormatError),
    ('person@-example.com', True, dc.FormatError),
    ('person@exam-.ple-.com', True, dc.FormatError),
    ('person@exam-.-ple.com', True, dc.FormatError),
    ('person@.com', True, dc.FormatError),

    ('foo@sdkjhldkshfslkdjhdslkjhdlksfhgdslgdf.com', True, dc.InvalidError),
    ('foo@as-d-asd-asd-asdasda-sd-asd-asd.net', True, dc.InvalidError),
)
BAD_EMAIL_TESTS2 = (
    (1, False),
    (1.23, False),
    (Decimal('1'), False),
    (True, False),
    (1, True),
    (1.23, True),
    (Decimal('1'), True),
    (True, True),
)

def test_email_bad():
    for input, check_dns, expected_exception in BAD_EMAIL_TESTS:
        yield check_email_bad, input, check_dns, expected_exception
    for input, check_dns in BAD_EMAIL_TESTS2:
        yield check_email_bad, input, check_dns, dc.DataTypeError

def check_email_bad(input, check_dns, expected_exception):
    checker = dc.Checker(dc.email(check_dns=check_dns))
    try:
        output = checker.process(input)
    except expected_exception:
        pass
    else:
        assert False, 'Got output of: %s' % output

