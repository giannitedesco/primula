from .base import Level, Pin
from .component import Component, EventGenerator


class Latch(Component):
    pass


class JK(Latch):
    _pin_names = (
        'clk',
        'j',
        'k',
        'q',
        'q_',
    )

    def __init__(self):
        super().__init__()
        self._set_pin_direction(0, Pin.IN)
        self._set_pin_direction(1, Pin.IN)
        self._set_pin_direction(2, Pin.IN)
        self._set_pin_direction(3, Pin.OUT)
        self._set_pin_direction(4, Pin.OUT)

    def _on_change(self, pin: int) -> EventGenerator:
        if pin != 0:
            return

        if self._levels[pin] != Level.HI.value:
            return

        # on rising edge of clk

        s = self._levels[1]
        r = self._levels[2]

        if s and r:
            yield from self.assert_pin(3, not self._levels[3])
            yield from self.assert_pin(4, not self._levels[4])
        elif s:
            yield from self.assert_pin(3, True)
            yield from self.assert_pin(4, False)
        elif r:
            yield from self.assert_pin(3, False)
            yield from self.assert_pin(4, True)
