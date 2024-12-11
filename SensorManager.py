import globals
import logging
import logging.config
from Sensors.SensorFactory import SensorFactory

supported_sensor_types = ['amperometer', 'mock_bool', 'mock_number']


class SensorManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sensorMap = dict()

    def setup(self, sensors_config):
        self.logger.info('setting up sensors')

        try:
            self.check_sensor_config(sensors_config)
        except Exception as e:
            self.logger.exception(e)
            raise e

        s_factory = SensorFactory()

        for sConfig in sensors_config:
            # instantiate all the sensors
            sensor_type = sConfig.get(globals.sensor_type_key)
            sensor = s_factory.create(sensor_type, sConfig)

            if sensor is None:
                self.logger.error('invalid sensor. Not created')
                raise Exception(
                    'failed in creating sensor ' + sensor_type + ' for name ' + sConfig.get(globals.sensor_name_key))

            self.sensorMap[sensor.name] = sensor

        return self.sensorMap.values()

    @staticmethod
    def check_sensor_config(sensor_config):
        found_pins = []
        found_names = []

        for sConfig in sensor_config:
            if sConfig.get(globals.sensor_name_key) is None:
                raise Exception(globals.sensor_name_key + ' missing')
            if sConfig.get(globals.sensor_type_key) is None:
                raise Exception(globals.sensor_type_key + ' missing')
            if sConfig.get(globals.circuit_key) is None:
                raise Exception(globals.circuit_key + ' missing')

            sensor_type = sConfig.get(globals.sensor_type_key)
            if sensor_type not in supported_sensor_types:
                raise Exception('sensor type ' + sensor_type + ' is not supported')

            sensor_name = sConfig.get(globals.sensor_name_key)
            if sensor_name in found_names:
                raise Exception('name ' + sensor_name + ' is already defined')

            found_names.append(sensor_name)

    def get_value(self, sensor_name):
        if sensor_name not in self.sensorMap:
            print('Invalid sensor with name ' + sensor_name)
            return False

        sensor = self.sensorMap[sensor_name]
        return sensor.get_value()
