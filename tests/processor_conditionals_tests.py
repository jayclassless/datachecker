from decimal import Decimal

import datachecker as dc


obj = object()


GOOD_REQUIRED_TESTS = (
    1,
    1.23,
    Decimal('1.23'),
    False,
    'foo',
    [],
    (),
    {},
    obj,
)

def test_good_required():
    for input in GOOD_REQUIRED_TESTS:
        yield check_good_required, input

def check_good_required(input):
    checker = dc.Checker(dc.required)
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output


BAD_REQUIRED_TESTS = (
    None,
)

def test_bad_required():
    for input in BAD_REQUIRED_TESTS:
        yield check_bad_required, input

def check_bad_required(input):
    checker = dc.Checker(dc.required)
    try:
        output = checker.process(input)
    except dc.DataRequiredError:
        pass
    else:
        assert False, 'Got output of: %s' % output


GOOD_OPTIONAL_TESTS = (
    (1, None, 1),
    (1.23, None, 1.23),
    (Decimal('1.23'), None, Decimal('1.23')),
    (False, None, False),
    ('foo', None, 'foo'),
    ([], None, []),
    ((), None, ()),
    ({}, None, {}),
    (obj, None, obj),

    (1, 'abc', 1),
    (1.23, 'abc', 1.23),
    (Decimal('1.23'), 'abc', Decimal('1.23')),
    (False, 'abc', False),
    ('foo', 'abc', 'foo'),
    ([], 'abc', []),
    ((), 'abc', ()),
    ({}, 'abc', {}),
    (obj, 'abc', obj),

    (None, 1, 1),
    (None, 1.23, 1.23),
    (None, Decimal('1.23'), Decimal('1.23')),
    (None, False, False),
    (None, 'foo', 'foo'),
    (None, [], []),
    (None, (), ()),
    (None, {}, {}),
    (None, obj, obj),
)

def test_good_optional():
    for input, default, expected in GOOD_OPTIONAL_TESTS:
        yield check_good_optional, input, default, expected

def check_good_optional(input, default, expected):
    checker = dc.Checker(dc.optional(default=default))
    output = checker.process(input)
    assert output == expected, 'Got output of: %s' % output

