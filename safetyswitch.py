
from microcontroller import Pin
import digitalio
import logging

log = logging.getLogger(__name__)
### seems to work on different OS's??? complains of pin error unccommnet in oven.py file to test also to work have you main oven controll gpio set to safety switch and give you heat output a new gpio seems to work backwards hmmmmmmm???? anyone

class SafetySwitch:
    def __init__(self, pin: Pin, active_value: bool = True) -> None:
        if pin is None:
            self._pin = None
            return
        self._active_value = active_value
        self._pin = digitalio.DigitalInOut(pin)
        self._pin.direction = digitalio.Direction.OUTPUT
        self.off()

    def on(self):
        if self._pin is not None:
            self._pin.value = self._active_value

    def off(self):
        if self._pin is not None:
            self._pin.value = not self._active_value
