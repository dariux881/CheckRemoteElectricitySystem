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
    Sensors = []

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

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

        pin = sensor_config.get(globals.pin_key)
        self.logger.info('selected pin: ' + str(pin))

        if any(sensor.pin == pin for sensor in DHT11Sensor.Sensors):
            self.sensor = next((sensor.instance for sensor in DHT11Sensor.Sensors if sensor.pin == pin), None)
        else:
            self.sensor = dht11.DHT11(pin=pin)
            DHT11Sensor.Sensors.append({'pin': pin, 'instance': self.sensor})

        self.logger.info('created sensor')

        return super().setup(sensor_config)

    def read_value(self):
        pass

    def get_value(self):
        return self.read_value()

class DHT11Temperature(DHT11Sensor):
    def read_value(self):
        try:
            result = self.sensor.read()
            self.logger.info('Temp: ' + str(result.temperature) + '°C')
            return result.temperature
        except Exception as e:
            self.logger.exception(e)
            return None

class DHT11Humidity(DHT11Sensor):
    def read_value(self):
        try:
            result = self.sensor.read()
            self.logger.info('Hum: ' + str(result.humidity) + '%')
            return result.humidity
        except Exception as e:
            self.logger.exception(e)
            return None