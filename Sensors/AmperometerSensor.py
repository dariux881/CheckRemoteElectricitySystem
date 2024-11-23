from Sensors.Sensor import Sensor
import globals
import Adafruit_ADS1x15
import RPi.GPIO as GPIO


class AmperometerSensor(Sensor):
    def __init__(self):
        super().__init__()

        # Configura il sensore ADC (se usi STC013 con ADC)
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gain = 0
        self.threshold = 0

    def check_sensor_config(self, sensor_config):
        if sensor_config.get(globals.pin_key) is None:
            print(globals.pin_key + ' missing')
            return False
        if sensor_config.get(globals.sensor_threshold_key) is None:
            print(globals.sensor_threshold_key + ' missing')
            return False
        if sensor_config.get(globals.sensor_gain_key) is None:
            print(globals.sensor_gain_key + ' missing')
            return False

        return super().check_sensor_config(sensor_config)

    def setup(self, sensor_config):
        if not self.check_sensor_config(sensor_config):
            print('setup failed')
            return False
        
        super().setup(sensor_config)

        self.gain = sensor_config[globals.sensor_gain_key]
        self.threshold = sensor_config[globals.sensor_threshold_key]

        # Pin GPIO per il sensore STC013
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor_config[globals.pin_key], GPIO.IN)

    def read_current(self, sensor_gain):
        # Leggi il valore dal sensore (ADC)
        value = self.adc.read_adc(0, gain=sensor_gain)
        return value

    def get_value(self):
        # Controlla se la corrente è presente
        current_value = self.read_current(self.gain)
        if current_value > self.threshold:
            return True  # Corrente presente
        else:
            return False  # Corrente assente