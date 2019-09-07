
import rockrover
import logging

log = logging.getLogger(__name__)

class Rockrover():

    def __init__(self):
        self.__motormanager = rockrover.Motors.Manager(self)
        self.__core = rockrover.Core.Core(self)

    def setup(self):
        self.__motormanager.setup()
        self.__core.setup()

    def run(self):
        print('Press Ctrl+C to exit...')
        self.__motormanager.failsafe = False
        while True:
            pass

    def __del__(self):
        log.debug("received destruct on rockrover")
        self.stop()
    
    def stop(self):
        log.info("stopping rockrover")
        if self.__motormanager:
            self.__motormanager.failsafe = True
