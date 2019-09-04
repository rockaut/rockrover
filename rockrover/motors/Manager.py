
from rockrover.motors.Board import *

class Manager():

    def __init__(self, rockrover):
        self.__rockrover = rockrover
        self.__board = Board(self)
        self.failsafe = True

    def init(self):
        self.failsafe = True
        self.__board.init()

    def get_failsafe(self):
        return self._failsafe
    
    def set_failsafe(self, value):
        self._failsafe = value

    failsafe = property(get_failsafe, set_failsafe)
