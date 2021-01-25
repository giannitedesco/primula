from __future__ import annotations
from typing import Generator, NamedTuple, Iterator
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum


class Level(Enum):
    """
    Different logical levels that a wire can be at
    """

    LO = 0  # LO state
    HI = 1  # HI state
    FLT = 2  # floating, just a conductor with no current accross it...
    ERR = 3  # error, pseudo-state so that errors can be located


class Pin(Enum):
    """
    Logical directions of pins.

    Are they inputs/outputs/disconnected?
    """

    IN = 0
    OUT = 1
    HIZ = 0xff  # High-impedence / Hi-Z state


class Pull(Enum):
    """
    A pull-up or pull-down resistor.

    Used to drive a line to a specific logical level.
    """

    DOWN = 0
    UP = 1

    @property
    def level(self) -> Level:
        return Level(self.value)


@dataclass
class ComponentPin:
    component: ComponentBase
    pin: int

    @property
    def level(self) -> Level:
        return self.component.get_level(self.pin)

    @property
    def direction(self) -> Pin:
        return self.component.get_direction(self.pin)

    def propagate(self,
                  level: Level,
                  epoch: SimStep) -> EventGenerator:
        yield from self.component.propagate(self.pin, level, epoch)

    def connected_pin(self, other: ComponentPin) -> None:
        return self.component.connected_pin(self.pin, other)

    def __iter__(self) -> Iterator[object]:
        return iter((self.component, self.pin))

    def __str__(self) -> str:
        return f'{self.component}#{self.pin}'

    def __repr__(self) -> str:
        return f'{self.component}#{self.pin}'


class SimStep:
    __slots__ = ('__weakref__')


class ComponentBase(ABC):
    __slots__ = ()

    @abstractmethod
    def propagate(self,
                  pin: int,
                  level: Level,
                  epoch: SimStep) -> EventGenerator:
        pass

    @abstractmethod
    def get_level(self, pin: int) -> Level:
        pass

    @abstractmethod
    def get_direction(self, pin: int) -> Pin:
        pass

    @abstractmethod
    def connected_pin(self, pin: int, other: ComponentPin) -> None:
        pass

    def pin(self, pin: int) -> ComponentPin:
        return ComponentPin(self, pin)


class Event(NamedTuple):
    src: ComponentPin
    dst: ComponentPin
    level: Level


EventGenerator = Generator[Event, None, None]

__all__ = (
    'Level',
    'Pin',
    'Pull',
    'ComponentPin',
    'SimStep',
    'ComponentBase',
    'Event',
    'EventGenerator',
)
