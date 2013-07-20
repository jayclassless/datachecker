
__all__ = (
    'CheckerError',
    'DataTypeError',
    'BoundsError',
    'InvalidError',
    'FormatError',
    'DataRequiredError',
    'DictionaryError',
    'ExtraDataError',
    'CheckerSignal',
    'ShortCircuitSignal',
)


class CheckerError(Exception):
    field = None


class DataTypeError(CheckerError):
    def __init__(self, expected_type):
        super(DataTypeError, self).__init__('Value is not of type: %s' % expected_type)


class BoundsError(CheckerError):
    def __init__(self, direction, limit):
        super(BoundsError, self).__init__('Value is %s the limit of %s' % (direction, limit))


class InvalidError(CheckerError):
    def __init__(self, data):
        super(InvalidError, self).__init__('%s is not a valid data value' % data)


class FormatError(CheckerError):
    def __init__(self, data):
        super(FormatError, self).__init__('%s is not formatted properly' % data)


class DataRequiredError(CheckerError):
    def __init__(self):
        super(DataRequiredError, self).__init__('A value is required')


class DictionaryError(CheckerError):
    def __init__(self, errors):
        super(DictionaryError, self).__init__('')
        self.errors = errors


class ExtraDataError(CheckerError):
    def __init__(self):
        super(ExtraDataError, self).__init__('Extraneous data was provided')



class CheckerSignal(Exception):
    pass

class ShortCircuitSignal(CheckerSignal):
    data = None

