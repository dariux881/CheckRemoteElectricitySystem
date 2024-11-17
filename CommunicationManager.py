import json
import logging
import requests
import globals


class CommunicationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.token = None

    def login(self, username, password, url):
        payload = {
            'username': username,
            'password': password,
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.logger.info("Successful login")
            else:
                self.logger.error("Error in sending data: ", response.status_code)

            try:
                data = response.json()
            except requests.JSONDecodeError:
                data = None
                self.logger.error('invalid json received after login')

            self.token = data.get('token')

        except Exception as e:
            self.logger.exception(e)

    def send_data(self, status, device_id, api_key, url):
        # Sends status to server
        payload = {
            globals.api_key_key: api_key,
            globals.device_result_key: device_id,
            globals.status_result_key: status
        }

        headers = {
            "Authorization": self.token
        }

        self.logger.debug("Sending data:\n" + json.dumps(payload))

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                self.logger.info("Data correctly sent")
            else:
                self.logger.error("Error in sending data: ", response.status_code, str(response.content))
        except Exception as e:
            self.logger.exception(e)