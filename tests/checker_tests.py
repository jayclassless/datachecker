import datachecker as dc


GOOD_ISVALID_TESTS = (
    ('foo', dc.string),
    (1, dc.integer),
    (1.23, dc.float),
)

def test_good_isvalid():
    for input, processor in GOOD_ISVALID_TESTS:
        yield check_good_isvalid, input, processor

def check_good_isvalid(input, processor):
    checker = dc.Checker(processor)
    output = checker.process(input)
    assert input == output, 'Got output of: %s' % output
    assert checker.is_valid(input) == True, 'is_valid() failed'


BAD_ISVALID_TESTS = (
    ('foo', dc.float),
    (1, dc.string),
    (1.23, dc.integer),
)

def test_bad_isvalid():
    for input, processor in BAD_ISVALID_TESTS:
        yield check_bad_isvalid, input, processor

def check_bad_isvalid(input, processor):
    checker = dc.Checker(processor)
    try:
        output = checker.process(input)
    except dc.CheckerError:
        assert checker.is_valid(input) == False, 'is_valid() failed'
    else:
        assert False, 'Got output of: %s' % output

