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
SERVER_LOGIN_URL = config.get(globals.remote_section_key, globals.remote_login_url_key)
USERNAME = config.get(globals.remote_section_key, globals.username_key)
PASSWORD = config.get(globals.remote_section_key, globals.password_key)
API_KEY = config.get(globals.remote_section_key, globals.api_key_key)
DEVICE_ID = config.get(globals.device_section_key, globals.device_id_key)

ac_ok_time_wait = config.getint(globals.device_section_key, globals.time_sleep_status_ok_key)
ac_ko_time_wait = config.getint(globals.device_section_key, globals.time_sleep_status_ko_key)


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

    try:
        comm_manager.login(USERNAME, PASSWORD, SERVER_LOGIN_URL)
    except Exception as e:
        logger.exception(e)
        return

    while True:
        # iterate on all the configured sensors. If at least one fails, wait ac_ko_time_wait
        power_status = True
        total_result = []

        logger.info('checking power from sensors')
        for sensor in sensors:
            single_status = sensor_manager.check_power(sensor.id)

            if single_status:
                logger.debug("Power OK for sensor " + sensor.id)
            else:
                logger.warning("Power KO for sensor " + sensor.id)

            single_result = {globals.sensor_result_key: sensor.id, globals.status_result_key: single_status}
            total_result.append(single_result)

            power_status &= single_status

        # TODO notify on device that system is properly working or not due to config errors

        # TODO handle errors from sendData
        try:
            comm_manager.send_data(total_result, DEVICE_ID, API_KEY, SERVER_URL)
        except Exception as e:
            logger.exception(e)

        if power_status:
            time.sleep(ac_ok_time_wait)
        else:
            time.sleep(ac_ko_time_wait)


if __name__ == "__main__":
    main()
