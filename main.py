import time
import configparser
from CommunicationManager import CommunicationManager
from SensorManagerMock import SensorManagerMock
import json

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Guadagno per la lettura del sensore, può essere modificato
sensor_gain = config.get('Sensor', 'sensor-gain')

# Pin GPIO collegato al sensore STC013
sensors_config = json.loads(config.get('Sensor', 'sensors-config'))

# Soglia per rilevare la corrente (dipende dal sensore)
THRESHOLD = config.get('Sensor', 'value-threshold') # deve essere regolato in base al sensore

# API del server dove inviare i dati
SERVER_URL = config.get('Remote', 'send-read-url')
API_KEY = config.get('Remote', 'api-key')
DEVICE_ID = config.get('Device', 'device-id')

ac_ok_time_wait = config.get('Device', 'device-time-sleep-seconds-current-ok')
ac_ko_time_wait = config.get('Device', 'device-time-sleep-seconds-current-ko')

sensorManager = SensorManagerMock()
commManager = CommunicationManager()

def main():
    sensorManager.setup(sensors_config)

    while True:
        #TODO iterare su tutti i sensori configurati. ac_status va messo in OR. Almeno un fallimento comporta il check con ac_ko_time_wait
        ac_status = sensorManager.checkPower(sensor_gain, THRESHOLD)

        if ac_status:
            print("Corrente rilevata!")
        else:
            print("Corrente assente!")

        commManager.sendData(ac_status, DEVICE_ID, API_KEY, SERVER_URL)

        if ac_status:
            time.sleep(ac_ok_time_wait)
        else:
            time.sleep(ac_ko_time_wait)

if __name__ == "__main__":
    main()
