from decimal import Decimal
from random import choice

import datachecker as dc


def test_constant_good():
    for input in ('foo', 100, Decimal('1.234')):
        checker = dc.Checker(dc.constant(input))
        output = checker.process(input)
        assert output == input, 'Got output of: %s' % output

def test_constant_bad():
    checker = dc.Checker(dc.constant('foo'))
    try:
        output = checker.process('bar')
    except dc.InvalidError:
        pass
    except Exception as ex:
        raise ex
    else:
        assert False, 'Got output of: %s' % output


def test_choice_good():
    choices = (5, 10, 15, 20, 25, 'foo', 'bar')
    checker = dc.Checker(dc.choice(*choices))
    for input in choices:
        output = checker.process(input)
        assert output == input, 'Got output of: %s' % output

def test_choice_bad():
    choices = ('a', 'b', 'c')
    checker = dc.Checker(dc.choice(*choices))
    for input in (1, 'foo', False, Decimal('1.234')):
        try:
            output = checker.process(input)
        except dc.InvalidError:
            pass
        except Exception as ex:
            raise ex
        else:
            assert False, 'Got output of: %s' % output

