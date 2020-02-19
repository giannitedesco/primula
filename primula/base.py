from __future__ import annotations
from typing import Generator, NamedTuple, Callable, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
from enum import Enum


class Level(Enum):
    LO = 0
    HI = 1
    FLT = 2
    ERR = 3


class Pin(Enum):
    IN = 0
    OUT = 1
    HIZ = 0xff  # High-impedence / Hi-Z state


class Pull(Enum):
    DOWN = 0
    UP = 1

    @property
    def level(self):
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

    def connected_pin(self, other: ComponentPin):
        return self.component.connected_pin(self.pin, other)

    def __iter__(self):
        return iter((self.component, self.pin))

    def __str__(self):
        return f'{self.component}#{self.pin}'

    def __repr__(self):
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
    def connected_pin(self, pin: int, other: ComponentPin):
        pass

    def pin(self, pin: int):
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
