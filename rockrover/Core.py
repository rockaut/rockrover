
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


class Board(rockrover.Base.BoardBase):
    def __init__(self, manager):
        super().__init__(manager)
        self.__motion = None
        self.__leds = None
        self.__light = None
        self.__weather = None
        self.__analog = None

    def setup(self):
        self.__motion = envirophat.motion
        self.__leds = envirophat.leds
        self.__light = envirophat.light
        self.__weather = envirophat.weather
        self.__analog = envirophat.analog
