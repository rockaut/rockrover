

class ManagerBase():

    def __init__(self, rockrover):
        self.__rockrover = rockrover

    def setup(self):
        pass

class BoardBase():

    def __init__(self, manager):
        self.__manager = manager
    
    def setup(self):
        pass
