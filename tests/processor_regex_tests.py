from decimal import Decimal

import datachecker as dc


REGEX_GOOD_TESTS = (
    (dc.alpha, 'abc'),

    (dc.numeric, '123'),

    (dc.alphanumeric, 'abc'),
    (dc.alphanumeric, '123'),
    (dc.alphanumeric, 'abc123'),
    (dc.alphanumeric, '123abc'),
    (dc.alphanumeric, 'a1b2c3'),
)

def test_regex_good():
    for processor, input in REGEX_GOOD_TESTS:
        yield check_regex_good, processor, input

def check_regex_good(processor, input):
    checker = dc.Checker(processor)
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


REGEX_BAD_TESTS = (
    (dc.alpha, '123'),
    (dc.alpha, 'abc123'),
    (dc.alpha, 'abc '),
    (dc.alpha, '!abc'),
    (dc.alpha, 'a_b'),
    (dc.alpha, ''),

    (dc.numeric, 'abc'),
    (dc.numeric, 'abc123'),
    (dc.numeric, '123 '),
    (dc.numeric, '!123'),
    (dc.numeric, '1_2'),
    (dc.numeric, ''),

    (dc.alphanumeric, ' abc'),
    (dc.alphanumeric, ' 123'),
    (dc.alphanumeric, '!abc'),
    (dc.alphanumeric, '!123'),
    (dc.alphanumeric, 'a_c'),
    (dc.alphanumeric, ''),
)
REGEX_BAD_TESTS2 = (
    (dc.alpha, 123),
    (dc.alpha, 1.23),
    (dc.alpha, Decimal('1.23')),
    (dc.numeric, 123),
    (dc.numeric, 1.23),
    (dc.numeric, Decimal('1.23')),
    (dc.alphanumeric, 123),
    (dc.alphanumeric, 1.23),
    (dc.alphanumeric, Decimal('1.23')),
)

def test_regex_bad():
    for processor, input in REGEX_BAD_TESTS:
        yield check_regex_bad, processor, input, dc.FormatError
    for processor, input in REGEX_BAD_TESTS2:
        yield check_regex_bad, processor, input, dc.DataTypeError

def check_regex_bad(processor, input, expected_exception):
    checker = dc.Checker(processor)
    try:
        output = checker.process(input)
    except expected_exception:
        pass
    except Exception as ex:
        raise ex
    else:
        assert False, 'Got output of: %s' % output

