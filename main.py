import globals
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
sensors_config = json.loads(config.get(globals.sensor_section_key, globals.sensor_config_key))

# API del server dove inviare i dati
SERVER_URL = config.get(globals.remote_section_key, globals.remote_send_status_url_key)
API_KEY = config.get(globals.remote_section_key, globals.api_key_key)
DEVICE_ID = config.get(globals.device_section_key, globals.device_id_key)

ac_ok_time_wait = config.getint(globals.device_section_key, globals.time_sleep_status_ok_key)
ac_ko_time_wait = config.getint(globals.device_section_key, globals.time_sleep_status_ko_key)

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
            singleStatus = sensorManager.checkPower(sConfig[globals.sensor_gain_key], sConfig[globals.sensor_threshold_key])

            if singleStatus:
                print("Corrente rilevata!")
            else:
                print("Corrente assente!")

            singleResult = {globals.circuit_result_key: sConfig.get(globals.circuit_key), globals.status_result_key: singleStatus}
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
