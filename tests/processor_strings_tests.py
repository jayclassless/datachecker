from decimal import Decimal

import datachecker as dc


STRING_MANIP_GOOD_TESTS = (
    (dc.lower, 'FOO', 'foo'),
    (dc.lower, 'Foo', 'foo'),
    (dc.lower, 'foo', 'foo'),
    (dc.lower, '', ''),

    (dc.upper, 'FOO', 'FOO'),
    (dc.upper, 'Foo', 'FOO'),
    (dc.upper, 'foo', 'FOO'),
    (dc.upper, '', ''),

    (dc.strip, '  foo  ', 'foo'),
    (dc.strip, 'foo  ', 'foo'),
    (dc.strip, '  foo', 'foo'),
    (dc.strip, '  ', ''),
    (dc.strip, '', ''),
    (dc.strip(left=False), '  foo  ', '  foo'),
    (dc.strip(left=False), 'foo  ', 'foo'),
    (dc.strip(left=False), '  foo', '  foo'),
    (dc.strip(left=False), '  ', ''),
    (dc.strip(left=False), '', ''),
    (dc.strip(right=False), '  foo  ', 'foo  '),
    (dc.strip(right=False), 'foo  ', 'foo  '),
    (dc.strip(right=False), '  foo', 'foo'),
    (dc.strip(right=False), '  ', ''),
    (dc.strip(right=False), '', ''),
    (dc.strip(left=False, right=False), '  foo  ', '  foo  '),
    (dc.strip(left=False, right=False), 'foo  ', 'foo  '),
    (dc.strip(left=False, right=False), '  foo', '  foo'),
    (dc.strip(left=False, right=False), '  ', '  '),
    (dc.strip(left=False, right=False), '', ''),
)

def test_string_manip_good():
    for processor, input, expected in STRING_MANIP_GOOD_TESTS:
        yield check_string_manip_good, processor, input, expected

def check_string_manip_good(processor, input, expected):
    checker = dc.Checker(processor)
    output = checker.process(input)
    assert output == expected, 'Got output of: %s' % output


STRING_MANIP_BAD_TESTS = (
    (dc.lower, 1),
    (dc.lower, 1.234),
    (dc.lower, False),
    (dc.lower, Decimal('1.234')),

    (dc.upper, 1),
    (dc.upper, 1.234),
    (dc.upper, False),
    (dc.upper, Decimal('1.234')),

    (dc.strip, 1),
    (dc.strip, 1.234),
    (dc.strip, False),
    (dc.strip, Decimal('1.234')),
)

def test_string_manip_bad():
    for processor, input in STRING_MANIP_BAD_TESTS:
        yield check_string_manip_bad, processor, input

def check_string_manip_bad(processor, input):
    checker = dc.Checker(processor)
    try:
        output = checker.process(input)
    except dc.DataTypeError:
        pass
    except Exception as ex:
        raise ex
    else:
        assert False, 'Got output of: %s' % output

