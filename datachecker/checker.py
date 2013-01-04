from .util import is_processor_generator


__all__ = (
    'Checker',
)


class Checker(object):
    def __init__(self, *processors):
        self.processors = []
        for processor in processors:
            if is_processor_generator(processor):
                processor = processor()
        self.processors.append(processor)

    def process(self, data):
        clean_data = data
        for processor in self.processors:
            clean_data = processor(clean_data)
        return clean_data

    def is_valid(self, data):
        try:
            self.process(data)
            return True
        except CheckerError:
            return False

