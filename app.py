from CommunicationManager import CommunicationManager
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

# Getting the sensors configuration
sensors_config = json.loads(config.get(globals.device_section_key, globals.sensor_config_key))

# Getting the remote server parameters
SERVER_URL = config.get(globals.remote_section_key, globals.remote_send_status_url_key)
API_KEY = config.get(globals.remote_section_key, globals.api_key_key)
DEVICE_ID = config.get(globals.device_section_key, globals.device_id_key)

after_read_time_wait = config.getint(globals.device_section_key, globals.after_read_time_wait_key)


def main():
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    sensor_manager = SensorManager()
    # TODO make communication manager more configurable based on connection type
    comm_manager = CommunicationManager()

    logger.debug('setting up sensor manager')
    try:
        sensors = sensor_manager.setup(sensors_config)
    except Exception as e:
        logger.exception(e)
        return

    while True:
        total_result = []

        logger.info('getting data from sensors')
        for sensor in sensors:
            single_value = sensor_manager.get_value(sensor.name)

            if single_value is not None:
                logger.debug("value received from sensor " + sensor.name)
            else:
                logger.warning("Invalid value received from sensor " + sensor.name)

            single_result = {globals.sensor_result_key: sensor.name, globals.value_result_key: single_value}
            total_result.append(single_result)

        try:
            comm_manager.send_data(total_result, DEVICE_ID, API_KEY, SERVER_URL)
        except Exception as e:
            logger.exception(e)

        # TODO notify on device that system is properly working or not due to config errors

        time.sleep(after_read_time_wait)


if __name__ == "__main__":
    main()
