from typing import Deque
from collections import deque
import logging
from .base import Level, \
                  Event, \
                  ComponentPin, \
                  SimStep


sim = logging.getLogger('sim')


class Simulation:
    __slots__ = ()

    @staticmethod
    def run(seed: ComponentPin, level: Level):
        epoch = SimStep()
        q: Deque[Event] = deque()
        sim.debug(f'Simulation seed is {seed}')
        q.extend(seed.propagate(level, epoch))
        while q:
            evt = q.popleft()
            sim.debug(f'pop {evt}')
            sim.debug(f'driving {evt.dst} to {evt.level}')
            q.extend(evt.dst.propagate(evt.level, epoch=epoch))
        sim.debug('---')
