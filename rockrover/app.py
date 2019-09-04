
from . import motors
from . import core

class Rockrover():

    def __init__(self, *args, **kwargs):
        self.__motormanager = motors.Manager(self)
        self.__core = core.Core(self)

    def init(self):
        self.__motormanager.init()
        self.__core.init()

    def run(self):
        print('Press Ctrl+C to exit...')
        try:
            while True:
                pass
        except KeyboardInterrupt:
            return None
