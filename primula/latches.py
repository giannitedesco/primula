from typing import Generator
from .base import Level, Pin
from .component import Component, EventGenerator


class Latch(Component):
    pass


class SR(Latch):
    _pin_names = (
        's',
        'r',
        'q',
        'q_',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.OUT)
        self._set_pin_direction(3, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        if self._levels[pin] != Level.HI.value:
            return

        s = self._levels[0]
        r = self._levels[1]

        if s and r:
            yield from self.float_pin(2)
            yield from self.float_pin(3)
        elif s:
            yield from self.assert_pin(2, True)
            yield from self.assert_pin(3, False)
        elif r:
            yield from self.assert_pin(2, False)
            yield from self.assert_pin(3, True)
