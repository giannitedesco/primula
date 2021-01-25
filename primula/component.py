from typing import List, Optional, Any, Iterable, Type
from array import array
from abc import ABCMeta
import logging
import weakref
from .base import Level, \
                  Pin, \
                  SimStep, \
                  ComponentBase, \
                  ComponentPin, \
                  Event, \
                  EventGenerator
from . import errors


sim = logging.getLogger('sim')


class PinsBase:
    """
    Proxy for accessing pins by their names

    All components have a 'pins' member. Accessing pins.PIN will lookup the
    name 'PIN' to the pin index and return Component.pin(index) so that pins
    can be hooked up. Performance of this proxy isn't a priority, the priority
    is simulation speed. So all of this rigmarole is just to hide the fact that
    pin configurations and states are in byte arrays.
    """

    __slots__ = (
        '_owner',
        '_nr_pins',
    )

    _nr_pins: int

    def __init__(self, owner, names: Iterable[str]):
        nr_pins = 0
        for index, name in enumerate(names):
            super().__setattr__(name, index)
            nr_pins += 1
        super().__setattr__('_owner', owner)
        super().__setattr__('_nr_pins', nr_pins)

    def __len__(self):
        return self._nr_pins

    def __setattr__(self, k, v):
        raise TypeError

    def __getattribute__(self, name: str) -> Any:
        owner = super().__getattribute__('_owner')
        ret = super().__getattribute__(name)
        if name in {'_nr_pins', }:
            return ret
        return owner().pin(ret)


class _ComponentMeta(ABCMeta):
    """
    Metaclass to setup subclasses of the Component class.

    This metaclass looks at the '_pin_names' array of any class which gets
    instantiated. It creates the pins proxy type which is used to implement
    Component.pins accessors which let you program pins by their names instead
    of their numbers.
    """
    __slots__ = ()

    _pin_names: Iterable[str]

    def __new__(cls, name, bases, dct):
        cls = super().__new__(cls, name, bases, dct)

        # Abstract classes
        try:
            names = cls._pin_names
        except AttributeError:
            return cls

        pt = type(f'{name}Pins',
                  (PinsBase,),
                  {'__slots__': names, })
        cls._proxy = pt

        return cls


class Component(ComponentBase, metaclass=_ComponentMeta):
    """
    All components should derive from this.

    It implements all the pin configurations and simulation state.  Subclasses
    merely need to provide a `_pin_names` tuple as a class variable and an
    `_on_change' method to implement the logic. You may also wish to override
    the constructor in order to set the configurations for the pins which all
    default in to high-impedance state.
    """

    __slots__ = (
        '__weakref__',
        '_directions',
        '_levels',
        '_conns',
        'pins',
    )

    # instance variables
    _directions: array
    _levels: array
    _conns: List[Optional[ComponentPin]]

    # class variables
    _proxy: Type[PinsBase]
    _pin_names: Iterable[str]

    def __init__(self):
        self.pins = self._proxy(weakref.ref(self), self._pin_names)
        nr_pins = len(self.pins)

        hiz = Pin.HIZ.value
        self._directions = array('B', (hiz for x in range(nr_pins)))

        flt = Level.FLT.value
        self._levels = array('B', (flt for x in range(nr_pins)))

        self._conns = [None for x in range(nr_pins)]

    def connected_pin(self, pin: int, other: ComponentPin):
        if self._conns[pin] is not None:
            raise errors.AlreadyConnectedError(f'{self}#{pin} '
                                               'already attached')
        self._conns[pin] = other

    def _set_pin_direction(self, pin: int, direction: Pin):
        self._directions[pin] = direction.value

    def pin(self, pin: int) -> ComponentPin:
        if pin < len(self._directions):
            return super().pin(pin)
        raise errors.PinNotFoundError(f'{self}#{pin} no such pin')

    def get_level(self, pin: int) -> Level:
        return Level(self._levels[pin])

    def get_direction(self, pin: int) -> Pin:
        return Pin(self._directions[pin])

    def _set_output_level(self, pin: int, new_level: int) -> EventGenerator:
        d = self._directions[pin]
        if d == Pin.HIZ.value:
            sim.info(f'asserting high-z pin on {self} #{pin}')
            return
        if d == Pin.IN.value:
            sim.warning(f'asserting input pin on {self} #{pin}')
            return

        old_level = self._levels[pin]
        if new_level == old_level:
            return

        self._levels[pin] = new_level
        other = self._conns[pin]
        if other is None:
            return

        sim.info(f'assert: {self} #{pin} {Level(old_level)} '
                 f'-> {Level(new_level)}')
        yield Event(self.pin(pin), other, Level(new_level))

    def assert_pin(self, pin: int, level: bool) -> EventGenerator:
        """
        Drive a pin to logical 1 (True) or logical 0 (False)
        """

        yield from self._set_output_level(pin, int(level))

    def error_pin(self, pin: int) -> EventGenerator:
        """
        Set a pin in to the error state.
        """

        yield from self._set_output_level(pin, Level.ERR.value)

    def float_pin(self, pin: int) -> EventGenerator:
        """
        Set a pin as floating / disconnected
        """

        yield from self._set_output_level(pin, Level.FLT.value)

    def _on_change(self, pin: int) -> EventGenerator:
        return
        yield

    def propagate(self,
                  pin: int,
                  level: Level,
                  epoch: SimStep) -> EventGenerator:
        # Floating and Error levels never propagate
        if level in (Level.FLT, Level.ERR):
            sim.info(f'{self}#{pin} ignoring {level}')
            return

        pd = self._directions[pin]

        # If pin disconnected, do nothing
        if pd == Pin.HIZ.value:
            sim.debug('{self}#{pin} disconnected')
            return

        # If output pin, then we're not going to accept a signal
        if pd == Pin.OUT.value:
            sim.warning(f'driving output pin on {self} #{pin}')
            return

        sim.info(f'{self}#{pin} level changed')
        self._levels[pin] = level.value
        yield from self._on_change(pin)

    def __str__(self):
        return type(self).__name__

    def __repr__(self):
        return type(self).__name__
