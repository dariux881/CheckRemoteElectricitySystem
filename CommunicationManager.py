import json
import logging
import requests
import globals


class CommunicationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.token = None

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
            else:
                self.logger.error("Error in sending data: ", response.status_code, str(response.content))
        except Exception as e:
            self.logger.exception(e)