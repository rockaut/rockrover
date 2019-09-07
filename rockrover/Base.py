

class ManagerBase():

    def __init__(self, rockrover):
        self._rockrover = rockrover

    def setup(self):
        pass

class BoardBase():

    def __init__(self, manager):
        self._manager = manager
    
    def setup(self):
        pass
