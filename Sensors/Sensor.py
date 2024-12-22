import globals
import logging

class Sensor:
    __Sensors = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.name = ""
        self.circuit = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.sensor_name_key) is None:
            self.logger.error(globals.sensor_name_key + ' missing')
            return False
        if sensor_config.get(globals.sensor_type_key) is None:
            self.logger.error(globals.sensor_type_key + ' missing')
            return False
        if sensor_config.get(globals.circuit_key) is None:
            self.logger.error(globals.circuit_key + ' missing')
            return False
        
        return True

    def _is_object_defined_with_key(self, key):
        return any(sensor['key'] == key for sensor in Sensor.__Sensors)

    def _get_object_from_key(self, key):
        if self._is_object_defined_with_key(key):
            return next((sensor['instance'] for sensor in Sensor.__Sensors if sensor['key'] == key), None)
        else:
            raise Exception

    def _push_object_for_key(self, key, instance):
        Sensor.__Sensors.append({'key': key, 'instance': instance})

    def setup(self, sensor_config):
        self.name = sensor_config[globals.sensor_name_key]
        self.circuit = sensor_config[globals.circuit_key]
        return True

    def get_value(self):
        pass
