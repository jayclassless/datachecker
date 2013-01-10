from decimal import Decimal

import datachecker as dc


GOOD_LIST_TESTS = (
    ([1,2,3], [1,2,3], [dc.integer], False),
    ([1,2,3], [1,2,3], [dc.integer], True),
    (['1','2','3'], [1,2,3], [dc.integer(coerce=True)], False),
    (['1','2','3'], [1,2,3], [dc.integer(coerce=True)], True),
    (['1',2,'3'], [1,2,3], [dc.integer(coerce=True)], False),
    (['1',2,'3'], [1,2,3], [dc.integer(coerce=True)], True),
    (['1',2,'3'], ['1','2','3'], [dc.string(coerce=True)], False),
    (['1',2,'3'], ['1','2','3'], [dc.string(coerce=True)], True),

    (1, [1], [dc.integer], True),
    (1.23, [1.23], [dc.float], True),
    (Decimal('1.23'), [Decimal('1.23')], [dc.decimal], True),
    ('foo', ['foo'], [dc.string], True),
    (False, [False], [dc.boolean], True),
    (None, [], [dc.string], True),
    ((1,2,3), [1,2,3], [dc.integer], True),

    (['  foo','bar  '], ['foo','bar'], [dc.string, dc.strip], False),
    (['  foo','bar  '], ['foo','bar'], [dc.string, dc.strip], True),
)

def test_good_lists():
    for input, expected, processors, coerce in GOOD_LIST_TESTS:
        yield check_good_list, input, expected, processors, coerce

def check_good_list(input, expected, processors, coerce):
    checker = dc.Checker(dc.list(*processors, coerce=coerce))
    output = checker.process(input)
    assert output == expected, 'Got output of: %s' % output


BAD_LIST_TESTS = (
    (1, [dc.integer], False),
    (1.23, [dc.float], False),
    (Decimal('1.23'), [dc.decimal], False),
    ('foo', [dc.string], False),
    (False, [dc.boolean], False),
    (None, [dc.string], False),
    ((1,2,3), [dc.integer], False),

    ([1,'foo'], [dc.integer], False),
    ([1,'foo'], [dc.integer], True),
    (['foo', 'blah'], [dc.string, dc.length(exact=3)], False),
    (['foo', 'blah'], [dc.string, dc.length(exact=3)], True),
)

def test_bad_lists():
    for input, processors, coerce in BAD_LIST_TESTS:
        yield check_bad_list, input, processors, coerce

def check_bad_list(input, processors, coerce):
    checker = dc.Checker(dc.list(*processors, coerce=coerce))
    try:
        output = checker.process(input)
    except dc.CheckerError:
        pass
    else:
        assert False, 'Got output of: %s' % output


GOOD_TUPLE_TESTS = (
    ((1,2,3), (1,2,3), [dc.integer], False),
    ((1,2,3), (1,2,3), [dc.integer], True),
    (('1','2','3'), (1,2,3), [dc.integer(coerce=True)], False),
    (('1','2','3'), (1,2,3), [dc.integer(coerce=True)], True),
    (('1',2,'3'), (1,2,3), [dc.integer(coerce=True)], False),
    (('1',2,'3'), (1,2,3), [dc.integer(coerce=True)], True),
    (('1',2,'3'), ('1','2','3'), [dc.string(coerce=True)], False),
    (('1',2,'3'), ('1','2','3'), [dc.string(coerce=True)], True),

    (1, (1,), [dc.integer], True),
    (1.23, (1.23,), [dc.float], True),
    (Decimal('1.23'), (Decimal('1.23'),), [dc.decimal], True),
    ('foo', ('foo',), [dc.string], True),
    (False, (False,), [dc.boolean], True),
    (None, (), [dc.string], True),
    ([1,2,3], (1,2,3), [dc.integer], True),

    (('  foo','bar  '), ('foo','bar'), [dc.string, dc.strip], False),
    (('  foo','bar  '), ('foo','bar'), [dc.string, dc.strip], True),
)

def test_good_tuples():
    for input, expected, processors, coerce in GOOD_TUPLE_TESTS:
        yield check_good_tuple, input, expected, processors, coerce

def check_good_tuple(input, expected, processors, coerce):
    checker = dc.Checker(dc.tuple(*processors, coerce=coerce))
    output = checker.process(input)
    assert output == expected, 'Got output of: %s' % output


BAD_TUPLE_TESTS = (
    (1, [dc.integer], False),
    (1.23, [dc.float], False),
    (Decimal('1.23'), [dc.decimal], False),
    ('foo', [dc.string], False),
    (False, [dc.boolean], False),
    (None, [dc.string], False),
    ([1,2,3], [dc.integer], False),

    ((1,'foo'), [dc.integer], False),
    ((1,'foo'), [dc.integer], True),
    (('foo', 'blah'), [dc.string, dc.length(exact=3)], False),
    (('foo', 'blah'), [dc.string, dc.length(exact=3)], True),
)

def test_bad_tuples():
    for input, processors, coerce in BAD_TUPLE_TESTS:
        yield check_bad_tuple, input, processors, coerce

def check_bad_tuple(input, processors, coerce):
    checker = dc.Checker(dc.tuple(*processors, coerce=coerce))
    try:
        output = checker.process(input)
    except dc.CheckerError:
        pass
    else:
        assert False, 'Got output of: %s' % output

