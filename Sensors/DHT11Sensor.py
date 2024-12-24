import dht11
import globals
import logging
from Sensors.GPIOSensor import GPIOSensor
import time

class DHT11Sensor(GPIOSensor):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

        self.sensor = None

    def _check_sensor_config(self, sensor_config):
        params = sensor_config.get(globals.sensor_params_key)
        if params is None:
            self.logger.error(globals.sensor_params_key + ' missing')
            return False

        if not any(p['key']=='pin' for p in params):
            # pin not found
            self.logger.error(globals.pin_key + ' missing')
            return False

        return super()._check_sensor_config(sensor_config)

    def setup(self, sensor_config):
        if not self._check_sensor_config(sensor_config):
            self.logger.error('setup failed')
            return False

        params = sensor_config.get(globals.sensor_params_key)
        pin = next((p['value'] for p in params if p['key'] == 'pin'), None)
        self.logger.info('selected pin: ' + str(pin))

        if self._is_object_defined_with_key(pin):
            self.logger.info('found sensor for pin ' + str(pin))
            self.sensor = self._get_object_from_key(pin)
        else:
            self.logger.info('creating sensor for pin ' + str(pin))
            self.sensor = dht11.DHT11(pin=int(pin))
            self._push_object_for_key(pin, self.sensor)

        self.logger.info('created sensor')

        return super().setup(sensor_config)

    def _read_value(self):
        pass

    def get_value(self):
        return self._read_value()

class DHT11Temperature(DHT11Sensor):
    def _read_value(self):
        try:
            result = self.sensor.read()
            self.logger.info('Temp: ' + str(result.temperature) + ' °C\tstatus: ' + str(result.error_code))

            time.sleep(1)

            return result.temperature
        except Exception as e:
            self.logger.exception(e)
            return None

class DHT11Humidity(DHT11Sensor):
    def _read_value(self):
        try:
            result = self.sensor.read()
            self.logger.info('Hum: ' + str(result.humidity) + ' %\tstatus ' + str(result.error_code))

            time.sleep(1)

            return result.humidity
        except Exception as e:
            self.logger.exception(e)
            return None
