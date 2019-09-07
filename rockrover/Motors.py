
import rockrover
import logging

from adafruit_motorkit import MotorKit

log = logging.getLogger(__name__)

class Manager(rockrover.Base.ManagerBase):

    def __init__(self, rockrover):
        super().__init__(rockrover)
        self.__board = Board(self)

    def setup(self, leftMotors = [0,1], rightMotors = [2,3]):
        log.debug('Setup {}'.format(__name__))
        self.__board.setup(leftMotors, rightMotors)
        self.failsafe = True

    def get_failsafe(self):
        return self._failsafe

    def set_failsafe(self, value):
        self._failsafe = value
        if(self.__board and value):
            self.__board.leftThrottle(0.0)
            self.__board.rightThrottle(0.0)

    def set_throttles(self, left = 0.0, right = 0.0):
        if self.failsafe:
            log.warning("failsave active - no throttle")
            return
        
        self.__board.leftThrottle(left)
        self.__board.rightThrottle(right)

    failsafe = property(get_failsafe, set_failsafe)

class Board(rockrover.Base.BoardBase):
    address = 96
    leftMotors = None
    rightMotors = None

    def __init__(self, manager):
        self.__manager = manager

    def setup(self, leftMotors = [0,1], rightMotors = [2,3]):
        log.debug('setting up motorkit')
        self.__kit = MotorKit(self.address)
        
        self.leftMotors = []
        for m in leftMotors:
            a = getattr(self.__kit, "motor{}".format(m+1))
            self.leftMotors += [ a ]

        self.rightMotors = []
        for m in rightMotors:
            a = getattr(self.__kit, "motor{}".format(m+1))
            self.rightMotors += [ a ]

    def leftThrottle(self, value = 0.0):
        for m in self.leftMotors:
            m.throttle = value
    
    def rightThrottle(self, value = 0.0):
        for m in self.rightMotors:
            m.throttle = value
