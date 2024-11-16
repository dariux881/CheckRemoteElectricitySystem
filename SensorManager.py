import globals
import logging
import logging.config
from Sensors.SensorFactory import SensorFactory

supported_sensor_types = ['amperometer', 'mock']


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
                    'failed in creating sensor ' + sensor_type + ' for id ' + sConfig.get(globals.sensor_id_key))

            self.sensorMap[sensor.id] = sensor

        return self.sensorMap.values()

    @staticmethod
    def check_sensor_config(sensor_config):
        found_circuits = []
        found_pins = []
        found_ids = []

        for sConfig in sensor_config:
            if sConfig.get(globals.sensor_id_key) is None:
                raise Exception(globals.sensor_id_key + ' missing')
            if sConfig.get(globals.sensor_type_key) is None:
                raise Exception(globals.sensor_type_key + ' missing')
            if sConfig.get(globals.circuit_key) is None:
                raise Exception(globals.circuit_key + ' missing')

            circuit = sConfig.get(globals.circuit_key)
            if circuit in found_circuits:
                raise Exception('circuit ' + circuit + ' is already defined')

            found_circuits.append(circuit)

            sensor_type = sConfig.get(globals.sensor_type_key)
            if sensor_type not in supported_sensor_types:
                raise Exception('sensor type ' + sensor_type + ' is not supported')

            sensor_id = sConfig.get(globals.sensor_id_key)
            if sensor_id in found_ids:
                raise Exception('id ' + sensor_id + ' is already defined')

            found_ids.append(sensor_id)

    def check_power(self, sensor_id):
        if sensor_id not in self.sensorMap:
            print('Invalid sensor with ID ' + sensor_id)
            return False

        sensor = self.sensorMap[sensor_id]
        return sensor.check_power()
