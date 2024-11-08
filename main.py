import time
#import Adafruit_ADS1x15
import configparser
import sendData
import readCurrent
import json

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Pin GPIO collegato al sensore STC013
sensors_config = json.loads(config.get('Sensor', 'sensors-config'))

# Guadagno per la lettura del sensore, può essere modificato
sensor_gain = config.get('Sensor', 'sensor-gain')

# Soglia per rilevare la corrente (dipende dal sensore)
THRESHOLD = config.get('Sensor', 'value-threshold') # deve essere regolato in base al sensore

# API del server dove inviare i dati
SERVER_URL = config.get('Remote', 'send-read-url')
API_KEY = config.get('Remote', 'api-key')
DEVICE_ID = config.get('Device', 'device-id')

ac_ok_time_wait = config.get('Device', 'device-time-sleep-seconds-current-ok')
ac_ko_time_wait = config.get('Device', 'device-time-sleep-seconds-current-ko')

# Configura il sensore ADC (se usi STC013 con ADC)
adc = Adafruit_ADS1x15.ADS1115()

def main():
    sensor_pins = [d['sensor-pin'] for d in sensors_config]
    readCurrent.setGPIO(sensor_pins)

    while True:
        #TODO iterare su tutti i sensori configurati. ac_status va messo in OR. Almeno un fallimento comporta il check con ac_ko_time_wait
        ac_status = readCurrent.check_ac_power(adc, sensor_gain, THRESHOLD)

        if ac_status:
            print("Corrente rilevata!")
        else:
            print("Corrente assente!")

        sendData.send_data(ac_status, DEVICE_ID, API_KEY, SERVER_URL)


        if ac_status:
            time.sleep(ac_ok_time_wait)
        else:
            time.sleep(ac_ko_time_wait)

if __name__ == "__main__":
    main()
