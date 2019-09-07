
import rockrover
import logging

import evdev
from select import select

log = logging.getLogger(__name__)

ABS_LEFTSTEER = evdev.ecodes.ABS_Y
ABS_RIGHTSTEER = evdev.ecodes.ABS_RZ
ABS_AXES = -1

class ControlsManager(rockrover.Base.ManagerBase):

    def __init__(self, rockrover):
        super().__init__(rockrover)
        self._absoluteMapings = { }
        self._keyMapings = { }
        self.__zones   = { }
        self.__emptyAxes = { }
        self._invertRight = True
        self._invertLeft = True

    def setup(self):
        log.debug("setting up controls")

    def searchControls(self):
        self._devices = []
        
        log.debug("Searching for controls ...")
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

        log.debug("Found [{}] control devices".format(len(devices)))
        for d in devices:
            if "Xbox".lower() in d.name.lower():
                log.debug("adding {} [{} / {}] to devices".format(d.name, d.path, d.phys))
                self._devices += [ d ]
                caps = d.capabilities(verbose=False)
                if evdev.ecodes.EV_ABS in caps.keys():
                    for (code, info) in caps[evdev.ecodes.EV_ABS]:
                        self.__zones[code] = info
                        self.__emptyAxes[code] = 0.0

        return len(self._devices)

    def _processEvents(self, events = []):
        axes = self.__emptyAxes
        for e in events:
            if e.type == evdev.ecodes.EV_ABS:
                e.value = self.__calcAbsolute(e)
                axes[e.code] = e.value
                if e.code in self._absoluteMapings.keys():
                    for mapping in self._absoluteMapings[e.code]:
                        mapping(e)

            if e.type == evdev.ecodes.EV_KEY:
                if e.code in self._keyMapings.keys():
                    for mapping in self._keyMapings[e.code]:
                        mapping(e)
        
        if ABS_AXES in self._absoluteMapings.keys():
            for mapping in self._absoluteMapings[ABS_AXES]:
                mapping(axes)

    def __calcAbsolute(self, e):
        mid  = (self.__zones[e.code].max - self.__zones[e.code].min) * 0.5
        raw  = (e.value - mid)

        if abs(raw) < self.__zones[e.code].flat:
            return 0.0

        if self._invertLeft and e.code == ABS_LEFTSTEER:
            raw = -raw
        if self._invertRight and e.code == ABS_RIGHTSTEER:
            raw = -raw

        if raw < 0:
            return round( (raw / mid), 1)
        
        return round( ( raw / mid ), 1)

    def addAbsoluteMapping(self, code, callback):
        log.debug("add steer mapping {} {}".format(code, callback))
        if code in self._absoluteMapings.keys():
            self._absoluteMapings[code] += [callback]
        else:
            self._absoluteMapings[code] = [ callback ]

    def addKeyMapping(self, code, callback):
        log.debug("add key mapping {} {}".format(code, callback))
        if code in self._keyMapings.keys():
            self._keyMapings[code] += [callback]
        else:
            self._keyMapings[code] = [ callback ]

#InputEvent(1567877203, 170930, 3, 5, 32619)
#code,,sec,type,usec,value
    def read(self):
        events = []
        for d in self._devices:
            gen = d.read()
            try:
                events += gen
            except IOError:
                pass
        
        if(len(events) <= 0):
            return
        
        self._processEvents(events)
