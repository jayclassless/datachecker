
__all__ = (
    'CheckerError',
    'DataTypeError',
    'BoundsError',
    'DataError',
    'DataRequiredError',
    'ExtraDataError',
)


class CheckerError(Exception):
    pass


class DataTypeError(CheckerError):
    def __init__(self, expected_type):
        super(DataTypeError, self).__init__('Value is not of type: %s' % expected_type)


class BoundsError(CheckerError):
    def __init__(self, direction, limit):
        super(BoundsError, self).__init__('Value is %s the limit of %s' % (direction, limit))


class DataError(CheckerError):
    def __init__(self, value):
        super(DataError, self).__init__('%s is not a valid value' % value)


class DataRequiredError(CheckerError):
    def __init__(self):
        super(DataRequiredError, self).__init__('A value is required')


class ExtraDataError(CheckerError):
    def __init__(self):
        super(ExtraDataError, self).__init__('Extraneous data was provided')

