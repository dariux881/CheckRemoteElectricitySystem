from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/monitor', methods=['POST'])
def monitor():
    data = request.get_json()
    print(f"Status corrente: {data['status']}")
    # Aggiungi qui la logica per gestire i dati ricevuti (es. salvataggio nel database)
    return jsonify({'message': 'Dati ricevuti con successo'}), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
