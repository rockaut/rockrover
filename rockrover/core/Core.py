
import envirophat

class Core():
    
    def __init__(self, rockrover):
        self.__rockrover = rockrover
        self.__motion = None
        self.__leds = None
        self.__light = None
        self.__weather = None
        self.__analog = None

    def init(self):
        self.__motion = envirophat.motion
        self.__leds = envirophat.leds
        self.__light = envirophat.light
        self.__weather = envirophat.weather
        self.__analog = envirophat.analog
