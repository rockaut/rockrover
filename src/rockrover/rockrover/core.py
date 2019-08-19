
from . import controls
from . import motors

from asyncio import ensure_future

class Core:
    """RockRover Core"""

    _controls = None
    _motors   = None

    def __init__(self, inputDevices):
        self._controls = controls.Controls(self, inputDevices=inputDevices)
        self._motors   = motors.Motors(self)

    def go(self):
        self._controls.listen()

    def close(self):
        self._controls.close()
        self._motors.close()

