import logging
import RPi.GPIO as GPIO
from Sensors.Sensor import Sensor

class GPIOSensor(Sensor):
    GPIOInitialized = False

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        if not GPIOSensor.GPIOInitialized:
            self.logger.info('initializing GPIO')
            self.__initialize_gpio()

    def __initialize_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        GPIOSensor.GPIOInitialized = True
