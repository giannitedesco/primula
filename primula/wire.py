from typing import Optional, Dict
from weakref import ref, ReferenceType
import logging
from .base import Pull, \
                  Pin, \
                  Level, \
                  Event, \
                  EventGenerator, \
                  ComponentBase, \
                  ComponentPin, \
                  SimStep
from .simulation import Simulation
from . import errors


sim = logging.getLogger('sim')


class LineDriver(ComponentBase):
    __slots__ = (
        '_target',
        '_level',
    )

    def __init__(self, target: ComponentPin, level: Level):
        self._target = target
        self._level = level

    def propagate(self,
                  pin: int,
                  level: Level,
                  epoch: SimStep) -> EventGenerator:
        self._level = level
        yield Event(self.pin(0), self._target, level)

    def connected_pin(self, pin: int, other: ComponentPin):
        raise NotImplementedError

    def get_level(self, pin: int) -> Level:
        assert(pin == 0)
        return self._level

    def get_direction(self, pin: int) -> Pin:
        assert(pin == 0)
        return Pin.OUT

    def __str__(self):
        return f'SimulationObject({self._target})'


class Wire(ComponentBase):
    __slots__ = (
        '__weakref__',
        '_name',
        '_level',
        '_pins',
        '_next_id',
        '_driver',
        '_epoch',
    )

    _name: Optional[str]
    _level: Level
    _pins: Dict[int, ComponentPin]
    _driver: int
    _next_id: int

    def __init__(self,
                 name: Optional[str] = None,
                 pull: Optional[Pull] = None):
        self._name = name
        self._next_id = 1
        self._driver = 0
        self._epoch: Optional[ReferenceType[SimStep]] = None
        if pull is None:
            self._level = Level.FLT
        else:
            self._level = pull.level

        me = ComponentPin(self, 0)
        sim = ComponentPin(LineDriver(me, self._level), 0)
        self._pins = {0: sim, }

    def get_level(self, pin: int) -> Level:
        # Level is the same at all pins
        return self._level

    def get_direction(self, pin: int) -> Pin:
        raise errors.PrimulaError('Wires are not directional')

    def pin(self, pin: int) -> ComponentPin:
        if pin in self._pins:
            return super().pin(pin)
        raise errors.PinNotFoundError(f'{self}#{pin} no such pin')

    def propagate(self,
                  pin: int,
                  level: Level,
                  epoch: SimStep) -> EventGenerator:

        # We reached a fix-point
        if self._level == level:
            return

        # Apply the change to this wire
        if self._epoch is not None and epoch == self._epoch():
            sim.warning(f'{self} driven twice this step')
            self._level = Level.ERR
            return

        self._level = level
        self._driver = pin
        self._epoch = ref(epoch)

        # Wires don't propagate errors. We will want to color them red to make
        # the location of the error obvious. That's made more difficult if we
        # propagate red all over the place!
        if level in {Level.FLT, Level.ERR}:
            return

        # Now to all pins
        driver = self.pin(pin)
        for pin, cp in self._pins.items():
            # Don't drive current back in to the pin which is driving current
            # in to this wire
            if self._driver == pin:
                continue

            yield Event(driver, cp, self._level)

    def drive(self, level: Level):
        self._level = Level.FLT
        seed = self._pins[0]
        Simulation.run(seed, level)

    def pulse(self):
        sim.debug('rising edge')
        self.drive(Level.HI)
        sim.debug('falling edge')
        self.drive(Level.LO)

    def new_pin(self) -> ComponentPin:
        this_id = self._next_id
        self._next_id += 1
        return self.pin(this_id)

    def connected_pin(self, pin: int, other: ComponentPin):
        raise NotImplementedError

    def connect(self, *args: ComponentPin):
        driver = None

        for cp in args:
            this_id = self._next_id
            self._next_id += 1
            self._pins[this_id] = cp

            c, p = cp

            # Register back-pointers
            me = ComponentPin(self, this_id)
            sim.debug(f'connect {me} to {cp}')
            cp.connected_pin(me)

            # Now we'll check if the pin we're adding is an output pin which is
            # either sourcing or sinking a current and then remember about it
            # so that we can use it to change the wires logic level and then
            # drive all other pins on the wire
            if cp.direction != Pin.OUT:
                continue

            if cp.level == Level.FLT:
                continue

            if driver is not None:
                self._level = Level.ERR
                sim.warning(f'Conflicting signals on {self}')
                return

            driver = cp

        if driver is None:
            # So all that's left to do is drive wire level in to the newly
            # connected pins
            level = self._level
            for cp in args:
                Simulation.run(cp, level)
        else:
            sim.info(f'connection drove {self} to {driver.level}')
            self.drive(driver.level)

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def level(self) -> Level:
        return self._level

    def __str__(self) -> str:
        if self._name is not None:
            return f'{self._name}({self._level.name})'
        else:
            return 'Wire()'
