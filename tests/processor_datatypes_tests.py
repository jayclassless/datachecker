import sys

from decimal import Decimal

import datachecker as dc


class strobject(object):
    def __unicode__(self):
        return unicode('MY STROBJECT')


GOOD_DATATYPE_TESTS = (
    # integer: normal ints
    (dc.integer, 1, False, 1),
    (dc.integer, 0, False, 0),
    (dc.integer, -1, False, -1),
    (dc.integer, sys.maxint, False, sys.maxint),
    (dc.integer, (-sys.maxint - 1), False, (-sys.maxint - 1)),
    (dc.integer, 1, True, 1),
    (dc.integer, 0, True, 0),
    (dc.integer, -1, True, -1),
    (dc.integer, sys.maxint, True, sys.maxint),
    (dc.integer, (-sys.maxint - 1), True, (-sys.maxint - 1)),

    # integer: longs
    (dc.integer, 1L, False, 1),
    (dc.integer, 0L, False, 0),
    (dc.integer, -1L, False, -1),
    (dc.integer, (sys.maxint + 1), False, (sys.maxint + 1)),
    (dc.integer, (-sys.maxint - 2), False, (-sys.maxint - 2)),
    (dc.integer, 1L, True, 1),
    (dc.integer, 0L, True, 0),
    (dc.integer, -1L, True, -1),
    (dc.integer, (sys.maxint + 1), True, (sys.maxint + 1)),
    (dc.integer, (-sys.maxint - 2), True, (-sys.maxint - 2)),

    # integer: string coercion
    (dc.integer, '1', True, 1),
    (dc.integer, '0', True, 0),
    (dc.integer, '-1', True, -1),
    (dc.integer, '1.234', True, 1),
    (dc.integer, '0.234', True, 0),
    (dc.integer, '-1.234', True, -1),

    # integer: float coercion
    (dc.integer, 1.0, True, 1),
    (dc.integer, 0.0, True, 0),
    (dc.integer, -1.0, True, -1),
    (dc.integer, 1.234, True, 1),
    (dc.integer, 0.234, True, 0),
    (dc.integer, -1.234, True, -1),

    # integer: Decimal coercion
    (dc.integer, Decimal('1'), True, 1),
    (dc.integer, Decimal('0'), True, 0),
    (dc.integer, Decimal('-1'), True, -1),
    (dc.integer, Decimal('1.234'), True, 1),
    (dc.integer, Decimal('0.234'), True, 0),
    (dc.integer, Decimal('-1.234'), True, -1),

    # integer: boolean coercion
    (dc.integer, True, True, 1),
    (dc.integer, False, True, 0),


    # float: floats
    (dc.float, 0.0, False, 0.0),
    (dc.float, 1.234, False, 1.234),
    (dc.float, 0.234, False, 0.234),
    (dc.float, -1.234, False, -1.234),
    (dc.float, sys.float_info.max, False, sys.float_info.max),
    (dc.float, sys.float_info.min, False, sys.float_info.min),
    (dc.float, 0.0, True, 0.0),
    (dc.float, 1.234, True, 1.234),
    (dc.float, 0.234, True, 0.234),
    (dc.float, -1.234, True, -1.234),
    (dc.float, sys.float_info.max, True, sys.float_info.max),
    (dc.float, sys.float_info.min, True, sys.float_info.min),

    # float: normal int coercion
    (dc.float, 1, True, 1.0),
    (dc.float, 0, True, 0.0),
    (dc.float, -1, True, -1.0),

    # float: long coercion
    (dc.float, 1L, True, 1.0),
    (dc.float, 0L, True, 0.0),
    (dc.float, -1L, True, -1.0),

    # float: string coercion
    (dc.float, '1', True, 1.0),
    (dc.float, '0', True, 0.0),
    (dc.float, '-1', True, -1.0),
    (dc.float, '1.234', True, 1.234),
    (dc.float, '0.234', True, 0.234),
    (dc.float, '-1.234', True, -1.234),

    # float: Decimal coercion
    (dc.float, Decimal('1'), True, 1.0),
    (dc.float, Decimal('0'), True, 0.0),
    (dc.float, Decimal('-1'), True, -1.0),
    (dc.float, Decimal('1.234'), True, 1.234),
    (dc.float, Decimal('0.234'), True, 0.234),
    (dc.float, Decimal('-1.234'), True, -1.234),


    # decimal: decimals
    (dc.decimal, Decimal('1'), False, Decimal('1.0')),
    (dc.decimal, Decimal('0'), False, Decimal('0.0')),
    (dc.decimal, Decimal('-1'), False, Decimal('-1.0')),
    (dc.decimal, Decimal('1.234'), False, Decimal('1.234')),
    (dc.decimal, Decimal('0.234'), False, Decimal('0.234')),
    (dc.decimal, Decimal('-1.234'), False, Decimal('-1.234')),
    (dc.decimal, Decimal('1'), True, Decimal('1.0')),
    (dc.decimal, Decimal('0'), True, Decimal('0.0')),
    (dc.decimal, Decimal('-1'), True, Decimal('-1.0')),
    (dc.decimal, Decimal('1.234'), True, Decimal('1.234')),
    (dc.decimal, Decimal('0.234'), True, Decimal('0.234')),
    (dc.decimal, Decimal('-1.234'), True, Decimal('-1.234')),

    # decimal: normal int coercion
    (dc.decimal, 1, True, Decimal('1.0')),
    (dc.decimal, 0, True, Decimal('0.0')),
    (dc.decimal, -1, True, Decimal('-1.0')),

    # decimal: long coercion
    (dc.decimal, 1L, True, Decimal('1.0')),
    (dc.decimal, 0L, True, Decimal('0.0')),
    (dc.decimal, -1L, True, Decimal('-1.0')),

    # decimal: string coercion
    (dc.decimal, '1', True, Decimal('1.0')),
    (dc.decimal, '0', True, Decimal('0.0')),
    (dc.decimal, '-1', True, Decimal('-1.0')),
    (dc.decimal, '1.234', True, Decimal('1.234')),
    (dc.decimal, '0.234', True, Decimal('0.234')),
    (dc.decimal, '-1.234', True, Decimal('-1.234')),
    (dc.decimal, 'infinity', True, Decimal('Infinity')),
    (dc.decimal, '-infinity', True, Decimal('-Infinity')),

    # decimal: float coercion
    (dc.decimal, 1.0, True, Decimal('1.0')),
    (dc.decimal, 0.0, True, Decimal('0.0')),
    (dc.decimal, -1.0, True, Decimal('-1.0')),
    (dc.decimal, 1.234, True, Decimal('1.234')),
    (dc.decimal, 0.234, True, Decimal('0.234')),
    (dc.decimal, -1.234, True, Decimal('-1.234')),


    # string: strings
    (dc.string, 'foo', False, 'foo'),
    (dc.string, 'foo', True, 'foo'),
    (dc.string, '', False, ''),
    (dc.string, '', True, ''),

    # string: normal int coercion
    (dc.string, 1, True, '1'),
    (dc.string, 0, True, '0'),
    (dc.string, -1, True, '-1'),

    # string: long coercion
    (dc.string, 1L, True, '1'),
    (dc.string, 0L, True, '0'),
    (dc.string, -1L, True, '-1'),

    # float: string coercion
    (dc.string, 1.0, True, '1.0'),
    (dc.string, 0.0, True, '0.0'),
    (dc.string, -1.0, True, '-1.0'),
    (dc.string, 1.234, True, '1.234'),
    (dc.string, 0.234, True, '0.234'),
    (dc.string, -1.234, True, '-1.234'),

    # string: Decimal coercion
    (dc.string, Decimal('1'), True, '1'),
    (dc.string, Decimal('0'), True, '0'),
    (dc.string, Decimal('-1'), True, '-1'),
    (dc.string, Decimal('1.0'), True, '1.0'),
    (dc.string, Decimal('0.0'), True, '0.0'),
    (dc.string, Decimal('-1.0'), True, '-1.0'),
    (dc.string, Decimal('1.234'), True, '1.234'),
    (dc.string, Decimal('0.234'), True, '0.234'),
    (dc.string, Decimal('-1.234'), True, '-1.234'),

    # string: object coercion
    (dc.string, strobject(), True, 'MY STROBJECT'),


    # boolean: booleans
    (dc.boolean, True, False, True),
    (dc.boolean, True, True, True),
    (dc.boolean, False, False, False),
    (dc.boolean, False, True, False),

    # boolean: normal int coercion
    (dc.boolean, 1, True, True),
    (dc.boolean, 0, True, False),

    # boolean: long coercion
    (dc.boolean, 1L, True, True),
    (dc.boolean, 0L, True, False),

    # boolean: string coercion
    (dc.boolean, 'TRUE', True, True),
    (dc.boolean, 'true', True, True),
    (dc.boolean, 'YES', True, True),
    (dc.boolean, 'yes', True, True),
    (dc.boolean, 'Y', True, True),
    (dc.boolean, 'y', True, True),
    (dc.boolean, 'ON', True, True),
    (dc.boolean, 'on', True, True),
    (dc.boolean, '1', True, True),
    (dc.boolean, 'FALSE', True, False),
    (dc.boolean, 'false', True, False),
    (dc.boolean, 'NO', True, False),
    (dc.boolean, 'no', True, False),
    (dc.boolean, 'N', True, False),
    (dc.boolean, 'n', True, False),
    (dc.boolean, 'OFF', True, False),
    (dc.boolean, 'off', True, False),
    (dc.boolean, '0', True, False),

    # boolean: Decimal coercion
    (dc.boolean, Decimal('1'), True, True),
    (dc.boolean, Decimal('0'), True, False),
)

def test_good_datatypes():
    for processor, input, coerce, expected in GOOD_DATATYPE_TESTS:
        yield check_good_datatype, processor, input, coerce, expected

def check_good_datatype(processor, input, coerce, expected):
    checker = dc.Checker(processor(coerce=coerce))
    output = checker.process(input)
    assert output == expected, 'Got output of: %s' % output


BAD_DATATYPE_TESTS = (
    # integer: String coercion
    (dc.integer, '1', False),
    (dc.integer, '0', False),
    (dc.integer, '-1', False),
    (dc.integer, '1.234', False),
    (dc.integer, '0.234', False),
    (dc.integer, '-1.234', False),
    (dc.integer, 'foo', True),
    (dc.integer, '', True),

    # integer: float coercion
    (dc.integer, 1.0, False),
    (dc.integer, 0.0, False),
    (dc.integer, -1.0, False),
    (dc.integer, 1.234, False),
    (dc.integer, 0.234, False),
    (dc.integer, -1.234, False),

    # integer: Decimal coercion
    (dc.integer, Decimal('1'), False),
    (dc.integer, Decimal('0'), False),
    (dc.integer, Decimal('-1'), False),
    (dc.integer, Decimal('1.234'), False),
    (dc.integer, Decimal('0.234'), False),
    (dc.integer, Decimal('-1.234'), False),

    # integer: Other coercions
    (dc.integer, None, False),
    (dc.integer, None, True),
    (dc.integer, {}, False),
    (dc.integer, {}, True),
    (dc.integer, [], False),
    (dc.integer, [], True),
    (dc.integer, (), False),
    (dc.integer, (), True),
    (dc.integer, object(), False),
    (dc.integer, object(), True),


    # float: Normal int coercion
    (dc.float, 1, False),
    (dc.float, 0, False),
    (dc.float, -1, False),

    # float: Normal long coercion
    (dc.float, 1L, False),
    (dc.float, 0L, False),
    (dc.float, -1L, False),

    # float: String coercion
    (dc.float, '1', False),
    (dc.float, '0', False),
    (dc.float, '-1', False),
    (dc.float, '1.234', False),
    (dc.float, '0.234', False),
    (dc.float, '-1.234', False),
    (dc.float, 'foo', True),
    (dc.float, '', True),

    # float: Decimal coercion
    (dc.float, Decimal('1'), False),
    (dc.float, Decimal('0'), False),
    (dc.float, Decimal('-1'), False),
    (dc.float, Decimal('1.234'), False),
    (dc.float, Decimal('0.234'), False),
    (dc.float, Decimal('-1.234'), False),

    # float: boolean coercion
    (dc.float, True, False),
    (dc.float, False, False),

    # float: Other coercions
    (dc.float, None, False),
    (dc.float, None, True),
    (dc.float, {}, False),
    (dc.float, {}, True),
    (dc.float, [], False),
    (dc.float, [], True),
    (dc.float, (), False),
    (dc.float, (), True),
    (dc.float, object(), False),
    (dc.float, object(), True),


    # decimal: Normal int coercion
    (dc.decimal, 1, False),
    (dc.decimal, 0, False),
    (dc.decimal, -1, False),

    # decimal: Normal long coercion
    (dc.decimal, 1L, False),
    (dc.decimal, 0L, False),
    (dc.decimal, -1L, False),

    # decimal: String coercion
    (dc.decimal, '1', False),
    (dc.decimal, '0', False),
    (dc.decimal, '-1', False),
    (dc.decimal, '1.234', False),
    (dc.decimal, '0.234', False),
    (dc.decimal, '-1.234', False),
    (dc.decimal, 'infinity', False),
    (dc.decimal, '-infinity', False),
    (dc.decimal, 'foo', True),
    (dc.decimal, '', True),

    # decimal: float coercion
    (dc.decimal, 1.0, False),
    (dc.decimal, 0.0, False),
    (dc.decimal, -1.0, False),
    (dc.decimal, 1.234, False),
    (dc.decimal, 0.234, False),
    (dc.decimal, -1.234, False),

    # decimal: boolean coercion
    (dc.decimal, True, False),
    (dc.decimal, False, False),

    # decimal: Other coercions
    (dc.decimal, None, False),
    (dc.decimal, None, True),
    (dc.decimal, {}, False),
    (dc.decimal, {}, True),
    (dc.decimal, [], False),
    (dc.decimal, [], True),
    (dc.decimal, (), False),
    (dc.decimal, (), True),
    (dc.decimal, object(), False),
    (dc.decimal, object(), True),


    # string: Normal int coercion
    (dc.string, 1, False),
    (dc.string, 0, False),
    (dc.string, -1, False),

    # string: long coercion
    (dc.string, 1L, False),
    (dc.string, 0L, False),
    (dc.string, -1L, False),

    # string: float coercion
    (dc.string, 1.0, False),
    (dc.string, 0.0, False),
    (dc.string, -1.0, False),
    (dc.string, 1.234, False),
    (dc.string, 0.234, False),
    (dc.string, -1.234, False),

    # string: Decimal coercion
    (dc.string, Decimal('1'), False),
    (dc.string, Decimal('0'), False),
    (dc.string, Decimal('-1'), False),
    (dc.string, Decimal('1.234'), False),
    (dc.string, Decimal('0.234'), False),
    (dc.string, Decimal('-1.234'), False),

    # string: boolean coercion
    (dc.string, True, False),
    (dc.string, False, False),

    # string: Other coercions
    (dc.string, None, False),
    (dc.string, None, True),
    (dc.string, {}, False),
    (dc.string, {}, True),
    (dc.string, [], False),
    (dc.string, [], True),
    (dc.string, (), False),
    (dc.string, (), True),
    (dc.string, strobject(), False),


    # boolean: Normal int coercion
    (dc.boolean, 1, False),
    (dc.boolean, 0, False),
    (dc.boolean, -1, False),

    # boolean: long coercion
    (dc.boolean, 1L, False),
    (dc.boolean, 0L, False),
    (dc.boolean, -1L, False),

    # boolean: float coercion
    (dc.boolean, 1.0, False),
    (dc.boolean, 0.0, False),
    (dc.boolean, -1.0, False),
    (dc.boolean, 1.234, False),
    (dc.boolean, 0.234, False),
    (dc.boolean, -1.234, False),

    # boolean: string coercion
    (dc.float, 'foo', True),
    (dc.float, '', True),

    # boolean: Decimal coercion
    (dc.boolean, Decimal('1'), False),
    (dc.boolean, Decimal('0'), False),
    (dc.boolean, Decimal('-1'), False),
    (dc.boolean, Decimal('1.234'), False),
    (dc.boolean, Decimal('0.234'), False),
    (dc.boolean, Decimal('-1.234'), False),

    # boolean: Other coercions
    (dc.boolean, None, False),
    (dc.boolean, None, True),
    (dc.boolean, {}, False),
    (dc.boolean, {}, True),
    (dc.boolean, [], False),
    (dc.boolean, [], True),
    (dc.boolean, (), False),
    (dc.boolean, (), True),
    (dc.boolean, strobject(), False),
)

def test_bad_datatypes():
    for processor, input, coerce in BAD_DATATYPE_TESTS:
        yield check_bad_datatype, processor, input, coerce

def check_bad_datatype(processor, input, coerce):
    checker = dc.Checker(processor(coerce=coerce))
    try:
        output = checker.process(input)
    except dc.CheckerError:
        pass
    else:
        assert False, 'Got output of: %s' % output
        


GOOD_BOUNDS_TESTS = (
    (5, 10, 5),
    (5, 10, 7),
    (5, 10, 10),
    (5, None, 5),
    (5, None, 100),
    (None, 10, -100),
    (None, 10, 0),
    (None, 10, 10),
)

def test_good_datatype_bounds():
    for processor in (dc.integer, dc.float, dc.decimal):
        for min, max, input in GOOD_BOUNDS_TESTS:
            yield check_good_datatype_bounds, processor, min, max, input

def check_good_datatype_bounds(processor, min, max, input):
    checker = dc.Checker(processor(coerce=True, min=min, max=max))
    output = checker.process(input)



BAD_BOUNDS_TESTS = (
    (5, 10, 1),
    (5, 10, 11),
    (5, None, 1),
    (None, 10, 11),
)

def test_bad_datatype_bounds():
    for processor in (dc.integer, dc.float, dc.decimal):
        for min, max, input in BAD_BOUNDS_TESTS:
            yield check_bad_datatype_bounds, processor, min, max, input

def check_bad_datatype_bounds(processor, min, max, input):
    checker = dc.Checker(processor(coerce=True, min=min, max=max))
    try:
        output = checker.process(input)
    except dc.CheckerError:
        pass
    else:
        assert False, 'Got output of: %s' % output

