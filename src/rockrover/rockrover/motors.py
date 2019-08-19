
import adafruit_motorkit

class Motors():

    __core = None

    __motorkit = None

    leftMotor = None
    rightMotor = None

    translation = 1

    def __init__(self, core, left = 1, right = 4):
        self.__core = core
        self.__motorkit = adafruit_motorkit.MotorKit()

        if left == 1:
            self.leftMotor = self.__motorkit.motor1
        elif left == 2:
            self.leftMotor = self.__motorkit.motor2
        elif left == 3:
            self.leftMotor = self.__motorkit.motor3
        elif left == 4:
            self.leftMotor = self.__motorkit.motor4

        if right == 1:
            self.rightMotor = self.__motorkit.motor1
        elif right == 2:
            self.rightMotor = self.__motorkit.motor2
        elif right == 3:
            self.rightMotor = self.__motorkit.motor3
        elif right == 4:
            self.rightMotor = self.__motorkit.motor4

    def close(self):
        self.totalStop()

    def setValues( self, leftValue = 0.0, rightValue = 0.0 ):

        leftValue = leftValue * self.translation
        rightValue = rightValue * self.translation

        self.leftMotor.throttle  = leftValue
        self.rightMotor.throttle = rightValue

    def totalStop( self ):
        self.leftMotor.throttle = 0
        self.leftMotor.throttle = 0
    