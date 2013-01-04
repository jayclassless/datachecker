
__all__ = (
    'processor',
)


def processor(func):
    func._processor_generator = True
    return func

def is_processor_generator(func):
    return getattr(func, '_processor_generator', False)

