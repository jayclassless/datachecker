from random import choice

import datachecker as dc


def test_length_exact_good():
    for length in (1, 5, 100):
        for base in ('a', [0], (0,)):
            yield check_length_exact_good, (base * length), length

def check_length_exact_good(input, length):
    checker = dc.Checker(dc.length(exact=length))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output

def test_length_exact_bad():
    for length in (1, 5, 100):
        for base in ('a', [0], (0,)):
            yield check_length_exact_bad, (base * length), (length + choice([1,-1]))

def check_length_exact_bad(input, length):
    checker = dc.Checker(dc.length(exact=length))
    try:
        output = checker.process(input)
    except dc.BoundsError:
        pass
    else:
        assert False, 'Got output of: %s' % output

GOOD_BOUNDS_TESTS = (
    (5, 10, 5),
    (5, 10, 7),
    (5, 10, 10),
    (5, None, 5),
    (5, None, 100),
    (None, 10, 0),
    (None, 10, 10),
)

def test_length_bounds_good():
    for min, max, length in GOOD_BOUNDS_TESTS:
        for base in ('a', [0], (0,)):
            yield check_length_bounds_good, (base * length), min, max

def check_length_bounds_good(input, min, max):
    checker = dc.Checker(dc.length(min=min, max=max))
    output = checker.process(input)
    assert output == input, 'Got output of: %s' % output

BAD_BOUNDS_TESTS = (
    (5, 10, 1),
    (5, 10, 11),
    (5, None, 1),
    (None, 10, 11),
)

def test_length_bounds_bad():
    for min, max, length in BAD_BOUNDS_TESTS:
        for base in ('a', [0], (0,)):
            yield check_length_bounds_bad, (base * length), min, max

def check_length_bounds_bad(input, min, max):
    checker = dc.Checker(dc.length(min=min, max=max))
    try:
        output = checker.process(input)
    except dc.BoundsError:
        pass
    else:
        assert False, 'Got output of: %s' % output


def test_length_noninterable():
    checker = dc.Checker(dc.length(min=5))
    try:
        output = checker.process(3)
    except dc.DataTypeError:
        pass
    else:
        assert False, 'Got output of: %s' % output

