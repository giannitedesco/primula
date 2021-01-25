from .base import Pin
from .component import Component, EventGenerator


class Gate(Component):
    __slots__ = ()
    pass


class Nor(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        out = not (a or b)

        yield from self.assert_pin(2, out)


class Nand(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        out = not (a and b)

        yield from self.assert_pin(2, out)


class And(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        out = a and b

        yield from self.assert_pin(2, out)


class And3(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'c',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.IN)
        self._set_pin_direction(3, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        c = self._levels[2]
        out = a and b and c

        yield from self.assert_pin(3, out)


class Or(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        out = a or b

        yield from self.assert_pin(2, out)


class Or3(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'c',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.IN)
        self._set_pin_direction(3, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        c = self._levels[2]
        out = a or b or c

        yield from self.assert_pin(3, out)


class Xor(Gate):
    __slots__ = ()
    _pin_names = (
        'a',
        'b',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        b = self._levels[1]
        out = bool(a) ^ bool(b)

        yield from self.assert_pin(2, out)


class Inverter(Gate):
    __slots__ = ()
    _pin_names = (
        'inp',
        'out',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        a = self._levels[0]
        out = not a

        yield from self.assert_pin(1, out)


__all__ = (
    'Gate',
    'Nor',
    'Nand',
    'And',
    'And3',
    'Or',
    'Or3',
    'Xor',
)
