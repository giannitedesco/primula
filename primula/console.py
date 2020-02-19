from typing import Optional
from sys import stdout
from signal import signal, SIGPIPE, SIG_DFL
import logging

_fmt = logging.Formatter('%(name)s: %(levelname)s: %(message)s')


class Handler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except BrokenPipeError:
            raise SystemExit(0)
        except Exception:
            self.handleError(record)


_stdio_handler = Handler(stream=stdout)
_stdio_handler.setFormatter(_fmt)


def sigpipe_ignore():
    signal(SIGPIPE, SIG_DFL)


def log_module_init(name: Optional[str], level=logging.INFO):
    log = logging.getLogger(name)
    log.addHandler(_stdio_handler)
    log.setLevel(level)
    return log


sigpipe_ignore()
log_module_init(None).name = 'primula'
