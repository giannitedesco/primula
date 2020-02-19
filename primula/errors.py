class PrimulaError(Exception):
    pass


class AlreadyConnectedError(PrimulaError):
    pass


class PinNotFoundError(PrimulaError, IndexError):
    pass


__all__ = (
    'PrimulaError',
    'AlreadyConnectedError',
    'PinNotFoundError',
)
