import globals


class Sensor:
    def __init__(self):
        self.name = ""
        self.circuit = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.sensor_name_key) is None:
            print(globals.sensor_name_key + ' missing')
            return False
        if sensor_config.get(globals.sensor_type_key) is None:
            print(globals.sensor_type_key + ' missing')
            return False
        if sensor_config.get(globals.circuit_key) is None:
            print(globals.circuit_key + ' missing')
            return False
        
        return True

    def setup(self, sensor_config):
        self.name = sensor_config[globals.sensor_name_key]
        self.circuit = sensor_config[globals.circuit_key]

    def get_value(self):
        pass
