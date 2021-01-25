from argparse import ArgumentParser
from . import console  # noqa
import logging

from primula import latches, Pull, Wire, Level

log = logging.getLogger()


def main():
    opts = ArgumentParser(description='Primula')
    opts.add_argument('--verbose', '-v',
                      action='count',
                      default=0,
                      help='Be more talkative')

    args = opts.parse_args()
    if args.verbose >= 2:
        log.setLevel(logging.DEBUG)
    elif args.verbose >= 1:
        log.setLevel(logging.INFO)
    else:
        log.setLevel(logging.WARNING)

    s = Wire('S', Pull.DOWN)
    r = Wire('R', Pull.DOWN)
    q = Wire('Q')
    q_ = Wire('Q_')

    latch = latches.SR()
    s.connect(latch.pins.s)
    r.connect(latch.pins.r)
    q.connect(latch.pins.q)
    q_.connect(latch.pins.q_)
    s.drive(Level.HI)
    r.drive(Level.HI)
    print(s, r, q, q_)


if __name__ == '__main__':
    main()
