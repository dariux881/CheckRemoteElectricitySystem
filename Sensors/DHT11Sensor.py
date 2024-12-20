import dht11
import globals
import logging
import RPi.GPIO as GPIO
from Sensors.Sensor import Sensor

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class DHT11Sensor(Sensor):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        
        self.pin = 0
        self.sensor = None

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.pin_key) is None:
            self.logger.error(globals.pin_key + ' missing')
            return False

        return super().check_sensor_config(sensor_config)

    def setup(self, sensor_config):
        if not self.check_sensor_config(sensor_config):
            self.logger.error('setup failed')
            return False

        self.pin = sensor_config.get(globals.pin_key)
        self.logger.info('selected pin: ' + str(self.pin))
        self.sensor = dht11.DHT11(pin = self.pin)
        self.logger.info('created sensor')

        return super().setup(sensor_config)

    def read_value(self):
        try:
            result = self.sensor.read()
            self.logger.debug('temperature: ' + str(result.temperature) + '°C humidity:' + str(result.humidity) + '%')
            return result.temperature
        except Exception as e:
            self.logger.exception(e)
            return None

    def get_value(self):
        return self.read_value()
