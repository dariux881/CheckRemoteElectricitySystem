import globals


class Sensor:
    def __init__(self):
        self.id = 0
        self.circuit = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.sensor_id_key) is None:
            print(globals.sensor_id_key + ' missing')
            return False
        if sensor_config.get(globals.sensor_type_key) is None:
            print(globals.sensor_type_key + ' missing')
            return False
        if sensor_config.get(globals.circuit_key) is None:
            print(globals.circuit_key + ' missing')
            return False
        
        return True

    def setup(self, sensor_config):
        self.id = sensor_config[globals.sensor_id_key]
        self.circuit = sensor_config[globals.circuit_key]

    def get_value(self):
        pass
