import json
import logging
import requests
import globals
from enum import Enum

class SendResult(Enum):
    OK = 0,
    ERROR = 1,
    ACTION_UPDATE = 2


class CommunicationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.token = None

    def get_sensors_config(self, device_id, api_key, url):
        request_url = (url
               .replace(globals.device_placeholder, device_id)
               .replace(globals.api_key_placeholder, api_key))

        try:
            response = requests.get(request_url)
            if response.status_code != 200:
                self.logger.error("Error in sending data: ", response.status_code, str(response.content))

            return response.content
        except Exception as e:
            self.logger.exception(e)

        return None

    def send_data(self, values, device_id, api_key, url):
        # Sends status to server
        payload = {
            globals.api_key_key: api_key,
            globals.device_result_key: device_id,
            globals.values_result_key: values
        }

        self.logger.debug("Sending data:\n" + json.dumps(payload))

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.logger.info("Data correctly sent")
                return SendResult.OK
            elif response.status_code == 205:
                self.logger.info("Data correctly sent")
                return SendResult.ACTION_UPDATE
            else:
                self.logger.error("Error in sending data: ", response.status_code, str(response.content))
                return SendResult.ERROR
        except Exception as e:
            self.logger.exception(e)