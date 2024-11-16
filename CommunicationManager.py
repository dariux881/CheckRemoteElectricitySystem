import logging
import requests


class CommunicationManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def send_data(self, status, device_id, api_key, url):
        # Sends status to server
        payload = {
            'api_key': api_key,
            'device': device_id,
            'status': status
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.logger.info("Data " + payload + " correctly sent.")
            else:
                self.logger.error("Error in sending data: ", response.status_code)
        except Exception as e:
            self.logger.exception(e)