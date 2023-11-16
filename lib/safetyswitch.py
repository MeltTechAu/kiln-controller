
from microcontroller import Pin
import digitalio
import logging

log = logging.getLogger(__name__)


class SafetySwitch:
    def __init__(self, pin: Pin, active_value: bool = True) -> None:
        if pin is None:
            log.warn("====================================================")
            log.warn("Running without safety switch. This is DANGEROUS!!!!")
            log.warn("====================================================")
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
