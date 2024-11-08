from SensorManager import SensorManager

class SensorManagerMock(SensorManager):
    def setup(self, sensorConfig):
        super().checkSensorConfig(sensorConfig)
        print('setup completed')

    def checkPower(self, gain, threshold):
        return True