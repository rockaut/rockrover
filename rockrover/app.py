
import rockrover
import logging
import time

log = logging.getLogger(__name__)

class Rockrover():

    def __init__(self):
        self.motormanager = rockrover.Motors.Manager(self)
        self.core = rockrover.Core.Core(self)
        self.controls = rockrover.Controls.ControlsManager(self)

    def setup(self):
        self.motormanager.setup()
        self.core.setup()
        self.controls.setup()

    def run(self):
        print('Press Ctrl+C to exit...')

        while True:
            foundControls = self.controls.searchControls()
            time.sleep(1)
            if foundControls: break

        while True:
            self.controls.read()

    def __del__(self):
        log.debug("received destruct on rockrover")
        self.stop()
    
    def stop(self):
        log.info("stopping rockrover")
        if self.motormanager:
            self.motormanager.failsafe = True
