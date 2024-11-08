import SensorManager
import Adafruit_ADS1x15
import RPi.GPIO as GPIO

class SensorManagerGPIO(SensorManager):
    def __init__(self):
        # Configura il sensore ADC (se usi STC013 con ADC)
        self.adc = Adafruit_ADS1x15.ADS1115()

    def setup(self, sensorConfig):
        super().checkSensorConfig(sensorConfig)
        
        # Pin GPIO per il sensore STC013
        GPIO.setmode(GPIO.BCM)

        for sConfig in sensorConfig:
            GPIO.setup(sConfig.sensorPin, GPIO.IN)

    def readCurrent(self, sensor_gain):
        # Leggi il valore dal sensore (ADC)
        value = self.adc.read_adc(0, gain=sensor_gain)
        return value

    def checkPower(self, sensor_gain, threshold):
        # Controlla se la corrente è presente
        current_value = self.readCurrent(self, sensor_gain)
        if current_value > threshold:
            return True  # Corrente presente
        else:
            return False  # Corrente assente