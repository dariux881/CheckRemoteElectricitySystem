import RPi.GPIO as GPIO

def setGPIO(sensor_pins):
    # Pin GPIO per il sensore STC013
    GPIO.setmode(GPIO.BCM)

    for pin in sensor_pins:
        GPIO.setup(pin, GPIO.IN)

def read_current(adc, sensor_gain):
    # Leggi il valore dal sensore (ADC)
    value = adc.read_adc(0, gain=sensor_gain)
    return value

def check_ac_power(adc, sensor_gain, threshold):
    # Controlla se la corrente è presente
    current_value = read_current(adc, sensor_gain)
    if current_value > threshold:
        return True  # Corrente presente
    else:
        return False  # Corrente assente