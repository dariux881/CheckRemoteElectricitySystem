
class SensorManager:
    def checkSensorConfig(self, sensorConfig):
        foundCircuits = []

        for sConfig in sensorConfig:
            if sConfig.get('sensor-pin') is None:
                raise Exception('sensor-pin missing')
            if sConfig.get('device-circuit') is None:
                raise Exception('device-circuit missing')
            if sConfig.get('value-threshold') is None:
                raise Exception('value-threshold missing')
            if sConfig.get('sensor-gain') is None:
                raise Exception('sensor-gain missing')
            
            circuit = sConfig.get('device-circuit')
            if circuit in foundCircuits:
                raise Exception('circuit '+ circuit +' is already defined')

            foundCircuits.append(circuit)

    def setup(self, sensorConfig):
        pass

    def checkPower(self, gain, threshold):
        pass

