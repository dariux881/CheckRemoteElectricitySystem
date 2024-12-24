from CommunicationManager import CommunicationManager, SendResult
import configparser
import globals
import json
import logging
import logging.config
from SensorManager import SensorManager
import time

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Getting the remote server parameters
SERVER_URL = config.get(globals.remote_section_key, globals.remote_send_status_url_key)
SERVER_CONFIG_URL = config.get(globals.remote_section_key, globals.remote_get_device_config_url_key)
API_KEY = config.get(globals.remote_section_key, globals.api_key_key)
DEVICE_ID = config.get(globals.device_section_key, globals.device_id_key)

after_read_time_wait = config.getint(globals.device_section_key, globals.after_read_time_wait_key)

def get_sensors_config(comm_manager, use_ini, use_remote, logger):
    # try getting data from ini
    if use_ini:
        try:
            ini_config = get_sensors_config_from_ini(logger)
            return ini_config
        except Exception as e:
            logger.exception(e)

    if use_remote:
        # as backup goes online
        try:
            remote_config = comm_manager.get_sensors_config(DEVICE_ID, API_KEY, SERVER_CONFIG_URL)
            if remote_config is None:
                return None

            remote_config_json = json.loads(remote_config)
            return remote_config_json['sensors']
        except Exception as e:
            logger.exception(e)

    return None

def get_sensors_config_from_ini(logger):
    # Getting the sensors configuration
    return json.loads(config.get(globals.device_section_key, globals.sensor_config_key))

def update_device_config_from_remote(comm_manager, sensor_manager, logger):
    try:
        dev_config = get_sensors_config(comm_manager, False, True, logger)

        if dev_config is None:
            logger.error('invalid config received')
            return None

        sensor_manager.setup(dev_config)
    except Exception as e:
        logger.exception(e)

def get_device_config_from_remote(comm_manager, device_id, api_key, logger):
    if not comm_manager:
        raise Exception

    try:
        device_config = comm_manager.get_sensors_config(device_id, api_key)
        return device_config
    except Exception as e:
        logger.exception(e)

    return None

def main():
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    sensor_manager = SensorManager()
    # TODO make communication manager more configurable based on connection type
    comm_manager = CommunicationManager()

    logger.debug('setting up sensor manager')
    try:
        sensors = (
            sensor_manager
                .setup(
                    get_sensors_config(comm_manager, True, True, logger)))
    except Exception as e:
        logger.exception(e)
        return

    while True:
        total_result = []

        logger.info('getting data from sensors')
        for sensor in sensors:
            single_value = sensor_manager.get_value(sensor.name)

            if single_value is None:
                logger.warning("Invalid value received from sensor " + sensor.name)
                continue

            single_result = {globals.sensor_result_key: sensor.name, globals.value_result_key: single_value}
            total_result.append(single_result)

        try:
            result = comm_manager.send_data(total_result, DEVICE_ID, API_KEY, SERVER_URL)
            if result == SendResult.ACTION_UPDATE:
                update_device_config_from_remote(comm_manager, sensor_manager, logger)
        except Exception as e:
            logger.exception(e)

        # TODO notify on device that system is properly working or not due to config errors

        time.sleep(after_read_time_wait)


if __name__ == "__main__":
    main()
