
class SensorManager:
    def checkSensorConfig(self, sensorConfig):
        for sConfig in sensorConfig:
            if sConfig.get('sensor-pin') is None:
                raise Exception('sensor-pin missing')

    def setup(self, sensorConfig):
        pass

    def checkPower(self, gain, threshold):
        pass

