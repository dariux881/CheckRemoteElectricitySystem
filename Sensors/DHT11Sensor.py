from Sensors.Sensor import Sensor
import globals
import Adafruit_DHT

SENSOR_TYPE = Adafruit_DHT.DHT11

class DHT11Sensor(Sensor):
    def __init__(self):
        super().__init__()
        self.pin = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.pin_key) is None:
            print(globals.pin_key + ' missing')
            return False

        return super().check_sensor_config(sensor_config)

    def setup(self, sensor_config):
        if not self.check_sensor_config(sensor_config):
            print('setup failed')
            return False

        self.pin = sensor_config.get(globals.pin_key)

        super().setup(sensor_config)

    def read_value(self):
        humidity, temperature = Adafruit_DHT.read_retry(
            SENSOR_TYPE,
            self.pin
        )
        return temperature

    def get_value(self):
        return self.read_value()
