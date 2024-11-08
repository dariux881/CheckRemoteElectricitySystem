import time
import configparser
from CommunicationManager import CommunicationManager
from SensorManagerMock import SensorManagerMock
import json

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Pin GPIO collegato al sensore STC013
sensors_config = json.loads(config.get('Sensor', 'sensors-config'))

# API del server dove inviare i dati
SERVER_URL = config.get('Remote', 'send-read-url')
API_KEY = config.get('Remote', 'api-key')
DEVICE_ID = config.get('Device', 'device-id')

ac_ok_time_wait = config.getint('Device', 'device-time-sleep-seconds-current-ok')
ac_ko_time_wait = config.getint('Device', 'device-time-sleep-seconds-current-ko')

sensorManager = SensorManagerMock()
#TODO make communication manager more configurable based on connection type
commManager = CommunicationManager()

def main():
    sensorManager.setup(sensors_config)

    while True:
        # itera su tutti i sensori configurati. Almeno un fallimento comporta il check con ac_ko_time_wait
        powerStatus = True
        totalResult = []
        for sConfig in sensors_config:
            singleStatus = sensorManager.checkPower(sConfig['sensor-gain'], sConfig['value-threshold'])

            if singleStatus:
                print("Corrente rilevata!")
            else:
                print("Corrente assente!")

            singleResult = {'circuit': sConfig.get('device-circuit'), 'result': singleStatus}
            totalResult.append(singleResult)

            powerStatus &= singleStatus

        #TODO notify on device that system is properly working or not due to config errors

        #TODO handle errors from sendData
        commManager.sendData(totalResult, DEVICE_ID, API_KEY, SERVER_URL)

        if powerStatus:
            time.sleep(ac_ok_time_wait)
        else:
            time.sleep(ac_ko_time_wait)

if __name__ == "__main__":
    main()
