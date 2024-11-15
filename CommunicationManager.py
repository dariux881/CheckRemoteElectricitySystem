import requests


class CommunicationManager:
    @staticmethod
    def send_data(status, device_id, api_key, url):
        # Sends status to server
        payload = {
            'api_key': api_key,
            'device': device_id,
            'status': status
        }

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print("Data correctly sent.")
            else:
                print("Error in sending data: ", response.status_code)
        except Exception as e:
            print("Error in connection:", e)