
from adafruit_motorkit import MotorKit

class Board():
    address = 96

    def __init__(self, manager):
        self.__manager = manager

    def init(self):
        self.__kit = MotorKit(self.address)
