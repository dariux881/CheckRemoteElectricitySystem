from SensorManager import SensorManager
from random import randrange

class SensorManagerMock(SensorManager):
    def setup(self, sensorConfig):
        super().checkSensorConfig(sensorConfig)
        print('setup completed')

    def checkPower(self, gain, threshold):
        return randrange(2*threshold) > threshold