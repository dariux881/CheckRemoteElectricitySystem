import globals
import logging
from random import randrange
from Sensors.Sensor import Sensor



class SensorMock(Sensor):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super().__init__()
        self.threshold = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.sensor_threshold_key) is None:
            self.logger.error(globals.sensor_threshold_key + ' missing')
            return False

        return super().check_sensor_config(sensor_config)

    def setup(self, sensor_config):
        if not self.check_sensor_config(sensor_config):
            self.logger.error('setup failed')
            return False

        super().setup(sensor_config)

        self.threshold = sensor_config[globals.sensor_threshold_key]
        self.logger.debug('setup completed')
        return True

    def check_power(self):
        return randrange(2*self.threshold) > self.threshold
