import globals
import logging
from Sensors.SensorFactory import SensorFactory

logger = logging.getLogger(__name__)
supported_sensor_types = ['amperometer', 'mock']


class SensorManager:
    def __init__(self):
        self.sensorMap = dict()

    def setup(self, sensors_config):
        logger.info('setting up sensors')

        try:
            self.check_sensor_config(sensors_config)
        except Exception as e:
            logger.exception(e)
            raise e

        s_factory = SensorFactory()

        for sConfig in sensors_config:
            # instantiate all the sensors
            sensor_type = sConfig.get(globals.sensor_type_key)
            sensor = s_factory.create(sensor_type, sConfig)

            if sensor is None:
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

            pin = sConfig.get(globals.pin_key)
            if pin is not None and pin in found_pins:
                raise Exception('pin ' + pin + ' is already defined')

            found_pins.append(pin)

            id = sConfig.get(globals.sensor_id_key)
            if id in found_ids:
                raise Exception('id ' + id + ' is already defined')

            found_ids.append(id)

    def check_power(self, sensor_id):
        if sensor_id not in self.sensorMap:
            print('Invalid sensor with ID ' + sensor_id)
            return False

        sensor = self.sensorMap[sensor_id]
        return sensor.check_power()
