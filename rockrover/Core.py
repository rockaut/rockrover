
import rockrover
import logging

import envirophat

log = logging.getLogger(__name__)

class Core(rockrover.Base.ManagerBase):
    
    def __init__(self, rockrover):
        super().__init__(rockrover)
        self.__environment = Board(self)
    
    def setup(self):
        log.debug('Setup {}'.format(__name__))
        self._rockrover.controls.addKeyMapping(304, self.turnOnLights)
        self.__environment.setup()
    
    def turnOnLights(self, event):
        if event.value == 0:
            if self.__environment.leds.is_on():
                self.__environment.leds.off()
            else:
                self.__environment.leds.on()

class Board(rockrover.Base.BoardBase):
    def __init__(self, manager):
        super().__init__(manager)
        self.motion = None
        self.leds = None
        self.light = None
        self.weather = None
        self.analog = None

    def setup(self):
        self.motion = envirophat.motion
        self.leds = envirophat.leds
        self.light = envirophat.light
        self.weather = envirophat.weather
        self.analog = envirophat.analog

    def __del__(self):
        self.leds.off()