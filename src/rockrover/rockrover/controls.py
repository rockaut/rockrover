
from enum import Enum
from contextlib import suppress
from asyncio import ensure_future, get_event_loop, Task, create_task, CancelledError
from evdev import InputDevice, categorize, RelEvent, SynEvent, KeyEvent, AbsEvent, ecodes, event_factory

import logging

class ControlType(Enum):
    Tracked = 1

class Controls:
    """RockRover Controls"""

    _core = None

    __controlType  = ControlType.Tracked
    __inputDevices = {}
    __inputLoop    = None
    __inputTasks   = []
    __zones        = {}
    __axes         = [ 0.0, 0.0, 0.0, 0.0 ]

    def __init__(self, core, inputDevices = {}):
        self._core = core
        self.__controlType = ControlType.Tracked
        
        for (name, devicePath) in inputDevices.items():
            device = InputDevice( devicePath )
            self.__inputDevices.update( { name: device })
            caps = device.capabilities(verbose=False)
            if ecodes.EV_ABS in caps.keys():
                for (code, info) in caps[ecodes.EV_ABS]:
                    self.__zones[code] = info
        
        self.__inputLoop = get_event_loop()
        self.__inputTasks = []
        for (name, device) in self.__inputDevices.items():
            t = ensure_future(self.input_event(name, device))
            self.__inputTasks.append(t)

    def close(self):
        self.__inputLoop.stop()

    def listen(self):
        try:
            self.__inputLoop.run_forever()
            self.__inputLoop.run_until_complete(self.__inputLoop.shutdown_asyncgens())       
        finally:
            for t in self.__inputTasks:
                t.cancel()
                with suppress(CancelledError):
                    self.__inputLoop.run_until_complete(t)
            self.__inputLoop.close()
            for (name, device) in self.__inputDevices.items():
                device.close()

    def __absAxisValue(self, code, value):
        mid  = (self.__zones[code].max - self.__zones[code].min) * 0.5
        raw  = (value - mid)

        if abs(raw) < self.__zones[code].flat:
            return 0.0

        if raw < 0:
            return ( raw ) / ( mid )
        
        return ( raw ) / ( mid )

    async def input_event(self, name, device):
        async for event in device.async_read_loop():
            etype = event.type
            ecat  = categorize(event)
            
            if isinstance(ecat, KeyEvent):
                if ecodes.BTN_A == ecat.scancode:
                    print("{} {}: {}".format("A", ecodes.BTN_A, ecat.keystate))
                if ecodes.BTN_START == ecat.scancode and ecat.keystate == 0:
                    self._core.close()
                    return
            elif isinstance(ecat, AbsEvent):

                value = self.__absAxisValue(ecat.event.code, ecat.event.value)

                if ecat.event.code == ecodes.ABS_X:
                    self.__axes[0] = value
                elif ecat.event.code == ecodes.ABS_Y:
                    self.__axes[1] = value
                elif ecat.event.code == ecodes.ABS_Z:
                    self.__axes[2] = value
                elif ecat.event.code == ecodes.ABS_RZ:
                    self.__axes[3] = value

                self._core._motors.setValues( self.__axes[1], self.__axes[3] )
                
                print("X: {:.1f} Y: {:.1f} | X: {:.1f} Y: {:.1f}".format(self.__axes[0], self.__axes[1], self.__axes[2], self.__axes[3]))
            elif isinstance(ecat, RelEvent):
                logging.debug("{} - {}".format(ecat, ecat.event.value))
            elif isinstance(ecat, SynEvent):
                pass
            elif etype == 4:
                pass
            else:
                logging.debug("{} - {}".format(event, event.value))
