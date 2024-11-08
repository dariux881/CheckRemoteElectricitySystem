import requests

def send_data(status, device_id, api_key, url):
    # Invia lo status al server tramite API
    payload = {
        'api_key': api_key,
        'device': device_id,
        'status': status
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Dati inviati correttamente.")
        else:
            print("Errore nell'invio dei dati:", response.status_code)
    except Exception as e:
        print("Errore nella connessione:", e)