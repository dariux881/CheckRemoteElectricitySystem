import globals

class SensorManager:
    def checkSensorConfig(self, sensorConfig):
        foundCircuits = []
        foundPins = []

        for sConfig in sensorConfig:
            if sConfig.get(globals.pin_key) is None:
                raise Exception(globals.pin_key + ' missing')
            if sConfig.get(globals.circuit_key) is None:
                raise Exception(globals.circuit_key + ' missing')
            if sConfig.get(globals.sensor_threshold_key) is None:
                raise Exception(globals.sensor_threshold_key + ' missing')
            if sConfig.get(globals.sensor_gain_key) is None:
                raise Exception(globals.sensor_gain_key + ' missing')
            
            circuit = sConfig.get(globals.circuit_key)
            if circuit in foundCircuits:
                raise Exception('circuit '+ circuit +' is already defined')

            foundCircuits.append(circuit)

            pin = sConfig.get(globals.pin_key)
            if pin in foundPins:
                raise Exception('pin '+ pin +' is already defined')

            foundPins.append(pin)

    def setup(self, sensorConfig):
        pass

    def checkPower(self, gain, threshold):
        pass

